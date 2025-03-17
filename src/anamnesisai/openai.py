"""Anamnesis AI core functions."""

from __future__ import annotations

import logging

from typing import cast

from fhir.resources.resource import Resource
from rago.generation import OpenAIGen
from typeguard import typechecked

from anamnesisai.config import (
    PROMPT_TEMPLATE,
    PROMPT_TEMPLATE_POSSIBLE_RESOURCES,
)
from anamnesisai.supported_fhir import (
    RESOURCES_CLASSES,
    FHIRResourceFoundModel,
)
from anamnesisai.utils import get_resource_detail

# this should be move to another module
# maybe it would be good to get the logging level from an environment variable
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)


@typechecked
def check_possible_fhir_resources(
    text: str, api_key: str
) -> FHIRResourceFoundModel:
    """Check possible FHIR resources from the given text."""
    try:
        gen = OpenAIGen(
            prompt_template=PROMPT_TEMPLATE_POSSIBLE_RESOURCES,
            model_name="gpt-4o-mini",
            api_key=api_key,
            output_max_length=10384,  # note: calc this number
            structured_output=FHIRResourceFoundModel,
        )
        # the query is already present in the prompt template
        result = gen.generate(query="", context=[text])
    except Exception as e:
        logging.debug(str(e))
        return FHIRResourceFoundModel(
            **{cls.__name__: False for cls in RESOURCES_CLASSES}
        )

    return cast(FHIRResourceFoundModel, result)


@typechecked
def extract_fhir(text: str, api_key: str) -> dict[str, Resource]:
    """Extract FHIR from the given text."""
    possible_fhir = check_possible_fhir_resources(text, api_key)

    results: dict[str, Resource] = {}
    for fhir_class in RESOURCES_CLASSES:
        resource_name = fhir_class.__name__

        if not getattr(possible_fhir, resource_name, False):
            logging.debug(
                f"{resource_name} resource not found in the conversation."
            )
            continue

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
            # the query is already present in the prompt template
            result = gen.generate(query="", context=[text])
        except Exception as e:
            logging.warning(str(e))
            continue

        fhir_obj = cast(Resource, result)
        results[resource_name] = fhir_obj
    return results
