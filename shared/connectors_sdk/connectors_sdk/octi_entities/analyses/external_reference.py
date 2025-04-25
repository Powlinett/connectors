from typing import Optional

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import BaseModelWithoutExtra
from pydantic import Field


class ExternalReference(BaseModelWithoutExtra):
    """Represents an external reference to a source of information."""

    source_name: str = Field(
        description="The name of the source of the external reference.",
    )
    description: Optional[str] = Field(
        description="Description of the external reference.",
        default=None,
    )
    url: Optional[str] = Field(
        description="URL of the external reference.",
        default=None,
    )
    external_id: Optional[str] = Field(
        description="An identifier for the external reference content.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.v21.ExternalReference:
        """Make stix object."""
        return stix2.ExternalReference(
            source_name=self.source_name,
            description=self.description,
            url=self.url,
            external_id=self.external_id,
            # unused
            hashes=None,
        )
