from abc import ABC, abstractmethod
from typing import Any, Iterable

from connectors_sdk.octi_entities import OrganizationAuthor, TLPMarking
from connectors_sdk.octi_entities.common import BaseEntity as OCTIBaseEntity


class BaseConverter(ABC):
    """
    Define a set of methods to convert external data into OCTI models.
    """

    @property
    @abstractmethod
    def author(self) -> OrganizationAuthor:
        """
        Define an author representing the connector's external service.
        This author SHOULD be used as the author of created OCTI entities.
        """

    @property
    @abstractmethod
    def tlp_marking(self) -> TLPMarking:
        """
        Define a TLP Marking to apply to created OCTI entities.
        """

    @abstractmethod
    def convert(self, object: Any) -> Iterable[OCTIBaseEntity]:
        """Convert external data into OCTI entities."""
