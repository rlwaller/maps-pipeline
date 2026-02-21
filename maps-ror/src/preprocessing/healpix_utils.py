"""HEALPix utility functions for map IO and preprocessing."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import healpy as hp
import numpy as np


def read_healpix_fits(path: str | Path, field: Optional[int] = None) -> np.ndarray:
    """Read a HEALPix FITS map into a NumPy array."""
    return np.asarray(hp.read_map(path, field=field, verbose=False))


def ud_grade_map(map_in: np.ndarray, nside_out: int, power: Optional[int] = None) -> np.ndarray:
    """Upgrade or degrade a HEALPix map to ``nside_out``."""
    return np.asarray(hp.ud_grade(map_in, nside_out=nside_out, power=power))


def ud_grade_mask(mask_in: np.ndarray, nside_out: int, threshold: float = 0.9) -> np.ndarray:
    """Upgrade/degrade mask and re-binarize with ``threshold``."""
    mask_float = np.asarray(hp.ud_grade(mask_in.astype(float), nside_out=nside_out, power=None))
    return (mask_float >= threshold).astype(float)


def apodize_mask(mask: np.ndarray, apodize_deg: float) -> np.ndarray:
    """Apodize mask via NaMaster when requested.

    Falls back to Gaussian smoothing if NaMaster apodization is unavailable.
    """
    mask = np.asarray(mask, dtype=float)
    if apodize_deg <= 0:
        return mask
    try:
        import pymaster as nmt

        return np.asarray(nmt.mask_apodization(mask, apodize_deg, apotype="C1"))
    except Exception:
        fwhm_rad = np.deg2rad(apodize_deg)
        smoothed = hp.smoothing(mask, fwhm=fwhm_rad, verbose=False)
        return np.clip(smoothed, 0.0, 1.0)


def remove_monopole_dipole(map_in: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Remove monopole + dipole from map on masked sky."""
    cleaned = np.asarray(map_in, dtype=float).copy()
    good = np.asarray(mask) > 0
    cleaned[~good] = hp.UNSEEN
    cleaned = hp.remove_dipole(cleaned, gal_cut=0, fitval=False, copy=True)
    cleaned[~good] = 0.0
    if not np.isfinite(cleaned).all():
        raise ValueError("remove_monopole_dipole produced non-finite values.")
    return cleaned
