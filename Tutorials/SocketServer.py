#!/usr/bin/env python3

import sys
import socket
import datetime

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f"usage: {sys.argv[0]} [port]")
        sys.exit()
    
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 21557

    # Create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    # Bind to localhost and given port
    s.bind(('localhost', port))
    # Passive, open and backlog
    s.listen(socket.SOMAXCONN)

    # Accept new connections from peer sockets
    try:
        while True:
            inSocket, addr = s.accept()
            print(f"Peer Socket Info: {inSocket.getsockname()}")
            inSocket.send(bytes(f"Hello {inSocket.getsockname()[0]}, nice to meet you\n", "utf-8"))
            inSocket.send(bytes(f"It's {datetime.datetime.now().strftime('%c')}\n", "utf-8"))
            inSocket.close()
    finally:
        s.close()