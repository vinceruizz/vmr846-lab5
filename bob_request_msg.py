from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
import socket
import sys

# ------ Send Key to CA -------
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
print("Waiting for Alice's message")

while True:
    clientSocket, addr = serverSocket.accept()
    print("Connection with " + addr[0] + " established")

    aliceMessage = clientSocket.recv(8192)
    aliceKey = RSA.import_key(open('alice_key.pem', 'r').read())
    aliceSignature = clientSocket.recv(8192)
    h = SHA256.new(aliceMessage)

    try:
        pkcs1_15.new(aliceKey).verify(h, aliceSignature)
        print("Signature is valid.")
    except (ValueError, TypeError):
        print("The signature is not valid.")

    bobKey = RSA.import_key(open('bob_key_priv.pem', 'r').read())

    cipher = PKCS1_OAEP.new(bobKey)
    decryped_msg = cipher.decrypt(aliceMessage).decode()

    print("Alice says: " + decryped_msg)

    clientSocket.close()
    sys.exit()