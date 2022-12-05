from typing import Optional
from mesh.model import Codable
from mesh.cdb.node.element import model as cdb
from mesh.model.meshAddress import MeshAddress


class Model(Codable):

    def __init__(self, model: Optional[dict] = None):
        self._modelId = 0
        self.publish = None
        self.bind = []
        self.subscribe = []
        if model:
            self.decode(model)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k == cdb.MODEL_ID:
                self._modelId = int(v, 16)

            elif k == cdb.PUBLISH:
                from mesh.model.node.element.model.publish import Publication
                self.publish = Publication(publish=v)

            elif k == cdb.BIND:
                self.bind = [index for index in v]

            elif k == cdb.SUBSCRIBE:
                self.subscribe = [MeshAddress(hex_=address) for address in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.MODEL_ID] = '%04X' % self._modelId if self._modelId <= 65535 else '%08X' % self._modelId
        if self.publish:
            data[cdb.PUBLISH] = self.publish.encode()
        data[cdb.BIND] = [index for index in self.bind]
        data[cdb.SUBSCRIBE] = [address.hex for address in self.subscribe]
        return data

    @property
    def modelId(self):
        return self._modelId
