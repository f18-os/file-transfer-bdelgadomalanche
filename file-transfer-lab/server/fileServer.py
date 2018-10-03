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

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    state = "nameCheck"
    fileName = ""
    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            print(payload)
            print(state)
            if state == "nameCheck":
                fileName = payload
                state = "firstRun"
                if debug: print("rec'd: ", payload)
                if not payload:
                    if debug: print("child exiting")
                    sys.exit(0)
                framedSend(sock, payload, debug)
                
            elif state == "firstRun":
                f = open(fileName, "w+")
                f.write(payload.decode("ascii") + "\n")
                state = "continue"
                if debug: print("rec'd: ", payload)
                if not payload:
                    if debug: print("child exiting")
                    sys.exit(0)
                framedSend(sock, payload, debug)
            
            else:
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
            
                
