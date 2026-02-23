# maps-ror

> **Note:** Codex hosted environments may block package installs; run locally or rely on CI.

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

## Docker (recommended on macOS for NaMaster)

Use Docker to build and run the Linux environment, which avoids local Apple Silicon build issues for `healpy`/`pymaster`.

```bash
make docker-build
make docker-toy
make docker-test
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
