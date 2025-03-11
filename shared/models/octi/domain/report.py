"""Define OpenCTI entities."""

from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from models.octi.common import BaseEntity, DomainObject
from models.octi.typings import Reliability, ReportType
from pydantic import AwareDatetime, Field


class Report(DomainObject):
    """Represent a report."""

    name: str = Field(
        ...,
        description="Name of the report.",
        min_length=1,
    )
    publication_date: AwareDatetime = Field(
        ...,
        description="Publication date of the report.",
    )
    objects: list[BaseEntity] = Field(
        ...,
        description="Objects of the report.",
        min_length=1,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the report.",
    )
    report_types: Optional[list[ReportType]] = Field(
        None,
        description="Report types.",
    )
    reliability: Optional[Reliability] = Field(
        None,
        description="Reliability of the report.",
    )

    def to_stix2_object(self) -> stix2.v21.Report:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Report(
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
