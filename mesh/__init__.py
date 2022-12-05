from mesh.model.network import MeshNetwork
from mesh.storage.localStorage import LocalStorage


class MeshNetworkManager:
    _instance = None
    network = None
    _storage = LocalStorage()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self):
        self.network = MeshNetwork(network=self._storage.load())

    def swap(self, name: str):
        self.network = MeshNetwork(network=self._storage.swap(profile='%s.json' % name))

    def save(self):
        self._storage.save(self.network.encode())
