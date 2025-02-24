import os
import pdfplumber
from django.conf import settings

def parse_resume(resume_object):
    file_path = resume_object.pdf_file.path
    raw_extracted_text = ""  # Initialize the variable

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:  # Iterate over pages
            text = page.extract_text()
            if text:  # Ensure text is not None before appending
                raw_extracted_text += text + "\n"

    return raw_extracted_text