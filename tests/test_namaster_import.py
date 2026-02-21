import importlib.util

import pytest


@pytest.mark.namaster
def test_optional_namaster_stack_importable() -> None:
    if importlib.util.find_spec("healpy") is None or importlib.util.find_spec("pymaster") is None:
        pytest.skip("Skipping NaMaster-dependent test: healpy or pymaster is unavailable in this environment.")
