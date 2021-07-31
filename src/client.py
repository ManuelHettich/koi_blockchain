import argparse
import sys
import os
import pickle
import requests
from src import block

SERVER_ID = "8dbaaa72-ff7a-4f95-887c-e3109e577edd"

HELP_MSG = "[send] / [check] a local file (relative path from root folder) or [quit]"
ERROR_CMD_MSG = "The provided command is unknown or the filepath is missing"
ERROR_FILE_MSG = "Could not access the given filepath"
ERROR_SRV_MSG = "Could not connect to the given server and verify its authenticity"


def main():
    """
    Run the main client program by checking the connection to the server
    and asking the user for a command. It can send a given file to the server
    and check whether it is stored there.

    :return: None
    """

    # Read in the hostname / address and port of the server from the command line arguments
    # with argparse
    args = parse_arguments()
    host = args.host
    port = args.port

    # Check if the given server is online and reports a correct ID
    check_connection(host, port)

    while True:
        # Ask user for an input what to do next
        print(HELP_MSG)
        user_input = input("> ").split()

        # Wrong amount of inputs
        if len(user_input) < 1 or len(user_input) > 2:
            print(ERROR_CMD_MSG)
            continue

        # Only one input term
        if len(user_input) == 1:
            if user_input[0] == "quit":
                # Quit program if the user only entered "quit"
                sys.exit()
            else:
                print(ERROR_CMD_MSG)
                continue
        else:
            # In this case we have got 2 input terms from the user
            # Parse command and filepath from provided user input
            command = user_input[0]
            filepath = user_input[1]

            if command == "send":
                # Send a new file to the blockchain server
                send(filepath, host, port)

            elif command == "check":
                # Check if a local file is stored on the blockchain server by sending its
                # SHA256 hash (checksum)
                check(filepath, host, port)

            else:
                # Could not parse a correct command
                print(ERROR_CMD_MSG)
                print(HELP_MSG)


def check_connection(host: str, port: int):
    """
    Check if the given server is online and reports a correct ID.

    :param host: The IP address or hostname of the server
    :param port: The port of the server
    :return: None
    """

    connection_error = False
    try:
        # Check the root path of the server to see if it provides the correct ID
        response = requests.get(f"http://{host}:{port}/")
        if not response.ok or response.json()["ID"] != SERVER_ID:
            connection_error = True
    except requests.exceptions.RequestException:
        connection_error = True

    if connection_error:
        # A connection to the authenticated server could not be established
        print(ERROR_SRV_MSG)
        sys.exit()


def parse_arguments():
    """
    Read in the hostname / address and port of the server from the command line arguments
    with argparse

    :return: Arguments parsed from the CLI with argparse
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="hostname or ip address of the server, e.g. 127.0.0.1")
    parser.add_argument("port", help="port of the server, e.g. 8000", type=int)
    return parser.parse_args()


def send(filepath: str, host: str, port: int):
    """
    Send a given file to the specified server using the Block class
    and print the response of the server in the command line.

    :param filepath: The filepath of the file to be sent to the server
    :param host: The IP address or hostname of the server
    :param port: The port of the server
    :return: None
    """

    try:
        # Generate all the necessary blocks of the local file
        blocks = block.generate_blocks(filepath)

        # Collect all blocks into a single binary file using pickle
        blocks_pickled = pickle.dumps(blocks)

        # Check connection to the server and its authenticity
        check_connection(host, port)

        # Send the collected blocks in a single transfer to the server
        response = requests.post(f"http://{host}:{port}/send",
                                 files={"file": blocks_pickled})

        # Print the response from the server
        print(f"Response from Server: {response.json()}")
    except requests.exceptions.RequestException:
        print(ERROR_SRV_MSG)
        sys.exit()
    except IOError:
        print(ERROR_FILE_MSG)


def check(filepath: str, host: str, port: int):
    """
    Check if a given file is stored on the specified server using its
    SHA256 checksum (hash) as well as the correct number of blocks
    and print the response of the server in the command line interface.

    :param filepath: The filepath of the file to be checked on the server
    :param host: The IP address or hostname of the server
    :param port: The port of the server
    :return: None
    """

    try:
        # Generate the SHA256 checksum of the given file
        file_hash = block.calculate_file_hash(filepath)

        # Calculate the number of blocks needed for this file
        filesize = os.path.getsize(filepath)
        index_all = filesize // 500 + (filesize % 500 > 0)

        # Check connection to the server and its authenticity
        check_connection(host, port)

        # Send the SHA256 checksum of the file to the server to be checked
        response = requests.get(f"http://{host}:{port}/check",
                                params={"file_hash": file_hash,
                                        "index_all": index_all})

        # Print the response from the server
        print(f"Response from Server: {response.json()}")
    except requests.exceptions.RequestException:
        print(ERROR_SRV_MSG)
        sys.exit()
    except IOError:
        print(ERROR_FILE_MSG)


if __name__ == "__main__":
    main()
