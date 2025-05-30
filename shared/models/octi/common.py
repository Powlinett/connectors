"""Offer common tools to create octi entities."""

from abc import ABC, abstractmethod
from typing import Any, Optional

import pycti  # type: ignore[import-untyped]  # pycti does not provide stubs
import stix2  # type: ignore[import-untyped] # stix2 does not provide stubs
import stix2.exceptions
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, PrivateAttr

from models.octi.typings import TLPLevel


class BaseModelWithoutExtra(BaseModel):
    """Represent a Pydantic BaseModel where non explicitly define fields are forbidden."""

    model_config = ConfigDict(
        extra="forbid",
    )

    def __hash__(self) -> int:
        """Create a hash based on the model's json representation dynamically."""
        return hash(self.model_dump_json())

    def __eq__(self, other: Any) -> bool:
        """Implement comparison between similar object."""
        if not isinstance(other, self.__class__):
            raise NotImplementedError("Cannot compare objects from different type.")
        # Compare the attributes by converting them to a dictionary
        return self.model_dump_json() == other.model_dump_json()


class BaseEntity(BaseModelWithoutExtra):
    """Base class to implement common attributes and methods for all entities."""

    model_config = ConfigDict(
        **BaseModelWithoutExtra.model_config,
        arbitrary_types_allowed=True,
    )

    _stix2_representation: Optional[Any] = PrivateAttr(None)
    _id: str = PrivateAttr("")

    def model_post_init(
        self, context__: Any
    ) -> None:  # pylint: disable=unused-argument
        """Define the post initialization method, automatically called after __init__ in a pydantic model initialization.

        Notes:
            This allows a last modification of the pydantic Model before it is eventually frozen.

        Args:
            context__(Any): The pydantic context used by pydantic framework.

        References:
            https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_parametrized_name [consulted on
                October 4th, 2024]

        """
        try:
            self._stix2_representation = self.to_stix2_object()
        except stix2.exceptions.STIXError as err:
            # Wrap STIXError so Pydantic can catch it and raise its own ValidationError
            raise ValueError(str(err)) from err

        self._id = self._stix2_representation["id"]

    @abstractmethod
    def to_stix2_object(self) -> stix2.v21._STIXBase21:  # noqa: W0212
        """Make stix object (usually from stix2 python lib objects)."""

    @property
    def id(self) -> str:
        """Return the unique identifier of the entity."""
        return self._id


