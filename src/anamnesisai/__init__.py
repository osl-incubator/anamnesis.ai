"""anamnesis.ai."""

from importlib import metadata as importlib_metadata

from anamnesisai.core import extract_fhir_openai


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.1.0"  # semantic-release


version = get_version()

__version__ = version
__author__ = "Satarupa Deb, Ivan Ogasawara"
__email__ = "satarupa2212@gmail.com, ivan.ogasawara@gmail.com"


__all__ = [
    "extract_fhir_openai",
]
