"""Anamnesis AI core functions."""

from __future__ import annotations

import warnings

from typing import Type, cast

from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.condition import Condition
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.encounter import Encounter
from fhir.resources.familymemberhistory import FamilyMemberHistory
from fhir.resources.immunization import Immunization
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.procedure import Procedure
from fhir.resources.resource import Resource
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

{resource_detail}

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

RESOURCES_CLASSES = (
    Patient,
    Condition,
    Practitioner,
    Encounter,
    Observation,
    FamilyMemberHistory,
    AllergyIntolerance,
    Immunization,
    MedicationStatement,
    Procedure,
    DiagnosticReport,
)


def get_resource_detail(resource_class: Type[Resource]) -> str:
    """Get the resource detail from the resource class."""
    # note: remove the first part because it is a just disclaimer about the
    #       python object.
    idx = 0
    docstring = resource_class.__doc__ or ""
    try:
        idx = docstring.index("\n\n")
    except ValueError:
        pass
    return " ".join(docstring[idx:].replace("\n", " ").strip().split())


@typechecked
def extract_fhir_openai(text: str, api_key: str) -> dict[str, Resource]:
    """Extract FHIR from the given text."""
    results: dict[str, Resource] = {}
    for fhir_class in RESOURCES_CLASSES:
        resource_name = fhir_class.__name__
        resource_detail = get_resource_detail(fhir_class)

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
                output_max_length=10384,  # note: calc this number
                structured_output=fhir_class,
            )
            result = gen.generate(query=text, context=[])
        except Exception as e:
            warnings.warn(str(e))
            continue

        fhir_obj = cast(Resource, result)
        results[resource_name] = fhir_obj
    return results
