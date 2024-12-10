"""Set of functions and variables used for configuration."""

from __future__ import annotations

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

In the conversation, `D:` means it is from the Doctor, and `P:` means
it is from the Patience.

Question: what fhir resource/types could be extract from this conversation?
note: I don't need the data just the name of the types/resources
"""


__all__ = [
    "PROMPT_TEMPLATE",
    "PROMPT_TEMPLATE_POSSIBLE_RESOURCES",
]
