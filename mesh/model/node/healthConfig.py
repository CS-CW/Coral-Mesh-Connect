from typing import Optional
from mesh.model import Codable


class HealthConfig(Codable):
    def __init__(self, health_config: Optional[dict] = None):
        self.fastPeriod = 0
        self.attention = 0
        if health_config:
            self.decode(health_config)

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
