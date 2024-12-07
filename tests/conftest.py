"""Configuration for the tests."""

from __future__ import annotations

from glob import glob
from pathlib import Path
from typing import Optional

import pytest

from dotenv import dotenv_values, load_dotenv


@pytest.fixture
def env() -> dict[str, Optional[str]]:
    """Return a fixture for the environment variables from .env."""
    dotenv_file = Path(__file__).parent / ".env"
    load_dotenv(dotenv_file)
    return dotenv_values(dotenv_file)


@pytest.fixture
def list_of_files() -> list[str]:
    """Return a dataset for the tests."""
    data_path = Path(__file__).parent / "data" / "transcripts" / "*"
    return glob(str(data_path))


@pytest.fixture
def transcript_1(list_of_files: list[str]) -> str:
    """Return a dataset for the tests."""
    with open(list_of_files[0]) as f:
        return f.read()
