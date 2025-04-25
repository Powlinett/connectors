"""Define the OpenCTI Relationships."""

from typing import Literal

from connectors_sdk.octi_entities.common import Observable
from connectors_sdk.octi_entities.observations.indicator import Indicator
from connectors_sdk.octi_entities.relationships.common import Relationship
from pydantic import Field


class IndicatorBasedOnObservable(Relationship):
    """Represent a relationship indicating that an indicator is based on an observable."""

    _relationship_type: Literal["based-on"] = "based-on"

    source: Indicator = Field(
        description="Reference to the source entity of the relationship. Here an Indicator.",
    )
    target: Observable = Field(
        description="Reference to the target entity of the relationship. Here an Observable.",
    )
