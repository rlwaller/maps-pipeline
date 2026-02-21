from pathlib import Path
import subprocess

import pandas as pd


def test_toy_pipeline_generates_outputs() -> None:
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

    df = pd.read_csv(table_path)
    assert set(df.columns) == {"frequency", "power"}
    assert len(df) > 0
