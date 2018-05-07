from socket import *

serverName = 192.168.0.2 
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,socketPort))

data = "Hello World"

while bytesSent != len(data):
    bytesSent += clientSocket.send(data[bytesSent:])

clientSocket..close()
