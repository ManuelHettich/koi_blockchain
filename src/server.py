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


@app.get("/latest_block_hash")
def latest_block_hash():
    """
    Return the hash of the currently last block in the chain or '0' if there
    are no files stored on the server yet.

    :return: The hash of the last block in the chain or '0' encoded as JSON
    """

    if len(blocks) == 0:
        # There are no files stored on the server yet
        return {"last_block_hash": '0'}
    return {"last_block_hash": blocks[-1].generate_hash()}


@app.post("/send")
def send_file(file: UploadFile = File(...)):
    """
    Accept a list of Block objects encoded via pickle in a single transfer and store it in memory
    in a single list (non-persistent) if it is not already stored on the server.

    :param file: A list of all the Block objects encoded via pickle.dumps() related to a single file
    :return: The SHA256 hash checksum of the original file and the number of received Block
    objects as well as a success message and specifying whether it is a new file as JSON
    """

    # Load the transferred Block instances as a list
    received_blocks: [Block] = pickle.loads(file.file.read())
    file_hash = received_blocks[0].hash
    index_all = received_blocks[0].index_all

    # Only store the received list of blocks if it is non-empty and if it is a new file
    if len(received_blocks) > 0:
        for block in blocks:
            if block.hash == file_hash:
                # Return the hash of the original file and the number of blocks to the client
                return {"success": True,
                        "new_file": False,
                        "hash": file_hash,
                        "index_all": index_all}

        # Add the received blocks to the server list
        blocks.extend(received_blocks)

        # Return the hash of the original file and the number of blocks to the client as JSON
        return {"success": True,
                "new_file": True,
                "hash": received_blocks[0].hash,
                "index_all": len(received_blocks)}

    # Return an error message since the server did not receive any Block objects
    return {"success": False}


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

    # Find the first correct block in the server list and check its integrity
    for block_idx, block in enumerate(blocks):
        if block.hash == file_hash:
            # Check the integrity of the specified file stored on the server
            file_integrity = block \
                .check_file_integrity(blocks=blocks,
                                      index=block_idx,
                                      file_hash=file_hash,
                                      index_all=index_all)

            return {"check": file_integrity, "hash": file_hash}
    # Could not find a matching block on this server
    return {"check": False, "hash": file_hash}


@app.get("/check_integrity")
def check_integrity():
    """
    Check the integrity of all the files on the server by checking their respective
    hashes sequentially, starting from the first block.

    :return: The result of the integrity check as JSON in the format {"integrity_check": boolean}
    """

    if len(blocks) == 0:
        # There are no blocks stored on the server yet
        return {"integrity_check": True}

    # Initialise counter variables
    block_counter = 1
    num_blocks = len(blocks)
    current_block = blocks[0]
    current_block_hash = current_block.generate_hash()
    # next_block = list(filter(lambda block: block.hash_previous == current_block_hash))

    # The first block has to reference '0' as the previous hash
    if current_block.hash_previous != "0":
        return {"integrity_check": False}

    # Search the next block with the hash of the current block as its "hash_previous" attribute
    # until all blocks are accounted for
    while block_counter != num_blocks:
        next_block_found = False
        for block in blocks:
            if block.hash_previous == current_block_hash:
                # Found the next sequential block in line
                next_block_found = True
                current_block = block
                current_block_hash = current_block.generate_hash()
                break
        if next_block_found:
            block_counter += 1
        else:
            # Could not find the next block in the chain
            return {"integrity_check": block_counter == num_blocks}
    # Traversed successfully through all the blocks on the server
    return {"integrity_check": True}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
