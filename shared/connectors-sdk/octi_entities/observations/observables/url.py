"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from octi_entities.common import Observable
from octi_entities.enum import ObservableType, PatternType
from octi_entities.observations.indicator import Indicator
from pydantic import AwareDatetime, Field


class Url(Observable):
    """Represent a URL observable."""

    value: str = Field(
        description="The URL value.",
        min_length=1,
    )

    def to_stix2_object(self) -> stix2.v21.URL:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.URL(
            value=self.value,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )

    def to_indicator(
        self,
        valid_from: Optional[AwareDatetime] = None,
        valid_until: Optional[AwareDatetime] = None,
    ) -> Indicator:
        """Make stix indicator based on current observable.

        - Indicator's name is the value of the url.
        - Indicator's pattern is the value of the url.
        """
        return Indicator(
            name=self.value,
            pattern=f"[url:value='{self.value}']",
            pattern_type=PatternType.STIX.value,
            observable_type=ObservableType.URL.value,
            description=self.description,
            valid_from=valid_from,
            valid_until=valid_until,
            score=self.score,
            author=self.author,
            markings=self.markings,
            external_references=self.external_references,
        )
