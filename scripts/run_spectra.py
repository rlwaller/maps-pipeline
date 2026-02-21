#!/usr/bin/env python3
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a deterministic toy spectrum stage.")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    map_path = Path(cfg.get("output_map", "data_processed/mock_map.npy"))
    table_path = Path(cfg.get("output_table", "results/tables/spectrum.csv"))
    fig_path = Path(cfg.get("output_figure", "results/figures/spectrum.png"))

    signal = np.load(map_path)
    freq = np.fft.rfftfreq(signal.shape[0], d=1.0)
    power = np.abs(np.fft.rfft(signal)) ** 2

    table_path.parent.mkdir(parents=True, exist_ok=True)
    fig_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame({"frequency": freq, "power": power})
    df.to_csv(table_path, index=False)

    plt.figure(figsize=(6, 4))
    plt.plot(freq, power)
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=150)
    plt.close()

    print(f"Saved spectrum table to {table_path}")
    print(f"Saved spectrum plot to {fig_path}")


if __name__ == "__main__":
    main()
