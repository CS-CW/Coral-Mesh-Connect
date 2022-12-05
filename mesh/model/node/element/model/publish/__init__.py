from typing import Optional
from mesh.model import Codable
from mesh.cdb.node.element.model import publish as cdb
from mesh.model.meshAddress import MeshAddress
from mesh.model.node.element.model.publish.period import Period
from mesh.model.node.element.model.publish.retransmit import Retransmit


class Publication(Codable):

    def __init__(self, publish: Optional[dict] = None):
        self.address = MeshAddress()
        self.index = 0
        self.ttl = 0
        self.period = Period()
        self.retransmit = Retransmit()
        self.credentials = 0
        if publish:
            self.decode(publish)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k == cdb.ADDRESS:
                self.address = MeshAddress(hex_=v)

            elif k == cdb.INDEX:
                self.index = v

            elif k == cdb.TTL:
                self.ttl = v

            elif k == cdb.PERIOD:
                self.period = Period(period=v)

            elif k == cdb.RETRANSMIT:
                self.retransmit = Retransmit(retransmit=v)

            elif k == cdb.CREDENTIALS:
                self.credentials = v

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.ADDRESS] = self.address.hex
        data[cdb.INDEX] = self.index
        data[cdb.TTL] = self.ttl
        data[cdb.PERIOD] = self.period.encode()
        data[cdb.RETRANSMIT] = self.retransmit.encode()
        data[cdb.CREDENTIALS] = self.credentials
        return data
