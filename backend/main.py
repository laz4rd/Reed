from fastapi import UploadFile, File, Form
from fastapi import FastAPI
from backend.schemas import QueryRequest
from backend.rag import(
    initialize,
    ask_rag
)




app = FastAPI()

# @app.on_event("startup")
# def startup():

#     initialize()

@app.get("/")
def home():
    return {
        "status": "working"
    }
    
    
@app.post("/query")
def query(req: QueryRequest):

    answer = ask_rag(req.question)

    return {
        "answer": answer
    }
    
from pathlib import Path
from fastapi import UploadFile, File, Form

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)

# @app.post("/upload")
# async def upload(
#     course: str = Form(...),
#     unit: int = Form(...),
#     note_type: str = Form(...),
#     files: list[UploadFile] = File(...)
# ):

#     saved_files = []

#     for file in files:

#         file_path = UPLOAD_DIR / file.filename

#         with open(file_path, "wb") as f:
#             f.write(await file.read())

#         saved_files.append(str(file_path))

#     return {
#         "status": "success",
#         "files": saved_files
#     }
    
@app.post("/upload")
async def test_upload(
    course: str = Form(...),
    unit: int = Form(...),
    note_type: str = Form(...),
    file: UploadFile = File(...)
):
    uploaded_files = []
    
        
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    uploaded_files.append({
            "path": file_path,
            "course": course,
            "unit": unit,
            "note_type": note_type
        })
    
        
    
    initialize(uploaded_files)
    
    return {
        "status": "success",
        "uploaded": len(uploaded_files)
    }
    