"""Tracer map loaders for maps pipeline v1."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from src.preprocessing.healpix_utils import read_healpix_fits


def load_tracer_overdensity(config: dict[str, Any]) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    """Load tracer overdensity HEALPix map and mask."""
    tr_cfg = config["maps"]["tracer"]
    if tr_cfg.get("kind") != "unwise":
        raise NotImplementedError("v1 supports only maps.tracer.kind = 'unwise'.")

    path_map = Path(tr_cfg["path_map"])
    path_mask = Path(tr_cfg["path_mask"])
    if not path_map.exists() or not path_mask.exists():
        raise FileNotFoundError(
            "Missing tracer inputs. Please run scripts/fetch_data.sh and place files at "
            f"{path_map} and {path_mask}."
        )

    g_map = read_healpix_fits(path_map)
    g_mask = read_healpix_fits(path_mask)
    meta = {"kind": "unwise", "path_map": str(path_map), "path_mask": str(path_mask)}
    return g_map, g_mask, meta
