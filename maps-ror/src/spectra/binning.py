"""NaMaster binning utilities."""

from __future__ import annotations

import numpy as np
import pymaster as nmt


def make_nmt_bin(nside: int, bin_edges: list[int], lmax: int) -> nmt.NmtBin:
    """Build NaMaster binning object from explicit bin edges."""
    edges = np.asarray(bin_edges, dtype=int)
    if edges[0] < 2:
        raise ValueError("bin_edges must start at ell>=2")
    if edges[-1] != (lmax + 1):
        raise ValueError(
        f"By convention, last bin edge must equal lmax+1 (got {edges[-1]} vs {lmax+1}). "
        "Use half-open bin edges: [l0, l1) with last edge = lmax+1."
    )
    return nmt.NmtBin.from_edges(edges[:-1], edges[1:])


def effective_ells(binning: nmt.NmtBin) -> np.ndarray:
    """Return effective ell per bandpower bin."""
    return np.asarray(binning.get_effective_ells())
