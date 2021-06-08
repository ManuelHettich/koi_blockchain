#!/usr/bin/env python3

import sys
import socket

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"usage: {sys.argv[0]} host port [cmd]")
        sys.exit()

    if len(sys.argv) >= 3:
        host = sys.argv[1]
        port = int(sys.argv[2])

        # Open a connection to the host using the given port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        s.connect((host, port))

        print(f"My Socket Info: {s.getsockname()}")
        print(f"Peer Socket Info: {s.getpeername()}")
        print()
        
        # Send an (optional) command
        if len(sys.argv) == 4:
            command = sys.argv[3]
            print("Sending Bytes...")
            print()
            s.send(bytes(command, 'utf-8'))

        # Print the received data
        buffsize = 1024
        buffer = s.recv(buffsize)
        while buffer:
            print(buffer.decode('utf-8'))
            buffer = s.recv(buffsize)
        
        s.close()