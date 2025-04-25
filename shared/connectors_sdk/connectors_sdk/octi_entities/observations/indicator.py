"""Define OpenCTI entities."""

from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import DomainObject, KillChainPhase
from connectors_sdk.octi_entities.enum import (
    IndicatorType,
    ObservableType,
    PatternType,
    Platform,
)
from pydantic import AwareDatetime, Field


class Indicator(DomainObject):
    """Represent an Indicator."""

    name: str = Field(
        description="Name of the indicator.",
        min_length=1,
    )
    pattern: str = Field(
        description="Pattern. See Stix2.1 for instance : https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html#_me3pzm77qfnf",
    )
    pattern_type: PatternType = Field(
        description="Pattern type.",
    )
    observable_type: ObservableType = Field(
        description="Observable type.",
    )
    description: Optional[str] = Field(
        description="Description of the indicator.",
        default=None,
    )
    indicator_types: Optional[list[IndicatorType]] = Field(
        description="Indicator types.",
        default=None,
    )
    platforms: Optional[list[Platform]] = Field(
        description="Platforms.",
        default=None,
    )
    valid_from: Optional[AwareDatetime] = Field(
        description="Valid from.",
        default=None,
    )
    valid_until: Optional[AwareDatetime] = Field(
        description="Valid until.",
        default=None,
    )
    kill_chain_phases: Optional[list[KillChainPhase]] = Field(
        description="Kill chain phases.",
        default=None,
    )
    score: Optional[int] = Field(
        description="Score of the indicator.",
        default=None,
        ge=0,
        le=100,
    )

    def to_stix2_object(self) -> stix2.v21.Indicator:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Indicator(
            id=pycti.Indicator.generate_id(pattern=self.pattern),
            name=self.name,
            description=self.description,
            indicator_types=self.indicator_types,
            pattern_type=self.pattern_type,
            pattern=self.pattern,
            valid_from=self.valid_from,
            valid_until=self.valid_until,
            kill_chain_phases=[
                kill_chain_phase.to_stix2_object()
                for kill_chain_phase in self.kill_chain_phases or []
            ],
            external_references=[
                external_reference.to_stix2_object()
                for external_reference in self.external_references or []
            ],
            created_by_ref=self.author.id if self.author else None,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=dict(  # noqa: C408 # No literal dict for maintainability
                x_opencti_score=self.score,
                x_mitre_platforms=self.platforms,
                x_opencti_main_observable_type=self.observable_type,
                # unused
                x_opencti_detection=None,
            ),
            # unused
            created=None,
            modified=None,
            revoked=None,
            labels=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )
