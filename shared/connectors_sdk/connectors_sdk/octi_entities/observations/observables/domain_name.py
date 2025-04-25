"""Define the OpenCTI Observable."""

from typing import Optional

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from connectors_sdk.octi_entities.enum import ObservableType, PatternType
from connectors_sdk.octi_entities.observations.indicator import Indicator
from pydantic import AwareDatetime, Field

# from connectors_sdk.octi_entities.observables import IPV4Address, IPv6Address


class DomainName(Observable):
    """Represent a domain name observable on OpenCTI."""

    value: str = Field(
        description="Specifies the value of the domain name.",
        min_length=1,
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

    def to_indicator(
        self,
        valid_from: Optional[AwareDatetime] = None,
        valid_until: Optional[AwareDatetime] = None,
    ) -> Indicator:
        """Make stix indicator based on current observable.

        - Indicator's name is the value of the domain name.
        - Indicator's pattern is the value of the domain name.
        """
        return Indicator(
            name=self.value,
            pattern=f"[domain-name:value='{self.value}']",
            pattern_type=PatternType.STIX.value,
            observable_type=ObservableType.DOMAIN_NAME.value,
            description=self.description,
            valid_from=valid_from,
            valid_until=valid_until,
            score=self.score,
            author=self.author,
            markings=self.markings,
            external_references=self.external_references,
        )
