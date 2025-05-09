from http.client import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, UploadFile, File
from typing import List
from gemini import get_gemini_response


origins = [
    "https://o0nomar0o.github.io"
]

all = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogCard(BaseModel):
    id: int
    posted_by: str
    title: str
    summary: str



@app.get("/blogs")
async def generate_blog():

    generated_blog = BlogCard(
        id=1,
        posted_by="Eve",
        title="Generated Title from ",
        summary="This is a fake summary.",
    )
    return [generated_blog]


@app.post("/files")
async def upload_files(files: List[UploadFile] = File(...)):

    uploaded_files = []

    try:
        responses = []

        for file in files:

            contents = await file.read()
            decoded_contents = contents.decode('utf-8', errors='ignore')
            print(file.filename)
            print(decoded_contents)

            bot_response = await get_gemini_response(decoded_contents)

            responses.append({
                "filename": file.filename,
                "response": bot_response
            })

            print(bot_response)

        return {"message": "Upload successful", "data": responses}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {e}")
