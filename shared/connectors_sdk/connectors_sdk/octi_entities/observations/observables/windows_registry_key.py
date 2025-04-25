"""Define the OpenCTI Observable."""

from typing import Optional, Self

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import BaseModelWithoutExtra, Observable
from connectors_sdk.octi_entities.enum import WindowsRegistryDatatype
from pydantic import AwareDatetime, Field, model_validator

# from connectors_sdk.octi_entities.observations.observables import UserAccount


class _WindowsRegistryValue(BaseModelWithoutExtra):
    name: Optional[str] = Field(
        description="The name of the registry value.",
        default=None,
    )
    data: Optional[str] = Field(
        description="The data contained in the registry value.",
        default=None,
    )
    data_type: Optional[WindowsRegistryDatatype] = Field(
        description="The registry (REG_*) data type used in the registry value.",
        default=None,
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
        description="The full registry key including the hive.",
        default=None,
    )
    values: Optional[list[_WindowsRegistryValue]] = Field(
        description="The values found under the registry key.",
        default=None,
    )
    modified_time: Optional[AwareDatetime] = Field(
        description="The last date/time the registry key was modified.",
        default=None,
    )
    creator_user_ref: Optional[Observable] = Field(
        description="Reference to a user account that created the registry key.",
        default=None,
    )
    number_of_subkeys: Optional[int] = Field(
        description="The number of subkeys contained under the registry key.",
        default=None,
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
