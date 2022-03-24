from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import PKCS1_OAEP
import socket
import sys

# ------ Key generation ------
alice_key_priv = RSA.import_key(open('alice_key_priv.pem', 'r').read())
bob_key = RSA.import_key(open('bob_key.pem', 'r').read())
cipher = PKCS1_OAEP.new(bob_key)


message = input("Enter a message to be sent to Bob: ")
encoded_message = message.encode()
encrypted_message = cipher.encrypt(encoded_message)

hash_sha256 = SHA256.new(encrypted_message)
signature = pkcs1_15.new(alice_key_priv).sign(hash_sha256)

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

print("Successfully connected. Sending message to Bob")
s.send(encrypted_message)
print("Successfully sent message to Bob. Sending signature")
s.send(signature)
print("Signature successfully sent. Terminating connection")
s.close()