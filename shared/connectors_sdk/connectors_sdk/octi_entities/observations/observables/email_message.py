"""Define the OpenCTI Observable."""

from typing import Optional

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from pydantic import AwareDatetime, Field

# from dragos.domain.models.octi.observables import EmailAddress


class EmailMessage(Observable):
    """Represent an Email Message observable on OpenCTI.

    Example:
        >>> email_message = EmailMessage(
        ...     attribute_date=datetime.now(),
        ...     body="This is a test email",
        ...     content_type="text/plain",
        ...     is_multipart=True,
        ...     message_id="123456",
        ...     received_lines=2,
        ...     subject="Test Email",
        ...     from_=EmailAddress(value="hacker@example.com"),
        ...     to_=[EmailAddress(value="target@example.com")],
        ...     cc_=None,
        ...     bcc_=None,
        ...     author=OrganizationAuthor(name="author"),
        ...     markings=[TLPMarking(level="white")],
        ...     external_references=None,
        ...     score=None,
        ... )

    """

    subject: str = Field(
        description="Subject of the email message.",
        min_length=1,
    )
    is_multipart: bool = Field(
        description="Is the email message multipart.",
    )
    body: Optional[str] = Field(
        description="Body of the email message.",
        default=None,
    )
    attribute_date: Optional[AwareDatetime] = Field(
        description="Attribute date of the email message.",
        default=None,
    )
    content_type: Optional[str] = Field(
        description="Content type of the email message.",
        default=None,
    )
    message_id: Optional[str] = Field(
        description="Message ID of the email message.",
        default=None,
    )
    received_lines: Optional[list[str]] = Field(
        description="Received lines of the email message.",
        default=None,
    )

    # Nested relationships
    from_: Optional[Observable] = Field(None, description="From email address.")
    to_: Optional[list[Observable]] = Field(None, description="To email addresses.")
    cc_: Optional[list[Observable]] = Field(None, description="CC email addresses.")
    bcc_: Optional[list[Observable]] = Field(None, description="BCC email addresses.")

    def to_stix2_object(self) -> stix2.v21.EmailMessage:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.EmailMessage(
            subject=self.subject,
            is_multipart=self.is_multipart,
            body=self.body,
            date=self.attribute_date,
            content_type=self.content_type,
            message_id=self.message_id,
            received_lines=self.received_lines,
            from_ref=self.from_.id if self.from_ else None,
            sender_ref=self.from_.id if self.from_ else None,
            to_refs=[email.id for email in self.to_ or []],
            cc_refs=[email.id for email in self.cc_ or []],
            bcc_refs=[email.id for email in self.bcc_ or []],
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            body_multipart=None,  # not implemented on OpenCTI
            additional_header_fields=None,
            raw_email_ref=None,
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
