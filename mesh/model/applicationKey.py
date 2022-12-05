import uuid

from typing import Optional
from mesh.model import Codable
from mesh.cdb import appKeys as cdb


class ApplicationKey(Codable):
    def __init__(self, index: Optional[int] = 0, app_key: Optional[dict] = None):
        self.name = 'App Key'
        self.index = index
        self._key = uuid.uuid4()
        self._oldKey = None
        self.boundNetKey = 0
        if app_key:
            self.decode(app_key)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v
            elif k == cdb.INDEX:
                self.index = int(v)
            elif k == cdb.KEY:
                self._key = uuid.UUID(v)
            elif k == cdb.OLD_KEY:
                self._oldKey = uuid.UUID(v)
            elif k == cdb.BOUND_NET_KEY:
                self.boundNetKey = int(v)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.INDEX] = self.index
        data[cdb.KEY] = self._key.hex.upper()
        if self._oldKey:
            data[cdb.OLD_KEY] = self._oldKey.hex.upper()
        data[cdb.BOUND_NET_KEY] = self.boundNetKey
        return data

    @property
    def key(self):
        return self._key

    @property
    def oldKey(self):
        return self._oldKey
