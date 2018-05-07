from socket import *

import sys

#opens the socket initializer for TCP
serverSocket = socket(AF_INET,SOCK_STREAM)
#grabs the port from command line
portNumber   = int(sys.argv[1])
print(portNumber)
#sets the serverSocket to the Port specified from the command line
serverSocket.bind(('', portNumber))

#socket starts listening
serverSocket.listen(1)

#prints out to let user know it is listening on a certain port
print("Server is now listening on port: " + str(portNumber))

data =""
while 1:
        #accepts client connection
        connectionSocket, addr = serverSocket.accept()

        tempBuff = ""
        data = ""
        while len(data) != 40:
            #data buffer for the server
            tempBuff = connectionSocket.recv(40)

            #incase the other side has unexpectedly closed it socket
            if not tempBuff:
                break
            temp = tempBuff.decode('ASCII')
            data+=temp
        #prints out message
        print(data)
        connectionSocket.close()
