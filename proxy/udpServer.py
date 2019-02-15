#! /bin/python
from socket import *

# default params
serverAddr = ("", 50001)

import sys, os
def usage():
    print("usage: %s [--serverPort <port>]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverPort":
            serverAddr = ("", int(args[0])); del args[0]
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()

print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
print("ready to receive")
while 1:
    #message, clientAddrPort = serverSocket.recvfrom(2048)
    headerPayload, clientAddrPort = serverSocket.recvfrom(2048)
    print("from %s: rec'd connection" % (repr(clientAddrPort)))
    
    # Getting current working directory to create a new directory for server files
    cwd = os.getcwd()

    # Initializing fileName variable
    fileName = ''

    # While loop that waits for fileName to get initiated
    while fileName == '':
        # Recieve filename and save it as "header"
        #headerPayload = framedReceive(serverSocket)
        # If headerPayload is not NON
        if headerPayload:
            # Split the decoded payload by the spaces
            pl = headerPayload.decode().split()
        # If start is in the payload by the spaces
        if b'start' in headerPayload:
            fileName = pl[-1]
            # If serverDirectory does not exist, create it as a subdirectory
            if not os.path.exists(cwd + '/serverDirectory/'):
                os.makedirs(cwd + '/serverDirectory')
            # Open the file in serverDirectory (creating it if it does not exist)

            fileOpen = open(os.path.join(cwd + '/serverDirectory/', fileName), 'wb+')
            fileOpen.close()
            break
        # While loop for receiving the body of the file and writing it to the one created on the server
    while True:
        payload, port = serverSocket.recvfrom(2048)
        #print("payload is: %s " % (payload.decode()))
        if not payload:
            sys.exit(0)
        # Replacing the '~`" back to '\n' new line character
        payload = payload.decode().replace('~`', '\n')
        # Opening the file for appending
        #currFile = cwd + '/serverDirectory/' 
        fileOpen = open(cwd + '/serverDirectory/' + fileName, 'a')
        try:
            # If the finish character is found in the payload to show file is done sending
            if '~fInIs' in payload:
                fileOpen.close()
                success = b"File finished sending"
                #print(success)
                # Send that the file was received successully
                serverSocket.sendto(success, clientAddrPort)
                sys.exit(0)
            # If it is not finished, write to the file
            else:
                fileOpen.write(payload)
        except FileNotFoundError:
            print("Error trying to receive file")

    #message = sys.stdin.readline()[:-1]     # delete final \n
    #modifiedMessage = message.upper()
    #serverSocket.sendto(modifiedMessage, clientAddrPort)
    
                
