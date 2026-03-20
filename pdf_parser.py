"""
pdf_parser.py
-------------
Handles PDF text extraction and text preprocessing.
"""

import re
import io


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from an uploaded PDF file using pypdf.

    Args:
        uploaded_file: Streamlit UploadedFile object (BytesIO-compatible)

    Returns:
        Extracted raw text as a string.

    Raises:
        ValueError: If the PDF has no extractable text.
        Exception: For any other parsing errors.
    """
    try:
        from pypdf import PdfReader

        # Read bytes from the uploaded file
        file_bytes = uploaded_file.read()
        pdf_reader = PdfReader(io.BytesIO(file_bytes))

        if len(pdf_reader.pages) == 0:
            raise ValueError("The uploaded PDF has no pages.")

        text_parts = []
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        if not text_parts:
            raise ValueError(
                "No text could be extracted from the PDF. "
                "It may be a scanned/image-only document."
            )

        return "\n".join(text_parts)

    except ImportError:
        raise ImportError(
            "pypdf is not installed. Run: pip install pypdf"
        )
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Failed to parse PDF: {str(e)}")


def clean_text(raw_text: str) -> str:
    """
    Clean and preprocess raw extracted text.

    Steps:
        - Strip leading/trailing whitespace
        - Collapse multiple blank lines into one
        - Normalize multiple spaces into single spaces
        - Remove non-printable/control characters (except newlines)

    Args:
        raw_text: Raw string to clean.

    Returns:
        Cleaned string.
    """
    if not raw_text or not raw_text.strip():
        return ""

    # Remove non-printable characters except newlines/tabs
    text = re.sub(r'[^\x20-\x7E\n\t]', ' ', raw_text)

    # Collapse multiple spaces (not newlines) into one
    text = re.sub(r'[ \t]+', ' ', text)

    # Collapse more than 2 consecutive newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Strip each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    return text.strip()


def preprocess_input(uploaded_file=None, raw_text: str = "") -> str:
    """
    High-level dispatcher: process either an uploaded PDF or raw text input.

    Args:
        uploaded_file: Streamlit UploadedFile (or None).
        raw_text: Pasted text string (or empty string).

    Returns:
        Cleaned text string ready to send to the LLM.

    Raises:
        ValueError: If both inputs are empty/None.
    """
    if uploaded_file is not None:
        raw = extract_text_from_pdf(uploaded_file)
        return clean_text(raw)
    elif raw_text and raw_text.strip():
        return clean_text(raw_text)
    else:
        raise ValueError(
            "No input provided. Please upload a PDF or paste your SOP text."
        )
