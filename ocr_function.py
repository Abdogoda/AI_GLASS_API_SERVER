import cv2
import pytesseract
import pyttsx3
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image_to_text(image_path, lang=None):
 image = cv2.imread(image_path) 

 frame_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Ensure grayscale

 # Optional: Enhance for OCR (adjust as needed)
 frame_enh = cv2.adaptiveThreshold(frame_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 85, 11)

 # Perform OCR
 if(lang == 'ar'):
  txt = pytesseract.image_to_string(frame_enh)
 else:
  txt = pytesseract.image_to_string(frame_enh, lang='ara',config= ".")

 # Text-to-Speech
 if txt:
  return txt
 else:
  return "NO TEXT TO DETECT"


def test_ocr():
 print(ocr_image_to_text("static/logo.png"))
 print(ocr_image_to_text("static/logo.png", lang="ar"))
