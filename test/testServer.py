import socket
import sys

#opens the socket initializer for TCP
serverSocket = socket(AF_INET,SOCK_STREAM)
#grabs the port from command line
portNumber   = sys.argv
#sets the serverSocket to the Port specified from the command line
serverSocket.bind('', portNumber)

#socket starts listening
serverSocket.listen(1)

#prints out to let user know it is listening on a certain port
print("Server is now listening on port: " + portNumber)



while 1:
        connectionSocket, addr = serverSocket.accept()

        #data buffer for the server
        dataBuffer = ""

        while len(data) != 40:
            tempBuff = connectionSocket.recv(40)

            if not dataBuffer:
                break

            data += dataBuffer
        print(data)

        connectionSocket.close()
