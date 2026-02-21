import importlib.util
from pathlib import Path
import subprocess

import pytest


def _missing_core_deps():
    required = ("numpy", "pandas", "healpy")
    return [name for name in required if importlib.util.find_spec(name) is None]


def test_toy_pipeline_generates_outputs() -> None:
    missing = _missing_core_deps()
    if missing:
        pytest.skip(
            "Skipping toy pipeline test because required core dependencies are missing: "
            + ", ".join(missing)
        )

    subprocess.run(
        ["python", "scripts/build_maps.py", "--config", "configs/default.yaml"],
        check=True,
    )
    subprocess.run(
        ["python", "scripts/run_spectra.py", "--config", "configs/default.yaml"],
        check=True,
    )

    map_path = Path("data_processed/mock_map.npy")
    table_path = Path("results/tables/spectrum.csv")
    fig_path = Path("results/figures/spectrum.png")

    assert map_path.exists()
    assert table_path.exists()
    assert fig_path.exists()

    import pandas as pd

    df = pd.read_csv(table_path)
    assert set(df.columns) == {"frequency", "power"}
    assert len(df) > 0