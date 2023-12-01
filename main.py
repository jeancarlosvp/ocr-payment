from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import reader
from PIL import Image
from io import BytesIO
from typing import Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def resize_image(image_bytes, target_size=(800, 1200)):
    # Abrir la imagen y convertirla a modo RGB
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    print(img.size)
    # Redimensionar la imagen
    img = img.resize(target_size)

    # Crear un objeto BytesIO para almacenar la imagen redimensionada
    buffered = BytesIO()

    # Guardar la imagen redimensionada en formato JPEG
    img.save(buffered, format="JPEG")

    # Obtener los bytes de la imagen redimensionada
    resized_image = buffered.getvalue()

    return resized_image

@app.post("/process_image")
async def process_image(file: Union[UploadFile, None]):
    try:
        if file is not None:
            # Redimensionar la imagen antes de realizar OCR
            resized_image = resize_image(file.file.read())

            # Realizar OCR en la imagen redimensionada
            result = reader.readtext(resized_image, paragraph=True)

            # Convertir a mayúsculas el segundo elemento de cada tupla en result
            processed_result = [item[1].upper() for item in result]

            return processed_result

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
