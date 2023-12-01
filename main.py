from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import reader
from typing import Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process_image")
async def process_image(file: Union[UploadFile, None]):
    try:
        result = reader.readtext( file.file.read(), paragraph=True)
        return [item[1].upper() for item in result]

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
