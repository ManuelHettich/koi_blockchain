import pickle
from fastapi import FastAPI, File, UploadFile
from block import Block

blocks: [Block] = list()
app = FastAPI()


@app.post("/send")
def send_file(file: UploadFile = File(...)):
    """
    Accept a list of Block objects encoded via pickle in a single transfer and store it in-memory
    in a list of lists (non-persistent).

    :param file: A list of Block objects encoded via pickle.dumps() related to a single file
    :return: The SHA256 hash checksum of the original file and the number of received Block
    objects as JSON
    """
    received_blocks: [Block] = pickle.loads(file.file.read())

    # Only store the received list of blocks if it is non-empty
    if len(received_blocks) > 0:
        blocks.append(received_blocks)

    # Return the hash of the original file and the number of blocks to the client as JSON
    return {"hash": received_blocks[0].hash,
            "index_all": len(received_blocks)}


@app.get("/check")
def check_file(file_hash: str):
    """
    Accept the hash of a file as query parameter and check if the corresponding file has already
    been sent and stored on this server.

    :param file_hash: SHA256 hash checksum of a file stored on the client
    :return: The result of the check as JSON in the format {"check": boolean}
    """
    for blocks_per_file in blocks:
        if blocks_per_file[0].hash == file_hash:
            return {"check": True}
    return {"check": False}
