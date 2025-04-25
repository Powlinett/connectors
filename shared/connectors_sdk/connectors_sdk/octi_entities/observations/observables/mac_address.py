"""Define the OpenCTI Observable."""

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from pydantic import Field


class MACAddress(Observable):
    """Represent a MAC address observable on OpenCTI."""

    value: str = Field(
        description="Specifies the value of a single MAC address.",
        min_length=1,
    )

    def to_stix2_object(self) -> stix2.MACAddress:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.MACAddress(
            value=self.value,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
