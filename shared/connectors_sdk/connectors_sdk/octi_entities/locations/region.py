import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.enum import LocationType, Region
from connectors_sdk.octi_entities.locations.common import Location, OCTIStixLocation
from pydantic import Field, PrivateAttr


class Region(Location):
    """Represent a region entity."""

    _location_type: LocationType = PrivateAttr(LocationType.REGION)

    name: Region = Field(
        description="A name used to identify the Location.",
    )

    def to_stix2_object(self) -> stix2.Location:
        """Make stix object."""
        return OCTIStixLocation(
            id=pycti.Location.generate_id(
                name=self.name,
                x_opencti_location_type=self._location_type.value,
            ),
            name=self.name,
            region=self.name,
            description=self.description,
            custom_properties=dict(  # noqa: C408  # No literal dict for maintainability
                x_opencti_location_type=self._location_type.value,
            ),
            latitude=None,
            longitude=None,
            precision=None,
            country=None,
            administrative_area=None,
            city=None,
            street_address=None,
            postal_code=None,
            created=None,
            modified=None,
            revoked=None,
            labels=None,
            confidence=None,
            lang=None,
            granular_markings=None,
            extensions=None,
        )
