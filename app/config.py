from starlette import config
from app.services import get_ocr_model

config = config.Config("./.env")

CORS_ORIGINS = config("CORS_ORIGINS")

reader = get_ocr_model()
