import argparse
import sys
import pickle
import requests
from lib import block


def main():
    # Read in the hostname / address and port of the server from the command line arguments
    # with argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname or ip address of the server, e.g. 127.0.0.1")
    parser.add_argument("port", help="port of the server, e.g. 8000", type=int)
    args = parser.parse_args()
    host = args.host
    port = args.port

    # Ask for user input what to do next
    print("[send] / [check] a local file or [quit]")
    while True:
        # Ask for an input from user
        user_input = input("> ").split()

        if len(user_input) < 1 or len(user_input) > 2:
            print("[send] / [check] a local file or [quit]")
            continue

        # Parse command and filepath from provided user input
        command = user_input[0]
        # Quit program if the user entered "quit"
        if command == "quit":
            sys.exit()
        filepath = user_input[1]
        if command == "send":
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
