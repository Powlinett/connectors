"""Define the OpenCTI Observable."""

from typing import Optional, Self

import stix2  # type: ignore[import-untyped]  # stix2 does not provide stubs
from connectors_sdk.octi_entities.common import Observable
from connectors_sdk.octi_entities.enum import AccountType
from pydantic import AwareDatetime, Field, model_validator


class UserAccount(Observable):
    """Represent a user account observable."""

    user_id: Optional[str] = Field(
        description="The identifier of the account.",
        default=None,
    )
    credential: Optional[str] = Field(
        description="Cleartext credential.",
        default=None,
    )
    account_login: Optional[str] = Field(
        description="The account login string.",
        default=None,
    )
    account_type: Optional[AccountType] = Field(
        description="The type of the account.",
        default=None,
    )
    display_name: Optional[str] = Field(
        description="The display name of the account.",
        default=None,
    )
    is_service_account: Optional[bool] = Field(
        description="Indicates that the account is associated with a network service or system process (daemon), not a specific individual.",
        default=None,
    )
    is_privileged: Optional[bool] = Field(
        description="Indicates that the account has elevated privileges.",
        default=None,
    )
    can_escalate_privs: Optional[bool] = Field(
        description="That the account has the ability to escalate privileges (i.e., in the case of sudo on Unix or a Windows Domain Admin account).",
        default=None,
    )
    is_disabled: Optional[bool] = Field(
        description="Specifies if the account is disabled.",
        default=None,
    )
    account_created: Optional[AwareDatetime] = Field(
        description="Specifies when the account was created.",
        default=None,
    )
    account_expires: Optional[AwareDatetime] = Field(
        description="The expiration date of the account.",
        default=None,
    )
    credential_last_changed: Optional[AwareDatetime] = Field(
        description="Specifies when the account credential was last changed.",
        default=None,
    )
    account_first_login: Optional[AwareDatetime] = Field(
        description="Specifies when the account was first accessed.",
        default=None,
    )
    account_last_login: Optional[AwareDatetime] = Field(
        description="Specifies when the account was last accessed.",
        default=None,
    )

    @model_validator(mode="after")
    def _validate_model(self) -> Self:
        if not self.account_login and not self.account_type:
            raise ValueError(
                "At least one of the fields 'account_login' or 'account_type' must be provided."
            )
        return self

    def to_stix2_object(self) -> stix2.UserAccount:
        """Make stix object."""
        if self._stix2_representation is not None:
            return self._stix2_representation

        return stix2.UserAccount(
            account_login=self.account_login,
            account_type=self.account_type,
            object_marking_refs=[marking.id for marking in self.markings or []],
            custom_properties=self._custom_properties_to_stix(),
            # unused
            granular_markings=None,
            defanged=None,
            extensions=None,
        )
