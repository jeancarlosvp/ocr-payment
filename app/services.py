import easyocr as ocr

def get_ocr_model():
    reader = ocr.Reader(['en'], model_storage_directory='.')
    return reader