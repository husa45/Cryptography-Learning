import socket
import os
import Crypto.Util.Padding
from Crypto.Util import number
from Crypto.Cipher import ChaCha20
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from base64 import b64encode
SERVER_PORT=7777
SERVER_IP="127.0.0.1"
GENERATOR_PICKED=3
PRIME_GROUP=17
KEY_LENGTH=256
message="Crypto is func ,isnt it ?"
def convert_to_bytes(number)->'bytes':
    byte_count = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_count, "big")
def SendData(key:'bytes',client_socket)->'None':
    """
    THis fucntion lets you choose a file from the system ,to send it encrypted of the network using AES-ECB
    :return: Nothing
    """
    chacha20_ = ChaCha20.new(key=key)
    client_socket.sendall(b64encode(chacha20_.nonce))
    while True:
        path=input("Enter the path to file you want to send :\n").strip()
        if not os.path.exists(path):
                print("Invalid path supplied ,make sure you supply a correct path")
        elif not os.path.isfile(path):
            print("The supplied path is a path to a directory not a file")
        else:
            break
    data=b""
    with open(path,"rb") as reader:
        while True:
            print("sending!!!")
            data=reader.read(1024)
            encrypted=chacha20_.encrypt(data)
            client_socket.sendall(encrypted)
            data=reader.read(1024)
            if not data:
                break
        print("finished sending file!!!!")
        client_socket.shutdown(2)
        client_socket.close()

def main():
    #1.Connect to server
    client_socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP,SERVER_PORT))
    except socket.error as exc:
        print("Cant Connect to the server ,exiting")
        raise SystemExit("Caught exception socket.error : %s" % exc)
    #2.Send initial Beacon :
    client_socket.sendall(b"Hi Server ,lets Start our Key exchange,Shall we !!!!!")
    print(client_socket.recv(4096).decode())
    #3.Agree on prime group (to choose N) and genrator
    src = SourceFileLoader("DiffieHellman.py", "/opt/cryptography/DiffieHellman/DiffieHellman.py").load_module()
    algo=src.DiffieHellman(generator=GENERATOR_PICKED,group=PRIME_GROUP,key_length=KEY_LENGTH)
    client_socket.sendall(f"Use:{GENERATOR_PICKED},{PRIME_GROUP},{KEY_LENGTH}".encode())#first is the generator ,second is the group ,third is the key length
    #4.Exchange public keys:
    pub_key_me=algo.getPublicKey()
    client_socket.sendall(f"Public Key:{pub_key_me}".encode())
    pub_key_server = int(client_socket.recv(4096).decode().split(":")[1])
    #5.Generate secrets :
    secret_key=algo.getSecretKey(pub_key_server)
    secret_key=convert_to_bytes(secret_key)
    print(secret_key)
    key_hash=sha256(secret_key).digest()
    #Testing for Sending messages secretely:
    SendData(key_hash,client_socket)
if __name__=="__main__":
    main()