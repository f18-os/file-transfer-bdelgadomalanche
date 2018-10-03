#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

#Reused Dr. Freudenthal's Client code for the most part

inputStr = input("Input your file's name: ")
#If file does not exist it will keep prompting the user to send the name of an existing file
while not os.path.exists(inputStr):
    print("Invalid File, Try Again")
    inputStr = input("Input your file's name: ")

inFile = open(inputStr, "r")

#Try catch block to handle errors while reading the file
try:
    #File's name is sent first to create file on server side
    print("sending name: " + inputStr)
    framedSend(s, bytes(inputStr.rstrip("\n\r"), encoding='ascii'), debug)
    print("received:", framedReceive(s, debug))
    
    #For every line in the file the client will send a message containing that line
    for line in inFile:
        if len(line) > 0:
            print("sending: " + line)
            framedSend(s, bytes(line.rstrip("\n\r"), encoding='ascii'), debug)
            print("received:", framedReceive(s, debug))
except:
    print("Error reading file")
