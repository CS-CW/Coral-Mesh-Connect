import abc
import enum

from typing import Optional


class Codable(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def decode(self, data: Optional[dict] = None):
        pass

    @abc.abstractmethod
    def encode(self) -> Optional[dict]:
        pass


class StrEnum(str, enum.Enum):
    pass
