from abc import ABC, abstractmethod
from datetime import timedelta
from pathlib import Path
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    HttpUrl,
    PlainSerializer,
)
from pydantic_core.core_schema import SerializationInfo
from pydantic_settings import (
    BaseSettings,
    NoDecode,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

"""
All the variables that have default values will override configuration from the OpenCTI helper.

All the variables of this classes are customizable through:
    - config.yml 
    - .env
    - environment variables.

If a variable is set in 2 different places, the first one will be used in this order:
    1. YAML file
    2. .env file
    3. Environment variables
    4. Default value
    
WARNING:
    The Environment variables in the .env or global environment must be set in the following format:
    OPENCTI_<variable>
    CONNECTOR_<variable>
    
    the split is made on the first occurrence of the "_" character.
"""


class ConfigRetrievalError(Exception):
    """Known errors wrapper for config loaders."""


def pycti_list_validator(value: str | list[str]) -> list[str]:
    """
    Convert comma-separated string into a list of values.

    Example:
        > values = pycti_list_validator("e1,e2,e3")
        > print(values) # [ "e1", "e2", "e3" ]
    """
    if isinstance(value, str):
        return [string.strip() for string in value.split(",")]
    return value


def pycti_list_serializer(value: list[str], info: SerializationInfo) -> str | list[str]:
    """
    Serialize list of values as comma-separated string.

    Example:
        > serialized_values = pycti_list_serializer([ "e1", "e2", "e3" ])
        > print(serialized_values) # "e1,e2,e3"
    """
    if isinstance(value, list) and info.context and info.context.get("mode") == "pycti":
        return ",".join(value)
    return value


ListFromString = Annotated[
    list[str],
    NoDecode,
    BeforeValidator(pycti_list_validator),
    PlainSerializer(pycti_list_serializer, when_used="json"),
]


class _ConfigBaseModel(BaseModel):
    """
    Base class for frozen config models, i.e. not alter-able after `model_post_init()`.
    """

    model_config = ConfigDict(frozen=True)


class _OpenCTIConfig(_ConfigBaseModel):
    """
    Define config specific to OpenCTI.
    """

    url: HttpUrl
    token: str
    json_logging: bool = Field(default=True)
    ssl_verify: bool = Field(default=False)


class _ConnectorConfig(_ConfigBaseModel):
    """
    Define config specific to this type of connector, e.g. an `external-import`.
    """

    id: str
    name: str
    type: str = "EXTERNAL_IMPORT"
    scope: ListFromString
    duration_period: timedelta

    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = Field(default="error")
    auto: bool = Field(default=False)
    expose_metrics: bool = Field(default=False)
    metrics_port: int = Field(default=9095)
    only_contextual: bool = Field(default=False)
    run_and_terminate: bool = Field(default=False)
    validate_before_import: bool = Field(default=False)
    queue_protocol: str = Field(default="amqp")
    queue_threshold: int = Field(default=500)

    send_to_queue: bool = Field(default=True)
    send_to_directory: bool = Field(default=False)
    send_to_directory_path: str | None = Field(default=None)
    send_to_directory_retention: int = Field(default=7)


class BaseConfig(BaseSettings, ABC):
    """
    Define a complete config for a connector with:
        - opencti: the config specific to OpenCTI
        - connector: the config specific to the `external-import` connectors
        - [custom_config]: (Optional) the config specific to the finale connector
    """

    opencti: _OpenCTIConfig
    connector: _ConnectorConfig

    # Setup model config and env vars parsing
    model_config = SettingsConfigDict(
        frozen=True,
        extra="allow",
        env_nested_delimiter="_",
        env_nested_max_split=1,
    )
    # Setup type of extra fields
    __pydantic_extra__: _ConfigBaseModel

    def __init__(self) -> None:
        """
        Wrap BaseConnectorConfig initialization to raise custom exception in case of error.
        """
        try:
            super().__init__()
        except Exception as e:
            raise ConfigRetrievalError("Invalid OpenCTI configuration.", e) from e

    @abstractmethod
    def _get_custom_config(self) -> tuple[str, _ConfigBaseModel]:
        """
        Retrieve config specific to the final connector.
        This function will be called during `model_post_init()`.
        Should return a tuple, e.g. `(name, config)`, where `name` is the name to assign as extra field
        and `config` is the object holding the custom config values.
        """
        pass

    def model_post_init(self, _) -> None:
        """
        Add custom config as extra field.
        """
        (custom_config_name, custom_config_data) = self._get_custom_config()
        self[custom_config_name] = custom_config_data

    def model_dump_pycti(self) -> dict:
        """
        Convert model into a valid dict for `pycti.OpenCTIConnectorHelper`.
        """
        return self.model_dump(mode="json", context={"mode": "pycti"})

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customise the sources of settings for the connector.

        This method is called by the Pydantic BaseSettings class to determine the order of sources

        The configuration come in this order either from:
            1. YAML file
            2. .env file
            3. Environment variables
            4. Default values
        """
        if Path(settings_cls.model_config["yaml_file"] or "").is_file():  # type: ignore
            return (YamlConfigSettingsSource(settings_cls),)
        if Path(settings_cls.model_config["env_file"] or "").is_file():  # type: ignore
            return (dotenv_settings,)
        return (env_settings,)
