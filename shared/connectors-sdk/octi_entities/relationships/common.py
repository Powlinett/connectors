from typing import Any, Optional

import pycti
import stix2
from octi_entities.analyses.external_reference import ExternalReference
from octi_entities.common import Author, BaseEntity, TLPMarking
from pydantic import AwareDatetime, Field, PrivateAttr


class Relationship(BaseEntity):
    """Base class for OpenCTI relationships."""

    _relationship_type: str = PrivateAttr("")

    source: BaseEntity = Field(
        description="The source entity of the relationship.",
    )
    target: BaseEntity = Field(
        description="The target entity of the relationship.",
    )
    description: Optional[str] = Field(
        description="Description of the relationship.",
        default=None,
    )
    start_time: Optional[AwareDatetime] = Field(
        description="Start time of the relationship in ISO 8601 format.",
        default=None,
    )
    stop_time: Optional[AwareDatetime] = Field(
        description="End time of the relationship in ISO 8601 format.",
        default=None,
    )
    author: Optional[Author] = Field(
        description="Reference to the author that reported this relationship.",
        default=None,
    )
    markings: Optional[list[TLPMarking]] = Field(
        description="References for object marking",
        default=None,
    )
    external_references: Optional[list[ExternalReference]] = Field(
        description="External references",
        default=None,
    )

    def to_stix2_object(self) -> stix2.v21.Relationship:
        """Make stix object."""
        return stix2.Relationship(
            id=pycti.StixCoreRelationship.generate_id(
                relationship_type=self._relationship_type,
                source_ref=self.source.id,
                target_ref=self.target.id,
                start_time=self.start_time,
                stop_time=self.stop_time,
            ),
            relationship_type=self._relationship_type,
            **self._common_stix2_args(),
        )

    def _common_stix2_args(self) -> dict[str, Any]:
        """Factorize custom params."""
        return dict(  # noqa: C408 # No literal dict for maintainability
            source_ref=self.source.id,
            target_ref=self.target.id,
            description=self.description,
            start_time=self.start_time,
            stop_time=self.stop_time,
            created_by_ref=self.author.id if self.author else None,
            object_marking_refs=[marking.id for marking in self.markings or []],
            external_references=[
                ref.to_stix2_object() for ref in self.external_references or []
            ],
            # unused
            created=None,
            modified=None,
        )
