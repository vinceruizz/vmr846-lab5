import socket
import sys

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
print("Socket listening.")

while (True):
    clientSocket, addr = serverSocket.accept()
    print("Connection with " + addr[0] + " established")
    request = clientSocket.recv(8192).decode().strip()

    # ----- handle key sends -----
    if request[0:2] == 'bs': #bs = "bob send"
        bobKey = open('bob_key.pem','w')
        bobKey.write(request[2:])
        bobKey.close()
        print("Key received")
    elif request[0:2] == 'as': #as = "alice send"
        aliceKey = open('alice_key.pem', 'w')
        aliceKey.write(request[2:])
        aliceKey.close()
        print("Key received")

    # ----- handle key requests -----
    if request[0:2] == 'br': #br = "bob request"
        aliceKey = open('alice_key.pem', 'r')
        key = aliceKey.read().encode()
        clientSocket.send(key)
        aliceKey.close()
        print("Key sent")
    elif request[0:2] == 'ar':
        bobKey = open('bob_key.pem', 'r')
        key = bobKey.read().encode()
        clientSocket.send(key)
        bobKey.close()
        print("Key sent")




    clientSocket.close()
