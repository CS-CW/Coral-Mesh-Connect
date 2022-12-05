import uuid

from typing import Optional
from mesh.model.address import Address


class MeshAddress:
    def __init__(self, hex_: str = '0'):
        self._address = None
        self._virtual_label = None

        address = Address(hex_=hex_)
        if address.address is not None:
            self._address = address
        else:
            try:
                virtual_label = uuid.UUID(hex_)
                if address:
                    self._virtual_label = virtual_label
            except TypeError:
                pass

    @property
    def hex(self) -> Optional[str]:
        if self._address:
            return '%04X' % self._address.address
        elif self._virtual_label:
            return self._virtual_label.hex.upper()
        else:
            return None
