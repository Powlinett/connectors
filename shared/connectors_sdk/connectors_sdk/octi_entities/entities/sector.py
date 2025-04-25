from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import DomainObject
from connectors_sdk.octi_entities.enum import IdentityClass, IndustrySector, Reliability
from pydantic import Field, PrivateAttr


class Sector(DomainObject):
    """Represents a sector entity."""

    # OpenCTI maps STIX Identity SDO to OCTI Sector entity based on `identity_class`.
    # To create a Sector entity on OpenCTI, `identity_class` MUST be 'class'.
    _identity_class = PrivateAttr(IdentityClass.CLASS.value)

    name: str = Field(
        description="Name of the sector.",
        min_length=1,
    )
    description: Optional[str] = Field(
        description="Description of the sector.",
        default=None,
    )
    sectors: Optional[list[IndustrySector]] = Field(
        description="The list of industry sectors that this Identity belongs to.",
        default=None,
    )
    reliability: Optional[Reliability] = Field(
        description="OpenCTI Reliability of the sector.",
        default=None,
    )
    aliases: Optional[list[str]] = Field(
        description="Aliases of the sector.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.Identity:
        """Make stix object."""
        return stix2.Identity(
            id=pycti.Identity.generate_id(
                identity_class=self._identity_class, name=self.name
            ),
            identity_class=self._identity_class,
            name=self.name,
            description=self.description,
            sectors=self.sectors,
            external_references=[
                external_reference.to_stix2_object()
                for external_reference in self.external_references or []
            ],
            object_marking_refs=[marking.id for marking in self.markings or []],
            created_by_ref=self.author.id if self.author else None,
            custom_properties=dict(  # noqa: C408  # No literal dict for maintainability
                x_opencti_reliability=self.reliability,
                x_opencti_aliases=self.aliases,
            ),
            # unused
            created=None,
            modified=None,
            roles=None,
            contact_information=None,
            revoked=None,
            labels=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )
