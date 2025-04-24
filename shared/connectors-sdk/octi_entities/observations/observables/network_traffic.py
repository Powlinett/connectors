"""Define the OpenCTI Observable."""

from typing import Optional, Self

import stix2
from octi_entities.common import Observable
from pydantic import AwareDatetime, Field, model_validator

# from octi_entities.observations.observables import (
#     Artifact,
#     DomainName,
#     IPv4Address,
#     IPv6Address,
#     MACAddress,
# )


class NetworkTraffic(Observable):
    """Represent a network traffic observable on OpenCTI."""

    protocols: list[str] = Field(
        description="The protocols observed in the network traffic, along with their corresponding state.",
        min_length=1,
    )
    start: Optional[AwareDatetime] = Field(
        description="Date/time the network traffic was initiated.",
        default=None,
    )
    end: Optional[AwareDatetime] = Field(
        description="Date/time the network traffic ended.",
        default=None,
    )
    is_active: Optional[bool] = Field(
        description="Whether the network traffic is still ongoing  If the end property is provided, this property MUST be false.",
        default=None,
    )
    src_ref: Optional[Observable] = Field(
        description="Reference to the source of the network traffic, as an Observable Object.",
        default=None,
    )
    dst_ref: Optional[Observable] = Field(
        description="Reference to the destination of the network traffic, as an Observable Object.",
        default=None,
    )
    src_port: Optional[int] = Field(
        description="The source port used in the network traffic.",
        default=None,
        ge=0,
        le=65535,
    )
    dst_port: Optional[int] = Field(
        description="The destination port used in the network traffic.",
        default=None,
        ge=0,
        le=65535,
    )
    src_byte_count: Optional[int] = Field(
        description="The number of bytes sent from the source to the destination.",
        default=None,
    )
    dst_byte_count: Optional[int] = Field(
        description="The number of bytes sent from the destination to the source.",
        default=None,
    )
    src_packets: Optional[int] = Field(
        description="The number of packets sent from the source to the destination.",
        default=None,
    )
    dst_packets: Optional[int] = Field(
        description="The number of packets sent from the destination to the source.",
        default=None,
    )
    ipfix: Optional[dict[str, int | str]] = Field(
        description="Any IP Flow Information Export (IPFIX) data for the traffic.",
        default=None,
    )
    src_payload_ref: Optional[Observable] = Field(
        description="Specifies the bytes sent from the source to the destination.",
        default=None,
    )
    dst_payload_ref: Optional[Observable] = Field(
        description="Specifies the bytes sent from the destination to the source.",
        default=None,
    )
    encapsulated_by_ref: Optional[Observable] = Field(
        description="Links to another network-traffic object which encapsulates this object.",
        default=None,
    )
    encapsulates_refs: Optional[list[Observable]] = Field(
        description="Links to other network-traffic objects encapsulated by a network-traffic.",
        default=None,
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
