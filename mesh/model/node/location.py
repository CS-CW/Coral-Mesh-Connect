import enum
import math
from typing import Optional
from mesh.model import Codable
from mesh.cdb.node import location as cdb
from util.bits import twos_complement

"""
 World Geodetic System
"""


class WGSType(str, enum.Enum):
    NORTH = 'North'
    EAST = 'East'

    def degrees_range(self) -> (float, float):
        if self == WGSType.NORTH:
            return -90, 90
        if self == WGSType.EAST:
            return -180, 180


class WorldGeodeticSystem:

    NOT_CONFIGURED = 0x00000080

    @staticmethod
    def to_degree(value: int, type_: WGSType) -> Optional[float]:
        if value == WorldGeodeticSystem.NOT_CONFIGURED:
            return None
        _, high = type_.degrees_range()
        return (float(value) / (pow(2, 31) - 1)) * high

    @staticmethod
    def to_value(degrees: float, type_: WGSType) -> int:
        _, high = type_.degrees_range()
        return int(math.floor((float(degrees/high)*(pow(2, 31)-1))))

    def __init__(self, type_: WGSType,  hex_: Optional[str] = None):
        self._value = WorldGeodeticSystem.NOT_CONFIGURED
        self._type = type_
        if hex_:
            try:
                self._value = twos_complement(hex_, 32)
            except Exception as e:
                print('WorldGeodeticSystem init with', hex_, type_, e)

    def set(self, value: int):
        self._value = value

    @property
    def hex(self):
        return '%08X' % (self._value & 0xFFFFFFFF)


"""
 Altitude
"""


class AltitudeType(str, enum.Enum):
    GLOBAL = 'Global'
    LOCAL = 'Local'

    @property
    def unit(self) -> str:
        if self == AltitudeType.GLOBAL:
            return 'Meters'
        if self == AltitudeType.LOCAL:
            return 'Decimeters'


class Altitude:

    NOT_CONFIGURED = 0xFF7F

    GREATER_OR_EQUAL_32766 = 0xFE7F

    def __init__(self, type_: AltitudeType, hex_: Optional[str] = None):
        self._value = Altitude.NOT_CONFIGURED
        self._type = type_
        if hex_:
            try:
                self._value = twos_complement(hex_, 16)
            except Exception as e:
                print('Altitude init with', hex_, type_, e)

    def set(self, value: int):
        self._value = value

    @property
    def hex(self):
        return '%04X' % (self._value & 0xFFFF)


"""
 Local Coordinate System
"""


class LCSType(str, enum.Enum):
    NORTH = 'North'
    EAST = 'East'


class LocalCoordinateSystem:

    NOT_CONFIGURED = 0x0080

    UNIT = 'Decimeters'

    def __init__(self, type_: LCSType, hex_: Optional[str] = None):
        self._value = LocalCoordinateSystem.NOT_CONFIGURED
        self._type = type_
        if hex_:
            try:
                self._value = twos_complement(hex_, 16)
            except Exception as e:
                print('LocalCoordinateSystem init with', hex_, type_, e)

    def set(self, value: int):
        self._value = value

    @property
    def hex(self):
        return '%04X' % (self._value & 0xFFFF)


"""
 Floor Number
"""


class FloorNumber:

    NOT_CONFIGURED = 0xFF

    FLOOR_FIRST = 0xFE

    FLOOR_ZERO = 0xFE

    GREATER_OR_EQUAL_232 = 0xFC

    LESS_OR_EQUAL_MINUS_20 = 0x00

    def __init__(self, hex_: Optional[str] = None):
        self._value = FloorNumber.NOT_CONFIGURED
        if hex_:
            try:
                self._value = int(hex_, 16)
            except Exception as e:
                print('FloorNumber init with', hex_, e)

    def set(self, number_: int):
        if number_ >= FloorNumber.NOT_CONFIGURED:
            self._value = FloorNumber.NOT_CONFIGURED
        elif number_ == FloorNumber.FLOOR_FIRST:
            self._value = FloorNumber.FLOOR_FIRST
        elif number_ == FloorNumber.FLOOR_ZERO:
            self._value = FloorNumber.FLOOR_ZERO
        elif number_ == FloorNumber.GREATER_OR_EQUAL_232:
            self._value = FloorNumber.GREATER_OR_EQUAL_232
        elif number_ <= FloorNumber.LESS_OR_EQUAL_MINUS_20:
            self._value = FloorNumber.LESS_OR_EQUAL_MINUS_20
        else:
            self._value = number_ + 20

    @property
    def number(self) -> Optional[int]:
        if self._value == FloorNumber.NOT_CONFIGURED:
            return None
        elif self._value == FloorNumber.FLOOR_FIRST:
            return 1
        elif self._value == FloorNumber.FLOOR_ZERO:
            return 0
        elif self._value == FloorNumber.GREATER_OR_EQUAL_232:
            return 232
        elif self._value == FloorNumber.LESS_OR_EQUAL_MINUS_20:
            return -20
        else:
            return self._value - 20

    @property
    def hex(self):
        return '%02X' % self._value


