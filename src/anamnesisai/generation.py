"""Anamnesis AI custom generation model classes."""

from __future__ import annotations

import logging

from typing import cast

from instructor.exceptions import InstructorRetryException
from pydantic import BaseModel
from rago.generation import OpenAIGen
from typeguard import typechecked

from anamnesisai.supported_fhir import InvalidFHIRResource


@typechecked
class OpenAI4MiniGen(OpenAIGen):
    """OpenAI generation model for text generation."""

    default_model_name = "o4-mini"

    def generate(
        self,
        query: str,
        context: list[str],
    ) -> str | BaseModel | InvalidFHIRResource:
        """Generate text using OpenAI's API with dynamic model support."""
        input_text = self.prompt_template.format(
            query=query, context=" ".join(context)
        )

        if not self.model:
            raise Exception("The model was not created.")

        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        messages.append({"role": "user", "content": input_text})

        model_params = dict(
            model=self.model_name,
            messages=messages,
            max_completion_tokens=self.output_max_length,
            **self.api_params,
        )

        if self.structured_output:
            model_params["response_model"] = self.structured_output

        self.logs["model_params"] = model_params

        resource_name = (
            self.structured_output.__name__
            if self.structured_output
            else "UnknownModel"
        )

        try:
            response = self.model.chat.completions.create(**model_params)
            fhir_resource: str | BaseModel

            has_choices = hasattr(response, "choices")
            if has_choices and isinstance(response.choices, list):
                fhir_resource = cast(
                    str, response.choices[0].message.content.strip()
                )
            else:
                fhir_resource = cast(BaseModel, response)

            logging.debug(f"[SUCCESS] Parsed {resource_name} resource.")
            return fhir_resource
        except InstructorRetryException as e:
            raw_response = (
                e.last_completion.choices[0]
                .message.tool_calls[0]
                .function.arguments
                if e.last_completion and e.last_completion.choices
                else "Unavailable"
            )
            fhir_resource = InvalidFHIRResource(
                resource_type=resource_name,
                error_message=str(e),
                raw_response=raw_response,
            )
            logging.debug(
                f"[ERROR] Failed to parse {resource_name} "
                "resource. InvalidFHIRResource created."
            )
            return fhir_resource
