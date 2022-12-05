from typing import Optional
from mesh.model import Codable
from mesh.cdb import sceneRange as cdb


class SceneRange(Codable):
    def __init__(self, range_: dict = None):
        self.firstScene = 0x0000
        self.lastScene = 0xFFFF
        if range_:
            self.decode(range_)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.FIRST_SCENE:
                self.firstScene = int(v, 16)
            elif k == cdb.LAST_SCENE:
                self.lastScene = int(v, 16)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.FIRST_SCENE] = '%04X' % self.firstScene
        data[cdb.LAST_SCENE] = '%04X' % self.lastScene
        return data
