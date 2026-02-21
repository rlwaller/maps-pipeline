"""Pseudo-C_ell estimators using NaMaster for spin-0 fields."""

from __future__ import annotations

from typing import Any

import numpy as np
import pymaster as nmt

from src.spectra.binning import effective_ells


def compute_bandpowers_spin0_spin0(
    map_x: np.ndarray,
    map_y: np.ndarray,
    mask: np.ndarray,
    binning: nmt.NmtBin,
    lmax: int,
) -> dict[str, Any]:
    """Compute decoupled binned pseudo-C_ell using standard NaMaster workflow."""
    field_x = nmt.NmtField(mask, [map_x], purify_b=False, purify_e=False)
    field_y = nmt.NmtField(mask, [map_y], purify_b=False, purify_e=False)

    workspace = nmt.NmtWorkspace()
    workspace.compute_coupling_matrix(field_x, field_y, binning, lmax=lmax)

    cl_coupled = nmt.compute_coupled_cell(field_x, field_y)
    cl_decoupled = workspace.decouple_cell(cl_coupled)
    return {
        "cl_binned": np.asarray(cl_decoupled[0]),
        "ell_eff": effective_ells(binning),
        "cl_coupled": np.asarray(cl_coupled[0]),
    }


def compute_Tg_and_gg(
    t_map: np.ndarray,
    g_map: np.ndarray,
    mask: np.ndarray,
    binning: nmt.NmtBin,
    lmax: int,
) -> dict[str, dict[str, Any]]:
    """Compute Tg cross and gg auto binned spectra."""
    tg = compute_bandpowers_spin0_spin0(t_map, g_map, mask, binning, lmax=lmax)
    gg = compute_bandpowers_spin0_spin0(g_map, g_map, mask, binning, lmax=lmax)
    return {"tg": tg, "gg": gg}
