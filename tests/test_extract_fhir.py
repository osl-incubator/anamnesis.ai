"""Tests for anamnesisai package."""

from __future__ import annotations

import platform
import random

from typing import Literal

import pytest

from anamnesisai import AnamnesisAI
from anamnesisai.supported_fhir import FHIRResourceFoundModel

IS_OS_MACOS = platform.system().lower() == "darwin"

API_MAP = {
    "openai": "openai_api_key",
    "ollama": "",
}

CI_BACKEND = ["ollama"]
NO_CI_BACKEND = ["openai"]


def test_fixture(transcript_1: str, openai_api_key: str) -> None:
    """Run simple test for fixture to avoid zero tests collected."""
    assert transcript_1
    assert openai_api_key


@pytest.mark.skip_on_ci
@pytest.mark.parametrize("backend", NO_CI_BACKEND)
def test_random_transcript_file_extraction(
    list_of_files: list[str],
    openai_api_key: str,
    backend: Literal["openai", "ollama"],
) -> None:
    """Test FHIR extraction on a randomly selected transcript file."""
    assert len(list_of_files) > 0, "No transcript files found for testing"

    random_file = random.choice(list_of_files)
    print(f"Testing random transcript file: {random_file}")

    with open(random_file, "r") as f:
        transcript_content = f.read()

    api_key = openai_api_key if backend == "openai" else ""
    aai = AnamnesisAI(backend=backend, api_key=api_key)

    fhir_resources, invalid_fhir_resources = aai.extract_fhir(
        transcript_content
    )

    assert len(fhir_resources) > 0, (
        f"Expected at least one FHIR resource from {random_file}"
    )


@pytest.mark.skip_on_ci
@pytest.mark.parametrize("backend", NO_CI_BACKEND)
def test_extract_fhir(
    transcript_1: str,
    openai_api_key: str,
    backend: Literal["openai", "ollama"],
) -> None:
    """Test FHIR resources are extracted correctly."""
    api_key = openai_api_key if backend == "openai" else ""
    aai = AnamnesisAI(backend=backend, api_key=api_key)
    fhir_resources, invalid_fhir_resources = aai.extract_fhir(transcript_1)

    assert len(fhir_resources) > 0, (
        "Expected at least one resource in FHIR output"
    )

    found_types = {resource.__class__.__name__ for resource in fhir_resources}
    required_types = {"Patient", "FamilyMemberHistory", "AllergyIntolerance"}

    assert required_types.issubset(
        found_types
    ), f"""Missing required resource types. Expected {required_types},
        found {found_types}"""


@pytest.mark.skip_on_ci
@pytest.mark.skipif(IS_OS_MACOS, reason="ollama is not working on macos")
@pytest.mark.parametrize("backend", CI_BACKEND)
def test_check_fhir_resources_ci(
    transcript_1: str, backend: Literal["openai", "ollama"]
) -> None:
    """Test if fhir resources present in the text for CI environments."""
    aai = AnamnesisAI(backend=backend, api_key="")
    fhir_data = aai._check_possible_fhir_resources(transcript_1)

    assert fhir_data
    assert isinstance(fhir_data, FHIRResourceFoundModel)
    assert fhir_data.Patient is True
    assert fhir_data.FamilyMemberHistory is True


@pytest.mark.skip_on_ci
@pytest.mark.skipif(IS_OS_MACOS, reason="ollama is not working on macos")
@pytest.mark.parametrize("backend", CI_BACKEND)
def test_random_transcript_file_extraction_ci(
    list_of_files: list[str], backend: Literal["openai", "ollama"]
) -> None:
    """Test FHIR extraction on a randomly selected transcript file for CI."""
    assert len(list_of_files) > 0, "No transcript files found for testing"

    random_file = random.choice(list_of_files)
    print(f"Testing random transcript file: {random_file}")

    with open(random_file, "r") as f:
        transcript_content = f.read()

    aai = AnamnesisAI(backend=backend, api_key="")

    fhir_resources, invalid_fhir_resources = aai.extract_fhir(
        transcript_content
    )
    assert len(fhir_resources) > 0, (
        f"Expected at least one FHIR resource from {random_file}"
    )
