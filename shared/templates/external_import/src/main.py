import traceback

from pycti import OpenCTIConnectorHelper
from collector import TemplateCollector
from config import TemplateConfig
from connector import TemplateConnector
from converter import TemplateConverter


if __name__ == "__main__":
    try:
        config = TemplateConfig()
        helper = OpenCTIConnectorHelper(config.model_dump_pycti())

        collector = TemplateCollector()
        converter = TemplateConverter(config=config)

        connector = TemplateConnector(
            helper=helper,
            config=config,
            collector=collector,
            converter=converter,
        )
        connector.run(duration_period=config.connector.duration_period)
    except Exception as e:
        traceback.print_exc()
        exit(1)
