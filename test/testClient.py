from socket import *
import subprocess

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
    
    while len(recvBuff) < numBytes:
        
        tmpBuff =  sock.recv(numBytes)
        
        if not tmpBuff:
            break
        
        recvBuff += tmpBuff
    
    return recvBuff
    
'''
uploadToServer(fileName)
    PARAM:  fileName name of the file to save
    RETURN: Number of bytes sent
    USE:    This function uploads a file to the server
'''
def uploadToServer(fileName):
    # We need to create a separate data connection
    ephemeralPort = int(recvAll(clientSocket, 2));
    serverName = sys.argv[1]
    dataSocket = connectToServer(serverName, ephemeralPort)
    
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
            
            # Send the data
            while len(fileData) > bytesSent:
                bytesSent += dataSocket.send(fileData[bytesSent:])
        
        else:
            break
            
    fileObj.close()
    dataSocket.close()
    return bytesSent
    
'''
downloadFromServer(fileName)
    PARAM:  fileName name of the file to save
    RETURN: size of the file saved
    USE:    This function downloads a file from the server and saves it to the client
'''
def downloadFromServer(fileName):
    # We need to create a separate data connection
    ephemeralPort = int(recvAll(clientSocket, 2));
    serverName = sys.argv[1]
    dataSocket = connectToServer(serverName, ephemeralPort)
    
    # Receive the first 10 bytes indicating the
    # size of the file
    fileSizeBuff = recvAll(dataSocket, 10)
        
    # Get the file size
    fileSize = int(fileSizeBuff)
    
    # Get the file data
    fileData = recvAll(dataSocket, fileSize)
    
    # Write to file
    fileObj = open(fileName, "w")
    fileObj.write(fileData);
    
    fileObj.close()
    dataSocket.close()
    return fileSize 
  
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
    ephemeralPort = int(recvAll(clientSocket, 2));
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
def cmdsConfirmation():
    #menu dictionary
    menu = {"get":1,
            "put":2,
            "ls":3,
            "lls":4,
            "quit":5,
            "help":6}

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
				sendCommand(cmds)
                fileName = cmds[1]
                savedFileSize = downloadFromServer(fileName)
                print("Downloaded " + fileName + " (" + savedFileSize + " Bytes)")
                # asks to re-enter command
                cmds = input("ftp>")
            #checks if the help was entered
            if menu[cmds[0]] == 2:
                # uploads a file to the server
				sendCommand(cmds)
                fileName = cmds[1]
                uploadedFileSize = uploadToServer(fileName)
                print("Uploaded " + fileName + " (" + uploadedFileSize + " Bytes)")
                # asks to re-enter command
                cmds = input("ftp>")
            #checks if the help was entered
            if menu[cmds[0]] == 3:
                # send ls command to server
                sendCommand(cmds)
                output = receiveServerLsOutput()
                print(output)
                # asks to re-enter command
                cmds = input("ftp>")
            #checks if the help was entered
            if menu[cmds[0]] == 4:
                #prints out files on the client
                print(subprocess.call(["ls", "-l"]))
                # asks to re-enter command
                cmds = input("ftp>")
            #checks if exit command was made
            elif menu[cmds[0]] == 5:
                print("Connection is closing...")
                #closes socket after sending all data
                clientSocket.close()
            #checks if user wants to view files on the client
            elif menu[cmds[0]] == 6:
                #prints out the help menu
                print(helpString)
                # asks to re-enter command
                cmds = input("ftp>")

        #prints help menu
        else:
            print("Incorrect command entered! Enter help for more information.")
            cmds = input("ftp>")

'''
sendCommand(cmds)
    USE:    This function sends a given command message to the server
'''
def sendCommand(cmds):
    #data to send
    data = ''.join(cmds)

    #Python 3.6 requires byte-object so message needs to be encoded
    data = data.encode('ASCII')

    #number of bits sent
    bytesSent = 0

    #makes sure that the bits sent is less than the data message
    while bytesSent != len(data):
        # keeps sending data until it has all been sent
        bytesSent += clientSocket.send(data[bytesSent:])

#desired server and port number
#serverName = "192.168.1.39"
#serverPort = 12000
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

#connects to server
clientSocket = connectToServer(serverName, serverPort)
# listen for responses like ephemeral port
clientSocket.listen(1)

while 1:
    #gets the command entered by the user
    cmdsConfirmation()
    
