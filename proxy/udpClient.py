#! /bin/python
from socket import *

# default params
serverAddr = ('localhost', 50001)       

import sys, re                          

def usage():
    print("usage: %s [--serverAddr host:port]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()



clientSocket = socket(AF_INET, SOCK_DGRAM)
#print("Input lowercase msg")
usrInput =''
while usrInput is not 'q':
    # Asking user for input file and put or get command
    print("Entering 'put' and a file name will allow you to transfer a file:")
    usrInput = sys.stdin.readline()[:-1]     # delete final \n
    # Splitting input by space to check if put command and filename is present
    splitInput = usrInput.split(' ')
    if splitInput[0].strip() == 'put':
        usrFileName = splitInput[-1]
        # Try to open file, if not, print that file not found and loop again for input
        try:
            fileToSend = open(usrFileName, 'rb')

            # Starting message, to pass in file name and start message (header)
            clientSocket.sendto(b'start ' + usrFileName.encode(), serverAddr)

            # Opening the file as a binary, to be able to send 1000 bytes at a time
            with open(usrFileName.strip(), 'rb') as binary_file:
                # Variable to grab bytes from the file for sending
                byteData = binary_file.read()

            # Replacing new lines with special character to avoid errors and replace them back later
            byteData = byteData.replace(b'\n',b'~`')

            # Checking if the length of the byteData is 1000 bytes or more, if so, send the data
            while len(byteData) >= 1000:
                # Send variable for the beginning 1000 bytes
                send = byteData[:1000]

                # Move the byteData from the last send 1000 bytes to the next 1000 bytes, or end of the byteData
                byteData = byteData[1000:]

                # Try to send the 1000 bytes of byteData (send)
                try:
                    clientSocket.sendto(send, serverAddr)
                except:
                    print("Broken pipe, exiting")
                    sys.exit(1)

            # If byteData is still greater than 0, send the remaining bytes that were not apart of the last 1000 bytes
            if len(byteData) > 0:
                clientSocket.sendto(byteData, serverAddr)
            
            # Sending the end signal to know that the file is done sending
            clientSocket.sendto(b"~fInIs", serverAddr)
            
            # Receiving the file received success message
            recMessage, serverAddrPort = clientSocket.recvfrom(2048)
            if recMessage:
                print("received %s from %s:" % (recMessage, repr(serverAddrPort)))
                sys.exit(0)

        # Match enclosing try
        except FileNotFoundError:
            print("Wrong file or file path")
            continue
        #print(sending file %s" %s (usrFileName))

    # Else for enclosing userInput if statement
    elif usrInput.strip() == 'q':
        print("Exiting")
        sys.exit(0)

    else:
        print("Invalid please try again, enter 'q' to exit")


#print("Input lowercase msg")
#message = sys.stdin.readline()[:-1]     # delete final \n
#message = input("Input lowercase msg:")
#clientSocket.sendto(message.encode(), serverAddr)
#modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
#print("Modified message from %s is <%s>" % (repr(serverAddrPort), modifiedMessage))
