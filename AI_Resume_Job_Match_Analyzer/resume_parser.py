import fitz


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF resume.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text from the PDF
    """

    try:
        pdf_bytes = uploaded_file.read()

        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"Could not read PDF: {str(e)}")