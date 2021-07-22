# blockchain_project
[![Pylint](https://gitlab.ub.uni-bielefeld.de/manuel.hettich/blockchain_project/-/jobs/artifacts/main/raw/pylint/pylint.svg?job=pylint)](https://gitlab.ub.uni-bielefeld.de/manuel.hettich/blockchain_project)

Blockchain Server und Client für Netzwerkprogrammierung (SS2021)

## Starten des Servers
`$ uvicorn server:app`


## Starten & Verwendung des Clients
`$ python3 client.py 127.0.0.1 8000`

`> send test_files/isaac-martin-61d2hT57MAE-unsplash.jpg`
`> check test_files/isaac-martin-61d2hT57MAE-unsplash.jpg`
`> check test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg`

## Test-Cases

Filename: test_files/isaac-martin-61d2hT57MAE-unsplash.jpg
hash (SHA256-Hash): 45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12
index_all: 5285 


## Packages
fastapi: Web framework for building APIs with Python 3.6+ based on standard Python type hints
uvicorn: Necessary to start the server using FastAPI
python-multipart: Necessary to send large files as part of a POST request
requests: Necessary to send RESTful HTTP requests to the server
pytest: Necessary to execute unit tests in Python

The rest of the dependencies in requirements.txt are installed automatically alongside those
packages mentioned above.