# Utility to reflect bits
def reflect(value, bits):
    result = 0
    for i in range(bits):
        if value & (1 << i):
            result |= 1 << (bits - 1 - i)
    return result

# Your CRC32 class (slightly adjusted to use `reflect`)
class Crc32Algo:
    def __init__(self, generator, initial_crc=0, input_reflection=False, result_reflection=False, final_xor=0):
        self.generator = generator
        self.crc32_lookup_table = [0] * 256
        self.initial_crc = initial_crc
        self.is_reflection = input_reflection
        self.is_result_reflection = result_reflection
        self.XOR = final_xor

    def crc32_single(self, byte, crc=0) -> int:
        crc ^= (byte << 24)
        for _ in range(8):
            if crc & 0x80000000:
                crc = (crc << 1) ^ self.generator
            else:
                crc <<= 1
            crc &= 0xFFFFFFFF
        return crc

    def crc32_multibyte_effecient(self, data: bytearray) -> int:
        crc = self.initial_crc
        for b in data:
            byte = reflect(b, 8) if self.is_reflection else b
            index = ((byte ^ (crc >> 24))) & 0xFF
            intermediate = self.crc32_lookup_table[index]
            crc = ((crc << 8) ^ intermediate) & 0xFFFFFFFF
        crc = reflect(crc, 32) if self.is_result_reflection else crc
        return crc ^ self.XOR

    def crc32_multibyte(self, data: bytearray) -> int:
        crc = self.initial_crc
        for b in data:
            byte = reflect(b, 8) if self.is_reflection else b
            crc = self.crc32_single(byte, crc)
        crc = reflect(crc, 32) if self.is_result_reflection else crc
        return crc ^ self.XOR

    def crc32_lookuptable_prepare(self):
        for i in range(256):
            crc = (i << 24) & 0xFFFFFFFF
            for _ in range(8):
                if crc & 0x80000000:
                    crc = ((crc << 1) ^ self.generator) & 0xFFFFFFFF
                else:
                    crc = (crc << 1) & 0xFFFFFFFF
            self.crc32_lookup_table[i] = crc

# --------------------------
# TEST HARNESS
# --------------------------

# Example parameters for "classic" CRC-32
generator = 0x04C11DB7
initial_crc = 0xFFFFFFFF
input_reflection = True
result_reflection = True
final_xor = 0xFFFFFFFF

# Create CRC object
crc_algo = Crc32Algo(generator, initial_crc, input_reflection, result_reflection, final_xor)
crc_algo.crc32_lookuptable_prepare()

# Test array
test_data = bytearray([0x41, 0x42, 0x43])  # ASCII "ABC"

# Bitwise CRC
crc_bitwise = crc_algo.crc32_multibyte(test_data)

# Table CRC
crc_table = crc_algo.crc32_multibyte_effecient(test_data)

print(f"Bitwise CRC: 0x{crc_bitwise:08X}")
print(f"Table CRC:   0x{crc_table:08X}")

# Check they match
if crc_bitwise == crc_table: #"Bitwise and Table CRC do not match!"
	print("✅ Bitwise and Table CRC match correctly.")
