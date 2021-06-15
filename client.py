import sys
import pickle
import requests
import block

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} host port")
        sys.exit()
    else:
        # Read in the hostname / address and port of the server from the command line arguments
        host = sys.argv[1]
        port = sys.argv[2]

        while True:
            print("[send] / [check] a local file or [quit]")

            # Ask for an input from user
            user_input = input("> ").split()

            if len(user_input) != 2:
                continue

            # Parse command and filename from provided user input
            command = user_input[0]
            filename = user_input[1]

            if command == "quit":
                # Quit program
                sys.exit()

            elif command == "send":
                # Send a new file to the blockchain server
                blocks = block.Block.generate_blocks(filename)
                for block in blocks:
                    response = requests.post(f"http://{host}:{port}/send",
                                             files={"file": pickle.dumps(block)})
                    print(response.text)

            elif command == "check":
                # Check if a local file is stored on the blockchain server
                file = {"file": open(filename, "rb")}
                response = requests.post(f"http://{host}:{port}/check",
                                         files=file)
                print(response.text)

            else:
                print("The provided command is unknown")
