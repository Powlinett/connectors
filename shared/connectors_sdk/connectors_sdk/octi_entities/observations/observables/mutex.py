"""Define the OpenCTI Observable."""

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from pydantic import Field


class Mutex(Observable):
    """Represent a mutex observable on OpenCTI."""

    name: str = Field(
        description="The name of the mutex object.",
        min_length=1,
    )

    def to_stix2_object(self) -> stix2.v21.Mutex:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Mutex(
            name=self.name,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
