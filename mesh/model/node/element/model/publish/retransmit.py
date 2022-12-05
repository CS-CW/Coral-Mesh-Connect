from typing import Optional
from mesh.model import Codable


class Retransmit(Codable):

    def __init__(self, retransmit: Optional[dict] = None):
        self.count = 0
        self.interval = 0
        if retransmit:
            self.decode(retransmit)

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
