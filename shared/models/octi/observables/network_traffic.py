"""Define the OpenCTI Observable."""

from datetime import datetime
from typing import Optional, Self

import stix2
from models.octi.common import Observable

# from dragos.domain.models.octi.observables import (
#     Artifact,
#     DomainName,
#     IPv4Address,
#     IPv6Address,
#     MACAddress,
# )
from pydantic import Field, model_validator


class NetworkTraffic(Observable):
    """Represent a network traffic observable on OpenCTI."""

    protocols: list[str] = Field(
        ...,
        description="The protocols observed in the network traffic, along with their corresponding state.",
        min_length=1,
    )
    start: Optional[datetime] = Field(
        None,
        description="Date/time the network traffic was initiated.",
    )
    end: Optional[datetime] = Field(
        None,
        description="Date/time the network traffic ended.",
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the network traffic is still ongoing  If the end property is provided, this property MUST be false.",
    )
    src_ref: Optional[Observable] = Field(
        None,
        description="Reference to the source of the network traffic, as an Observable Object.",
    )
    dst_ref: Optional[Observable] = Field(
        None,
        description="Reference to the destination of the network traffic, as an Observable Object.",
    )
    src_port: Optional[int] = Field(
        None,
        description="The source port used in the network traffic.",
        ge=0,
        le=65535,
    )
    dst_port: Optional[int] = Field(
        None,
        description="The destination port used in the network traffic.",
        ge=0,
        le=65535,
    )
    src_byte_count: Optional[int] = Field(
        None,
        description="The number of bytes sent from the source to the destination.",
    )
    dst_byte_count: Optional[int] = Field(
        None,
        description="The number of bytes sent from the destination to the source.",
    )
    src_packets: Optional[int] = Field(
        None,
        description="The number of packets sent from the source to the destination.",
    )
    dst_packets: Optional[int] = Field(
        None,
        description="The number of packets sent from the destination to the source.",
    )
    ipfix: Optional[dict[str, int | str]] = Field(
        None,
        description="Any IP Flow Information Export (IPFIX) data for the traffic.",
    )
    src_payload_ref: Optional[Observable] = Field(
        None,
        description="Specifies the bytes sent from the source to the destination.",
    )
    dst_payload_ref: Optional[Observable] = Field(
        None,
        description="Specifies the bytes sent from the destination to the source.",
    )
    encapsulated_by_ref: Optional[Observable] = Field(
        None,
        description="Links to another network-traffic object which encapsulates this object.",
    )
    encapsulates_refs: Optional[list[Observable]] = Field(
        None,
        description="Links to other network-traffic objects encapsulated by a network-traffic.",
    )

    @model_validator(mode="after")
    def _validate_model(self) -> Self:
        """Check fields combination."""
        if self.src_ref is None and self.dst_ref is None:
            raise ValueError(
                "At least one of 'src_ref' or 'dst_ref' fields must be provided."
            )
        return self

    def to_stix2_object(self) -> stix2.v21.NetworkTraffic:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.NetworkTraffic(
            protocols=self.protocols,
            start=self.start,
            end=self.end,
            is_active=self.is_active,
            src_ref=self.src_ref.id if self.src_ref else None,
            dst_ref=self.dst_ref.id if self.dst_ref else None,
            src_port=self.src_port,
            dst_port=self.dst_port,
            src_byte_count=self.src_byte_count,
            dst_byte_count=self.dst_byte_count,
            src_packets=self.src_packets,
            dst_packets=self.dst_packets,
            ipfix=self.ipfix,
            src_payload_ref=self.src_payload_ref.id if self.src_payload_ref else None,
            dst_payload_ref=self.dst_payload_ref.id if self.dst_payload_ref else None,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            encapsulated_by_ref=None,  # not implemented on OpenCTI
            encapsulates_refs=None,  # not implemented on OpenCTI
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
