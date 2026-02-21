"""Null tests for tracer/CMB cross-correlation pipeline."""

from __future__ import annotations

from typing import Any

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np

from src.spectra.namaster_estimators import compute_bandpowers_spin0_spin0


def _rotate_map_random(g_map: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    rot = hp.Rotator(rot=(rng.uniform(0, 360), rng.uniform(0, 360), rng.uniform(0, 360)), deg=True)
    nside = hp.get_nside(g_map)
    theta, phi = hp.pix2ang(nside, np.arange(g_map.size))
    theta_r, phi_r = rot(theta, phi)
    return hp.get_interp_val(g_map, theta_r, phi_r)


def random_rotation_test(
    t_map: np.ndarray,
    g_map: np.ndarray,
    mask: np.ndarray,
    binning: Any,
    lmax: int,
    n_rot: int,
    seed: int,
) -> dict[str, np.ndarray]:
    """Rotate tracer map randomly and compute Tg for each rotation."""
    rng = np.random.default_rng(seed)
    cl_rot = []
    for _ in range(n_rot):
        g_rot = _rotate_map_random(g_map, rng)
        res = compute_bandpowers_spin0_spin0(t_map, g_rot, mask, binning, lmax=lmax)
        cl_rot.append(res["cl_binned"])
    return {"cl_rot": np.asarray(cl_rot), "ell_eff": np.asarray(binning.get_effective_ells())}


def save_rotation_null_plot(null_res: dict[str, np.ndarray], out_path: str) -> None:
    """Save summary plot for rotated Tg null test."""
    ell = null_res["ell_eff"]
    arr = null_res["cl_rot"]
    mean = arr.mean(axis=0)
    std = arr.std(axis=0)

    plt.figure(figsize=(6, 4))
    plt.axhline(0.0, color="k", lw=1, ls="--")
    plt.errorbar(ell, mean, yerr=std, fmt="o", ms=4, label="rotated Tg mean ± std")
    plt.xlabel(r"$\\ell_{\\rm eff}$")
    plt.ylabel(r"$C_\\ell^{Tg}$")
    plt.title("Rotation null test")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
