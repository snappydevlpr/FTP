from socket import *
import subprocess
import sys

'''
initializeSocket()
    USE:    This function initializes the socket connection
'''
def initializeSocket():
    #opens the socket initializer for TCP
    serverSocket = socket(AF_INET,SOCK_STREAM)
    #grabs the port from command line
    portNumber   = int(sys.argv[1])
    #sets the serverSocket to the Port specified from the command line
    serverSocket.bind(('', portNumber))
    #socket starts listening
    serverSocket.listen(2)
    #prints out to let user know it is listening on a certain port
    print("Server is now listening on port: " + str(portNumber))

    return serverSocket

'''
commands(cmds)
    PARAM:  Takes in user's commands
    USE:    This function takes in user commands and
            decides which functions to call based on the command
'''
def commands(cmds):
    #splits commands into a list
    cmds = cmds.split()
    menu = {"get":1,
            "put":2,
            "ls":3,
            "lls":4,
            "quit":5}

    #checks if it is a get file if so run get file
    if menu[cmds[0]] == 1:
        getFile(cmds[1])
    #if the server is receiving a file run putFile
    elif menu[cmds[0]] == 2:
        putFile(cmds[1])
    #if client wants to know files on the server
    elif menu[cmds[0]] == 3:
        print(subprocess.call(["ls", "-l"]))


def getFile(fileName):
    return

def putFile(fileName):
    return

#control Connection
serverSocket = initializeSocket()
#accepts client connection
connectionSocket, addr = serverSocket.accept()
#gets the client ip and port to output
client_IP, client_Port = serverSocket.getsockname()
print("Connected to client IP:" + str(client_IP))
print("Connected to client port:" + str(client_Port))

#continue forever
while 1:
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
            if data != '':
                commands(''.join(data))
