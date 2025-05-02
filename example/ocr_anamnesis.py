import pytesseract
from PIL import Image
import PyPDF2
import docx

from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv('API_KEY')

from anamnesisai.openai import extract_fhir

def extract_text(file_path):
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif']:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text

def pipeline(file_path):
    result_string = extract_text(file_path)
    fhir_data = extract_fhir(result_string, openai_key)
    return fhir_data
