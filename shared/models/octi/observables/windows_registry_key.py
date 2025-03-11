"""Define the OpenCTI Observable."""

from datetime import datetime
from typing import Optional, Self

import stix2
from models.octi.common import BaseModelWithoutExtra, Observable
from models.octi.typings import WindowsRegistryDatatype

# from dragos.domain.models.octi.observables import UserAccount
from pydantic import Field, model_validator


class _WindowsRegistryValue(BaseModelWithoutExtra):
    name: Optional[str] = Field(
        None,
        description="The name of the registry value.",
    )
    data: Optional[str] = Field(
        None,
        description="The data contained in the registry value.",
    )
    data_type: Optional[WindowsRegistryDatatype] = Field(
        None,
        description="The registry (REG_*) data type used in the registry value.",
    )

    @model_validator(mode="after")
    def _validate_model(self) -> Self:
        if self.name is None and self.data is None and self.data_type is None:
            raise ValueError(
                "At least one of 'name', 'data' or 'data_type' fields must be defined."
            )
        return self

    def to_stix2_object(self) -> stix2.v21.WindowsRegistryValueType:
        return stix2.WindowsRegistryValueType(
            name=self.name,
            data=self.data,
            data_type=self.data_type,
        )


class WindowsRegistryKey(Observable):
    key: Optional[str] = Field(
        None,
        description="The full registry key including the hive.",
    )
    values: Optional[list[_WindowsRegistryValue]] = Field(
        None,
        description="The values found under the registry key.",
    )
    modified_time: Optional[datetime] = Field(
        None,
        description="The last date/time the registry key was modified.",
    )
    creator_user_ref: Optional[Observable] = Field(
        None,
        description="Reference to a user account that created the registry key.",
    )
    number_of_subkeys: Optional[int] = Field(
        None,
        description="The number of subkeys contained under the registry key.",
    )

    def to_stix2_object(self) -> stix2.v21.WindowsRegistryKey:
        return stix2.WindowsRegistryKey(
            key=self.key,
            values=(
                [value.to_stix2_object() for value in self.values]
                if self.values
                else None
            ),
            modified_time=self.modified_time,
            creator_user_ref=(
                self.creator_user_ref.id if self.creator_user_ref else None
            ),
            number_of_subkeys=self.number_of_subkeys,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
