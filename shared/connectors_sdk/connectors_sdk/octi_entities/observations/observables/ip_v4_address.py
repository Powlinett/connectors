"""Define the OpenCTI Observable."""

import ipaddress
from typing import Optional

import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from connectors_sdk.octi_entities.enum import ObservableType, PatternType
from connectors_sdk.octi_entities.observations.indicator import Indicator
from pydantic import AwareDatetime, Field, field_validator


class IPV4Address(Observable):
    """Represent an IP address observable on OpenCTI."""

    value: str = Field(
        description="The IP address value.",
        min_length=1,
    )

    @field_validator("value", mode="before")
    @classmethod
    def _validate_value(cls, value: str) -> str:
        """Validate the value of the IP V4 address."""
        try:
            ipaddress.IPv4Address(value)
        except ValueError:
            raise ValueError(f"Invalid IP V4 address {value}") from None
        return value

    def to_stix2_object(self) -> stix2.v21.IPv4Address:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.IPv4Address(
            value=self.value,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            resolves_to_refs=None,  # not implemented on OpenCTI, this has to be an explicit resolves to mac address relationships
            belongs_to_refs=None,  # not implemented on OpenCTI, this has to be an explicit belongs to autonomous system relationship
            granular_markings=None,
            defanged=None,
            extensions=None,
        )

    def to_indicator(
        self,
        valid_from: Optional[AwareDatetime] = None,
        valid_until: Optional[AwareDatetime] = None,
    ) -> Indicator:
        """Make stix indicator based on current observable.

        - Indicator's name is the value of the IP address.
        - Indicator's pattern is the value of the IP address.
        """
        return Indicator(
            name=self.value,
            pattern=f"[ipv4-addr:value='{self.value}']",
            pattern_type=PatternType.STIX.value,
            observable_type=ObservableType.IPV4_ADDR.value,
            description=self.description,
            valid_from=valid_from,
            valid_until=valid_until,
            score=self.score,
            author=self.author,
            markings=self.markings,
            external_references=self.external_references,
        )
