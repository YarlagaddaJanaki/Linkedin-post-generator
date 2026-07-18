from pypdf import PdfReader


class PDFService:

    def read_pdf(self, uploaded_file):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text