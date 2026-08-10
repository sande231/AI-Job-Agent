from pypdf import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    return resume_text