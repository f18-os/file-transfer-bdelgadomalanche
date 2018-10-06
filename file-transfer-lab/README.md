Overview:
    -This lab uses Dr. Freundenthal's code to send a file via Client - Server 

Process:
    -The user is asked to input an input file
    -Once input is entered the program sends the name to the server to create a replica on its directory
    -The server forks once it receives a client
    -The client and server are kept in seperate directories to avoid overwriting the input file being used
        as it would share the name and path as the output file being created
    -The client then sends the data in the file every 100 bytes to the server
    -The server then appends the bytes to the new file that was created
    -After the server receives an empty payload it exits the child and waits for a new connection

Steps:
    -Run fileServer on its directory
    -Run fileClient on its directory
    -I provided 3 test files where fileClient is located
    -When you run fileClient, simply give it the exact name of the file you'd like to send to the server and press enter

Resources:
    -Used part of the source code from Framed-echo provided to us
    -Reused some of my code from the shell lab to read and write to files
    
Collaborators:
    -Found on COLLABOTATORS.md file
