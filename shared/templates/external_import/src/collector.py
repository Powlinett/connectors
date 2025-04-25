from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from connectors_sdk.external_import import BaseCollector


# These are for example purpose only, they MUST be removed before merge
@dataclass
class FakeIOC:
    type: str
    value: str


@dataclass
class FakeReport:
    title: str
    published_at: datetime
    iocs: list[FakeIOC]


class FakeClient:
    def fetch_reports(self) -> list[FakeReport]:
        return [
            FakeReport(
                title="Report1",
                published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                iocs=[FakeIOC(type="url", value="example1.com")],
            ),
            FakeReport(
                title="Report2",
                published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
                iocs=[FakeIOC(type="url", value="example2.com")],
            ),
        ]


class TemplateCollector(BaseCollector):
    """
    Implement methods to collect data from external source(s).
    """

    def __init__(self) -> None:
        self.client = FakeClient()

    def collect(self) -> Iterable[FakeReport]:
        """
        Collect data from external source(s).
        This method MUST be implemented by each connector.
        """

        # ===========================
        # === Add your code below ===
        # ===========================

        # For example:
        reports = self.client.fetch_reports()

        # ===========================
        # === Add your code above ===
        # ===========================

        return reports