"""
 Uncertainty
"""


class Uncertainty:
    def __init__(self, hex_: Optional[str] = None):
        self.stationary = True
        self.update_time = 0.0
        self.precision = 0.0
        self._value = 0

        if hex_:
            try:
                self._value = int(hex_, 16)
                self.stationary = (self._value & 0x0001) == 0x0000
                tmp = self._value >> 8
                self.updateTime = pow(2, float(tmp & 0b1111) - 3)
                tmp = tmp >> 4
                self.precision = pow(2, float(tmp) - 3)
            except Exception as e:
                print('Uncertainty init with', hex_, e)

    def set(self, stationary: bool, update_time: float, precision: float):
        self.stationary = stationary
        self.update_time = update_time
        self.precision = precision
        precision_y = math.log2(precision)
        if math.isfinite(precision_y) or math.isnan(precision_y):
            precision_y = 0
        update_time_x = math.log2(update_time)
        if math.isfinite(update_time_x) or math.isnan(update_time_x):
            update_time_x = 0
        self._value = int(precision_y + 3) << 12 | int(update_time_x + 3) << 8 | int(0x0000 if stationary else 0x0001)

    @property
    def hex(self):
        return '%04X' % self._value


"""
 Location
"""


class Location(Codable):
    def __init__(self, location: Optional[dict] = None):
        self.globalLatitude = WorldGeodeticSystem(type_=WGSType.NORTH)
        self.globalLongitude = WorldGeodeticSystem(type_=WGSType.EAST)
        self.globalAltitude = Altitude(type_=AltitudeType.GLOBAL)
        self.localNorth = LocalCoordinateSystem(type_=LCSType.NORTH)
        self.localEast = LocalCoordinateSystem(type_=LCSType.EAST)
        self.localAltitude = Altitude(type_=AltitudeType.LOCAL)
        self.floorNumber = FloorNumber()
        self.uncertainty = Uncertainty()
        if location:
            self.decode(location)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.GLOBAL_LATITUDE:
                self.globalLatitude = WorldGeodeticSystem(type_=WGSType.NORTH, hex_=v)

            elif k == cdb.GLOBAL_LONGITUDE:
                self.globalLongitude = WorldGeodeticSystem(type_=WGSType.EAST, hex_=v)

            elif k == cdb.GLOBAL_ALTITUDE:
                self.globalAltitude = Altitude(type_=AltitudeType.GLOBAL, hex_=v)

            elif k == cdb.LOCAL_NORTH:
                self.localNorth = LocalCoordinateSystem(type_=LCSType.NORTH, hex_=v)

            elif k == cdb.LOCAL_EAST:
                self.localEast = LocalCoordinateSystem(type_=LCSType.EAST, hex_=v)

            elif k == cdb.LOCAL_ALTITUDE:
                self.localAltitude = Altitude(type_=AltitudeType.LOCAL, hex_=v)

            elif k == cdb.FLOOR_NUMBER:
                self.floorNumber = FloorNumber(hex_=v)

            elif k == cdb.UNCERTAINTY:
                self.uncertainty = Uncertainty(hex_=v)

            else:
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.GLOBAL_LATITUDE] = self.globalLatitude.hex
        data[cdb.GLOBAL_LONGITUDE] = self.globalLongitude.hex
        data[cdb.GLOBAL_ALTITUDE] = self.globalAltitude.hex
        data[cdb.LOCAL_NORTH] = self.localNorth.hex
        data[cdb.LOCAL_EAST] = self.localEast.hex
        data[cdb.LOCAL_ALTITUDE] = self.localAltitude.hex
        data[cdb.GLOBAL_LATITUDE] = self.globalLatitude.hex
        data[cdb.FLOOR_NUMBER] = self.floorNumber.hex
        data[cdb.UNCERTAINTY] = self.uncertainty.hex
        return data
