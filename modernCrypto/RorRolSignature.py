def rol(x, r, bits=8):
    return ((x << r) | (x >> (bits - r))) & ((1 << bits) - 1)

def ror(x, r, bits=8):
    return ((x >> r) | (x << (bits - r))) & ((1 << bits) - 1)
