from Cryptodome.Random  import *
random:'bytes'=get_random_bytes(64)
with open("key.config","wb") as writer:
    writer.write(random)
