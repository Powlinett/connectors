"""Define OpenCTI entities."""

from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import DomainObject
from connectors_sdk.octi_entities.enum import AttackMotivation, AttackResourceLevel
from pydantic import AwareDatetime, Field


class IntrusionSet(DomainObject):
    """Represent an intrusion set."""

    name: str = Field(
        description="A name used to identify this Intrusion Set.",
        min_length=1,
    )
    description: Optional[str] = Field(
        description="A description that provides more details and context about the Intrusion Set.",
        default=None,
    )
    aliases: Optional[list[str]] = Field(
        description="Alternative names used to identify this Intrusion Set.",
        default=None,
    )
    first_seen: Optional[AwareDatetime] = Field(
        description="The time that this Intrusion Set was first seen.",
        default=None,
    )
    last_seen: Optional[AwareDatetime] = Field(
        description="The time that this Intrusion Set was last seen.",
        default=None,
    )
    goals: Optional[list[str]] = Field(
        description="The high-level goals of this Intrusion Set, namely, what are they trying to do.",
        default=None,
    )
    resource_level: Optional[AttackResourceLevel] = Field(
        description="The organizational level at which this Intrusion Set typically works.",
        default=None,
    )
    primary_motivation: Optional[AttackMotivation] = Field(
        description="The primary reason, motivation, or purpose behind this Intrusion Set.",
        default=None,
    )
    secondary_motivations: Optional[list[AttackMotivation]] = Field(
        description="The secondary reasons, motivations, or purposes behind this Intrusion Set.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.v21.IntrusionSet:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.IntrusionSet(
            id=pycti.IntrusionSet.generate_id(name=self.name),
            name=self.name,
            description=self.description,
            aliases=self.aliases,
            first_seen=self.first_seen,
            last_seen=self.last_seen,
            goals=self.goals,
            resource_level=self.resource_level,
            primary_motivation=self.primary_motivation,
            secondary_motivations=self.secondary_motivations,
            created_by_ref=self.author.id if self.author else None,
            external_references=[
                external_reference.to_stix2_object()
                for external_reference in self.external_references or []
            ],
            object_marking_refs=[marking.id for marking in self.markings or []],
            # unused
            created=None,
            modified=None,
            labels=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )
