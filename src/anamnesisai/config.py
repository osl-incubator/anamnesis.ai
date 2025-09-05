"""Set of functions and variables used for configuration."""

from __future__ import annotations

from anamnesisai.supported_fhir import RESOURCES_CLASSES

_DISCLAIMER_TEXT = """
Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.
""".strip()

FHIR_RESOURCES_NAMES = {
    cls.__name__: " ".join(
        (cls.__doc__ or "")
        .replace(_DISCLAIMER_TEXT, "")
        .replace("\n", " ")
        .strip()
        .split()
    )
    for cls in RESOURCES_CLASSES
}

# prompt template for getting the given FHIR resource from the given
# conversation between m.d. and patient.
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
{context}
```
""".strip()

# prompt template for checking possible FHIR resources present in the given
# conversation
PROMPT_TEMPLATE_POSSIBLE_RESOURCES = """
please read the conversation between patient and md doctor in the given
context:

```
{context}
```

In the conversation, `D:` means Doctor, and `P:` means Patience.

Question: what fhir resource/types could be extract from this conversation?
The answer should be a JSON with the name of the types/resources as a key and
true or false as the value. `true` if the types/resource is present in the
conversation or `false` otherwise. The current FHIR resources you should check
are:

{FHIR_RESOURCES}
""".replace(
    "{FHIR_RESOURCES}",
    "/n* ".join([f"{k}" for k, v in FHIR_RESOURCES_NAMES.items()]),
)

__all__ = [
    "PROMPT_TEMPLATE",
    "PROMPT_TEMPLATE_POSSIBLE_RESOURCES",
]
