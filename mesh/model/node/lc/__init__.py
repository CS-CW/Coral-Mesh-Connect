from typing import Optional
from mesh.cdb.node import lc as cdb
from mesh.model import Codable
from mesh.model.node.lc.lcProperty import LcProperty


class LightLC(Codable):
    def __init__(self, lc: Optional[dict] = None):
        self.element = 0
        self.lcMode = 0
        self.lcOccupancyMode = 1
        self.lcProperty = LcProperty()
        if lc:
            self.decode(lc)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.LC_PROPERTY:
                self.lcProperty = LcProperty(property=v)
            else:
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        for k, v in self.__dict__.items():
            if k == cdb.LC_PROPERTY:
                data[k] = self.lcProperty.encode()
            else:
                data[k] = v
        return data
