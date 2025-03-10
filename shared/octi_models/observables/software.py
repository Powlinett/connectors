"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from ..common import Observable
from pydantic import Field


class Software(Observable):
    """Represents a software observable."""

    name: str = Field(
        ...,
        description="Name of the software.",
        min_length=1,
    )
    version: Optional[str] = Field(
        None,
        description="Version of the software.",
    )
    vendor: Optional[str] = Field(
        None,
        description="Vendor of the software.",
    )
    swid: Optional[str] = Field(
        None,
        description="SWID of the software.",
    )
    cpe: Optional[str] = Field(
        None,
        description="CPE of the software.",
    )
    languages: Optional[list[str]] = Field(
        None,
        description="Languages of the software.",
    )

    def to_stix2_object(self) -> stix2.v21.Software:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Software(
            name=self.name,
            version=self.version,
            vendor=self.vendor,
            swid=self.swid,
            cpe=self.cpe,
            languages=self.languages,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
