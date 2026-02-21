import healpy as hp
import numpy as np

from src.preprocessing.healpix_utils import remove_monopole_dipole, ud_grade_map


def test_ud_grade_map_size():
    m = np.ones(hp.nside2npix(16))
    m2 = ud_grade_map(m, nside_out=8)
    assert m2.size == hp.nside2npix(8)


def test_remove_monopole_dipole_no_nans():
    nside = 16
    npix = hp.nside2npix(nside)
    m = np.random.default_rng(0).normal(size=npix)
    mask = np.ones(npix)
    out = remove_monopole_dipole(m, mask)
    assert np.isfinite(out).all()
