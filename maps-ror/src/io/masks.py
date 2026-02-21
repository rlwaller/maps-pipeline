"""Mask helpers for combining analysis masks."""

from __future__ import annotations

import numpy as np


def intersect_masks(*masks: np.ndarray) -> np.ndarray:
    """Compute intersection mask (float in [0,1])."""
    if not masks:
        raise ValueError("At least one mask is required.")
    out = np.asarray(masks[0], dtype=float)
    for m in masks[1:]:
        out *= np.asarray(m, dtype=float)
    return np.clip(out, 0.0, 1.0)
