#! /usr/bin/env python3

import sys
sys.path.append("../../lib")       # for params

import os, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

#Reused Dr. Freudenthal's ForkServer code for the most part
while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    #Added states to let the server know how to handle the data being passed
    state = "nameCheck"
    fileName = ""
    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            
            #Code would get stuck adding empty lines so 
            #I just added a whitespace to get rid of the error
            if payload == b'':
                payload += b" "
                
            #In this state the name of the file is recieved and stored 
            #to create a file of the same nama as the one being read
            if state == "nameCheck":
                fileName = payload
                state = "firstRun"
                if debug: print("rec'd: ", payload)
                if not payload:
                    if debug: print("child exiting")
                    sys.exit(0)
                framedSend(sock, payload, debug)
            
            #In this state the file overwrites the file if it already exists in the server directory 
            elif state == "firstRun":
                f = open(fileName, "w+")
                f.write(payload.decode("ascii") + "\n")
                state = "continue"
                if debug: print("rec'd: ", payload)
                if not payload:
                    if debug: print("child exiting")
                    sys.exit(0)
                framedSend(sock, payload, debug)
            
            #This state appends after the firstRun state changes so that the data is added to the new file
            else:
                #If the payload is not None then it will continue append otherwise it will close the child
                if payload != None:
                    f = open(fileName, "a+")
                    f.write(payload.decode("ascii") + "\n")
                    state = "continue"
                    if debug: print("rec'd: ", payload)
                    if not payload:
                        if debug: print("child exiting")
                        sys.exit(0)
                    framedSend(sock, payload, debug)
                else:
                    print("File Sent")
                    sys.exit(0)
            
                
