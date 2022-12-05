from typing import Optional
from mesh.model import Codable


class Period(Codable):

    def __init__(self, period: Optional[dict] = None):
        self.numberOfSteps = 0
        self.resolution = 0
        if period:
            self.decode(period)

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
