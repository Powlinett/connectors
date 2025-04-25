"""Define the OpenCTI Observable."""

from typing import Any, Optional, Self

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from connectors_sdk.octi_entities.enum import HashAlgorithm, ObservableType, PatternType
from connectors_sdk.octi_entities.observations.indicator import Indicator
from pydantic import AwareDatetime, Field, PositiveInt, model_validator

# from dragos.domain.models.octi.observables import Artifact, Directory


class File(Observable):
    """Represent a file observable on OpenCTI."""

    hashes: Optional[dict[HashAlgorithm, str]] = Field(
        description="A dictionary of hashes for the file.",
        default=None,
        min_length=1,
    )
    size: Optional[PositiveInt] = Field(
        description="The size of the file in bytes.",
        default=None,
    )
    name: Optional[str] = Field(
        description="The name of the file.",
        default=None,
    )
    name_enc: Optional[str] = Field(
        description="The observed encoding for the name of the file.",
        default=None,
    )
    magic_number_hex: Optional[str] = Field(
        description="The hexadecimal constant ('magic number') associated with the file format.",
        default=None,
    )
    mime_type: Optional[str] = Field(
        description="The MIME type name specified for the file, e.g., application/msword.",
        default=None,
    )
    ctime: Optional[AwareDatetime] = Field(
        description="Date/time the directory was created.",
        default=None,
    )
    mtime: Optional[AwareDatetime] = Field(
        description="Date/time the directory was last writtend to or modified.",
        default=None,
    )
    atime: Optional[AwareDatetime] = Field(
        description="Date/time the directory was last accessed.",
        default=None,
    )
    additional_names: Optional[list[str]] = Field(
        description="Additional names of the file.",
        default=None,
    )

    @model_validator(mode="after")
    def _validate_model(self) -> Self:
        """Add further validation after model initialization. Automatically called by Pydantic."""
        if not self.name and not self.hashes:
            raise ValueError("Either 'name' or one of 'hashes' must be provided.")
        return self

    def _custom_properties_to_stix(self) -> dict[str, Any]:
        """Convert custom properties to stix."""
        custom_properties = super()._custom_properties_to_stix()
        custom_properties.update({"x_opencti_additional_names": self.additional_names})
        return custom_properties

    def to_stix2_object(self) -> stix2.File:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.File(
            hashes=self.hashes,
            size=self.size,
            name=self.name,
            name_enc=self.name_enc,
            magic_number_hex=self.magic_number_hex,
            mime_type=self.mime_type,
            ctime=self.ctime,
            mtime=self.mtime,
            atime=self.atime,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            parent_directory_ref=None,  # not implemented on OpenCTI
            contains_refs=None,  # not implemented on OpenCTI
            content_ref=None,  # not implemented on OpenCTI
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

        - Indicator's name is either the name or the first hash value of the file.
        - Indicator's pattern is a combination of the name and the hash values of the file.
        """
        name = self.name or (list(self.hashes.values())[0] if self.hashes else None)

        stix_pattern = None
        comparison_expressions = []
        if self.name:
            comparison_expressions.append(f"file:name='{self.name}'")
        if self.hashes:
            for key in self.hashes:
                comparison_expressions.append(
                    f"file:hashes.'{key}'='{self.hashes[key]}'"
                )
        if comparison_expressions:
            stix_pattern = f"[{' AND '.join(comparison_expressions)}]"

        return Indicator(
            name=name,
            pattern=stix_pattern,
            pattern_type=PatternType.STIX.value,
            observable_type=ObservableType.FILE.value,
            description=self.description,
            valid_from=valid_from,
            valid_until=valid_until,
            score=self.score,
            author=self.author,
            markings=self.markings,
            external_references=self.external_references,
        )
