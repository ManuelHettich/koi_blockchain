import sys
import requests

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} host port")
        sys.exit()
    else:
        host = sys.argv[1]
        port = sys.argv[2]

        print("[send] / [check] a local file or [quit]")

        while True:
            # Ask for an input from user
            user_input = input("> ").split()

            # Parse command and filename from provided user input
            command = user_input[0]
            filename = user_input[1]

            if command == "quit":
                # Quit program
                exit()
            elif command == "send":
                # Send a new file to the blockchain server
                # TODO: Create Blocks from local file
                file = {"file": open(filename, "rb")}
                response = requests.post(f"http://{host}:{port}/send", files=file)
                print(response.text)
            elif command == "check":
                # Check if a local file is stored on the blockchain server
                file = {"file": open(filename, "rb")}
                response = requests.post(f"http://{host}:{port}/check", files=file)
                print(response.text)
            else:
                print("provided command is unknown")
                print("[send] / [check] a local file or [quit]")
