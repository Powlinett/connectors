from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.enum import LocationType
from connectors_sdk.octi_entities.locations.common import Location, OCTIStixLocation
from pydantic import Field, PrivateAttr


class Position(Location):
    """Represent a position entity."""

    _location_type: LocationType = PrivateAttr(LocationType.POSITION)

    latitude: Optional[float] = Field(
        description="The latitude of the Location in decimal degrees.",
        default=None,
    )
    longitude: Optional[float] = Field(
        description="The longitude of the Location in decimal degrees.",
        default=None,
    )
    street_address: Optional[str] = Field(
        description="The street address that this Location describes.",
        default=None,
    )
    postal_code: Optional[str] = Field(
        description="The postal code for this Location.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.Location:
        """Make stix object."""
        return OCTIStixLocation(
            id=pycti.Location.generate_id(
                name=self.name,
                x_opencti_location_type=self._location_type.value,
                latitude=self.latitude,
                longitude=self.longitude,
            ),
            name=self.name,
            description=self.description,
            latitude=self.latitude,
            longitude=self.longitude,
            street_address=self.street_address,
            postal_code=self.postal_code,
            custom_properties=dict(  # noqa: C408  # No literal dict for maintainability
                x_opencti_location_type=self._location_type.value,
            ),
            region=None,
            country=None,
            city=None,
            administrative_area=None,
            precision=None,
            created=None,
            modified=None,
            revoked=None,
            labels=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )
