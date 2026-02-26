ENV_NAME ?= maps-ror
MAMBA_BIN := $(shell command -v micromamba || command -v mamba)

.PHONY: conda conda-update venv install test toy clean docker-build docker-test docker-toy

conda:
	@if [ -z "$(MAMBA_BIN)" ]; then \
		echo "No micromamba or mamba found. Install one of them, then run: $(MAKE) conda"; \
		exit 1; \
	fi
	$(MAMBA_BIN) env create -n $(ENV_NAME) -f environment.yml

conda-update:
	@if [ -z "$(MAMBA_BIN)" ]; then \
		echo "No micromamba or mamba found. Install one of them, then run: $(MAKE) conda-update"; \
		exit 1; \
	fi
	$(MAMBA_BIN) env update -n $(ENV_NAME) -f environment.yml --prune

venv:
	python -m venv .venv

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=maps-ror pytest -q maps-ror/tests

toy:
	python scripts/build_maps.py --config configs/default.yaml
	python scripts/run_spectra.py --config configs/default.yaml

clean:
	rm -rf data_processed/*
	rm -f results/tables/*.csv
	rm -f results/figures/*.png


docker-build:
	docker compose build

docker-test:
	docker compose run --rm maps make test

docker-toy:
	docker compose run --rm maps make toy
