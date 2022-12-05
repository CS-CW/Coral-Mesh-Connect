from typing import Optional
from mesh.model import Codable
from mesh.cdb import scene as cdb


class Scene(Codable):
    def __init__(self, number: Optional[int] = 0, scene: Optional[dict] = None):
        self.name = 'Scene'
        self.addresses = []
        self.number = number
        if scene:
            self.decode(scene)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v
            elif k == cdb.ADDRESSES:
                self.addresses = [int(address, 16) for address in v]
            elif k == cdb.NUMBER:
                self.number = int(v, 16)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.ADDRESSES] = ['%04X' % address for address in self.addresses]
        data[cdb.NUMBER] = '%04X' % self.number
        return data
