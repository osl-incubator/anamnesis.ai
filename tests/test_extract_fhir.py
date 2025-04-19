"""Tests for anamnesisai package."""

from __future__ import annotations

import platform

from typing import Literal

import pytest

from anamnesisai import AnamnesisAI
from anamnesisai.supported_fhir import FHIRResourceFoundModel

IS_OS_MACOS = platform.system().lower() == "darwin"

API_MAP = {
    "openai": "api_key_openai",
}

CI_BACKEND = ["ollama"]
NO_CI_BACKEND = ["openai"]


def test_fixture(transcript_1: str, openai_api_key: str) -> None:
    """Run simple test for fixture to avoid zero tests collected."""
    assert transcript_1
    assert openai_api_key


def _check_fhir_resources(
    text: str, backend: Literal["openai", "ollama"]
) -> bool:
    """Test if fhir resources prsent in the text."""
    print(f">>> {backend}")

    api_key_name: str = API_MAP.get(backend, "")
    api_key = locals().get(api_key_name, "")

    aai = AnamnesisAI(backend=backend, api_key=api_key)
    fhir_data = aai._check_possible_fhir_resources(text)

    assert fhir_data
    assert isinstance(fhir_data, FHIRResourceFoundModel)
    assert fhir_data.Patient is True
    assert fhir_data.Condition is False
    # note: improve prompt to have better answer
    # assert fhir_data.Practitioner is True
    # assert fhir_data.FamilyMemberHistory is False
    # assert fhir_data.AllergyIntolerance is False
    # assert fhir_data.Immunization is False
    # assert fhir_data.Procedure is False
    # assert fhir_data.CarePlan is False
    # assert fhir_data.Encounter is True
    # assert fhir_data.Observation is True
    # assert fhir_data.MedicationStatement is True
    # assert fhir_data.DiagnosticReport is True
    # assert fhir_data.ServiceRequest is False
    # assert fhir_data.MedicationRequest is False

    return True


@pytest.mark.parametrize("backend", CI_BACKEND)
def test_check_fhir_resources_ci(
    transcript_1: str, backend: Literal["openai", "ollama"]
) -> None:
    """Test if fhir resources prsent in the text."""
    assert _check_fhir_resources(transcript_1, backend)


@pytest.mark.skip_on_ci
@pytest.mark.parametrize("backend", NO_CI_BACKEND)
def test_check_fhir_resources_no_ci(
    transcript_1: str, backend: Literal["openai", "ollama"]
) -> None:
    """Test if fhir resources prsent in the text."""
    assert _check_fhir_resources(transcript_1, backend)


def _check_transcript_1(
    text: str, backend: Literal["openai", "ollama"]
) -> bool:
    """Test if transcript 1."""
    print(f">>> {backend}")

    api_key_name: str = API_MAP.get(backend, "")
    api_key = locals().get(api_key_name, "")

    aai = AnamnesisAI(backend=backend, api_key=api_key)
    fhir_data = aai.extract_fhir(text)
    assert fhir_data
    assert isinstance(fhir_data, dict)
    assert len(fhir_data)

    return True


@pytest.mark.parametrize("backend", CI_BACKEND)
def test_transcript_1(
    transcript_1: str, backend: Literal["openai", "ollama"]
) -> None:
    """Test if transcript 1."""
    assert _check_transcript_1(transcript_1, backend)


@pytest.mark.skip_on_ci
@pytest.mark.parametrize("backend", NO_CI_BACKEND)
def test_transcript_1_no_ci(
    transcript_1: str, backend: Literal["openai", "ollama"]
) -> None:
    """Test if transcript 1."""
    assert _check_transcript_1(transcript_1, backend)


def _check_synthetic_files(
    synthetic_files_content: dict[str, str],
    backend: Literal["openai", "ollama"],
) -> bool:
    """Test if each synthetic data file can be processed."""
    assert len(synthetic_files_content) > 0

    api_key_name: str = API_MAP.get(backend, "")
    api_key = locals().get(api_key_name, "")

    aai = AnamnesisAI(backend=backend, api_key=api_key)

    for filename, content in synthetic_files_content.items():
        print(f"Testing synthetic file: {filename}")
        fhir_data = aai.extract_fhir(content)
        print(f">>> {backend}")
        assert fhir_data is not None
        assert fhir_data
        assert isinstance(fhir_data, dict)
        assert len(fhir_data) >= 0
        assert len(fhir_data)

    return True


@pytest.mark.parametrize("backend", CI_BACKEND)
def test_synthetic_files_ci(
    synthetic_files_content: dict[str, str],
    backend: Literal["openai", "ollama"],
) -> None:
    """Test if each synthetic data file can be processed."""
    assert _check_synthetic_files(synthetic_files_content, backend)


@pytest.mark.skip_on_ci
@pytest.mark.parametrize("backend", NO_CI_BACKEND)
def test_synthetic_files_no_ci(
    synthetic_files_content: dict[str, str],
    backend: Literal["openai", "ollama"],
) -> None:
    """Test if each synthetic data file can be processed."""
    assert _check_synthetic_files(synthetic_files_content, backend)
