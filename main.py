#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bijoy2unicode import converter
from PyPDF2 import PdfReader
import docx

# PDF filename - Update this line with your PDF filename
PDF_FILENAME = "bn.pdf"

def convert_pdf_to_docx(pdf_filename):
    """
    Extract text from PDF in the current directory,
    convert Bijoy encoded Bengali text to Unicode,
    and save as a DOCX file.
    
    Args:
        pdf_filename (str): Name of the PDF file in the current directory
    
    Returns:
        str: Path to the saved DOCX file
    """
    # Create Unicode converter
    unicode_converter = converter.Unicode()
    
    # Get the current directory and full paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, pdf_filename)
    docx_filename = os.path.splitext(pdf_filename)[0] + '.docx'
    docx_path = os.path.join(current_dir, docx_filename)
    
    # Extract text from PDF
    print(f"Processing PDF: {pdf_path}")
    pdf_text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Some pages might not have extractable text
                pdf_text += page_text + "\n\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    
    # Convert extracted text from Bijoy to Unicode
    print("Converting Bijoy text to Unicode...")
    try:
        unicode_text = unicode_converter.convertBijoyToUnicode(pdf_text)
    except Exception as e:
        print(f"Error during conversion: {e}")
        print("Saving original extracted text without conversion...")
        unicode_text = pdf_text
    
    # Save the Unicode text to a DOCX file
    try:
        # Create a new Document
        doc = docx.Document()
        
        # Add the converted text to the document
        doc.add_paragraph(unicode_text)
        
        # Save the document
        doc.save(docx_path)
        
        print(f"Successfully saved text to: {docx_path}")
        return docx_path
    except Exception as e:
        print(f"Error saving DOCX file: {e}")
        return None

def main():
    # Process the PDF
    result_path = convert_pdf_to_docx(PDF_FILENAME)
    
    if result_path:
        print(f"Conversion completed successfully. Output saved to: {result_path}")
    else:
        print("Conversion failed.")

if __name__ == "__main__":
    main()