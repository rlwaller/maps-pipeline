#!/usr/bin/env python3
"""Run NaMaster spectra and validation null tests for v1 pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import os
import tempfile

os.environ["MPLBACKEND"] = "Agg"
mpl_tmp = tempfile.mkdtemp(prefix="mplconfig_")
os.environ["MPLCONFIGDIR"] = mpl_tmp

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

print("Matplotlib pyplot imported", flush=True)

import numpy as np
import pandas as pd
import yaml

from src.spectra.binning import make_nmt_bin
from src.spectra.namaster_estimators import compute_Tg_and_gg
from src.validation.null_tests import random_rotation_test, save_rotation_null_plot
from src.validation.sanity_checks import assert_finite


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_bandpower_plot(ell: np.ndarray, cl: np.ndarray, out_path: Path, title: str, ylabel: str) -> None:
    print("Entered save_bandpower_plot", flush=True)
    plt.figure(figsize=(6, 4))
    plt.axhline(0.0, color="k", ls="--", lw=1)
    plt.plot(ell, cl, marker="o")
    plt.xlabel(r"$\\ell_{\\rm eff}$")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    print(f"Saving figure to {out_path}", flush=True)
    plt.savefig(out_path, dpi=150)
    print("Saved figure", flush=True)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    cfg = load_config(args.config)
    print("Loaded config", cfg.get("nside_out"), cfg.get("lmax"), flush=True)
    proc_dir = Path(cfg["output"]["processed_dir"])
    res_dir = Path(cfg["output"]["results_dir"])
    tables_dir = res_dir / "tables"
    figs_dir = res_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    t_path, g_path, m_path = proc_dir / "t_map.npy", proc_dir / "g_map.npy", proc_dir / "mask.npy"
    if not (t_path.exists() and g_path.exists() and m_path.exists()):
        raise FileNotFoundError(
            f"Processed maps not found in {proc_dir}. Run `python scripts/build_maps.py --config {args.config}` first."
        )

    t_map = np.load(t_path)
    g_map = np.load(g_path)
    mask = np.load(m_path)
    print("Loaded processed maps", t_map.shape, g_map.shape, mask.shape, flush=True)

    nside = int(cfg["nside_out"])
    print("Creating binning", flush=True)
    binning = make_nmt_bin(nside=nside, bin_edges=cfg["bin_edges"], lmax=int(cfg["lmax"]))
    print("Binning lmax", getattr(binning, "lmax", None), flush=True)
    print("Computing Tg and gg (NaMaster)", flush=True)
    out = compute_Tg_and_gg(t_map=t_map, g_map=g_map, mask=mask, binning=binning, lmax=int(cfg["lmax"]))
    print("Computed bandpowers; saving tables", flush=True)

    for key in ["tg", "gg"]:
        assert_finite(f"{key}_cl", out[key]["cl_binned"])

    tg_df = pd.DataFrame({"ell_eff": out["tg"]["ell_eff"], "cl_tg": out["tg"]["cl_binned"]})
    gg_df = pd.DataFrame({"ell_eff": out["gg"]["ell_eff"], "cl_gg": out["gg"]["cl_binned"]})
    tg_df.to_csv(tables_dir / "tg_bandpowers.csv", index=False)
    gg_df.to_csv(tables_dir / "gg_bandpowers.csv", index=False)

    if cfg.get("plot", True):
        print("Plotting figures", flush=True)
        save_bandpower_plot(out["tg"]["ell_eff"], out["tg"]["cl_binned"], figs_dir / "tg_bandpowers.png", "Tg bandpowers", r"$C_\ell^{Tg}$")
        save_bandpower_plot(out["gg"]["ell_eff"], out["gg"]["cl_binned"], figs_dir / "gg_bandpowers.png", "gg bandpowers", r"$C_\ell^{gg}$")
    else:
        print("Skipping plotting (plot: false)", flush=True)

    null_cfg = cfg.get("null_test", {})
    n_rot = int(null_cfg.get("n_rot", 16))

    if n_rot <= 0:
        print("Skipping rotation null test (n_rot <= 0)", flush=True)
    else:
        print("Running rotation null test", n_rot, flush=True)
        null_res = random_rotation_test(
            t_map=t_map,
            g_map=g_map,
            mask=mask,
            binning=binning,
            lmax=int(cfg["lmax"]),
            n_rot=n_rot,
            seed=int(null_cfg.get("seed", 0)),
        )
        save_rotation_null_plot(null_res, str(figs_dir / "null_rotation_tg.png"))

    print(f"Wrote spectra tables to {tables_dir}")
    print(f"Wrote figures to {figs_dir}")


if __name__ == "__main__":
    main()
