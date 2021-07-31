"""
This module provides tests for most important functions in the different modules of the project.

@author: Manuel Hettich
"""

import pickle
import os
from fastapi.testclient import TestClient
from src.server import app
from src.block import generate_blocks

client = TestClient(app)


def test_server_connection():
    """
    Check the connection to the server.

    :return: None
    """
    response = client.get("/")
    assert response.ok
    assert response.json() == {"ID": "8dbaaa72-ff7a-4f95-887c-e3109e577edd"}


def test_send_positive():
    """
    Check if the server can correctly receive a new file.

    :return: None
    """

    # Generate the blocks for the test file
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/isaac-martin-61d2hT57MAE-unsplash.jpg")
    blocks = generate_blocks(test_file, '0')
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send",
                           files={"file": blocks_pickled})
    assert response.ok
    assert response.json() \
           == {"success": True,
               "new_file": True,
               "hash": "45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12",
               "index_all": 5285}


def test_check_positive():
    """
    Check if the server can correctly check a previously sent file, even if it is sent twice.

    :return: None
    """

    # Generate the blocks for the test file
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/isaac-martin-61d2hT57MAE-unsplash.jpg")
    blocks = generate_blocks(test_file, '0')
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send",
                           files={"file": blocks_pickled})

    assert response.ok
    assert response.json() \
           == {"success": True,
               "new_file": False,
               "hash": "45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12",
               "index_all": 5285}

    # Send the SHA256 checksum of the file to the server to be checked
    response = client.get("/check",
                          params={"file_hash": blocks[0].hash,
                                  "index_all": blocks[0].index_all})
    assert response.ok
    assert response.json() \
           == {"check": True,
               "hash": "45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12"}


def test_check_negative():
    """
    Check if the server can correctly fail a check of a file which has not been previously sent
    to it.

    :return: None
    """

    # Generate the blocks for the test file which is not present on the server
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg")
    # Ask the server for the hash of the last block
    response = client.get("/latest_block_hash")
    last_block_hash = response.json()["last_block_hash"]
    blocks = generate_blocks(test_file, last_block_hash)

    # Send the SHA256 checksum of the file to the server to be checked
    response = client.get("/check",
                          params={"file_hash": blocks[0].hash,
                                  "index_all": blocks[0].index_all})
    assert response.ok
    assert response.json() \
           == {"check": False,
               "hash": "415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9"}


def test_send_second_file():
    """
    Check if the server can correctly receive a second file.

    :return: None
    """

    # Generate the blocks for the test file which is not present on the server
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg")
    # Ask the server for the hash of the last block
    response = client.get("/latest_block_hash")
    last_block_hash = response.json()["last_block_hash"]
    blocks = generate_blocks(test_file, last_block_hash)
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send",
                           files={"file": blocks_pickled})
    assert response.ok
    assert response.json() \
           == {"success": True,
               "new_file": True,
               "hash": "415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9",
               "index_all": 1704}


def test_send_empty_file():
    """
    Check if the server can correctly handle an empty file.

    :return: None
    """

    # Generate the blocks for the empty test file which is not already present on the server
    empty_file = os.path.join(os.path.dirname(__file__), "../test_files/empty.txt")
    # Ask the server for the hash of the last block
    response = client.get("/latest_block_hash")
    last_block_hash = response.json()["last_block_hash"]
    block = generate_blocks(empty_file, last_block_hash)
    # Encode the generated block into a binary file using pickle
    block_pickled = pickle.dumps(block)
    # Send the encoded block to the test server
    response = client.post("/send",
                           files={"file": block_pickled})

    assert response.ok
    assert response.json() \
           == {"success": True,
               "new_file": True,
               "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
               "index_all": 1}

    # Send the SHA256 checksum of the empty file to the server to be checked
    response = client.get("/check",
                          params={"file_hash": block[0].hash,
                                  "index_all": block[0].index_all})
    assert response.ok
    assert response.json() \
           == {"check": True,
               "hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}


def test_integrity_check():
    """
    Check if the server can correctly check the integrity of its chain.

    :return: None
    """

    # Call the integrity check on the server
    response = client.get("/check_integrity")

    assert response.ok
    assert response.json() == {"integrity_check": True}
