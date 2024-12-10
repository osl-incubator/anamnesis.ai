"""Set of generic functions that supports other modules."""

from __future__ import annotations

from typing import Type

from fhir.resources.resource import Resource
from typeguard import typechecked


@typechecked
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
