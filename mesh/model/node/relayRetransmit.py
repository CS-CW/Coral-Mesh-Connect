from typing import Optional
from mesh.model import Codable


class RelayRetransmit(Codable):
    def __init__(self, transmit: Optional[dict] = None):
        self.count = 0
        self.interval = 0
        if transmit:
            self.decode(transmit)

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
