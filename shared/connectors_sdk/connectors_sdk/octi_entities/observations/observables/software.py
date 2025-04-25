"""Define the OpenCTI Observable."""

from typing import Optional

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from pydantic import Field


class Software(Observable):
    """Represents a software observable."""

    name: str = Field(
        description="Name of the software.",
        min_length=1,
    )
    version: Optional[str] = Field(
        description="Version of the software.",
        default=None,
    )
    vendor: Optional[str] = Field(
        description="Vendor of the software.",
        default=None,
    )
    swid: Optional[str] = Field(
        description="SWID of the software.",
        default=None,
    )
    cpe: Optional[str] = Field(
        description="CPE of the software.",
        default=None,
    )
    languages: Optional[list[str]] = Field(
        description="Languages of the software.",
        default=None,
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
