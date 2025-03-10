"""Define the OpenCTI Relationships."""

from typing import Literal

from ..common import Relationship, Observable
from ..domain.indicator import Indicator
from pydantic import Field


class IndicatorBasedOnObservable(Relationship):
    """Represent a relationship indicating that an indicator is based on an observable."""

    _relationship_type: Literal["based-on"] = "based-on"

    source: Indicator = Field(
        ...,
        description="Reference to the source entity of the relationship. Here an Indicator.",
    )
    target: Observable = Field(
        ...,
        description="Reference to the target entity of the relationship. Here an Observable.",
    )
