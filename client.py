import sys
import pickle
import requests
import block


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} host port")
        sys.exit()
    else:
        # Read in the hostname / address and port of the server from the command line arguments
        host = sys.argv[1]
        port = sys.argv[2]

        print("[send] / [check] a local file or [quit]")
        while True:
            # Ask for an input from user
            user_input = input("> ").split()

            if len(user_input) < 1 or len(user_input) > 2:
                print("[send] / [check] a local file or [quit]")
                continue

            # Parse command and filepath from provided user input
            command = user_input[0]
            filepath = user_input[1]

            if command == "quit":
                # Quit program
                sys.exit()

            elif command == "send":
                # Send a new file to the blockchain server

                # Generate the necessary blocks of the local file
                blocks = block.generate_blocks(filepath)
                # Collect all blocks into a single binary file using pickle
                blocks_pickled = pickle.dumps(blocks)
                # Send the collected blocks in a single transfer to the server
                response = requests.post(f"http://{host}:{port}/send",
                                         files={"file": blocks_pickled})
                # Print the response from the server
                print(f"Response from Server: {response.text}")

            elif command == "check":
                # Check if a local file is stored on the blockchain server by sending its
                # SHA256 hash (checksum)
                file_hash = block.calculate_file_hash(filepath)
                response = requests.get(f"http://{host}:{port}/check",
                                        params={"file_hash": file_hash})

                # Print the response from the server
                print(f"Response from Server: {response.text}")

            else:
                print("The provided command is unknown")
                print("[send] / [check] a local file or [quit]")

if __name__ == "__main__":
    main()
