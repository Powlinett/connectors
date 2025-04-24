"""Define OpenCTI entities."""

from collections import OrderedDict
from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from octi_entities.common import BaseEntity, DomainObject, UploadedFile
from octi_entities.enum import Reliability, ReportType
from pydantic import AwareDatetime, Field
from stix2.properties import (  # type: ignore[import-untyped]
    ListProperty,
    ReferenceProperty,
)


class OCTIStixReport(stix2.v21.Report):  # type: ignore[misc]
    # considered as Any because stix2 does not provide stubs
    """Override stix2 Report to not require any object_refs and so be compliant with OpenCTI Report entities."""

    _properties = OrderedDict(
        stix2.v21.Report._properties
    )  # Copy the parent class properties
    _properties["object_refs"] = ListProperty(
        ReferenceProperty(valid_types=["SCO", "SDO", "SRO"], spec_version="2.1"),
        required=False,
    )


class Report(DomainObject):
    """Represent a report."""

    name: str = Field(
        description="Name of the report.",
        min_length=1,
    )
    publication_date: AwareDatetime = Field(
        description="Publication date of the report.",
    )
    objects: list[BaseEntity] = Field(
        description="Objects of the report.",
    )
    description: Optional[str] = Field(
        description="Description of the report.",
        default=None,
    )
    report_types: Optional[list[ReportType]] = Field(
        description="Report types.",
        default=None,
    )
    reliability: Optional[Reliability] = Field(
        description="Reliability of the report.",
        default=None,
    )
    files: Optional[list[UploadedFile]] = Field(
        description="Files to upload with the report, e.g. report as a PDF.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.Report:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return OCTIStixReport(
            id=pycti.Report.generate_id(
                name=self.name, published=self.publication_date
            ),
            name=self.name,
            description=self.description,
            object_refs=[obj.id for obj in self.objects],
            report_types=self.report_types,
            published=self.publication_date,
            created_by_ref=self.author.id if self.author else None,
            external_references=[
                external_reference.to_stix2_object()
                for external_reference in self.external_references or []
            ],
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=dict(  # noqa: C408  # No literal dict for maintainability
                x_opencti_reliability=self.reliability,
                x_opencti_files=[file.to_stix2_object() for file in self.files or []],
                # unused
                x_opencti_workflow_id=None,  # set by OpenCTI only, workflow ids are customizable
            ),
            # unused
            created=None,
            modified=None,
            revoked=None,
            confidence=None,
            labels=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )
