from fileinput import filename
from http.client import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, UploadFile, File
from typing import List

import gemini_v2

from gemini import get_gemini_response


origins = [
    "https://o0nomar0o.github.io"
]

all = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=all,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


######################################################################################################################################################################################



@app.post("/files_v2")
async def upload_files(files: List[UploadFile] = File(...)):
    try:

        responses = []
        combined_content = ""
        fn = ""
        for file in files:
            contents = await file.read()
            decoded_contents = contents.decode('utf-8', errors='ignore')
            combined_content += f"=== {file.filename} ===\n{decoded_contents}\n\n"
            fn = file.filename

        bot_response = await gemini_v2.get_gemini_response(combined_content)

        # Create response
        responses.append({
            "filename": fn,
            "response": bot_response
        })

        print(bot_response)

        return {"message": "Upload successful", "data": responses}

    except Exception as e:
        raise HTTPException()

