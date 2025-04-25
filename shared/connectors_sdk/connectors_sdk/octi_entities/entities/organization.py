"""Define OpenCTI entities."""

from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Author, DomainObject
from connectors_sdk.octi_entities.enum import (
    IdentityClass,
    OrganizationType,
    Reliability,
)
from pydantic import Field, PrivateAttr


class Organization(DomainObject):
    """Represent an organization."""

    # OpenCTI maps STIX Identity SDO to OCTI Organization entity based on `identity_class`.
    # To create an Organization entity on OpenCTI, `identity_class` MUST be 'organization'.
    _identity_class = PrivateAttr(IdentityClass.ORGANIZATION.value)

    name: str = Field(
        description="Name of the organization.",
        min_length=1,
    )
    description: Optional[str] = Field(
        description="Description of the organization.",
        default=None,
    )
    contact_information: Optional[str] = Field(
        description="Contact information for the organization.",
        default=None,
    )
    organization_type: Optional[OrganizationType] = Field(
        description="OpenCTI Type of the organization.",
        default=None,
    )
    reliability: Optional[Reliability] = Field(
        description="OpenCTI Reliability of the organization.",
        default=None,
    )
    aliases: Optional[list[str]] = Field(
        description="Aliases of the organization.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.v21.Identity:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Identity(
            id=pycti.Identity.generate_id(
                identity_class=self._identity_class, name=self.name
            ),
            identity_class=self._identity_class,
            name=self.name,
            description=self.description,
            contact_information=self.contact_information,
            external_references=[
                external_reference.to_stix2_object()
                for external_reference in self.external_references or []
            ],
            object_marking_refs=[marking.id for marking in self.markings or []],
            created_by_ref=self.author.id if self.author else None,
            custom_properties=dict(  # noqa: C408  # No literal dict for maintainability
                x_opencti_organization_type=self.organization_type,
                x_opencti_reliability=self.reliability,
                x_opencti_aliases=self.aliases,
            ),
            # unused
            created=None,
            modified=None,
            roles=None,
            sectors=None,
            revoked=None,
            labels=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )


class OrganizationAuthor(Author, Organization):
    """Represent an organization author."""

    def to_stix2_object(self) -> stix2.v21.Identity:
        """Make stix object."""
        return Organization.to_stix2_object(self)
