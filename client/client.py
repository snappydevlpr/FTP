from socket import *
import subprocess
import sys

'''
connectToServer(ip_address, server_port)
    PARAM:  ip_address of the server,
            server_port port to send to
    USE:    This function error checks for appropriate commands are entered by the user
'''
def connectToServer(ip_address, server_port):
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    return clientSocket

'''
recvAll(sock, numBytes)
    PARAM:  sock socket to receive from
    PARAM:  numBytes number of bytes to receive
    USE:    This function gets an amount of data from the socket
'''
def recvAll(sock, numBytes):
    recvBuff = ""
    tmpBuff = ""

    while len(recvBuff) != numBytes:
        tmpBuff =  sock.recv(numBytes)

        if not tmpBuff:
            break
        #decodes the message the client sent
        temp = tmpBuff.decode('ASCII')
        recvBuff += temp

    return recvBuff


'''
receiveServerLsOutput()
    RETURN: the string output of the server's ls command
    USE:    This function receives the output from the
            server side ls command
'''
def receiveServerLsOutput():
    # We need to create a separate data connection
    # The ls command sent to the server should send the client the eph port
    # in order to get the output from the dataSocket
    ephemeralPort = int(recvAll(clientSocket, 10));
    serverName = sys.argv[1]
    dataSocket = connectToServer(serverName, ephemeralPort)

    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(dataSocket, 10)

    # Get the file size
    fileSize = int(fileSizeBuff)

    # Get the file data
    fileData = recvAll(dataSocket, fileSize)

    return str(fileData, 'utf-8')

'''
cmdsConfirmation()
    USE:    This function error checks for appropriate commands are entered by the user
'''
def cmdsConfirmation(clientSocket):
    #menu dictionary
    menu = {"get":1,"put":2,"ls":3,"lls":4,"quit":5}

    #help menu
    helpString = ("\nftp> get <file name> (downloads file <file name> from the server)\n"
                 "ftp> put <filename> (uploads file <file name> to the server)\n"
                 "ftp> ls (lists files on the server)\n"
                 "ftp> lls (lists files on the client)\n"
                 "ftp> quit (disconnects from the server and exits)\n")

    #now connected to the server menu
    cmds = input("ftp>")

    #keeps getting the command until acceptable command
    while True:

        #splits the command
        cmds = cmds.split()
        #checks if the command is in the menu
        if cmds[0] in menu.keys():
            #checks if the help was entered
            if menu[cmds[0]] == 1:
                # downloads file from server
                cmds = ' '.join(cmds)
                sendCommand(clientSocket,cmds)
                #receives the port number
                dataPortNumber = recvAll(clientSocket,10)

                #connects to temp socket
                dataSocket = socket(AF_INET,SOCK_STREAM)
                client_IP, client_Port = clientSocket.getsockname()
                print("\nNow connected on temp port: ",int(dataPortNumber))
                dataSocket.connect((client_IP,int(dataPortNumber)))

                # Receive the first 10 bytes indicating the size of the file
                fileSizeBuff = recvAll(dataSocket, 10)
                # Get the file size
                fileSize = int(fileSizeBuff)
                print("Receiving " + fileSizeBuff + " bytes")
                # Get the file data
                fileData = recvAll(dataSocket, fileSize)

                # Write to file
                fileName = cmds.split(' ')[1]
                fileObj = open(fileName, "w")
                fileObj.write(fileData);

                fileObj.close()
                dataSocket.close()
                print("Temp port now closed")
                print("file received\n")
            # uploads a file to the server
            elif menu[cmds[0]] == 2:
                # Send command to server
                cmds = ' '.join(cmds)
                sendCommand(clientSocket,cmds)

                # Create temporary dataSocket
                dataPortNumber = recvAll(clientSocket,10)
                dataSocket = socket(AF_INET,SOCK_STREAM)
                client_IP, client_Port = clientSocket.getsockname()
                print("\nNow connected on temp port: ",int(dataPortNumber))
                dataSocket.connect((client_IP,int(dataPortNumber)))

                # Send file to server
                fileName = cmds.split(' ')[1]
                file = open(fileName, "r")
                fileData = None
                bytesSent = 0

                while True:
                    fileData = file.read(65536)
                    if fileData:
                            dataSize = str(len(fileData))
                            while len(dataSize) < 10:
                                dataSize = "0" + dataSize

                            fileData = dataSize + fileData
                            fileData = fileData.encode('ASCII')

                            while len(fileData) > bytesSent:
                                print("Sent " + str(bytesSent) + " bytes")
                                bytesSent += dataSocket.send(fileData[bytesSent:])
                    else:
                        break

                file.close()
                dataSocket.close()
                print("Temp port now closed")
                print("file transferred")
            #checks if the help was entered
            elif menu[cmds[0]] == 3:
                # send ls command to server
                cmds = ''.join(cmds)
                sendCommand(clientSocket,cmds)
                dataSize = recvAll(clientSocket,10)
                print('\n' + recvAll(clientSocket,int(dataSize)))

            #checks if the help was entered
            elif menu[cmds[0]] == 4:
                #prints out files on the client
                print(str(subprocess.check_output(["ls", "-l"]), 'utf-8'))

            #checks if exit command was made
            elif menu[cmds[0]] == 5:
                print("Connection is closing...")
                #closes socket after sending all data
                clientSocket.close()


        #prints help menu
        else:
            print("Incorrect command entered! Enter help for more information.")
        cmds = input("ftp>")

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

#desired server and port number
#serverName = "192.168.1.39"
#serverPort = 12000
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

#connects to server
clientSocket = connectToServer(serverName, serverPort)

while 1:
    #gets the command entered by the user
    cmdsConfirmation(clientSocket)
