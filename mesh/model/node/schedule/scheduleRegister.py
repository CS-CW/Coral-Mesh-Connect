from typing import Optional
from mesh.model import Codable
from mesh.cdb.node.schedule import scheduleRegister as cdb


class ScheduleRegister(Codable):
    def __init__(self, register: Optional[dict] = None):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.dayOfWeek = 0
        self.action = 0
        self.transition = 0
        self.sceneNumber = 0
        if register:
            self.decode(register)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.SCENE_NUMBER:
                self.sceneNumber = int(v, 16)
            else:
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        for k, v in self.__dict__.items():
            if k == cdb.SCENE_NUMBER:
                data[k] = '%04X' % self.sceneNumber
            else:
                data[k] = v
        return data
