from typing import Optional
from mesh.cdb.node import heartbeatPub as cdb
from mesh.model import Codable
from mesh.model.address import Address


class HeartbeatPublication(Codable):
    def __init__(self, publish: Optional[dict] = None):
        self.address = Address(hex_='0')
        self.index = 0
        self.features = []
        self.period = 0
        self.ttl = 0
        if publish:
            self.decode(publish)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.ADDRESS:
                self.address = Address(hex_=v)
            elif k == cdb.INDEX:
                self.index = v
            elif k == cdb.FEATURES:
                self.features = v
            elif k == cdb.TTL:
                self.ttl = v
            elif k == cdb.PERIOD:
                self.period = v
            else:
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.ADDRESS] = self.address.hex
        data[cdb.INDEX] = self.index
        data[cdb.FEATURES] = [feature for feature in self.features]
        data[cdb.TTL] = self.ttl
        data[cdb.PERIOD] = self.period
        return data
