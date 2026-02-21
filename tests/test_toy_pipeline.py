import importlib.util

import pytest


def _missing_core_deps():
    required = ("numpy", "pandas", "healpy")
    missing = [name for name in required if importlib.util.find_spec(name) is None]
    return missing


def test_toy_pipeline_runs_with_core_dependencies():
    missing = _missing_core_deps()
    if missing:
        pytest.skip(
            "Skipping toy pipeline test because required core dependencies are missing: "
            + ", ".join(missing)
        )

    import numpy as np
    import pandas as pd
    import healpy as hp

    df = pd.DataFrame({"x": np.arange(4), "y": np.arange(4) * 2})
    assert not df.empty
    assert hp.nside2npix(1) == 12
