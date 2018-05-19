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
ephemeral()
    Purpose: Sets up temporary port for data transfer use
'''
def ephemeral(connectionSocket):
    #create the ephemeral port

    dataSocket = socket(AF_INET,SOCK_STREAM)
    client_IP, client_Port = connectionSocket.getsockname()
    dataSocket.bind((client_IP,0))
    #socket starts listening
    dataSocket.listen(2)
    #accepts incoming client
    print("hello")
    dataPortNumber = str(dataSocket.getsockname()[1])
    print("bye")
    # makes the port length 10
    while len(dataPortNumber) < 10:
        dataPortNumber = '0' + dataPortNumber

    dataPortNumber = dataPortNumber.encode('ASCII')
    #Send the port number to the client over control connection
    bytesSent = 0

    while bytesSent != 10:
        # keeps sending data until it has all been sent
        bytesSent += connectionSocket.send(dataPortNumber[bytesSent:])

    return dataSocket

'''
recvAll(sock, numBytes)
    PARAM:  sock socket to receive from
    PARAM:  numBytes number of bytes to receive
    USE:    This function gets an amount of data from the socket
'''
def recvAll(sock, numBytes):
    recvBuff = ""
    tmpBuff = ""

    while len(recvBuff) < numBytes:

        tmpBuff =  sock.recv(numBytes)

        if not tmpBuff:
            break
        #decodes the message the client sent
        temp = tmpBuff.decode('ASCII')
        recvBuff += temp

    return recvBuff

'''
getFile()
    Purpose:Sends file to the client
'''
def getFile(fileName,serverSocket):
    # create ephemeral port and send the port number to the client
    dataSocket = ephemeral(serverSocket)
    dataConSocket, addr = dataSocket.accept()

    # Get the file object and stuff
    fileObj = open(fileName, "r")
    fileData = None
    bytesSent = 0

    while True:

        # Read 65536 bytes of data
        fileData = fileObj.read(65536)

        # Make sure we did not hit EOF
        if fileData:

            # convert data to string
            dataSizeStr = str(len(fileData))

            # Prepend 0's to the size string
            # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Prepend the size string to the data
            fileData = dataSizeStr + fileData
            #Python 3.6 requires byte-object so message needs to be encoded
            fileData = fileData.encode('ASCII')
            # Send the data
            while len(fileData) > bytesSent:
                bytesSent += dataConSocket.send(fileData[bytesSent:])

        else:
            break

    fileObj.close()
    dataSocket.close()
    return bytesSent


'''
putFile(fileName)
    PARAM:  name of file
'''
def putFile(fileName, serverSocket):
    # create ephemeral port and send the port number to the client
    dataSocket = ephemeral(serverSocket)
    dataConSocket, addr = dataSocket.accept()

    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(dataConSocket, 10)

    # Get the file size
    fileSize = int(fileSizeBuff)

    # Get the file data
    fileData = recvAll(dataConSocket, fileSize)

    # Write to file
    fileObj = open(fileName, "w")
    fileObj.write(fileData);

    fileObj.close()
    dataSocket.close()
    return fileSize

'''
sendCommand(cmds)
    USE:    This function sends a given command message to the server
'''
def sendCommand(sock, data):
    #Python 3.6 requires byte-object so message needs to be encoded
    data = data.encode('ASCII')

    #number of bits sent
    bytesSent = 0

    #makes sure that the bits sent is less than the data message
    while bytesSent != len(data):
        # keeps sending data until it has all been sent
        bytesSent += sock.send(data[bytesSent:])

'''
commands(cmds)
    PARAM:  Takes in user's commands
    USE:    This function takes in user commands and
            decides which functions to call based on the command
'''
def commands(cmds,serverSocket):
    #splits commands into a list
    cmds = cmds.split(' ')
    menu = {"get":1,"put":2,"ls":3,"lls":4,"quit":5}
    if cmds[0] in menu.keys():
        print("Success")
    #checks if it is a get file if so run get file
    if menu[cmds[0]] == 1:
        print(cmds[1])
        getFile(cmds[1],serverSocket)
    #if the server is receiving a file run putFile
    elif menu[cmds[0]] == 2:
        putFile(cmds[1],serverSocket)
    #if client wants to know files on the server
    elif menu[cmds[0]] == 3:
        #gets the ls command info
        data = str(subprocess.check_output(["ls", "-l"]), 'utf-8')
        dataSize = str(len(data))
        while len(dataSize) < 10:
            dataSize = '0' + dataSize

        #Python 3.6 requires byte-object so message needs to be encoded
        dataSize = dataSize.encode('ASCII')
        #number of bits sent
        bytesSent = 0
        #makes sure that the bits sent is less than the data message
        while bytesSent != len(dataSize):
            # keeps sending data until it has all been sent
            bytesSent += serverSocket.send(dataSize[bytesSent:])

        recvAll(serverSocket,1)

        #Python 3.6 requires byte-object so message needs to be encoded
        data = data.encode('ASCII')
        #number of bits sent
        bytesSent = 0
        #makes sure that the bits sent is less than the data message
        while bytesSent != len(data):
            # keeps sending data until it has all been sent
            bytesSent += serverSocket.send(data[bytesSent:])

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
                commands(data,connectionSocket)
