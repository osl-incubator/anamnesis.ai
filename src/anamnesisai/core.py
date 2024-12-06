"""Anamnesis AI core functions."""

from __future__ import annotations

from typing import cast

from rago.generation import OpenAIGen


def extract_fhir(text: str) -> str:
    """Extract FHIR from the given text."""
    prompt_template = """
    You are a FHIR Resource generating expert. Given a conversion
    between doctor and patient, first create a syntactically correct
    FHIR resource in JSON Format as specified by the user then look at
    the results  and return the FHIR resource to the input conversation.
    Never create random values for values that are not present in the
    conversation. You must only the columns that are needed to answer
    the question. Wrap each column name in backticks (`) to denote
    them as delimited identifiers.
    Generate the following FHIR resources based on the conversation and exam:
    Patient: Capture the patient's demographics and medical history details.
    Practitioner: Identify the doctor involved in the encounter.
    Encounter: Describe the patient-doctor interaction, including the reason
    for the visit.
    Observation: Record the patient's reported symptoms and the physical
    exam findings.

    Use clear and concise language for each resource. Maintain patient
    confidentiality and adhere to HIPAA regulations. Strive for accuracy
    and consistency in your FHIR structures.

    Conversation:
    ```
    {query}
    ```
    """
    gen = OpenAIGen(
        prompt_template=prompt_template,
    )
    result = gen.generate(query=text, context=[])
    return cast(str, result)
