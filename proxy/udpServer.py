#! /bin/python
from socket import *
import time
import select
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

cwd = os.getcwd()

###################################################################
#############             PUT METHOD         ######################
###################################################################
def put(fileName, numPacketsi, inputs, outputs):
    # If serverDirectory does not exist, create it as a subdirectory
    if not os.path.exists(cwd + '/serverDirectory/'):
        os.makedirs(cwd + '/serverDirectory')


    # Open the file in serverDirectory (creating it if it does not exist)
    fileOpen = open(os.path.join(cwd + '/serverDirectory/', fileName), 'wb+')
    fileOpen.close()

    
    #serverSocket.sendto(b"Received request, being sending file", clientAddrPort)
    #time.sleep(1)
    # While loop for receiving the body of the file and writing it to the one created on the server
    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 5)
        for s in readable:
            if s is serverSocket:
                sequenceNumber = 0 
                payload, port = serverSocket.recvfrom(2048)
                #select(5)
                #print("payload is: %s " % (payload.decode()))
                if not payload:
                    sys.exit(0)

                payload = payload.decode()
                sequenceNumber = payload[0]
                payload = payload[1:]
                # Replacing the '~`" back to '\n' new line character
                payload = payload.replace('~`', '\n')
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
    #                   serverSocket.sendto(str(sequenceNumber).encode() + b' packet(s) received ', clientAddrPort)
                except FileNotFoundError:
                    print("Error trying to receive file")
            else:
                if s in outputs:
                   outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]

    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            # No messages waiting so stop checking for writability.
           # print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            outputs.remove(s)
        else:
            #print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
            #s.send(next_msg)
            print("else")

        # Handle "exceptional conditions"
    for s in exceptional:
        #print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]

###################################################################
#############             BEGIN CODE         ######################
###################################################################
print("binding datagram socket to %s" % repr(serverAddr))

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
#print("ready to receive")

# Sockets from which we expect to read
inputs = [serverSocket]

# Sockets to which we expect to write
outputs = []

# Outgoing message queues (socket:Queue)
message_queues = {}

while 1:
    #message, clientAddrPort = serverSocket.recvfrom(2048)

    readable, writable, exceptional = select.select(inputs, outputs, inputs, 5)
    # Handle inputs
    for s in readable:
        if s is serverSocket:
            # A "readable" server socket is ready to accept a connection
            #connection, client_address = s.accept()

            # Recieving first message
            headerPayload, clientAddrPort = s.recvfrom(2048)
            print("from %s: rec'd connection" % (repr(clientAddrPort)))

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
                        PorG = pl[0]
                        fileName = pl[-1]

                    if PorG == 'put':
                        numPackets = pl[2]
                        put(fileName, numPackets, inputs, outputs)

                    elif PorG == 'get':
                        get(fileName)
                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)

                else:
                   # serverSocket.sendto(b"Invalid request, closing connection", clientAddrPort)
                    #clientAddrPort.close()
                    # Interpret empty result as closed connection
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    # Remove message queue
                    del message_queues[s]

            #connection.setblocking(0)
            #inputs.append(connection)

            # Give the connection a queue for data we want to send
            #message_queues[connection] = Queue.Queue()

        #else:
                    #message_queues[s].put(data)
    #print("from %s: rec'd connection" % (repr(clientAddrPort)))


    #message = sys.stdin.readline()[:-1]     # delete final \n
    #modifiedMessage = message.upper()
    #serverSocket.sendto(modifiedMessage, clientAddrPort)
    
                
