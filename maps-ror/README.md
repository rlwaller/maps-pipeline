# Maps project pipeline (v1)

Minimal v1 implementation for:
- Planck SMICA temperature + one tracer (unWISE placeholder)
- Map ingest and standardization to common NSIDE/mask
- Binned pseudo-$C_\ell$ with NaMaster (spin-0 only)
- Spectra: $Tg$ and $gg$
- Tracer random-rotation null test
- Toy mode for reproducible local/CI runs

## Install

From repo root (`maps-ror/`):

```bash
pip install -r requirements.txt
```

## Data setup

To scaffold expected raw-data paths:

```bash
bash scripts/fetch_data.sh
```

If running with real data (`toy_mode.enabled: false`), place files at:
- `data_raw/planck/SMICA_T.fits`
- `data_raw/planck/COMMON_MASK.fits`
- `data_raw/unwise/unwise_overdensity.fits`
- `data_raw/unwise/unwise_mask.fits`

If files are missing, scripts raise `FileNotFoundError` with instructions.

## End-to-end run

```bash
python scripts/build_maps.py --config configs/default.yaml
python scripts/run_spectra.py --config configs/default.yaml
```

## Outputs

- Processed maps/mask/meta in `data_processed/run1/`
- Tables:
  - `results/tables/tg_bandpowers.csv`
  - `results/tables/gg_bandpowers.csv`
- Figures:
  - `results/figures/tg_bandpowers.png`
  - `results/figures/gg_bandpowers.png`
  - `results/figures/null_rotation_tg.png`

## Toy mode

`configs/default.yaml` has:

```yaml
toy_mode:
  enabled: true
  seed: 0
  toy_signal_amp: 0.2
```

- Uses `healpy.synfast` to generate correlated Gaussian `T` and `g` maps.
- `toy_signal_amp > 0` yields nonzero expected `Tg`.
- `toy_signal_amp = 0` yields null expected `Tg` (up to realization noise).

## Notes / non-goals in v1

Not implemented in v1:
- CMB lensing
- Multi-tracer support
- Covariance/MC/model fitting
- Shared residual analysis
- Parallel/performance optimizations
- CLI frameworks beyond `argparse`
