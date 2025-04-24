from abc import ABC, abstractmethod
from typing import Any, Iterable

from octi_entities import OrganizationAuthor, TLPMarking
from octi_entities.common import BaseEntity as OCTIBaseEntity


class BaseConverter(ABC):
    """
    Define a set of methods to convert external data into OCTI models.
    """

    @abstractmethod
    @property
    def author(self) -> OrganizationAuthor:
        """
        Define an author representing the connector's external service.
        This author SHOULD be used as the author of created OCTI entities.
        """
        pass

    @abstractmethod
    @property
    def tlp_marking(self) -> TLPMarking:
        """
        Define a TLP Marking to apply to created OCTI entities.
        """
        pass

    @abstractmethod
    def convert(self, object: Any) -> Iterable[OCTIBaseEntity]:
        """Convert external data into OCTI entities."""
        pass
