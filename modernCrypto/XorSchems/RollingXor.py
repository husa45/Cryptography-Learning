


def RollingXorEncrypt(plainData:'bytes')->'bytes':
    k=0x30
    plainLength=len(plainData)
    ciphertext=bytearray([0]*plainLength)
    for i in range(0,plainLength):
        ciphertext[i]=plainData[i]^k
        k=ciphertext[i]
    return bytes(ciphertext)
def RollingXorDecrypt(cipherData:'bytes')->'bytes':
    k = 0x30
    cipherLength = len(cipherData)
    plaintext = bytearray([0] * cipherLength)
    for i in range(0, cipherLength):
        plaintext[i] = cipherData[i] ^ k
        k = cipherData[i]
    return bytes(plaintext)

with open('Screenshot From 2025-12-19 18-21-11.png','rb') as byteReader:
    image=byteReader.read()
encrypted=RollingXorEncrypt(image)
with open('afterDecryption','wb') as byteWriter:
    byteWriter.write(RollingXorDecrypt(encrypted))
