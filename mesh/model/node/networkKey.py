from typing import Optional
from mesh.model import Codable


class NetworkKey(Codable):
    def __init__(self, index: Optional[int] = 0, net_key: Optional[dict] = None):
        self.index = index
        self.updated = False
        if net_key:
            self.decode(net_key)

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
