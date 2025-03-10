"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from ..common import Observable

# from dragos.domain.models.octi.observables import IPV4Address, IPv6Address
from pydantic import Field


class DomainName(Observable):
    """Represent a domain name observable on OpenCTI."""

    value: str = Field(
        ...,
        description="Specifies the value of the domain name.",
        min_length=1,
    )
    resolves_to_ref: Optional[list[Observable]] = Field(
        None,
        description="References to one or more IP addresses or domain names that the domain name resolves to.",
    )

    def to_stix2_object(self) -> stix2.DomainName:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.DomainName(
            value=self.value,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            resolves_to_refs=None,  # not implemented on OpenCTI
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
