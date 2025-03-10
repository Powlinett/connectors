"""Define the OpenCTI Observable."""

import stix2
from ..common import Observable
from pydantic import Field


class Url(Observable):
    """Represent a URL observable."""

    value: str = Field(
        ...,
        description="The URL value.",
        min_length=1,
    )

    def to_stix2_object(self) -> stix2.v21.URL:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.URL(
            value=self.value,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
