from typing import Optional
from mesh.model import Codable


class Fov(Codable):
    def __init__(self, fov: Optional[dict] = None):
        self.degree = 0
        self.distance = 0
        if fov:
            self.decode(fov)

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
