"""Tests for anamnesisai package."""

import pytest


@pytest.fixture
def response_pytest() -> bool:
    """Sample pytest fixture."""
    return True


def test_content_pytest() -> None:
    """Test with pytest."""
    assert True
