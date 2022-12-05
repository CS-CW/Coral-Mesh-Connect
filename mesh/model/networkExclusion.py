from typing import Optional
from mesh.model import Codable
from mesh.cdb import networkExclusion as cdb


class NetworkExclusion(Codable):
    def __init__(self, network_exclusion: Optional[dict] = None):
        self.addresses = []
        self.ivIndex = 0
        if network_exclusion:
            self.decode(network_exclusion)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.ADDRESSES:
                self.addresses = [int(address, 16) for address in v]
            elif k == cdb.IV_INDEX:
                self.ivIndex = int(v)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.ADDRESSES] = ['%04X' % address for address in self.addresses]
        data[cdb.IV_INDEX] = self.ivIndex
        return data
