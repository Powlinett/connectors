"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from models.octi.common import Observable
from pydantic import Field


class AutonomousSystem(Observable):
    """Represent an autnomous system (AS) observable on OpenCTI."""

    number: int = Field(
        ...,
        description="The number assigned to the AS.",
    )
    name: Optional[str] = Field(
        None,
        description="The name of the AS.",
    )
    rir: Optional[str] = Field(
        None,
        description="The name of the Regional Internet Registry (RIR) that assigned the number to the AS.",
    )

    def to_stix2_object(self) -> stix2.v21.AutonomousSystem:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.AutonomousSystem(
            number=self.number,
            name=self.name,
            rir=self.rir,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
