from typing import Optional


class Address:
    def __init__(self, hex_: str):
        self._address = None
        if 0 < len(hex_) <= 4:
            try:
                self._address = int(hex_, 16)
            except ValueError:
                pass

    @property
    def address(self) -> Optional[int]:
        return self._address

    @property
    def hex(self) -> Optional[str]:
        if self._address:
            return '%04X' % self._address
