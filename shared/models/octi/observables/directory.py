"""Define the OpenCTI Observable."""

from datetime import datetime
from typing import Optional

import stix2
from models.octi.common import Observable

# from dragos.domain.models.octi.observables import File
from pydantic import Field


class Directory(Observable):
    """Represent a directory observable on OpenCTI."""

    path: str = Field(
        ...,
        description="The path, as originally observed, to the directory on the file system.",
        min_length=1,
    )
    path_enc: Optional[str] = Field(
        None,
        description="The observed encoding for the path.",
    )
    ctime: Optional[datetime] = Field(
        None,
        description="Date/time the directory was created.",
    )
    mtime: Optional[datetime] = Field(
        None,
        description="Date/time the directory was last written to or modified.",
    )
    atime: Optional[datetime] = Field(
        None,
        description="Date/time the directory was last accessed.",
    )
    contains_refs: Optional[list[Observable]] = Field(
        None,
        description="References to other File and/or Directory objects contained within the directory.",
    )

    def to_stix2_object(self) -> stix2.Directory:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Directory(
            path=self.path,
            path_enc=self.path_enc,
            ctime=self.ctime,
            mtime=self.mtime,
            atime=self.atime,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            contains_refs=None,  # not implemented on OpenCTI
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
