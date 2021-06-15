import pickle
from fastapi import FastAPI, File, UploadFile
import block

app = FastAPI()


@app.post("/send/")
def send_file(file: UploadFile = File(...)):
    received_block: block = pickle.loads(file.file.read())
    return {"hash": received_block.hash, "hash_previous": received_block.hash_previous}


@app.post("/check/")
def check_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
