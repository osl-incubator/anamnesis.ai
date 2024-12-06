"""Configuration for the tests."""

from __future__ import annotations

import zipfile

from pathlib import Path

import pandas as pd
import pytest


def extract_zip_file(zip_path: str, extract_to: str) -> None:
    """
    Extracts a ZIP file to a specified directory.

    Parameters
    ----------
    zip_path : str
        Path to the ZIP file.
    extract_to : str
        Directory where the contents will be extracted.
    """
    # Ensure the extraction directory exists
    Path(extract_to).mkdir(parents=True, exist_ok=True)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted '{zip_path}' to '{extract_to}'.")


@pytest.fixture
def data() -> pd.DataFrame:
    """Return a dataset for the tests."""
    # Example usage
    path_dir = Path(__file__).parent / "data"
    filename = "hospital-triage-and-patient-history"

    zip_file_path = path_dir / f"{filename}.zip"
    extraction_directory = path_dir

    extract_zip_file(zip_file_path, extraction_directory)

    data_path = path_dir / f"{filename}.parquet"

    return pd.read_parquet(data_path)
