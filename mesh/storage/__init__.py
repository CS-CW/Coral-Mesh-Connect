import abc

from typing import Optional


class Storage(metaclass=abc.ABCMeta):
    """
    Abstract class for adapting other databases in the future
    """
    @abc.abstractmethod
    def load(self) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def swap(self, profile: str) -> Optional[dict]:
        pass

    @abc.abstractmethod
    def save(self, data: dict):
        pass
