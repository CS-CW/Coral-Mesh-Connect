import uuid

from typing import Optional
from mesh.model import Codable
from mesh.cdb import provisioner as cdb


class Provisioner(Codable):
    def __init__(self, provisioner: Optional[dict] = None):
        self.provisionerName = 'Provisioner'
        self._uuid = uuid.uuid4()
        self.allocatedGroupRange = []
        self.allocatedUnicastRange = []
        self.allocatedSceneRange = []
        if provisioner:
            self.decode(provisioner)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.PROVISIONER_NAME:
                self.provisionerName = v

            elif k == cdb.UUID:
                self._uuid = uuid.UUID(v)

            elif k == cdb.ALLOCATED_GROUP_RANGE:
                from mesh.model.groupRange import GroupRange
                self.allocatedGroupRange = [GroupRange(range_) for range_ in v]

            elif k == cdb.ALLOCATED_UNICAST_RANGE:
                from mesh.model.unicastRange import UnicastRange
                self.allocatedUnicastRange = [UnicastRange(range_) for range_ in v]

            elif k == cdb.ALLOCATED_SCENE_RANGE:
                from mesh.model.sceneRange import SceneRange
                self.allocatedSceneRange = [SceneRange(range_) for range_ in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.PROVISIONER_NAME] = self.provisionerName
        data[cdb.UUID] = str(self._uuid).upper()
        data[cdb.ALLOCATED_GROUP_RANGE] = [range_.encode() for range_ in self.allocatedGroupRange]
        data[cdb.ALLOCATED_UNICAST_RANGE] = [range_.encode() for range_ in self.allocatedUnicastRange]
        data[cdb.ALLOCATED_SCENE_RANGE] = [range_.encode() for range_ in self.allocatedSceneRange]
        return data

    @property
    def uuid(self):
        return self._uuid
