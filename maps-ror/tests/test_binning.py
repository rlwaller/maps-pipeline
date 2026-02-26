import numpy as np

from src.spectra.binning import effective_ells, make_nmt_bin


def test_binning_shape_and_monotonic():
    lmax = 64
    b = make_nmt_bin(nside=32, bin_edges=[2, 10, 20, 40, lmax + 1], lmax=64)
    ell = effective_ells(b)
    assert len(ell) == 4
    assert np.all(np.diff(ell) > 0)