class ExternalReference(BaseModelWithoutExtra):
    """Represents an external reference to a source of information."""

    source_name: str = Field(
        ...,
        description="The name of the source of the external reference.",
    )
    description: Optional[str] = Field(
        None,
        description="Description of the external reference.",
    )
    url: Optional[str] = Field(
        None,
        description="URL of the external reference.",
    )
    external_id: Optional[str] = Field(
        None,
        description="An identifier for the external reference content.",
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


class KillChainPhase(BaseModelWithoutExtra):
    """Represent a kill chain phase."""

    chain_name: str = Field(..., description="Name of the kill chain.")
    phase_name: str = Field(..., description="Name of the kill chain phase.")

    def to_stix2_object(self) -> stix2.v21.KillChainPhase:
        """Make stix object."""
        return stix2.KillChainPhase(
            kill_chain_name=self.chain_name,
            phase_name=self.phase_name,
        )


class Author(ABC, BaseEntity):
    """Represent an author.

    Warning:
        This class cannot be used directly, it must be subclassed.

    """

    @abstractmethod
    def to_stix2_object(self) -> stix2.v21._STIXBase21:
        """Make stix object."""
        raise NotImplementedError()


class TLPMarking(BaseEntity):
    """Represent a TLP marking definition."""

    level: TLPLevel = Field(
        ...,
        description="The level of the marking.",
    )

    def to_stix2_object(self) -> stix2.v21.MarkingDefinition:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        mapping = {
            "white": stix2.TLP_WHITE,
            "green": stix2.TLP_GREEN,
            "amber": stix2.TLP_AMBER,
            "amber+strict": stix2.MarkingDefinition(
                id=pycti.MarkingDefinition.generate_id("TLP", "TLP:AMBER+STRICT"),
                definition_type="statement",
                definition={"statement": "custom"},
                custom_properties=dict(  # noqa: C408  # No literal dict for maintainability
                    x_opencti_definition_type="TLP",
                    x_opencti_definition="TLP:AMBER+STRICT",
                ),
            ),
            "red": stix2.TLP_RED,
        }
        return mapping[self.level]


class DomainObject(BaseEntity):
    """Base class for OpenCTI Domain Objects."""

    author: Optional[Author] = Field(
        None,
        description="Author of the report.",
    )
    markings: Optional[list[TLPMarking]] = Field(
        None,
        description="Markings of the report.",
    )
    external_references: Optional[list[ExternalReference]] = Field(
        None,
        description="External references of the report.",
    )

    @abstractmethod
    def to_stix2_object(self) -> Any:
        """Make stix object"""


class Observable(BaseEntity):
    """Base class for OpenCTI Observables.

    NOTA BENE: Observables do not need deterministic stix id generation. STIX python lib handles it.
    """

    score: Optional[int] = Field(
        None,
        description="Score of the observable.",
        ge=0,
        le=100,
    )
    description: Optional[str] = Field(
        None,
        description="Description of the observable.",
    )
    labels: Optional[list[str]] = Field(
        None,
        description="Labels of the observable.",
    )
    external_references: Optional[list[ExternalReference]] = Field(
        None,
        description="External references of the observable.",
    )
    markings: Optional[list[TLPMarking]] = Field(
        None,
        description="References for object marking.",
    )
    author: Optional[Author] = Field(
        None,
        description="The Author reporting this Observable.",
    )

    def _custom_properties_to_stix(self) -> dict[str, Any]:
        """Factorize custom params."""
        return dict(  # noqa: C408 # No literal dict for maintainability
            x_opencti_score=self.score,
            x_opencti_description=self.description,
            x_opencti_labels=self.labels,
            x_opencti_external_references=[
                external_ref.to_stix2_object()
                for external_ref in self.external_references or []
            ],
            x_opencti_created_by_ref=self.author.id if self.author else None,
        )

    @abstractmethod
    def to_stix2_object(self) -> stix2.v21._STIXBase21:
        """Make stix object."""

    @abstractmethod
    def to_indicator(self) -> Indicator:
        """Make stix indicator based on current observable."""


class Relationship(BaseEntity):
    """Base class for OpenCTI relationships."""

    _relationship_type: str = PrivateAttr("")

    source: BaseEntity = Field(
        ...,
        description="The source entity of the relationship.",
    )
    target: BaseEntity = Field(
        ...,
        description="The target entity of the relationship.",
    )
    description: Optional[str] = Field(
        None,
        description="Description of the relationship.",
    )
    start_time: Optional[AwareDatetime] = Field(
        None,
        description="Start time of the relationship in ISO 8601 format.",
    )
    stop_time: Optional[AwareDatetime] = Field(
        None,
        description="End time of the relationship in ISO 8601 format.",
    )
    author: Optional[Author] = Field(
        None,
        description="Reference to the author that reported this relationship.",
    )
    markings: Optional[list[TLPMarking]] = Field(
        None,
        description="References for object marking",
    )
    external_references: Optional[list[ExternalReference]] = Field(
        None,
        description="External references",
    )

    def to_stix2_object(self) -> stix2.v21.Relationship:
        """Make stix object."""
        return stix2.Relationship(
            id=pycti.StixCoreRelationship.generate_id(
                relationship_type=self._relationship_type,
                source_ref=self.source.id,
                target_ref=self.target.id,
                start_time=self.start_time,
                stop_time=self.stop_time,
            ),
            relationship_type=self._relationship_type,
            **self._common_stix2_args(),
        )

    def _common_stix2_args(self) -> dict[str, Any]:
        # keep dict constructor rather than literal dict for maintainance.
        return dict(  # noqa: C408
            source_ref=self.source.id,
            target_ref=self.target.id,
            description=self.description,
            start_time=self.start_time,
            stop_time=self.stop_time,
            created_by_ref=self.author.id,
            object_marking_refs=[marking.id for marking in self.markings or []],
            external_references=[
                ref.to_stix2_object() for ref in self.external_references or []
            ],
            # unused
            created=None,
            modified=None,
        )
