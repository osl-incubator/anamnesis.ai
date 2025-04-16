"""Tests for anamnesisai package FHIR extraction capabilities."""

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
