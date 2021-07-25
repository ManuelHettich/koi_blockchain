import pickle
from fastapi.testclient import TestClient
from server import app
from lib.block import generate_blocks

client = TestClient(app)


def test_send_server():
    blocks = generate_blocks("test_files/isaac-martin-61d2hT57MAE-unsplash.jpg")
    # Collect all blocks into a single binary file using pickle
    blocks_pickled = pickle.dumps(blocks)
    # Send the collected blocks in a single transfer to the test server
    response = client.post("/send", files={"file": blocks_pickled})
    assert response.status_code == 200
    assert response.json() == {"hash": "45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12",
                               "index_all": 5285}
