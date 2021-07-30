import argparse
import sys
import pickle
import requests
from src import block

SERVER_ID = "8dbaaa72-ff7a-4f95-887c-e3109e577edd"


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

    # Ask for user input what to do next
    print("[send] / [check] a local file or [quit]")
    while True:
        # Ask for an input from user
        user_input = input("> ").split()

        if len(user_input) < 1 or len(user_input) > 2:
            print("[send] / [check] a local file or [quit]")
            continue

        # Parse command from provided user input
        command = user_input[0]
        # Quit program if the user entered "quit"
        if command == "quit":
            sys.exit()

        # Parse filepath from provided user input
        filepath = user_input[1]

        if command == "send":
            # Send a new file to the blockchain server
            send(filepath, host, port)

        elif command == "check":
            # Check if a local file is stored on the blockchain server by sending its
            # SHA256 hash (checksum)
            check(filepath, host, port)

        else:
            print("The provided command is unknown")
            print("[send] / [check] a local file or [quit]")


def check_connection(host: str, port: int):
    """
    Check if the given server is online and reports a correct ID.

    :param host: The IP address or hostname of the server
    :param port: The port of the server
    :return: None
    """
    connection_error = False
    try:
        response = requests.get(f"http://{host}:{port}/")
        if not response.ok or response.json()["ID"] != SERVER_ID:
            connection_error = True
    except requests.exceptions.RequestException:
        connection_error = True

    if connection_error:
        print("Could not connect to the given server and verify its authenticity")
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

    # Generate the necessary blocks of the local file
    blocks = block.generate_blocks(filepath)
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the server
    response = requests.post(f"http://{host}:{port}/send",
                             files={"file": blocks_pickled})
    # Print the response from the server
    print(f"Response from Server: {response.json()}")


def check(filepath: str, host: str, port: int):
    """
    Check if a given file is stored on the specified server using its
    SHA256 checksum (hash) and print the response of the server in the
    command line interface.

    :param filepath: The filepath of the file to be checked on the server
    :param host: The IP address or hostname of the server
    :param port: The port of the server
    :return: None
    """

    # Generate the SHA256 checksum of the given file
    file_hash = block.calculate_file_hash(filepath)
    response = requests.get(f"http://{host}:{port}/check",
                            params={"file_hash": file_hash})

    # Print the response from the server
    print(f"Response from Server: {response.json()}")


if __name__ == "__main__":
    main()
