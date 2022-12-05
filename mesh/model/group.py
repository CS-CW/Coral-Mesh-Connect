from typing import Optional
from mesh.model import Codable
from mesh.cdb import group as cdb
from mesh.model.meshAddress import MeshAddress


class Group(Codable):
    def __init__(self, address: Optional[str] = 'C000', group: Optional[dict] = None):
        self.name = 'Group'
        self.address = MeshAddress(hex_=address)
        self.parentAddress = MeshAddress(hex_='0')
        if group:
            self.decode(group)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v
            elif k == cdb.ADDRESS:
                self.address = MeshAddress(hex_=v)
            elif k == cdb.PARENT_ADDRESS:
                self.parentAddress = MeshAddress(hex_=v)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.ADDRESS] = self.address.hex
        data[cdb.PARENT_ADDRESS] = self.parentAddress.hex
        return data
