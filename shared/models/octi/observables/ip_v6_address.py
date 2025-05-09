"""Define the OpenCTI Observable."""

import ipaddress

import stix2
from models.octi.common import Observable
from pydantic import Field, field_validator


class IPV6Address(Observable):
    """Represent an IP address observable on OpenCTI."""

    value: str = Field(
        ...,
        description="The IP address value.",
        min_length=1,
    )

    @field_validator("value", mode="before")
    @classmethod
    def _validate_value(cls, value: str) -> str:
        """Validate the value of the IP V6 address."""
        try:
            ipaddress.IPv6Address(value)
        except ValueError:
            raise ValueError(f"Invalid IP V6 address {value}") from None
        return value

    def to_stix2_object(self) -> stix2.v21.IPv6Address:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.IPv6Address(
            value=self.value,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            resolves_to_refs=None,  # not implemented on OpenCTI, his has to be an explicit resolves to mac address relationships
            belongs_to_refs=None,  # not implemented on OpenCTI, his has to be an explicit belongs to autonomous system relationship
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
