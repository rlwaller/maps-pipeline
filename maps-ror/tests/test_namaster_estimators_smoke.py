import healpy as hp
import numpy as np

from src.spectra.binning import make_nmt_bin
from src.spectra.namaster_estimators import compute_Tg_and_gg


def test_namaster_smoke_toy():
    nside = 32
    lmax = 64
    ell = np.arange(lmax + 1)
    cl_tt = np.zeros(lmax + 1)
    cl_gg = np.zeros(lmax + 1)
    cl_tg = np.zeros(lmax + 1)
    v = ell >= 2
    cl_tt[v] = 1e-5 / (ell[v] * (ell[v] + 1))
    cl_gg[v] = 8e-6 / (ell[v] * (ell[v] + 1))
    cl_tg[v] = 0.2 * np.sqrt(cl_tt[v] * cl_gg[v])

    t_map, g_map = hp.synfast([cl_tt, cl_gg, cl_tg], nside=nside, lmax=lmax, new=True, pol=False)
    mask = np.ones(hp.nside2npix(nside))
    b = make_nmt_bin(nside=nside, bin_edges=[2, 10, 20, 40, lmax + 1], lmax=lmax)

    out = compute_Tg_and_gg(t_map=t_map, g_map=g_map, mask=mask, binning=b, lmax=lmax)
    assert np.isfinite(out["tg"]["cl_binned"]).all()
    assert len(out["tg"]["cl_binned"]) == len(out["tg"]["ell_eff"])
