#!/usr/bin/env python3
"""Build standardized maps/masks for v1 maps pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import healpy as hp
import numpy as np
import yaml

from src.io.masks import intersect_masks
from src.io.planck import load_planck_temperature
from src.io.tracers import load_tracer_overdensity
from src.preprocessing.healpix_utils import (
    apodize_mask,
    remove_monopole_dipole,
    ud_grade_map,
    ud_grade_mask,
)


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_toy_maps(cfg: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    nside = int(cfg["nside_out"])
    lmax = int(cfg["lmax"])
    toy_cfg = cfg["toy_mode"]
    seed = int(toy_cfg.get("seed", 0))
    amp = float(toy_cfg.get("toy_signal_amp", 0.0))

    ell = np.arange(lmax + 1)
    cl_tt = np.zeros(lmax + 1)
    cl_gg = np.zeros(lmax + 1)
    cl_tg = np.zeros(lmax + 1)
    valid = ell >= 2
    cl_tt[valid] = 1e-5 / (ell[valid] * (ell[valid] + 1))
    cl_gg[valid] = 5e-6 / (ell[valid] * (ell[valid] + 1))
    cl_tg[valid] = amp * np.sqrt(cl_tt[valid] * cl_gg[valid])

    np.random.seed(seed)
    t_map, g_map = hp.synfast([cl_tt, cl_gg, cl_tg], nside=nside, lmax=lmax, new=True, pol=False)
    mask = np.ones(hp.nside2npix(nside), dtype=float)
    return np.asarray(t_map), np.asarray(g_map), mask


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    out_dir = Path(cfg["output"]["processed_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    if cfg.get("toy_mode", {}).get("enabled", False):
        t_map, g_map, analysis_mask = build_toy_maps(cfg)
        meta = {"mode": "toy", "toy_mode": cfg["toy_mode"]}
    else:
        t_raw, t_mask_raw, t_meta = load_planck_temperature(cfg)
        g_raw, g_mask_raw, g_meta = load_tracer_overdensity(cfg)
        nside_out = int(cfg["nside_out"])

        t_map = ud_grade_map(t_raw, nside_out=nside_out, power=None)
        g_map = ud_grade_map(g_raw, nside_out=nside_out, power=None)
        t_mask = ud_grade_mask(t_mask_raw, nside_out=nside_out)
        g_mask = ud_grade_mask(g_mask_raw, nside_out=nside_out)
        analysis_mask = intersect_masks(t_mask, g_mask)
        meta = {"mode": "real", "cmb": t_meta, "tracer": g_meta}

    if cfg.get("apodize_deg", 0.0) > 0:
        analysis_mask = apodize_mask(analysis_mask, float(cfg["apodize_deg"]))

    if cfg.get("remove_dipole", True):
        g_map = remove_monopole_dipole(g_map, analysis_mask)

    np.save(out_dir / "t_map.npy", t_map)
    np.save(out_dir / "g_map.npy", g_map)
    np.save(out_dir / "mask.npy", analysis_mask)
    with open(out_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Wrote processed maps to {out_dir}")


if __name__ == "__main__":
    main()
