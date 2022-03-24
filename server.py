from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
from Cryptodome import Random
import socket
import sys

random_generator = Random.new().read
serverKey = RSA.generate(1024, random_generator)
keyFile = open('server_key_priv.pem', 'wb')
keyFile.write(serverKey.exportKey())
keyFile.close()
publicKey = serverKey.public_key()

message = publicKey.exportKey()

# ----- Socket creation ----- #
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Socket created")

host, port = 'localhost', 1234

try:
    serverSocket.bind((host,port))
except socket.error as msg:
    print("Binding failed. Error code: " + str(msg[0]) + ", Message: " + msg[1])
    sys.exit()
print("Binding complete")

serverSocket.listen(5)
print("Waiting for client's message") #bob = client

while True:
    clientSocket, addr = serverSocket.accept()
    print("Connection with " + addr[0] + " established")

    # ----- send server's public key to client ------ #
    print("Sending server's public key to client")
    clientSocket.send(message)

    clientMessage = clientSocket.recv(8192)
    clientSocket.send("Encrypted message received!".encode())

    serverKey = RSA.import_key(open('server_key_priv.pem', 'r').read())

    cipher = PKCS1_OAEP.new(serverKey)
    decrypted_sym_key = cipher.decrypt(clientMessage)

    nonce = clientSocket.recv(8192)
    clientSocket.send("nonce received.".encode())
    ciphertext = clientSocket.recv(8192)
    clientSocket.send("ciphertext received.".encode())
    tag = clientSocket.recv(8192)
    clientSocket.send("tag received.".encode())

    aes_cipher = AES.new(decrypted_sym_key, AES.MODE_EAX, nonce=nonce)
    plaintext = aes_cipher.decrypt(ciphertext)

    try:
        aes_cipher.verify(tag)
        print("The message is authentic:", plaintext.decode())
    except ValueError:
        print("Key incorrect or message corrupted.")

    clientSocket.close()
    sys.exit()