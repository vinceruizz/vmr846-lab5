from Cryptodome.PublicKey import RSA
import socket
import sys

message = "br".encode()

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

print("Successfully connected. Requesting Bob's key from CA")
s.send(message)
key_string = s.recv(8192)
aliceKey = open("alice_key.pem", 'wb')
aliceKey.write(key_string)
aliceKey.close()
print("Key successfully received. Terminating connection")

s.close()