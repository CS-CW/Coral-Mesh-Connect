import uuid
import datetime
import dateutil.parser

from typing import Optional
from mesh.model import Codable
from mesh import cdb


class MeshNetwork(Codable):

    def __init__(self, network: Optional[dict] = None):
        self._meshUUID = uuid.uuid4()
        self.meshName = 'Mesh Network'
        self.timestamp = datetime.datetime.now()
        self.netKeys = []
        self.appKeys = []
        self.provisioners = []
        self.nodes = []
        self.groups = []
        self.scenes = []
        self.partial = False
        self.networkExclusions = []
        if network:
            self.decode(network)

    @property
    def schema(self):
        return 'http://json-schema.org/draft-04/schema#'

    @property
    def id(self):
        return 'http://www.bluetooth.com/specifications/assigned-numbers/mesh-profile/cdb-schema.json#'

    @property
    def version(self):
        return '1.0.0'

    @property
    def meshUUID(self):
        return self._meshUUID

    def decode(self, data: Optional[dict] = None):
        if not data:
            return

        for k, v in data.items():
            if k in [cdb.SCHEMA, cdb.ID, cdb.VERSION]:
                continue

            if k == cdb.MESH_UUID:
                self._meshUUID = uuid.UUID(v)

            elif k == cdb.TIMESTAMP:
                # be able to parse for RFC 3339 and ISO 8601
                self.timestamp = dateutil.parser.isoparse(v)

            elif k == cdb.NET_KEYS:
                from mesh.model.networkKey import NetworkKey
                self.netKeys = [NetworkKey(net_key=n) for n in v]

            elif k == cdb.APP_KEYS:
                from mesh.model.applicationKey import ApplicationKey
                self.appKeys = [ApplicationKey(app_key=a) for a in v]

            elif k == cdb.PROVISIONERS:
                from mesh.model.provisioner import Provisioner
                self.provisioners = [Provisioner(provisioner=p) for p in v]

            elif k == cdb.NODES:
                from mesh.model.node import Node
                self.nodes = [Node(node=n) for n in v]

            elif k == cdb.GROUPS:
                from mesh.model.group import Group
                self.groups = [Group(group=g) for g in v]

            elif k == cdb.SCENES:
                from mesh.model.scene import Scene
                self.scenes = [Scene(scene=s) for s in v]

            elif k == cdb.PARTIAL:
                self.partial = v

            elif k == cdb.NETWORK_EXCLUSIONS:
                from mesh.model.networkExclusion import NetworkExclusion
                self.networkExclusions = [NetworkExclusion(network_exclusion=n) for n in v]

            else:  # others or news
                setattr(self, k, v)

    def encode(self) -> Optional[dict]:
        """
        Remember to add news
        """
        data = dict()
        data[cdb.SCHEMA] = self.schema
        data[cdb.ID] = self.id
        data[cdb.VERSION] = self.version
        data[cdb.MESH_UUID] = str(self.meshUUID).upper()
        data[cdb.MESH_NAME] = self.meshName
        data[cdb.TIMESTAMP] = self.timestamp.isoformat()
        data[cdb.NET_KEYS] = [netKey.encode() for netKey in self.netKeys]
        data[cdb.APP_KEYS] = [appKey.encode() for appKey in self.appKeys]
        data[cdb.PROVISIONERS] = [provisioner.encode() for provisioner in self.provisioners]
        data[cdb.NODES] = [node.encode() for node in self.nodes]
        data[cdb.GROUPS] = [group.encode() for group in self.groups]
        data[cdb.SCENES] = [scene.encode() for scene in self.scenes]
        data[cdb.PARTIAL] = self.partial
        data[cdb.NETWORK_EXCLUSIONS] = [networkExclusion.encode() for networkExclusion in self.networkExclusions]
        return data
