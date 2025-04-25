import traceback

from config import TemplateConfig
from connector import TemplateConnector


if __name__ == "__main__":
    try:
        config = TemplateConfig()
        connector = TemplateConnector(config=config)
        connector.run(duration_period=config.connector.duration_period)
    except Exception as e:
        traceback.print_exc()
        exit(1)
