from typing import Optional
from mesh.cdb.node import schedule as cdb
from mesh.model import Codable
from mesh.model.node.schedule.scheduleRegister import ScheduleRegister


class Schedule(Codable):
    def __init__(self, schedule: Optional[dict] = None):
        self.name = 'Schedule'
        self.element = 0
        self.index = 0
        self.scheduleRegister = ScheduleRegister()
        if schedule:
            self.decode(schedule)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.SCHEDULE_REGISTER:
                self.scheduleRegister = ScheduleRegister(register=v)
            else:
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        for k, v in self.__dict__.items():
            if k == cdb.SCHEDULE_REGISTER:
                data[k] = self.scheduleRegister.encode()
            else:
                data[k] = v
        return data
