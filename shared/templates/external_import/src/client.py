"""
Implement methods to collect data from external source(s).
The following code is provided as example, it MUST be removed before merge.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


# =============================
# === Change the code below ===
# =============================


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
    def fetch_reports(self, since) -> list[FakeReport]:
        _ = since

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


# =============================
# === Change the code above ===
# =============================
