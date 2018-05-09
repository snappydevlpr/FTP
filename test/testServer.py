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
    serverSocket.listen(1)
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
    # Run ls command, get output, and print it
    print(cmds)
    if cmds == '':
        return
    cmds = cmds.split()
    menu = {"get":1,
            "put":2,
            "ls":3,
            "lls":4,
            "quit":5}
    if menu[cmds[0]] == 1:
        getFile(cmds[1])
    elif menu[cmds[0]] == 2:
        putFile(cmds[1])
    elif menu[cmds[0]] == 3:
        print(subprocess.call(["ls", "-l"]))


# def getFile(fileName):
#     # Create a socket
#     welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # Bind the socket to port 0
#     welcomeSocket.bind(('',0))
#     #socket starts listening
#     serverSocket.listen(1)
#
#     #send message back to the client server
#
#     # Open the file
#     fileObj = open(fileName, "r")
#     # The number of bytes sent
#     numSent = 0
#     # The file data
#     fileData = None
#     # Keep sending until all is sent
#     while True:
#
#     	# Read 65536 bytes of data
#     	fileData = fileObj.read(65536)
#
#     	# Make sure we did not hit EOF
#     	if fileData:
#
#     		# Get the size of the data read
#     		# and convert it to string
#     		dataSizeStr = str(len(fileData))
#
#     		# Prepend 0's to the size string
#     		# until the size is 10 bytes
#     		while len(dataSizeStr) < 10:
#     			dataSizeStr = "0" + dataSizeStr
#
#     		# Prepend the size of the data to the
#     		# file data.
#     		fileData = dataSizeStr + fileData
#
#     		# The number of bytes sent
#     		numSent = 0
#
#     		# Send the data!
#     		while len(fileData) > numSent:
#     			numSent += connSock.send(fileData[numSent:])
#
#     	# The file has been read. We are done
#     	else:
#     		break
#
#     print("Sent ", numSent, " bytes.")
#     # Close the socket and the file
#     connSock.close()
#     fileObj.close()


#control Connection
serverSocket = initializeSocket()
#accepts client connection
connectionSocket, addr = serverSocket.accept()
client_IP, client_Port = serverSocket.getsockname()
print("Connected to client IP:" + str(client_IP))
print("Connected to client port:" + str(client_Port))

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
            commands(''.join(data))
