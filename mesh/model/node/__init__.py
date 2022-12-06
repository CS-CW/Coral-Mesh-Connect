import uuid

from typing import Optional
from mesh.model import Codable
from mesh.model.address import Address
from mesh.model.security import Security
from mesh.model.node.features import Features
from mesh.model.node.networkTransmit import NetworkTransmit
from mesh.model.node.relayRetransmit import RelayRetransmit
from mesh.model.node.features import Features
from mesh.cdb import node as cdb


class Node(Codable):
    def __init__(self, node: Optional[dict] = None):
        self._uuid = uuid.uuid4()
        self.name = 'Node'
        self._deviceKey = None
        self.unicastAddress = Address(hex_='0')
        self.security = Security.SECURE
        self.cid = 0
        self.pid = 0
        self.vid = 0
        self.crpl = 0
        self.features = Features()
        self.elements = []
        self.configComplete = False
        self.netKeys = []
        self.appKeys = []
        self.networkTransmit = NetworkTransmit()
        self.relayTransmit = RelayRetransmit()
        self.secureNetworkBeacon = False
        self.defaultTTL = 3
        self.excluded = False
        self.heartbeatPub = None
        self.heartbeatSub = None
        self.schedules = []
        self.icon = None
        self.temporaryGuest = False
        self.virtualNode = False
        self.location = None
        self.lightControls = []
        self.healthConfig = None
        self.fov = None
        self.ipAddress = None
        self.modbusTcp = None
        self.qrCode = None
        if node:
            self.decode(node)

    def decode(self, data: Optional[dict] = None):
        if not data:
            return
        for k, v in data.items():
            if k == cdb.UUID:
                self._uuid = uuid.UUID(v)

            elif k == cdb.NAME:
                self.name = v

            elif k == cdb.DEVICE_KEY:
                self._deviceKey = uuid.UUID(v)

            elif k == cdb.UNICAST_ADDRESS:
                self.unicastAddress = Address(hex_=v)

            elif k == cdb.SECURITY:
                self.security = v

            elif k == cdb.CID:
                self.cid = int(v, 16)

            elif k == cdb.PID:
                self.pid = int(v, 16)

            elif k == cdb.VID:
                self.vid = int(v, 16)

            elif k == cdb.CRPL:
                self.crpl = int(v, 16)

            elif k == cdb.FEATURES:
                self.features = Features(features=v)

            elif k == cdb.ELEMENTS:
                from mesh.model.node.element import Element
                self.elements = [Element(element=e) for e in v]

            elif k == cdb.CONFIG_COMPLETE:
                self.configComplete = v

            elif k == cdb.NET_KEYS:
                from mesh.model.node.networkKey import NetworkKey
                self.netKeys = [NetworkKey(net_key=n) for n in v]

            elif k == cdb.APP_KEYS:
                from mesh.model.node.applicationKey import ApplicationKey
                self.appKeys = [ApplicationKey(app_key=a) for a in v]

            elif k == cdb.NETWORK_TRANSMIT:
                self.networkTransmit = NetworkTransmit(transmit=v)

            elif k == cdb.RELAY_RETRANSMIT:
                self.relayTransmit = RelayRetransmit(transmit=v)

            elif k == cdb.SECURE_NETWORK_BEACON:
                self.secureNetworkBeacon = v

            elif k == cdb.DEFAULT_TTL:
                self.defaultTTL = v

            elif k == cdb.EXCLUDED:
                self.excluded = v

            elif k == cdb.HEARTBEAT_PUB:
                from mesh.model.node.heartbeatPub import HeartbeatPublication
                self.heartbeatPub = HeartbeatPublication(publish=v)

            elif k == cdb.HEARTBEAT_SUB:
                from mesh.model.node.heartbeatSub import HeartbeatSubscription
                self.heartbeatSub = HeartbeatSubscription(subscribe=v)

            elif k == cdb.SCHEDULES:
                from mesh.model.node.schedule import Schedule
                self.schedules = [Schedule(schedule=s) for s in v]

            elif k == cdb.ICON:
                self.icon = v

            elif k == cdb.TEMPORARY_GUEST:
                self.temporaryGuest = v

            elif k == cdb.VIRTUAL_NODE:
                self.virtualNode = v

            elif k == cdb.LOCATION:
                from mesh.model.node.location import Location
                self.location = Location(location=v)

            elif k == cdb.LIGHT_CONTROLS:
                from mesh.model.node.lc import LightLC
                self.lightControls = [LightLC(lc=lc) for lc in v]

            elif k == cdb.HEALTH_CONFIG:
                from mesh.model.node.healthConfig import HealthConfig
                self.healthConfig = HealthConfig(health_config=v)

            elif k == cdb.FOV:
                from mesh.model.node.fov import Fov
                self.fov = Fov(fov=v)

            elif k == cdb.IP_ADDRESS:
                self.ipAddress = v

            elif k == cdb.MODBUS_TCP:
                self.modbusTcp = v

            elif k == cdb.QR_CODE:
                self.qrCode = v

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        data = dict()
        data[cdb.UUID] = str(self._uuid).upper()
        data[cdb.NAME] = self.name
        data[cdb.DEVICE_KEY] = self._deviceKey.hex.upper() if self._deviceKey else ''
        data[cdb.UNICAST_ADDRESS] = self.unicastAddress.hex
        data[cdb.SECURITY] = self.security
        data[cdb.CID] = '%04X' % self.cid
        data[cdb.PID] = '%04X' % self.pid
        data[cdb.VID] = '%04X' % self.vid
        data[cdb.CRPL] = '%04X' % self.crpl
        data[cdb.FEATURES] = self.features.encode()
        data[cdb.ELEMENTS] = [element.encode() for element in self.elements]
        data[cdb.CONFIG_COMPLETE] = self.configComplete
        data[cdb.NET_KEYS] = [netKey.encode() for netKey in self.netKeys]
        data[cdb.APP_KEYS] = [appKey.encode() for appKey in self.appKeys]
        data[cdb.NETWORK_TRANSMIT] = self.networkTransmit.encode()
        data[cdb.RELAY_RETRANSMIT] = self.relayTransmit.encode()
        data[cdb.SECURE_NETWORK_BEACON] = self.secureNetworkBeacon
        data[cdb.DEFAULT_TTL] = self.defaultTTL
        data[cdb.EXCLUDED] = self.excluded
        if self.heartbeatPub:
            data[cdb.HEARTBEAT_PUB] = self.heartbeatPub.encode()
        if self.heartbeatSub:
            data[cdb.HEARTBEAT_SUB] = self.heartbeatSub.encode()
        data[cdb.SCHEDULES] = [schedule.encode() for schedule in self.schedules]
        if self.icon:
            data[cdb.ICON] = self.icon
        data[cdb.TEMPORARY_GUEST] = self.temporaryGuest
        data[cdb.VIRTUAL_NODE] = self.virtualNode
        if self.location:
            data[cdb.LOCATION] = self.location.encode()
        data[cdb.LIGHT_CONTROLS] = [lc.encode() for lc in self.lightControls]
        if self.healthConfig:
            data[cdb.HEALTH_CONFIG] = self.healthConfig.encode()
        if self.fov:
            data[cdb.FOV] = self.fov.encode()
        if self.ipAddress:
            data[cdb.IP_ADDRESS] = self.ipAddress
        if self.modbusTcp:
            data[cdb.MODBUS_TCP] = self.modbusTcp
        if self.qrCode:
            data[cdb.QR_CODE] = self.qrCode
        return data

    @property
    def uuid(self):
        return self._uuid

    @property
    def deviceKey(self):
        return self._deviceKey
