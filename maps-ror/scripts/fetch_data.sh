#!/usr/bin/env bash
set -euo pipefail

mkdir -p data_raw/planck data_raw/unwise

echo "Created data directories under data_raw/."
echo "Place files at:"
echo "  data_raw/planck/SMICA_T.fits"
echo "  data_raw/planck/COMMON_MASK.fits"
echo "  data_raw/unwise/unwise_overdensity.fits"
echo "  data_raw/unwise/unwise_mask.fits"
echo
echo "Example placeholder commands (disabled):"
echo "  # wget -O data_raw/planck/SMICA_T.fits <PLANCK_URL>"
echo "  # wget -O data_raw/planck/COMMON_MASK.fits <PLANCK_MASK_URL>"
echo "  # wget -O data_raw/unwise/unwise_overdensity.fits <UNWISE_MAP_URL>"
echo "  # wget -O data_raw/unwise/unwise_mask.fits <UNWISE_MASK_URL>"
