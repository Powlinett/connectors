from functools import cached_property

from connectors_sdk.external_import import BaseConnector
from connectors_sdk.octi_entities.common import BaseEntity as OCTIBaseEntity
from client import FakeClient
from converter import OCTIConverter
from config import TemplateConfig


class TemplateConnector(BaseConnector):
    """
    The main class for the Template connector.
    It handles the initialization of the connector, the collection of data,
    and the conversion of that data into OpenCTI format.

    The following variables are accessible in the class:
    - helper: instance of OpenCTIConnectorHelper
    - config: instance of BaseConfig subclass

    The following methods MUST be implemented:
    - process_data: should return OCTI entities (from `connectors_sdk.octi_entities`)

    Any additional implementation is optional and depending on each use case.
    """

    config: TemplateConfig  # overwrite `BaseConfig` type hint (for typechecking only)

    # =============================
    # === Change the code below ===
    # =============================

    @cached_property
    def client(self) -> FakeClient:
        """
        Instantiate a client for the external source(s).
        """
        return FakeClient()

    @cached_property
    def converter(self) -> OCTIConverter:
        """
        Instantiate a converter to process data from external source(s).
        """
        return OCTIConverter(config=self.config)

    # =============================
    # === Change the code above ===
    # =============================

    def process_data(self) -> list[OCTIBaseEntity]:
        """
        Collect and convert data from external source(s) into OCTI entities.
        This method MUST be implemented by each connector and return OCTI entities.
        """

        octi_objects: list[OCTIBaseEntity] = []

        # =============================
        # === Change the code below ===
        # =============================

        reports = self.client.fetch_reports(
            since=self.config.template.import_start_date
        )
        for report in reports:
            extracted_octi_objects = self.converter.convert_report(report)
            octi_objects.extend(extracted_octi_objects)

        # =============================
        # === Change the code above ===
        # =============================

        return octi_objects
