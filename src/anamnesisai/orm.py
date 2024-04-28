from __future__ import annotations

import importlib
import pkgutil

from typing import Any, Type

import fhir
import fhir.resources

from fhir.resources.core.fhirabstractmodel import FHIRAbstractModel
from fhir.resources.fhirprimitiveextension import FHIRPrimitiveExtension
from pydantic import BaseModel
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlmodel import Field, SQLModel


# Assuming an existing Pydantic model
class ExistingPydanticModel(BaseModel):
    id: int
    name: str
    age: int


# SQLAlchemy setup
engine = create_engine("sqlite:///mydatabase.db")
metadata = MetaData()
# Assume the table is already defined in the database


class DatabaseOperations:
    def __init__(self, model: BaseModel, table: Table):
        self.model = model
        self.table = table

    def save(self):
        stmt = insert(self.table).values(self.model.dict(exclude_unset=True))
        with engine.connect() as conn:
            conn.execute(stmt)


# Usage
existing_model_instance = ExistingPydanticModel(id=1, name="John Doe", age=30)
users_table = Table(
    "users", metadata, autoload_with=engine
)  # Link to your table
db_operations = DatabaseOperations(existing_model_instance, users_table)
db_operations.save()


def create_sqlmodel_from_fhir(
    fhir_class: Type[FHIRAbstractModel],
) -> Type[SQLModel]:
    """
    Dynamically create an SQLModel class from a FHIR resource class.

    Args:
        fhir_class: The FHIR resource class to convert.

    Returns
    -------
        A dynamically created SQLModel class.
    """
    class_name = fhir_class.__name__ + "Model"
    attributes: dict[str, Any] = {"__tablename__": fhir_class.__name__.lower()}

    # Process each field in the FHIR class
    for field_name, field_meta in fhir_class.__fields__.items():
        # Skip extensions for simplicity
        if issubclass(field_meta.type_, FHIRPrimitiveExtension):
            continue

        # Basic type mapping; this should be expanded based on your needs
        field_type = Any  # Default to Any, customize this mapping as needed

        # Map field to SQLModel Field, with more specific types as required
        attributes[field_name] = Field(
            default=None,
            sa_column_kwargs={"nullable": True},
            title=field_name,
            # description=field_meta.description,
            sql_type=field_type,
        )

        #  attributes[field_name] = (Any, Field(default=None, title=field_name, description=field_meta.description))

    # Create the SQLModel class
    return type(class_name, (SQLModel,), attributes)


def convert_all_fhir_resources() -> list[str]:
    """
    Iterate over modules in the fhir.resources package and convert all
    FHIR resource classes into SQLModel entities.
    """
    fhir_resources_package = "fhir.resources"
    converted_models: dict[str, Type[SQLModel]] = {}

    # Iterate over all modules in the fhir.resources package
    for importer, module_name, _ in pkgutil.iter_modules(
        fhir.resources.__path__, fhir_resources_package + "."
    ):
        module = importlib.import_module(module_name)

        # Iterate over all attributes in the module
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            # Check if the attribute is a class and a subclass of
            # FHIRAbstractModel
            if (
                isinstance(attribute, type)
                and issubclass(attribute, FHIRAbstractModel)
                and attribute is not FHIRAbstractModel
            ):
                # Convert the FHIR class into an SQLModel entity
                converted_model = create_sqlmodel_from_fhir(attribute)
                converted_models[attribute.__name__] = converted_model

    globals().update(**converted_models)
    return list(converted_models.keys())


__all__ = convert_all_fhir_resources()
