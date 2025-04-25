import sys
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from connectors_sdk.external_import.base_config import BaseConfig
from connectors_sdk.octi_entities.common import BaseEntity
from pycti import OpenCTIConnectorHelper  # type: ignore[import-untyped]  # pycti does not provide stubs


class BaseConnector(ABC):
    """
    Specifications of the external import connector

    This class encapsulates the main actions, expected to be run by any external import connector.
    Note that the attributes defined below will be complemented per each connector type.
    This type of connector aim to fetch external data to create STIX bundle and send it in a RabbitMQ queue.
    The STIX bundle in the queue will be processed by the workers.
    This type of connector uses the basic methods of the helper.

    ---

    Attributes
        - `helper (OpenCTIConnectorHelper(config))`:
            This is the helper to use.
            ALL connectors have to instantiate the connector helper with configurations.
            Doing this will do a lot of operations behind the scene.
        - `config (BaseConfig)`:
            This is the connector configuration.

    ---

    Best practices
        - `self.helper.api.work.initiate_work(...)` is used to initiate a new work
        - `self.helper.schedule_process()` is used to encapsulate the main process in a scheduler
        - `self.helper.connector_logger.[info/debug/warning/error]` is used when logging a message
        - `self.helper.stix2_create_bundle(stix_objects)` is used when creating a bundle
        - `self.helper.send_stix2_bundle(stix_objects_bundle)` is used to send the bundle to RabbitMQ
        - `self.helper.set_state()` is used to set state

    """

    def __init__(self, config: BaseConfig) -> None:
        self.config = config
        self.helper = OpenCTIConnectorHelper(config.model_dump_pycti())

    @abstractmethod
    def process_data(self) -> Iterable[BaseEntity]:
        """
        Collect and process the source of CTI.
        This method MUST be implemented by each connector and return OCTI entities.
        """

    def get_state(self) -> dict[str, Any]:
        current_state = self.helper.get_state() or {}
        self.helper.connector_logger.info(
            f"Connector current state:", {"state": current_state}
        )
        return current_state

    def update_state(self, state: dict) -> None:
        current_state = self.get_state()
        current_state.update(state)
        self.helper.set_state(state=current_state)
        self.helper.connector_logger.info(
            f"Connector updated state:", {"state": current_state}
        )

    def initiate_work(self) -> str:
        return self.helper.api.work.initiate_work(
            connector_id=self.helper.connect_id,
            friendly_name=self.helper.connect_name,
        )

    def finalize_work(self, work_id: str, message: str, in_error: bool = False) -> None:
        self.helper.api.work.to_processed(
            work_id=work_id,
            message=message,
            in_error=in_error,
        )

    def create_and_send_bundles(
        self, work_id: str, octi_objects: list[BaseEntity]
    ) -> None:
        if not octi_objects:
            self.helper.connector_logger.info("No STIX objects to process.")
            return

        # TODO: Ensure consistent bundle (with valid Author(s) and TLPMarking(s))
        stix_objects = [item.to_stix2_object() for item in octi_objects]

        bundle = self.helper.stix2_create_bundle(items=stix_objects)
        bundles_sent = self.helper.send_stix2_bundle(
            bundle=bundle,
            work_id=work_id,
            cleanup_inconsistent_bundle=True,
        )
        self.helper.connector_logger.info(
            f"Sent STIX objects bundles to OpenCTI.",
            {"bundles_count": len(bundles_sent)},
        )

    def process(self) -> str | None:
        error_flag = False
        meta = {"connector_name": self.helper.connect_name}

        try:
            self.helper.connector_logger.info("Running connector...", meta=meta)
            run_time = datetime.now(tz=timezone.utc)

            work_id = self.initiate_work()

            octi_objects = self.process_data()
            self.create_and_send_bundles(work_id, octi_objects)

            self.update_state({"last_run": run_time.isoformat(timespec="seconds")})

        except (KeyboardInterrupt, SystemExit):
            self.helper.connector_logger.info("Connector stopped by user.", meta=meta)
            sys.exit(0)
        except Exception as e:
            error_flag = True
            traceback.print_exc()
            self.helper.connector_logger.error(f"Unexpected error: {e}", meta=meta)
            return "Unexpected error. See connector logs for details."
        finally:
            self.finalize_work(
                work_id=work_id,
                message="Connector successfully run",
                in_error=error_flag,
            )

        return None

    def run(self, duration_period: timedelta) -> None:
        self.helper.connector_logger.info("Starting connector...")
        self.helper.schedule_process(
            message_callback=self.process,
            duration_period=duration_period.total_seconds(),
        )
