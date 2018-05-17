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
            #if the cmd is not does not only deal with the client send the cmd
            else:
                #returns appropriate command
                return cmds

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
serverName = "192.168.1.39"
serverPort = 12000


#connects to server
clientSocket = connectToServer(serverName, serverPort)
while 1:
    #gets the command entered by the user
    cmds = cmdsConfirmation()

    #sends command to the server
    sendCommand(cmds)
