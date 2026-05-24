import socket
import Crypto
from Crypto.Util import Padding
from Crypto.Util import number
from Crypto.Cipher import ChaCha20
from hashlib import sha256
from base64 import b64decode
from importlib.machinery import SourceFileLoader
SERVER_PORT=7777
SERVER_IP="100.100.130.50"
def convert_to_bytes(number)->'bytes':
    byte_count = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_count, "big")
def recvData(key:'bytes',client_sock) ->'None':
    nonce=b64decode(client_sock.recv(1024))
    cipher = ChaCha20.new(key=key, nonce=nonce)
    with open("recieved.png","ab")as out:
        while True:
            print("Reciving!!!!")
            ciphertext= client_sock.recv(2048)
            if not ciphertext:
                break
            nonce=client_sock.recv(2048)

            plain = cipher.decrypt(ciphertext)
            out.write(plain)

    print("finsihed recieving")
    client_sock.shutdown(1)
    client_sock.close()
def main():
    #1.Creating server socket ,then waiting for a connection.
    server_socket=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen()
    client_sock, info = server_socket.accept()
    #2.Reciving initial Beacon
    print(f"Connection established from {info[0]} on port {info[1]}")
    print(client_sock.recv(8192).decode())
    client_sock.sendall(b"Lets Go!!")
    #3.Prime and generator agreement
    usage_agreement=client_sock.recv(4096).decode()
    print(usage_agreement)
    G , Group ,KeyLength=tuple(map(lambda elem:int(elem),(usage_agreement.split(":"))[1].split(",")))
    src = SourceFileLoader("DiffieHellman.py", "/opt/cryptography/DiffieHellman/DiffieHellman.py").load_module()
    algo=src.DiffieHellman(G,key_length=KeyLength,group=Group)
    #4.Exchange public keys:
    pub_key_client=int(client_sock.recv(4096).decode().split(":")[1])
    pub_key_me = algo.getPublicKey()
    client_sock.sendall(f"Public Key:{pub_key_me}".encode())
    #5.Create Secret Keys:
    #print(f"Secret key :{hex(algo.getSecretKey(pub_key_client))}")
    secret_key = algo.getSecretKey(pub_key_client)
    secret_key=convert_to_bytes(secret_key)
    key_hash = sha256(secret_key).digest()
    #6.Decrypting the recieved message to verify exchange success:
    recvData(key_hash,client_sock)
if __name__=="__main__":
    main()