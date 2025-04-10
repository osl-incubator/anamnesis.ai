"""Tests for anamnesisai package."""

from __future__ import annotations

import os

from typing import Optional

import pytest

from anamnesisai.openai import extract_fhir


@pytest.fixture
def api_key(env: dict[str, Optional[str]]) -> str:
    """Fixture for OpenAI API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Please set the OPENAI_API_KEY environment variable."
        )
    return api_key


def test_fixture(transcript_1: str, api_key: str) -> None:
    """Run simple test for fixture to avoid zero tests collected."""
    assert transcript_1
    assert api_key


@pytest.mark.skip_on_ci
def test_transcript_1(transcript_1: str, api_key: str) -> None:
    """Test if transcript 1."""
    fhir_data = extract_fhir(transcript_1, api_key)
    assert fhir_data
    assert isinstance(fhir_data, dict)
    assert len(fhir_data)


@pytest.mark.skip_on_ci
def test_synthetic_files(
    synthetic_files_content: dict[str, str], api_key: str
) -> None:
    """Test if each synthetic data file can be processed."""
    assert len(synthetic_files_content) > 0
    for filename, content in synthetic_files_content.items():
        print(f"Testing synthetic file: {filename}")
        fhir_data = extract_fhir(content, api_key)
        assert fhir_data is not None
        assert fhir_data
        assert isinstance(fhir_data, dict)
        assert len(fhir_data) >= 0
        assert len(fhir_data)
