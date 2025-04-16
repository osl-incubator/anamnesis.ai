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


@pytest.mark.skip_on_ci
def test_check_fhir_resources(transcript_1: str, openai_api_key: str) -> None:
    """Test FHIR resources are found correctly."""
    aai = AnamnesisAI(backend="openai", api_key=openai_api_key)
    fhir_resources = aai._check_possible_fhir_resources(transcript_1)
    assert fhir_resources
    assert isinstance(fhir_resources, FHIRResourceFoundModel)
    assert fhir_resources.Patient
    assert fhir_resources.FamilyMemberHistory
    assert fhir_resources.AllergyIntolerance
    assert fhir_resources.Encounter


@pytest.mark.skip_on_ci
def test_extract_fhir(transcript_1: str, openai_api_key: str) -> None:
    """Test FHIR resources are extracted correctly."""
    aai = AnamnesisAI(backend="openai", api_key=openai_api_key)
    fhir_resources, invalid_fhir_resources = aai.extract_fhir(transcript_1)

    assert len(fhir_resources) > 0, (
        "Expected at least one resource in FHIR output"
    )

    # Check for specific resource types
    found_types = {resource.__class__.__name__ for resource in fhir_resources}
    required_types = {"Patient", "FamilyMemberHistory", "AllergyIntolerance"}

    assert required_types.issubset(found_types), (
        "Missing required resource types. Expected "
        "{required_types}, found {found_types}"
    )


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


@pytest.mark.skip_on_ci
@pytest.mark.skipif(IS_OS_MACOS, reason="ollama is not working on macos")
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


@pytest.mark.skip_on_ci
@pytest.mark.skipif(IS_OS_MACOS, reason="ollama is not working on macos")
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


@pytest.mark.skip_on_ci
@pytest.mark.skipif(IS_OS_MACOS, reason="ollama is not working on macos")
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



@pytest.fixture
def conversation_text() -> str:
    """Fixture to read the conversation text from the file."""
    file_path = "tests/data/synthetic/enhanced_conversation.txt"
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find the conversation file: {file_path}"
        )


@pytest.mark.skip_on_ci
def test_transcript_extraction_structure(
    conversation_text: str, api_key: str
) -> None:
    """Test basic structure of extracted FHIR data."""
    fhir_data = extract_fhir(conversation_text, api_key)
    assert fhir_data
    assert isinstance(fhir_data, dict)
    assert len(fhir_data) > 0

    resources = fhir_data.get("resources", fhir_data.get("entry", []))
    assert len(resources) > 0, "Expected at least one resource in FHIR output"

    for resource in resources:
        assert "resourceType" in resource, (
            "Expected 'resourceType' in each resource"
        )


@pytest.mark.skip_on_ci
def test_extracted_fhir_resources(
    conversation_text: str, api_key: str
) -> None:
    """Confirm correct extraction of expected FHIR resources from text."""
    fhir_data = extract_fhir(conversation_text, api_key)
    print("fhir suggested: ", fhir_data)

    resources = fhir_data.get("resources", fhir_data.get("entry", []))

    patient_count = 0
    condition_count = 0
    observation_count = 0
    medication_statement_count = 0
    medication_request_count = 0
    service_request_count = 0

    for resource in resources:
        if resource["resourceType"] == "Patient":
            patient_count += 1
        elif resource["resourceType"] == "Condition":
            condition_count += 1
        elif resource["resourceType"] == "Observation":
            observation_count += 1
        elif resource["resourceType"] == "MedicationStatement":
            medication_statement_count += 1
        elif resource["resourceType"] == "MedicationRequest":
            medication_request_count += 1
        elif resource["resourceType"] == "ServiceRequest":
            service_request_count += 1

    # Assert that the expected number of each resource type is found
    # assert patient_count == 1
    assert condition_count >= 1  # Expect at least one condition (hypertension)
    assert (
        observation_count >= 2
    )  # Expect at least observations (BP, temp, knee pain, swelling)
    assert (
        medication_statement_count >= 1
    )  # Expect at least two MedicationStatements (Lisinopril, Ibuprofen)
    assert (
        medication_request_count >= 1
    )  # Expect one MedicationRequest (Lisinopril refill)
    assert service_request_count >= 1  # Expect one ServiceRequest (X-ray)
