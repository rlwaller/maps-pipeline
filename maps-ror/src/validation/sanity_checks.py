"""Basic sanity checks for processed maps and spectra outputs."""

from __future__ import annotations

import numpy as np


def assert_finite(name: str, arr: np.ndarray) -> None:
    """Raise if array contains non-finite values."""
    if not np.isfinite(arr).all():
        raise ValueError(f"{name} contains non-finite values")
