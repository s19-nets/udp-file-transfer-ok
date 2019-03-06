#! /bin/python
from socket import *
import time
import os
import select

# default params
serverAddr = ('localhost', 50001)       

import sys, re                          

# PRINTING USAGE
def usage():
    print("usage: %s [--serverAddr host:port]"  % sys.argv[0])
    sys.exit(1)

# GETTING SERVER ADDRESS ANF PORT
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

###################################################################
#############             PUT METHOD         ######################
###################################################################

def put(usrFileName):
    # Try to open file, if not, print that file not found and loop again for input
    try:
        fileToSend = open(usrFileName, 'rb')


        # Opening the file as a binary, to be able to send 1000 bytes at a time
        with open(usrFileName.strip(), 'rb') as binary_file:
            # Variable to grab bytes from the file for sending
            byteData = binary_file.read()

        # Replacing new lines with special character to avoid errors and replace them back later
        byteData = byteData.replace(b'\n',b'~`')

        
        # Counter to tell server how many packets are going to be sent
        numPackets = len(byteData) / 100

        # If file length is not directly divisible by 100, need to add to the number of packets
        #if (numPackets % 100) !=0:
        #    ++numPackets

        # We are sending a final packet with the finish flag, need to add one to number of packets
        #++numPackets

        
        # Starting message, to pass in file name and start message (header)
        clientSocket.sendto(b'put start ' + str(numPackets).encode() + b' ' + usrFileName.encode(), serverAddr)

        # Waiting to recieve message to start sending file
        #recMessage, serverAddrPort = clientSocket.recvfrom(2048)
        #select.select(5)
        #if "Received" in recMessage.decode():
        #    print("Sending now")
        
        # Counter to tell server which packet number this is
        sequenceNumber = 1;

        # Checking if the length of the byteData is 100 bytes or more, if so, send the data
        while len(byteData) >= 100:
            # Send variable for the beginning 100 bytes
            send = byteData[:100]
        
            # Appending current sequence number to buffer to send
            #send = str(sequenceNumber).encode() + b' ' + send

            # Move the byteData from the last send 100 bytes to the next 1000 bytes, or end of the byteData and incrementing sequence number
            byteData = byteData[100:]
            ++sequenceNumber
            
            #time.sleep(1)
            # Try to send the 100 bytes of byteData (send)
            try:
                clientSocket.sendto(send, serverAddr)
           #     time.sleep(1)
           #     recMessage, serverAddrPort = clientSocket.recvfrom(2048)
           #     if "received" in recMessage.decode():
           #         serverNum = recMessage.decode()
           #         serverNum = serverNum[0]
           #         #if serverNum == sequenceNumber:
          #      print(sequenceNumber + " packet received")
           #     continue

            except:
            #    clientSocket.sendto(b"ERROR: Broken pipe, exiting", serverAddr)
                print("Broken pipe, exiting")
                sys.exit(1)

        # If byteData is still greater than 0, send the remaining bytes that were not apart of the last 100 bytes
        if len(byteData) > 0:
            byteData = str(sequenceNumber).encode() + b' ' + byteData 
            clientSocket.sendto(byteData, serverAddr)
            
        # Sending the end signal to know that the file is done sending
        clientSocket.sendto(str(sequenceNumber).encode() + b' ' + b'~fInIs', serverAddr)
            
        # Receiving the file received success message
        recMessage, serverAddrPort = clientSocket.recvfrom(2048)
        if recMessage:
            print("%s from %s:" % (recMessage.decode(), repr(serverAddrPort)))
            sys.exit(0)

    # Match enclosing try
    except FileNotFoundError:
        print("Wrong file or file path")
    #print(sending file %s" %s (usrFileName))

###################################################################
#############             GET METHOD         ######################
###################################################################

#def get(usrFileName):


    

###################################################################
#############          START OF CODE         ######################
###################################################################

clientSocket = socket(AF_INET, SOCK_DGRAM)
#print("Input lowercase msg")
usrInput =''
while usrInput is not 'q':
    # Asking user for input file and put or get command
    print("Entering 'put' and a file name will allow you to transfer a file to the server, entering 'get' and a file name will allow you to get a file from the server:")
    usrInput = sys.stdin.readline()[:-1]     # delete final \n

    # Splitting input by space to check if put command and filename is present
    splitInput = usrInput.split(' ')

    # If user wants to put a file on the server
    if splitInput[0].strip() == 'put':
        usrFileName = splitInput[-1]
        try:
            fileToSend = open(usrFileName, 'rb')
            fileToSend.close()
        except FileNotFoundError:
            print("Wrong file or file path")
            continue
        put(usrFileName)
        #PorG = 'put'

    # If the user wants to get a file from the server
    elif splitInput[0] == 'get':
        usrFileName = splitInput[-1]
        get(usrFileName)
        #PorG = 'get'

    # If user chooses to quit
    elif usrInput.strip() == 'q':
        print("Exiting")
        sys.exit(0)

    # If user puts invalid input
    else:
        print("Invalid please try again, enter 'q' to exit")
        




#print("Input lowercase msg")
#message = sys.stdin.readline()[:-1]     # delete final \n
#message = input("Input lowercase msg:")
#clientSocket.sendto(message.encode(), serverAddr)
#modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
#print("Modified message from %s is <%s>" % (repr(serverAddrPort), modifiedMessage))
