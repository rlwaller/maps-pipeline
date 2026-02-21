#!/usr/bin/env python3
import argparse
from pathlib import Path

import numpy as np
import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a deterministic toy map.")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    seed = int(cfg.get("seed", 0))
    n_points = int(cfg.get("n_points", 32))
    out_path = Path(cfg.get("output_map", "data_processed/mock_map.npy"))
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(seed)
    x = np.linspace(0, 4 * np.pi, n_points)
    signal = np.sin(x) + 0.2 * rng.normal(size=n_points)
    np.save(out_path, signal)

    print(f"Saved map to {out_path}")


if __name__ == "__main__":
    main()
