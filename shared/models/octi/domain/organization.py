"""Define OpenCTI entities."""

from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from models.octi.common import Author, DomainObject
from models.octi.typings import OrganizationType, Reliability
from pydantic import Field


class Organization(DomainObject):
    """Represent an organization."""

    name: str = Field(
        ...,
        description="Name of the organization.",
        min_length=1,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the organization.",
    )
    contact_information: Optional[str] = Field(
        None,
        description="Contact information for the organization.",
    )
    organization_type: Optional[OrganizationType] = Field(
        None,
        description="OpenCTI Type of the organization.",
    )
    reliability: Optional[Reliability] = Field(
        None,
        description="OpenCTI Reliability of the organization.",
    )
    aliases: Optional[list[str]] = Field(
        None,
        description="Aliases of the organization.",
    )

    def to_stix2_object(self) -> stix2.v21.Identity:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        identity_class = "organization"
        return stix2.Identity(
            id=pycti.Identity.generate_id(
                identity_class=identity_class, name=self.name
            ),
            identity_class=identity_class,
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
