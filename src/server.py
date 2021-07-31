"""
This module provides all the functionalities of the server.
"""

import pickle
from fastapi import FastAPI, File, UploadFile
import uvicorn
from src.block import Block

blocks: [Block] = list()
app = FastAPI()


@app.get("/")
def health_check():
    """
    Indicate whether the server is online and reachable for the client. It also
    provides a unique ID to check its authenticity by the client.

    :return: A statement in JSON format with the unique ID of this server.
    """

    return {"ID": "8dbaaa72-ff7a-4f95-887c-e3109e577edd"}


@app.post("/send")
def send_file(file: UploadFile = File(...)):
    """
    Accept a list of Block objects encoded via pickle in a single transfer and store it in-memory
    in a list of lists (non-persistent).

    :param file: A list of Block objects encoded via pickle.dumps() related to a single file
    :return: The SHA256 hash checksum of the original file and the number of received Block
    objects as JSON
    """

    # Load the transferred Block instances as a list
    received_blocks: [Block] = pickle.loads(file.file.read())

    # Only store the received list of blocks if it is non-empty
    if len(received_blocks) > 0:
        blocks.append(received_blocks)

    # Return the hash of the original file and the number of blocks to the client as JSON
    return {"success": True,
            "hash": received_blocks[0].hash,
            "index_all": len(received_blocks)}


@app.get("/check")
def check_file(file_hash: str, index_all: int):
    """
    Accept the hash of a file and its number of blocks as query parameters and check if
    the corresponding file has already been sent and stored on this server with a valid
    integrity.

    :param file_hash: SHA256 hash checksum of a file stored on the client
    :param index_all: Number of blocks needed for the file stored on the client
    :return: The result of the check as JSON in the format {"check": boolean, "hash": file_hash}
    """

    # Boolean flag to indicate whether the file is stored on this server
    # and its integrity is valid
    integrity_valid = False

    # Find the right list of blocks in the server list and check its integrity
    for blocks_per_file in blocks:
        # Find the correct list of blocks
        if blocks_per_file[0].hash == file_hash:
            # Check the integrity of the file stored on the server
            integrity_valid = blocks_per_file[0]\
                .check_file_integrity(blocks_of_file=blocks_per_file,
                                      file_hash=file_hash,
                                      index_all=index_all)

    return {"check": integrity_valid, "hash": file_hash}


@app.get("/check_integrity")
def check_integrity():
    """
    Check the integrity of all the files on the server by checking their respective
    hashes sequentially, starting from the first block of each file.

    :return: The result of the integrity check as JSON in the format {"integrity_check": boolean}
    """

    # Go through each list of blocks stored on the server
    for blocks_per_file in blocks:
        counter = 1
        # Calculate the hash of the first block of each file
        current_block_hash = blocks_per_file[0].generate_hash()
        # Check if the next block of each file is present by checking
        # their attribute "hash_previous"
        while counter != len(blocks_per_file):
            next_block_found = False
            for block in blocks_per_file:
                if block.hash_previous == current_block_hash:
                    # Found the next sequential block in line
                    current_block_hash = block.generate_hash()
                    next_block_found = True
                    break
            if next_block_found:
                counter += 1
            else:
                # Could not find the correct next block in the chain
                return {"integrity_check": False}
    return {"integrity_check": True}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
