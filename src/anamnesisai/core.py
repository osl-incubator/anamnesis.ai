"""Anamnesis AI core functions."""

from __future__ import annotations

import warnings

from typing import Type, cast

from fhir.resources.encounter import Encounter
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.resource import Resource
from pydantic import BaseModel
from rago.generation import OpenAIGen
from typeguard import typechecked

PROMPT_TEMPLATE = """
You are a FHIR Resource generating expert. Given a conversion
between doctor and patient, first create a syntactically correct
FHIR resource in pure JSON Format as specified by the user then look at
the results  and return the FHIR resource to the input conversation.
Never create random values for values that are not present in the
conversation. You must return only the columns if the value is present
in the conversation. Extract and generate only the following FHIR
resources from the conversations and exams:

- {resource_detail}

Use clear and concise language for each resource. Maintain patient
confidentiality and adhere to HIPAA regulations. Strive for accuracy
and consistency in your FHIR structures.

In the conversation, `D:` means it is from the Doctor, and `P:` means
it is from the Patience.

Conversation:
```
{query}
```
"""

RESOURCES_CLASSES = {
    "patient": Patient,
    "practitioner": Practitioner,
    "encounter": Encounter,
    "observation": Observation,
}

RESOURCES_DETAILS = {
    "patient": (
        "capture the patient's demographics and medical history details."
    ),
    "practitioner": "identify the doctor involved in the encounter.",
    "encounter": (
        "describe the patient-doctor interaction, including the reason for "
        "the visit."
    ),
    "observation": (
        "record the patient's reported symptoms and the physical "
        "exam findings."
    ),
}


@typechecked
def extract_fhir_openai(text: str, api_key: str) -> dict[str, Resource]:
    """Extract FHIR from the given text."""
    results: dict[str, Resource] = {}
    for resource_name, resource_detail in RESOURCES_DETAILS.items():
        fhir_class: Type[BaseModel] = RESOURCES_CLASSES[resource_name]

        resource_prompt = (
            f"```Resource name: {resource_name}```\n"
            f"```Resource explanation: {resource_detail}```\n"
        )
        prompt_template = PROMPT_TEMPLATE.replace(
            "{resource_detail}",
            resource_prompt,
        )
        try:
            gen = OpenAIGen(
                prompt_template=prompt_template,
                model_name="gpt-4o-mini",
                api_key=api_key,
                output_max_length=10384,
                structured_output=fhir_class,
            )
            result = gen.generate(query=text, context=[])
        except Exception as e:
            warnings.warn(str(e))
            continue

        fhir_obj = cast(Resource, result)
        results[resource_name] = fhir_obj
    return results
