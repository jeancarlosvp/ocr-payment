from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
import requests
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

OCR_SPACE_API_KEY = "helloworld"  # Reemplaza esto con tu clave de API de OCR.Space

def resize_image(image_bytes, target_size=(800, 1200)):
    # Abrir la imagen y convertirla a modo RGB
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

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

            # Configurar la URL de la API de OCR.Space
            ocr_space_url = "https://api.ocr.space/parse/image"
            ocr_space_payload = {
                "apikey": OCR_SPACE_API_KEY,
                "language": "eng",  # Puedes ajustar el idioma según tus necesidades
                "OCREngine": 2
            }

            # Enviar la solicitud a OCR.Space
            response = requests.post(
                ocr_space_url,
                files={"file": ("image.jpg", resized_image)},
                data=ocr_space_payload,
            )

            # Procesar la respuesta JSON de OCR.Space
            ocr_result = response.json()
            print(ocr_result)
            parsed_text = [item["ParsedText"].upper() for item in ocr_result["ParsedResults"]]

            # Separar cada cadena en la lista usando '\n' como separador
            textos_separados = [texto.strip() for texto in parsed_text[0].split('\n') if texto.strip()]

            # Imprimir los textos separados
            for texto in textos_separados:
                print(texto)

            return textos_separados

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
