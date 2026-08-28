from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract


class PDFService:

    def read_pdf(self, uploaded_file):

        # 1. Try normal text extraction
        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        # If normal PDF text exists, return it
        if text.strip():
            return text

        # 2. No text found -> use OCR
        print("No text found. Using OCR...")

        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        )

        # Move file pointer back to the beginning
        uploaded_file.seek(0)

        # Read PDF as bytes
        pdf_bytes = uploaded_file.read()

        # Convert PDF pages to images
        images = convert_from_bytes(
            pdf_bytes,
            poppler_path=r"C:\\Users\\janak\\Downloads\\Release-26.02.0-0\\poppler-26.02.0\\Library\\bin"
        )

        # Extract text from images using OCR
        ocr_text = ""

        for image in images:
            page_text = pytesseract.image_to_string(image)

            if page_text:
                ocr_text += page_text + "\n"

        return ocr_text