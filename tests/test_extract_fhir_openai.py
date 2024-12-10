"""Tests for anamnesisai package."""

from __future__ import annotations

import os

from typing import Optional

import pytest

from anamnesisai import extract_fhir_openai


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
    fhir_data = extract_fhir_openai(transcript_1, api_key)
    assert fhir_data
    assert isinstance(fhir_data, dict)
    assert len(fhir_data)
