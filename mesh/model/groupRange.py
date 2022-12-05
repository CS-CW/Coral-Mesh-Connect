from typing import Optional
from mesh.model import Codable
from mesh.cdb import groupRange as cdb


class GroupRange(Codable):
    def __init__(self, range_: Optional[dict] = None):
        self.highAddress = 0xFFFF
        self.lowAddress = 0xC000
        if range_:
            self.decode(range_)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.HIGH_ADDRESS:
                self.highAddress = int(v, 16)
            elif k == cdb.LOW_ADDRESS:
                self.lowAddress = int(v, 16)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.HIGH_ADDRESS] = '%04X' % self.highAddress
        data[cdb.LOW_ADDRESS] = '%04X' % self.lowAddress
        return data
