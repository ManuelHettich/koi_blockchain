from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/send/")
def send_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/check/")
def check_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
