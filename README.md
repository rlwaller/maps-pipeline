# maps-ror

Research-grade, reproducible map/spectra toy pipeline with a conda-first workflow and pip fallback.

## Conda-first quickstart (recommended)

Use `micromamba` or `mamba` for reproducible environments from `environment.yml`.

```bash
# from repo root
make conda
micromamba activate maps-ror   # or: mamba activate maps-ror
make toy
make test
```

If the environment already exists and you want to sync it to `environment.yml`:

```bash
make conda-update
```

## Pip fallback quickstart

If conda/mamba are unavailable, use a virtual environment and pip requirements.

```bash
python -m venv .venv
source .venv/bin/activate
make install
make toy
make test
```

## How to cite

This repository includes citation metadata in `CITATION.cff`.

- Please cite the software using the fields in `CITATION.cff`.
- For archival/release citations, we recommend enabling Zenodo DOI minting for GitHub releases later.
