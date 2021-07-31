"""
This module provides tests for the server module using pytest.
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


def test_server_send_positive():
    """
    Check if the server can correctly receive a new file.

    :return: None
    """

    # Generate the blocks for the test file
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/isaac-martin-61d2hT57MAE-unsplash.jpg")
    blocks = generate_blocks(test_file)
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send",
                           files={"file": blocks_pickled})
    assert response.ok
    assert response.json() \
           == {"success": True,
               "hash": "45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12",
               "index_all": 5285}


def test_server_check_positive():
    """
    Check if the server can correctly check a previously sent file.

    :return: None
    """

    # Generate the blocks for the test file
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/isaac-martin-61d2hT57MAE-unsplash.jpg")
    blocks = generate_blocks(test_file)
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send",
                           files={"file": blocks_pickled})

    # Send the SHA256 checksum of the file to the server to be checked
    response = client.get("/check",
                          params={"file_hash": blocks[0].hash,
                                  "index_all": blocks[0].index_all})
    assert response.ok
    assert response.json() \
           == {"check": True,
               "hash": "45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12"}


def test_server_check_negative():
    """
    Check if the server can correctly fail a check of a file which has not been previously sent
    to it.

    :return: None
    """

    # Generate the blocks for the test file which is not present on the server
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg")
    blocks = generate_blocks(test_file)

    # Send the SHA256 checksum of the file to the server to be checked
    response = client.get("/check",
                          params={"file_hash": blocks[0].hash,
                                  "index_all": blocks[0].index_all})
    assert response.ok
    assert response.json() \
           == {"check": False,
               "hash": "415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9"}


def test_server_send_second_file():
    """
    Check if the server can correctly receive a second file.

    :return: None
    """

    # Generate the blocks for the test file which is not present on the server
    test_file = os.path.join(os.path.dirname(__file__),
                             "../test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg")
    blocks = generate_blocks(test_file)
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send",
                           files={"file": blocks_pickled})
    assert response.ok
    assert response.json() \
           == {"success": True,
               "hash": "415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9",
               "index_all": 1704}


def test_server_integrity_check():
    """
    Check if the server can correctly check the integrity of its chain.

    :return: None
    """

    # Call the integrity check on the server
    response = client.get("/check_integrity")

    assert response.ok
    assert response.json() == {"integrity_check": True}
