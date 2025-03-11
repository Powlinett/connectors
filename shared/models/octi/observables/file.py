"""Define the OpenCTI Observable."""

from datetime import datetime
from typing import Optional, Self

import stix2
from models.octi.common import Observable
from models.octi.typings import HashAlgorithm

# from dragos.domain.models.octi.observables import Artifact, Directory
from pydantic import Field, PositiveInt, model_validator


class File(Observable):
    """Represent a file observable on OpenCTI."""

    hashes: Optional[dict[HashAlgorithm, str]] = Field(
        None,
        description="A dictionary of hashes for the file.",
        min_length=1,
    )
    size: Optional[PositiveInt] = Field(
        None,
        description="The size of the file in bytes.",
    )
    name: Optional[str] = Field(
        None,
        description="The name of the file.",
    )
    name_enc: Optional[str] = Field(
        None,
        description="The observed encoding for the name of the file.",
    )
    magic_number_hex: Optional[str] = Field(
        None,
        description="The hexadecimal constant ('magic number') associated with the file format.",
    )
    mime_type: Optional[str] = Field(
        None,
        description="The MIME type name specified for the file, e.g., application/msword.",
    )
    ctime: Optional[datetime] = Field(
        None,
        description="Date/time the directory was created.",
    )
    mtime: Optional[datetime] = Field(
        None,
        description="Date/time the directory was last writtend to or modified.",
    )
    atime: Optional[datetime] = Field(
        None,
        description="Date/time the directory was last accessed.",
    )
    additional_names: Optional[list[str]] = Field(
        None,
        description="Additional names of the file.",
    )
    parent_directory_ref: Optional[Observable] = Field(
        None,
        description="Reference to the parent directory of the file.",
    )
    contains_refs: Optional[list[Observable]] = Field(
        None,
        description="References to other File and/or Directory objects contained within the directory.",
    )
    content_ref: Optional[Observable] = Field(
        None,
        description="Reference to the content of the file, represented as an Artifact object.",
    )

    @model_validator(mode="after")
    def _validate_model(self) -> Self:
        if self.name is None and len(self.hashes) == 0:
            raise ValueError("Either 'name' or one of 'hashes' must be provided.")
        return self

    def _custom_properties_to_stix(self):
        """Convert custom properties to stix."""
        custom_properties = super()._custom_properties_to_stix()
        custom_properties.update(dict(x_opencti_additional_names=self.additional_names))
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
