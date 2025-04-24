"""Define the OpenCTI Observable."""

from typing import Any, Optional

import stix2
from octi_entities.common import Observable
from octi_entities.enum import (
    EncryptionAlgorithm,
    HashAlgorithm,
    ObservableType,
    PatternType,
)
from octi_entities.observations.indicator import Indicator
from pydantic import AwareDatetime, Field


class OCTIArtifact(stix2.v21.Artifact):  # type: ignore[misc]
    # considered as Any because stix2 does not provide stubs
    """Override stix2 Artifact not to require payload_bin  xor url xor hash."""

    def _check_object_constraints(self) -> None:
        super(stix2.v21.Artifact, self)._check_object_constraints()


class Artifact(Observable):
    """Represent an artifact observable on OpenCTI."""

    payload_bin: Optional[bytes] = Field(
        description="Binary data contained in the artifact as a base64-encoded string.",
        default=None,
    )
    url: Optional[str] = Field(
        description="A valid URL that resolves to the unencoded content.",
        default=None,
    )
    hashes: Optional[dict[HashAlgorithm, str]] = Field(
        description="Specifies a dictionary of hashes for the contents of the 'url' or the 'payload_bin' field.",
        default=None,
        min_length=1,
    )
    mime_type: Optional[str] = Field(
        description="Artifact mime type, ideally from the IANA media type registry.",
        default=None,
    )
    encryption_algorithm: Optional[EncryptionAlgorithm] = Field(
        description="If the artifact is encrypted, specifies the type of encryption algorithm the binary data is encoded in.",
        default=None,
    )
    decryption_key: Optional[str] = Field(
        description="Specifies the decryption key for the encrypted binary data.",
        default=None,
    )
    additional_names: Optional[list[str]] = Field(
        description="OpenCTI additional names.",
        default=None,
    )

    def _custom_properties_to_stix(self) -> dict[str, Any]:
        """Convert custom properties to stix."""
        custom_properties = super()._custom_properties_to_stix()
        custom_properties.update({"x_opencti_additional_names": self.additional_names})
        return custom_properties

    def to_stix2_object(self) -> OCTIArtifact:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation  # type: ignore[no-any-return]
            # stix2 does not provide stubs

        content = dict(  # noqa: C408 # No literal dict for maintainability
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

        # remove all None values from the content dict
        content = {k: v for k, v in content.items() if v is not None}

        return OCTIArtifact(
            **content,
        )

    def to_indicator(
        self,
        valid_from: Optional[AwareDatetime] = None,
        valid_until: Optional[AwareDatetime] = None,
    ) -> Indicator:
        """Make stix indicator based on current observable.

        - Indicator's name is either the payload bin, or the url, or the first hash value of the artifact.
        - Indicator's pattern is a combination of both payload bin, url and hash values of the artifact, if present.
        """
        name = (
            (self.payload_bin.decode() if self.payload_bin else None)
            or self.url
            or (list(self.hashes.values())[0] if self.hashes else None)
        )

        stix_pattern = None
        comparison_expressions = []
        if self.payload_bin:
            comparison_expressions.append(
                f"artifact:payload_bin='{self.payload_bin.decode()}'"
            )
        if self.url:
            comparison_expressions.append(f"artifact:url='{self.url}'")
        if self.hashes:
            for key in self.hashes:
                comparison_expressions.append(
                    f"artifact:hashes.'{key}'='{self.hashes[key]}'"
                )
        if comparison_expressions:
            stix_pattern = f"[{' AND '.join(comparison_expressions)}]"

        return Indicator(
            name=name,
            pattern=stix_pattern,
            pattern_type=PatternType.STIX.value,
            observable_type=ObservableType.ARTIFACT.value,
            description=self.description,
            valid_from=valid_from,
            valid_until=valid_until,
            score=self.score,
            author=self.author,
            markings=self.markings,
            external_references=self.external_references,
        )
