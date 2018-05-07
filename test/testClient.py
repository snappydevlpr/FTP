from socket import *

serverName = "192.168.0.2"
serverPort = 12000

clientSocket = socket(AF_INET,SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

data = "Hello world! This is a very long string."
#Python 3.6 requires byte-object so message needs to be encoded
data = data.encode('ASCII')
bytesSent =0
while bytesSent != len(data):
    print(data)
    bytesSent += clientSocket.send(data[bytesSent:])
    print(bytesSent)

clientSocket.close()
