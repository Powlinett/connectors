from abc import ABC
from typing import Optional

from octi_entities.common import DomainObject
from octi_entities.enum import LocationType
from pydantic import Field, PrivateAttr


class OCTIStixLocation(stix2.Location):  # type: ignore[misc]  # stix2 does not provide stubs
    """Override stix2 Location to skip some constraints incompatible with OpenCTI Location entities."""

    def _check_object_constraints(self) -> None:
        """Override _check_object_constraints method."""
        location_type = (self.x_opencti_location_type or "").lower()
        if location_type in ["administrative-area", "city", "position"]:
            if self.get("precision") is not None:
                self._check_properties_dependency(
                    ["longitude", "latitude"], ["precision"]
                )

            self._check_properties_dependency(["latitude"], ["longitude"])
            self._check_properties_dependency(["longitude"], ["latitude"])

            # Skip region/country/latitude/longitude presence check because all of them are optional on OpenCTI
            # even though at least one of them is required in the STIX2.1 spec
        else:
            super()._check_object_constraints()


class Location(DomainObject, ABC):
    """Represents a location entity."""

    _location_type: LocationType = PrivateAttr()

    name: str = Field(
        ...,
        description="A name used to identify the Location.",
    )
    description: Optional[str] = Field(
        None,
        description="A textual description of the Location.",
    )
