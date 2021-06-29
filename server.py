import pickle
from fastapi import FastAPI, File, UploadFile
from block import Block

app = FastAPI()


@app.post("/send")
def send_file(file: UploadFile = File(...)):
    received_blocks: [Block] = pickle.loads(file.file.read())
    return {"hash": received_blocks[0].hash,
            "index_all": received_blocks[0].index_all,
            "hash_previous": received_blocks[0].hash_previous}


@app.get("/check")
def check_file(file_hash: str):
    return {"file_hash": file_hash}
