"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from ..common import Observable
from pydantic import Field


class EmailAddress(Observable):
    """Represent an Email Address observable on OpenCTI."""

    value: str = Field(
        ...,
        description="The Email address value.",
        min_length=1,
    )
    display_name: Optional[str] = Field(
        None,
        description="Display name.",
    )

    def to_stix2_object(self) -> stix2.v21.EmailAddress:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.EmailAddress(
            value=self.value,
            display_name=self.display_name,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            belongs_to_ref=None,  # belongs to user-account not implemented on OpenCTI
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
