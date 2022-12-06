from typing import Optional
from mesh.model import Codable


class LcProperty(Codable):
    def __init__(self, property_: Optional[dict] = None):
        self.occupancyDelayTime = 0
        self.transitionToRun = 0
        self.transitionToProlong = 0
        self.runTime = 0
        self.prolongTime = 0
        self.transitionToStandbyAuto = 0
        self.transitionToStandbyManual = 0
        self.runLevel = 0
        self.prolongLevel = 0
        self.standbyLevel = 0
        self.runLuxLevel = 0
        self.prolongLuxLevel = 0
        self.standbyLuxLevel = 0
        self.kiu = 250
        self.kid = 250
        self.kpu = 80
        self.kpd = 80
        self.accuracy = 4
        if property_:
            self.decode(property_)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        for k, v in self.__dict__.items():
            data[k] = v
        return data
