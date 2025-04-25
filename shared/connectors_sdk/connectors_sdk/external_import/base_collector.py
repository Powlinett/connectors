from abc import ABC, abstractmethod
from typing import Any, Iterable


class BaseCollector(ABC):
    """
    Define a set of methods to collect data from external source(s).
    """

    @abstractmethod
    def collect(self) -> Iterable[Any]:
        """Collect data from a source."""
