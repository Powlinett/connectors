"""Flatten imports from connectors_sdk.octi_entities module."""

from .analyses.external_reference import ExternalReference
from .analyses.report import Report
from .arsenals.malware import Malware
from .arsenals.vulnerability import Vulnerability
from .common import TLPMarking
from .entities.organization import Organization, OrganizationAuthor
from .entities.sector import Sector
from .locations.administrative_area import AdministrativeArea
from .locations.city import City
from .locations.country import Country
from .locations.position import Position
from .locations.region import Region
from .observations import (
    Artifact,
    AutonomousSystem,
    Directory,
    DomainName,
    EmailAddress,
    EmailMessage,
    File,
    Indicator,
    IPV4Address,
    IPV6Address,
    MACAddress,
    Mutex,
    NetworkTraffic,
    Process,
    Software,
    Url,
    UserAccount,
    WindowsRegistryKey,
)
from .threats.intrusion_set import IntrusionSet

__all__ = [
    "AdministrativeArea",
    "Artifact",
    "AutonomousSystem",
    "City",
    "Country",
    "Directory",
    "DomainName",
    "EmailAddress",
    "EmailMessage",
    "ExternalReference",
    "File",
    "Indicator",
    "IntrusionSet",
    "IPV4Address",
    "IPV6Address",
    "MACAddress",
    "Malware",
    "Mutex",
    "NetworkTraffic",
    "Organization",
    "OrganizationAuthor",
    "Position",
    "Process",
    "Region",
    "Report",
    "Sector",
    "Software",
    "TLPMarking",
    "Url",
    "UserAccount",
    "Vulnerability",
    "WindowsRegistryKey",
]
