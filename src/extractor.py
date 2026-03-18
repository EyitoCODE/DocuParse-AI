import fitz  # PyMuPDF
import os

def extract_text_from_pdf(file_path):
    """
    Extracts all text from a given PDF file.
    Args:
        file_path (str): The absolute or relative path to the PDF.
    Returns:
        str: The extracted raw text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    text = ""
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text("text") + "\n"
        doc.close()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return text