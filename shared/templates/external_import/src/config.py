from datetime import datetime, timedelta
from typing import Literal

from connectors_sdk.external_import import BaseConfig, _ConfigBaseModel


class _TemplateConfig(_ConfigBaseModel):
    """
    Define template custom config fields and any useful validation logic.
    """

    # ===========================
    # === Add your code below ===
    # ===========================

    # For example:
    tlp_level: Literal[
        "white",
        "clear",
        "green",
        "amber",
        "amber+strict",
        "red",
    ]
    import_start_date: datetime | timedelta
    api_base_url: str
    api_token: str

    # ===========================
    # === Add your code above ===
    # ===========================


class TemplateConfig(BaseConfig):
    """
    Main configuration class for the Template connector.
    Define any additional configs but `opencti` and `connector`
    """

    template: _TemplateConfig
