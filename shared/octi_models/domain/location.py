"""Define OpenCTI entities."""

from typing import Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
from ..common import DomainObject
from ..enum import LocationType as LocationTypeEnum
from ..typings import LocationType, Region
from pydantic import Field, PrivateAttr


class _Location(DomainObject):
    """Represents a location entity."""

    _location_type: LocationType = PrivateAttr(...)

    name: Optional[str] = Field(
        None,
        description="A name used to identify the Location.",
    )
    description: Optional[str] = Field(
        None,
        description="A textual description of the Location.",
    )
    latitude: Optional[float] = Field(
        None,
        description="The latitude of the Location in decimal degrees.",
    )
    longitude: Optional[float] = Field(
        None,
        description="The longitude of the Location in decimal degrees.",
    )
    precision: Optional[float] = Field(
        None,
        description="Defines the precision of the coordinates specified by the latitude and longitude properties.",
    )
    region: Optional[Region] = Field(
        None,
        description="The region that this Location describes.",
    )
    country: Optional[str] = Field(
        None,
        description="The country that this Location describes.",
    )
    administrative_area: Optional[str] = Field(
        None,
        description="The state, province, or other sub-national administrative area that this Location describes.",
    )
    city: Optional[str] = Field(
        None,
        description="The city that this Location describes.",
    )
    street_address: Optional[str] = Field(
        None,
        description="The street address that this Location describes.",
    )
    postal_code: Optional[str] = Field(
        None,
        description="The postal code for this Location.",
    )

    def to_stix2_object(self) -> stix2.Location:
        return stix2.Location(
            id=pycti.Location.generate_id(
                name=self.name,
                x_opencti_location_type=self._location_type,
                latitude=self.latitude,
                longitude=self.longitude,
            ),
            name=self.name,
            description=self.description,
            latitude=self.latitude,
            longitude=self.longitude,
            precision=self.precision,
            region=self.region,
            country=self.country,
            administrative_area=self.administrative_area,
            city=self.city,
            street_address=self.street_address,
            postal_code=self.postal_code,
            custom_properties=dict(
                x_opencti_location_type=self._location_type,
            ),
            created=None,
            modified=None,
            revoked=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )


class LocationAdministrativeArea(_Location):
    """Represent an administrative area entity."""

    _location_type = LocationTypeEnum.ADMINISTRATIVE_AREA.value


class LocationCity(_Location):
    """Represent a city entity."""

    _location_type = LocationTypeEnum.CITY.value


class LocationCountry(_Location):
    """Represent a country entity."""

    _location_type = LocationTypeEnum.COUNTRY.value


class LocationPosition(_Location):
    """Represent a position entity."""

    _location_type = LocationTypeEnum.POSITION.value


class LocationRegion(_Location):
    """Represent a region entity."""

    _location_type = LocationTypeEnum.REGION.value
