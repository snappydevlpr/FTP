import socket

serverName = ecs.fullerton.edu
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,socketPort))

data = "Hello World"

while bytesSent != len(data):
    bytesSent += clientSocket.send(data[bytesSent:])

clientSocket..close()
