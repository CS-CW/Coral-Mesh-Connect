from typing import Optional
from mesh.cdb.node import heartbeatSub as cdb
from mesh.model import Codable
from mesh.model.address import Address


class HeartbeatSubscription(Codable):
    def __init__(self, subscribe: Optional[dict] = None):
        self.source = Address(hex_='0')
        self.destination = Address(hex_='0')
        if subscribe:
            self.decode(subscribe)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.SOURCE:
                self.source = Address(hex_=v)
            elif k == cdb.DESTINATION:
                self.destination = Address(hex_=v)
            else:
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.SOURCE] = self.source.hex
        data[cdb.DESTINATION] = self.destination.hex
        return data
