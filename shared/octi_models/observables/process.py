"""Define the OpenCTI Observable."""

from datetime import datetime
from typing import Optional

import stix2
from ..common import Observable
from ..typings import (
    WindowsIntegrityLevel,
    WindowsServiceStartType,
    WindowsServiceStatus,
    WindowsServiceType,
)

# from dragos.domain.models.octi.observables import File, NetworkTraffic, UserAccount
from pydantic import Field


class Process(Observable):
    """Represent a process observable on OpenCTI."""

    command_line: str = Field(
        ...,
        description="The full command line used in executing the process.",
        min_length=1,
    )
    pid: Optional[int] = Field(
        None,
        description="The Process ID, or PID, of the process.",
    )
    is_hidden: Optional[bool] = Field(
        None,
        description="Whether the process is hidden.",
    )
    created_time: Optional[datetime] = Field(
        None,
        description="Date/time at which the process was created.",
    )
    cwd: Optional[str] = Field(
        None,
        description="The current working directory of the process.",
    )
    environment_variables: Optional[dict[str, str]] = Field(
        None,
        description="The environment variables associated with the process as a dictionary.",
    )
    opened_connection_refs: Optional[list[Observable]] = Field(
        None,
        description="The network connections opened by the process, as a reference to one or more Network Traffic Objects.",
    )
    creator_user_ref: Optional[Observable] = Field(
        None,
        description="The user that created the process, as a reference to a User Account Object.",
    )
    image_ref: Optional[Observable] = Field(
        None,
        description="The executable binary that was executed as the process image, as a reference to a File Object.",
    )
    parent_ref: Optional[Observable] = Field(
        None,
        description="The other process that spawned (i.e. is the parent of) this one, as represented by a Process Object.",
    )
    child_refs: Optional[list[Observable]] = Field(
        None,
        description="Specifies the other processes that were spawned by (i.e. children of) this process, as a reference to one or more other Process Objects.",
    )
    # Windows Process Extension
    aslr_enabled: Optional[bool] = Field(
        None,
        description="Whether Address Space Layout Randomization (ASLR) is enabled for the process.",
    )
    dep_enabled: Optional[bool] = Field(
        None,
        description="Whether Data Execution Prevention (DEP) is enabled for the process.",
    )
    owner_sid: Optional[str] = Field(
        None,
        description="The Security ID (SID) value of the owner of the process.",
    )
    priority: Optional[int] = Field(
        None,
        description="The current priority class of the process in Windows.",
    )
    window_title: Optional[str] = Field(
        None,
        description="The title of the main window of the process.",
    )
    integrity_level: Optional[WindowsIntegrityLevel] = Field(
        None,
        description="The Windows integrity level, or trustworthiness, of the process.",
    )
    # Windows Service Extension
    service_name: Optional[str] = Field(
        None,
        description="The name of the service.",
    )
    descriptions: Optional[list[str]] = Field(
        None,
        description="The descriptions defined for the service.",
    )
    display_name: Optional[str] = Field(
        None,
        description="The display name of the service in Windows GUI controls.",
    )
    group_name: Optional[str] = Field(
        None,
        description="The name of the load ordering group of which the service is a member.",
    )
    start_type: Optional[WindowsServiceStartType] = Field(
        None,
        description="The start options defined for the service.",
    )
    service_type: Optional[WindowsServiceType] = Field(
        None,
        description="The type of the service.",
    )
    service_status: Optional[WindowsServiceStatus] = Field(
        None,
        description="The current status of the service.",
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
