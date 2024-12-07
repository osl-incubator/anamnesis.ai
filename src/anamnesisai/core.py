"""Anamnesis AI core functions."""

from __future__ import annotations

import json

from typing import Any, Dict, cast

from rago.generation import OpenAIGen
from typeguard import typechecked

PROMPT_TEMPLATE = """
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

In the conversation, `D:` means it is from the Doctor, and `P:` means
it is from the Patience.

The output should be in pure json format.

Conversation:
```
{query}
```
"""


@typechecked
def extract_fhir_openai(text: str, api_key: str) -> dict[str, Any]:
    """Extract FHIR from the given text."""
    gen = OpenAIGen(
        prompt_template=PROMPT_TEMPLATE,
        model_name="gpt-4o-mini",
        api_key=api_key,
        output_max_length=128000,
    )
    result = gen.generate(query=text, context=[])
    content = cast(str, result)
    return cast(Dict[str, Any], json.loads(content))
