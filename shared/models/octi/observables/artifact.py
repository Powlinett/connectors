"""Define the OpenCTI Observable."""

from typing import Optional

import stix2
from models.octi.common import Observable
from models.octi.typings import EncryptionAlgorithm, HashAlgorithm
from pydantic import Field


class Artifact(Observable):
    """Represent an artifact observable on OpenCTI."""

    mime_type: Optional[str] = Field(
        None,
        description="Artifact mime type, ideally from the IANA media type registry.",
    )
    payload_bin: Optional[bytes] = Field(
        None,
        description="Binary data contained in the artifact as a base64-encoded string.",
    )
    url: Optional[str] = Field(
        None,
        description="A valid URL that resolves to the unencoded content.",
        min_length=1,
    )
    hashes: Optional[dict[HashAlgorithm, str]] = Field(
        None,
        description="Specifies a dictionary of hashes for the contents of the 'url' or the 'payload_bin' field.",
        min_length=1,
    )
    encryption_algorithm: Optional[EncryptionAlgorithm] = Field(
        None,
        description="If the artifact is encrypted, specifies the type of encryption algorithm the binary data is encoded in.",
    )
    decryption_key: Optional[str] = Field(
        None,
        description="Specifies the decryption key for the encrypted binary data.",
    )
    additional_names: Optional[list[str]] = Field(
        None,
        description="OpenCTI additional names.",
    )

    def _custom_properties_to_stix(self):
        """Convert custom properties to stix."""
        custom_properties = super()._custom_properties_to_stix()
        custom_properties.update(dict(x_opencti_additional_names=self.additional_names))
        return custom_properties

    def to_stix2_object(self) -> stix2.v21.Artifact:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.Artifact(
            mime_type=self.mime_type,
            payload_bin=self.payload_bin,
            url=self.url,
            hashes=self.hashes,
            encryption_algorithm=self.encryption_algorithm,
            decryption_key=self.decryption_key,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
