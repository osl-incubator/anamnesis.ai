"""Tests for anamnesisai package utility module."""

from typing import Type

import pytest

from anamnesisai.utils import get_resource_detail
from fhir.resources.resource import Resource


# ruff: noqa: D205
class MockResource(Resource):  # type: ignore[misc]
    """Disclaimer: Any field name ends with ``__ext`` doesn't part of
    Resource StructureDefinition, instead used to enable Extensibility feature
    for FHIR Primitive Data Types.

    This is a simulated DomainResource used to test resource
    handling functionality. It mimics the structure of a real
    FHIR resource but contains no actual implementation.
    """


@pytest.fixture
def resource() -> Type[Resource]:
    """Mock Resource fixture."""
    return MockResource


def test_get_resource_detail(resource: Type[Resource]) -> None:
    """Test get_resource_detail function."""
    expected = (
        "This is a simulated DomainResource used to test "
        "resource handling functionality. It mimics the "
        "structure of a real FHIR resource but contains no "
        "actual implementation."
    )
    assert get_resource_detail(resource) == expected
