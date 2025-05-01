"""Anamnesis AI core functions."""

from __future__ import annotations

import logging

from copy import copy
from typing import Any, Literal, Type, cast

from fhir.resources.resource import Resource
from rago.generation.base import GenerationBase
from typeguard import typechecked

from anamnesisai.config import (
    PROMPT_TEMPLATE,
    PROMPT_TEMPLATE_POSSIBLE_RESOURCES,
)
from anamnesisai.supported_fhir import (
    RESOURCES_CLASSES,
    FHIRResourceFoundModel,
    InvalidFHIRResource,
)
from anamnesisai.utils import get_resource_detail

# this should be move to another module
# maybe it would be good to get the logging level from an environment variable
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
)

DEFAULT_GEN_PARAMS = {
    "openai": {
        "model_name": "o4-mini",
        "output_max_length": 10384,  # note: calc this number
    },
    "ollama": {
        "model_name": "llama3.2:1b",
        "output_max_length": 10384,
    },
}


def get_generation_class(
    backend: Literal["openai", "ollama"],
) -> Type[GenerationBase]:
    """Get the generation class."""
    if backend == "openai":
        from anamnesisai.generation import OpenAI4MiniGen

        return OpenAI4MiniGen

    if backend == "ollama":
        from rago.generation import OllamaOpenAIGen

        return OllamaOpenAIGen


@typechecked
class AnamnesisAI:
    """Anamnesis AI class."""

    gen_class: Type[GenerationBase]
    api_key: str
    api_params: dict[str, Any]

    def __init__(
        self,
        backend: Literal["openai", "ollama"] = "ollama",
        api_key: str = "",
        api_params: dict[str, Any] = {},
    ) -> None:
        self.gen_class = get_generation_class(backend)

        params = copy(DEFAULT_GEN_PARAMS).get(backend, {})
        params.update(api_params)
        params["api_key"] = api_key

        self.api_params = params

    def _check_possible_fhir_resources(
        self,
        text: str,
    ) -> FHIRResourceFoundModel:
        """Check possible FHIR resources from the given text."""
        gen = self.gen_class(
            prompt_template=PROMPT_TEMPLATE_POSSIBLE_RESOURCES,
            structured_output=FHIRResourceFoundModel,
            **self.api_params,
        )
        # the query is already present in the prompt template
        result = gen.generate(query="", context=[text])
        return cast(FHIRResourceFoundModel, result)

    @typechecked
    def extract_fhir(
        self, text: str
    ) -> tuple[list[Resource], list[InvalidFHIRResource]]:
        """Extract FHIR from the given text."""
        possible_fhir = self._check_possible_fhir_resources(text)

        results: tuple[list[Resource], list[InvalidFHIRResource]] = ([], [])
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
            gen = self.gen_class(
                prompt_template=prompt_template,
                structured_output=fhir_class,
                **self.api_params,
            )

            # the query is already present in the prompt template
            result = gen.generate(query="", context=[text])
            fhir_obj = cast(Resource, result)

            if isinstance(fhir_obj, InvalidFHIRResource):
                results[1].append(fhir_obj)
            else:
                results[0].append(fhir_obj)

        return results
