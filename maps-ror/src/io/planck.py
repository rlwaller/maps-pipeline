"""Planck data loaders for maps pipeline v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from src.preprocessing.healpix_utils import read_healpix_fits


def load_planck_temperature(config: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Load Planck SMICA temperature map and mask for v1."""
    cmb_cfg = config["maps"]["cmb"]
    if cmb_cfg.get("kind") != "planck_smica":
        raise NotImplementedError("v1 supports only maps.cmb.kind = 'planck_smica'.")

    path_map = Path(cmb_cfg["path_map"])
    path_mask = Path(cmb_cfg["path_mask"])
    if not path_map.exists() or not path_mask.exists():
        raise FileNotFoundError(
            "Missing Planck inputs. Please run scripts/fetch_data.sh and place files at "
            f"{path_map} and {path_mask}."
        )

    t_map = read_healpix_fits(path_map)
    t_mask = read_healpix_fits(path_mask)
    meta = {"kind": "planck_smica", "path_map": str(path_map), "path_mask": str(path_mask)}
    return t_map, t_mask, meta
