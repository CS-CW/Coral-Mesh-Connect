from typing import Optional
from mesh.model import Codable
from mesh.cdb.node import element as cdb


class Element(Codable):

    def __init__(self, element: Optional[dict] = None):
        self.name = 'Element'
        self.index = 0
        self.location = 0
        self.models = []
        if element:
            self.decode(element)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v

            elif k == cdb.INDEX:
                self.index = v

            elif k == cdb.LOCATION:
                self.location = int(v, 16)

            elif k == cdb.MODELS:
                from mesh.model.node.element.model import Model
                self.models = [Model(model=m) for m in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.INDEX] = self.index
        data[cdb.LOCATION] = '%04X' % self.location
        data[cdb.MODELS] = [model.encode() for model in self.models]
        return data
