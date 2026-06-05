from fastapi import UploadFile, File, Form
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "working"
    }