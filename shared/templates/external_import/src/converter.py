"""
Implement methods to convert data collected from an external source into OCTI entities.
The code below is provided as example only, it MUST be removed before merge.
"""

from functools import cached_property
from typing import Iterable

from connectors_sdk.octi_entities import (
    Indicator,
    OrganizationAuthor,
    Report,
    TLPMarking,
)
from connectors_sdk.octi_entities.common import BaseEntity as OCTIBaseEntity
from connectors_sdk.octi_entities.enum import OrganizationType
from config import TemplateConfig
from client import FakeReport


# =============================
# === Change the code below ===
# =============================


class OCTIConverter:
    def __init__(self, config: TemplateConfig) -> None:
        self.config = config

    @cached_property
    def author(self) -> OrganizationAuthor:
        """
        Define an author representing the connector's external service.
        This author SHOULD be used as the author of created OCTI entities.
        """
        return OrganizationAuthor(
            name="Template Connector name",
            description="A useful description of the template connector",
            contact_information="https://www.example.com/contact",
            organization_type=OrganizationType.VENDOR,
            reliability=None,
            aliases=None,
            author=None,
            markings=None,
            external_references=None,
        )

    @cached_property
    def tlp_marking(self) -> TLPMarking:
        """
        Define a TLP Marking to apply to created OCTI entities.
        """
        return TLPMarking(level=self.config.template.tlp_level)

    def convert_report(self, collected_report: FakeReport) -> list[OCTIBaseEntity]:
        """
        Convert the collected data into OCTI entities.
        """
        octi_entities = []

        report_indicators = []
        for ioc in collected_report.iocs:
            indicator = Indicator(
                name=ioc.value,
                pattern=f"[{ioc.type}:value='{ioc.value}']",
                pattern_type="stix",
                observable_type=ioc.type.capitalize(),
                author=self.author,
                markings=[self.tlp_marking],
            )
            report_indicators.append(indicator)
            octi_entities.append(indicator)

        report = Report(
            name=collected_report.title,
            publication_date=collected_report.published_at,
            objects=report_indicators,
            author=self.author,
            markings=[self.tlp_marking],
        )
        octi_entities.append(report)

        return octi_entities


# =============================
# === Change the code above ===
# =============================
