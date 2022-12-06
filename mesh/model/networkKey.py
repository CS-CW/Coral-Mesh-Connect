import uuid
import datetime
import dateutil.parser

from typing import Optional
from mesh.model import Codable
from mesh.model.security import Security
from mesh.cdb import netKey as cdb


class NetworkKey(Codable):
    def __init__(self, index: Optional[int] = 0, net_key: Optional[dict] = None):
        self.name = 'Mesh Net Key'
        self.index = index
        self.key = uuid.uuid4()
        self.oldKey = None
        self.phase = 1
        self.minSecurity = Security.INSECURE
        self.timestamp = datetime.datetime.now()
        if net_key:
            self.decode(net_key)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.NAME:
                self.name = v
            elif k == cdb.INDEX:
                self.index = v
            elif k == cdb.KEY:
                self.key = uuid.UUID(v)
            elif k == cdb.OLD_KEY:
                self.oldKey = uuid.UUID(v)
            elif k == cdb.PHASE:
                self.phase = v
            elif k == cdb.MIN_SECURITY:
                self.minSecurity = v
            elif k == cdb.TIMESTAMP:
                # be able to parse for RFC 3339 and ISO 8601
                self.timestamp = dateutil.parser.isoparse(v)
            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.NAME] = self.name
        data[cdb.INDEX] = self.index
        data[cdb.KEY] = self.key.hex.upper()
        if self.oldKey:
            data[cdb.OLD_KEY] = self.oldKey.hex.upper()
        data[cdb.PHASE] = self.phase
        data[cdb.MIN_SECURITY] = self.minSecurity
        data[cdb.TIMESTAMP] = self.timestamp.isoformat()
        return data
