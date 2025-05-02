"""Gather all FHIR resources that is supported by Anamnesis.ai."""

from __future__ import annotations

from fhir.resources.allergyintolerance import AllergyIntolerance
from fhir.resources.careplan import CarePlan
from fhir.resources.condition import Condition
from fhir.resources.diagnosticreport import DiagnosticReport
from fhir.resources.encounter import Encounter
from fhir.resources.familymemberhistory import FamilyMemberHistory
from fhir.resources.immunization import Immunization
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.medicationstatement import MedicationStatement
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient
from fhir.resources.practitioner import Practitioner
from fhir.resources.procedure import Procedure
from fhir.resources.servicerequest import ServiceRequest
from pydantic import BaseModel, create_model

RESOURCES_CLASSES = (
    Patient,
    Condition,
    Practitioner,
    Encounter,
    Observation,
    FamilyMemberHistory,
    AllergyIntolerance,
    Immunization,
    MedicationStatement,
    Procedure,
    DiagnosticReport,
    CarePlan,
    ServiceRequest,
    MedicationRequest,
)

fields = {cls.__name__: (bool, ...) for cls in RESOURCES_CLASSES}
FHIRResourceFoundModel = create_model(  # type: ignore[call-overload]
    "FHIRResourceFoundModel",
    **fields,
)


class InvalidFHIRResource(BaseModel):
    """Resource the Model failed to parse."""

    resource_type: str
    error_message: str
    raw_response: str


__all__ = [
    "RESOURCES_CLASSES",
    "FHIRResourceFoundModel",
    "InvalidFHIRResource",
]
