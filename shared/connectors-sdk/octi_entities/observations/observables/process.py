"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from octi_entities.common import Observable
from octi_entities.enum import (
    WindowsIntegrityLevel,
    WindowsServiceStartType,
    WindowsServiceStatus,
    WindowsServiceType,
)
from pydantic import AwareDatetime, Field

# from dragos.domain.models.octi.observables import File, NetworkTraffic, UserAccount


class Process(Observable):
    """Represent a process observable on OpenCTI."""

    command_line: str = Field(
        description="The full command line used in executing the process.",
        min_length=1,
    )
    pid: Optional[int] = Field(
        description="The Process ID, or PID, of the process.",
        default=None,
    )
    is_hidden: Optional[bool] = Field(
        description="Whether the process is hidden.",
        default=None,
    )
    created_time: Optional[AwareDatetime] = Field(
        description="Date/time at which the process was created.",
        default=None,
    )
    cwd: Optional[str] = Field(
        description="The current working directory of the process.",
        default=None,
    )
    environment_variables: Optional[dict[str, str]] = Field(
        description="The environment variables associated with the process as a dictionary.",
        default=None,
    )
    opened_connection_refs: Optional[list[Observable]] = Field(
        description="The network connections opened by the process, as a reference to one or more Network Traffic Objects.",
        default=None,
    )
    creator_user_ref: Optional[Observable] = Field(
        description="The user that created the process, as a reference to a User Account Object.",
        default=None,
    )
    image_ref: Optional[Observable] = Field(
        description="The executable binary that was executed as the process image, as a reference to a File Object.",
        default=None,
    )
    parent_ref: Optional[Observable] = Field(
        description="The other process that spawned (i.e. is the parent of) this one, as represented by a Process Object.",
        default=None,
    )
    child_refs: Optional[list[Observable]] = Field(
        description="Specifies the other processes that were spawned by (i.e. children of) this process, as a reference to one or more other Process Objects.",
        default=None,
    )
    # Windows Process Extension
    aslr_enabled: Optional[bool] = Field(
        description="Whether Address Space Layout Randomization (ASLR) is enabled for the process.",
        default=None,
    )
    dep_enabled: Optional[bool] = Field(
        description="Whether Data Execution Prevention (DEP) is enabled for the process.",
        default=None,
    )
    owner_sid: Optional[str] = Field(
        description="The Security ID (SID) value of the owner of the process.",
        default=None,
    )
    priority: Optional[int] = Field(
        description="The current priority class of the process in Windows.",
        default=None,
    )
    window_title: Optional[str] = Field(
        description="The title of the main window of the process.",
        default=None,
    )
    integrity_level: Optional[WindowsIntegrityLevel] = Field(
        description="The Windows integrity level, or trustworthiness, of the process.",
        default=None,
    )
    # Windows Service Extension
    service_name: Optional[str] = Field(
        description="The name of the service.",
        default=None,
    )
    descriptions: Optional[list[str]] = Field(
        description="The descriptions defined for the service.",
        default=None,
    )
    display_name: Optional[str] = Field(
        description="The display name of the service in Windows GUI controls.",
        default=None,
    )
    group_name: Optional[str] = Field(
        description="The name of the load ordering group of which the service is a member.",
        default=None,
    )
    start_type: Optional[WindowsServiceStartType] = Field(
        description="The start options defined for the service.",
        default=None,
    )
    service_type: Optional[WindowsServiceType] = Field(
        description="The type of the service.",
        default=None,
    )
    service_status: Optional[WindowsServiceStatus] = Field(
        description="The current status of the service.",
        default=None,
    )

    def to_stix2_object(self) -> stix2.v21.Process:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Process(
            command_line=self.command_line,
            pid=self.pid,
            is_hidden=self.is_hidden,
            created_time=self.created_time,
            cwd=self.cwd,
            environment_variables=self.environment_variables,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # Windows Process Extension
            aslr_enabled=self.aslr_enabled,
            dep_enabled=self.dep_enabled,
            owner_sid=self.owner_sid,
            priority=self.priority,
            window_title=self.window_title,
            integrity_level=self.integrity_level,
            # Windows Service Extension
            service_name=self.service_name,
            descriptions=self.descriptions,
            display_name=self.display_name,
            group_name=self.group_name,
            start_type=self.start_type,
            service_type=self.service_type,
            service_status=self.service_status,
            # unused
            opened_connection_refs=None,  # not implemented on OpenCTI
            creator_user_ref=None,  # not implemented on OpenCTI
            image_ref=None,  # not implemented on OpenCTI
            parent_ref=None,  # not implemented on OpenCTI
            child_refs=None,  # not implemented on OpenCTI
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
