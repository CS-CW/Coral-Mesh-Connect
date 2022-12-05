import enum
from typing import Optional
from mesh.model import Codable


class FeatureState(int, enum.Enum):
    NOT_ENABLED = 0
    ENABLED = 1
    NOT_SUPPORTED = 2


class Features(Codable):
    def __init__(self, features: Optional[dict] = None):
        self.relay = FeatureState.NOT_SUPPORTED
        self.proxy = FeatureState.NOT_SUPPORTED
        self.friend = FeatureState.NOT_SUPPORTED
        self.lowPower = FeatureState.NOT_SUPPORTED
        if features:
            self.decode(features)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        for k, v in self.__dict__.items():
            data[k] = v
        return data
