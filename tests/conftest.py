"""Configuration for the tests."""

from __future__ import annotations

import kagglehub
import pyreadr
import pytest


@pytest.fixture
def data():
    """Return a dataset for the tests."""
    path = kagglehub.dataset_download(
        "maalona/hospital-triage-and-patient-history-data"
    )
    result = pyreadr.read_r(f"{path}/5v_cleandf.rdata")
    breakpoint()
    return result
