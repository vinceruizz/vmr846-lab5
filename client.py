from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Cipher import AES
import socket
import sys

symmetricKey = b'1234567891234567'

finalMessage = input("What do you want to tell the server?: ")

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

print("Successfully connected. Requesting server's public key")
# ------ Receive the server's public key -----
key_string = s.recv(8192)
serverKey = open("server_key.pem", 'wb')
serverKey.write(key_string)
serverKey.close()

server_key = RSA.import_key(open('server_key.pem', 'r').read())
cipher = PKCS1_OAEP.new(server_key)
encrypted_message = cipher.encrypt(symmetricKey)

print("Sending encrypted message to server")
s.send(encrypted_message)
ack = s.recv(8192)
print(ack.decode())

aes_cipher = AES.new(symmetricKey, AES.MODE_EAX)
nonce = aes_cipher.nonce
ciphertext, tag = aes_cipher.encrypt_and_digest(finalMessage.encode())

# ----- send nonce ----- #
s.send(nonce)
ack = s.recv(8192)
print(ack.decode())

# ----- send ciphertext ----- #
s.send(ciphertext)
ack = s.recv(8192)
print(ack.decode())

# ----- send tag ----- #
s.send(tag)
ack = s.recv(8192)
print(ack.decode())

s.close()