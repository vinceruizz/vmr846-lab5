from Cryptodome.PublicKey import RSA
from Cryptodome import Random
import socket
import sys

# ------ Key generation ------
random_generator = Random.new().read
aliceKey = RSA.generate(1024, random_generator)
keyFile = open('alice_key_priv.pem', 'wb')
keyFile.write(aliceKey.exportKey())
keyFile.close()
publicKey = aliceKey.public_key()

message = "as".encode() + publicKey.export_key()

# ------ Send Key to CA -------
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print("Socket creation failed. Error code: " + str(msg[0]) + ", Message: " + msg[1])
    sys.exit()
print("Socket created")

host, port = 'localhost', 1234

try:
    s.connect((host, port))
except ConnectionRefusedError:
    print("Connection could not be made")
    sys.exit()

print("Successfully connected. Sending key to CA")
s.send(message)
print("Key successfully sent. Terminating connection")
s.close()