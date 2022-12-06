
def twos_complement(hex_: str, bits: int):
    value = int(hex_, 16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value
