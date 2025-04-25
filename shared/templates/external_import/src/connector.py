from connectors_sdk.external_import import BaseConnector
from connectors_sdk.octi_entities.common import BaseEntity as OCTIBaseEntity


class TemplateConnector(BaseConnector):
    """
    The main class for the Template connector.
    It handles the initialization of the connector, the collection of data,
    and the conversion of that data into OpenCTI format.

    The following variables are accessible in the class:
    - helper: instance of OpenCTIConnectorHelper
    - config: instance of BaseConfig subclass
    - collector: instance of BaseCollector subclass
    - converter: instance of BaseConverter subclass
    """

    def process_data(self) -> list[OCTIBaseEntity]:
        """
        Collect and convert data from external source(s) into STIX objects.
        This method MUST be implemented by each connector and return a list of STIX objects.
        """

        octi_objects: list[OCTIBaseEntity] = []

        # ===========================
        # === Add your code below ===
        # ===========================

        # For example:
        reports = self.collector.collect()
        for report in reports:
            extracted_octi_objects = self.converter.convert(report)
            octi_objects.extend(extracted_octi_objects)

        # ===========================
        # === Add your code above ===
        # ===========================

        return octi_objects
