from socket import *
import subprocess

import sys
def initializeSocket():
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

    return serverSocket

def commands(cmds):
    # Run ls command, get output, and print it
    cmds = cmds.split()
    menu = {"get":1,
            "put":2,
            "ls":3,
            "lls":4,
            "quit":5}

    if   menu[cmds[0]] == 1:
        getFile(cmds[1])
    elif menu[cmds[0]] == 2:
        putFile(cmds[1])
    elif menu[cmds[0]] == 3:
        print(subprocess.call(["ls", "-l"]))
    elif menu[cmds[0]] == 5:
        connectionSocket.close()

serverSocket = initializeSocket()

while 1:
        #accepts client connection
        connectionSocket, addr = serverSocket.accept()

        # initializer the temporary buff
        tempBuff = ""
        data = ""

        #gets data of length 40
        while len(data) != 40:
            #data buffer for the server
            tempBuff = connectionSocket.recv(40)
            #incase the other side has unexpectedly closed it socket
            if not tempBuff:
                break
            #decodes the message the client sent
            temp = tempBuff.decode('ASCII')
            data+=temp

        #prints out message
        print(data)
        commands(data)
        #closes connection if the command by the user says so
        if data == "quit":
            connectionSocket.close()
