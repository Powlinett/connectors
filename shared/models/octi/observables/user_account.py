"""Define the OpenCTI Observable."""

from datetime import datetime
from typing import Optional, Self

import stix2
from models.octi.common import Observable
from models.octi.typings import AccountType
from pydantic import Field, model_validator


class UserAccount(Observable):
    """Represent a user account observable."""

    user_id: Optional[str] = Field(
        None,
        description="The identifier of the account.",
    )
    credential: Optional[str] = Field(
        None,
        description="Cleartext credential.",
    )
    account_login: Optional[str] = Field(
        None,
        description="The account login string.",
    )
    account_type: Optional[AccountType] = Field(
        None,
        description="The type of the account.",
    )
    display_name: Optional[str] = Field(
        None,
        description="The display name of the account.",
    )
    is_service_account: Optional[bool] = Field(
        None,
        description="Indicates that the account is associated with a network service or system process (daemon), not a specific individual.",
    )
    is_privileged: Optional[bool] = Field(
        None,
        description="Indicates that the account has elevated privileges.",
    )
    can_escalate_privs: Optional[bool] = Field(
        None,
        description="That the account has the ability to escalate privileges (i.e., in the case of sudo on Unix or a Windows Domain Admin account).",
    )
    is_disabled: Optional[bool] = Field(
        None,
        description="Specifies if the account is disabled.",
    )
    account_created: Optional[datetime] = Field(
        None,
        description="Specifies when the account was created.",
    )
    account_expires: Optional[datetime] = Field(
        None,
        description="The expiration date of the account.",
    )
    credential_last_changed: Optional[datetime] = Field(
        None,
        description="Specifies when the account credential was last changed.",
    )
    account_first_login: Optional[datetime] = Field(
        None,
        description="Specifies when the account was first accessed.",
    )
    account_last_login: Optional[datetime] = Field(
        None,
        description="Specifies when the account was last accessed.",
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
