import socket
from Crypto.Util import number
SERVER_IP="127.0.0.1"
SERVER_PORT=8556

def get_message():
    data=b""
    with open("test.jpeg","rb") as reader:
        data=reader.read()
    return data
def get_privatekey(key_length: 'int', p) -> 'int':
    """
    The key length is at least 180 bit ,to provide more security
    :param key_length:The key length to generate
    :return:Randomly chosen private key  < p
    """
    while True:
        priv_key = number.getPrime(key_length)
        if priv_key < p:
            return priv_key
def main():
    sock=socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER_IP,SERVER_PORT))
    sock.listen()
    client_sock, info = sock.accept()
    #Recieving and encrypting messages:
    pub_key=client_sock.recv(8096).decode().split(",")
    print(pub_key)
    generator=int(pub_key[0].split(":")[1])
    p = int(pub_key[1].split(":")[1])
    d = int(pub_key[2].split(":")[1])
    #Choosing private key:
    k=get_privatekey(12,p)
    #generating sender`s public  key:
    y=pow(generator,k,p)
    #sending the file conent encrypted 256 byte chunks at a time
    m=b"NWARA is the best artist"
    m = int.from_bytes(m, "big")
    z = (pow(d, k) * m) % p
    ciphertext=f"y:{y},z:{z}"
    client_sock.send(ciphertext.encode())
    client_sock.close()
    sock.close()
if __name__=="__main__":
    main()
# message=get_message()
#     for i in range(0,len(message),128):
#         m=""
#         if (len(message)-i) <128:
#             m=message[i:i+(len(message)-i)]
#         else:
#             m=message[i:i+128]
#         m=int.from_bytes(m, "big")
#         z=(pow(d,k)*m)%p
#         ciphertext=f"y:{y},z:{z}"
#         client_sock.send(ciphertext.decode())