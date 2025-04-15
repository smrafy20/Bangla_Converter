import os
from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import unicodeconverter
from docx import Document

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def convert_bijoy_pdf_to_unicode_docx(pdf_path, output_docx_path):
    bijoy_text = extract_text_from_pdf(pdf_path)
    unicode_text = unicodeconverter.convert_bijoy_to_unicode(bijoy_text)
    document = Document()
    for line in unicode_text.splitlines():
        document.add_paragraph(line)
    document.save(output_docx_path)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return "No file part"
        file = request.files['pdf_file']
        if file.filename == '':
            return "No selected file"
        if file:
            # Save uploaded file
            pdf_filename = file.filename
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
            file.save(pdf_path)

            # Create output .docx filename with the same name as input (just change extension)
            base_filename = os.path.splitext(pdf_filename)[0]
            docx_filename = base_filename + '.docx'
            docx_path = os.path.join(OUTPUT_FOLDER, docx_filename)

            # Convert and return the file
            convert_bijoy_pdf_to_unicode_docx(pdf_path, docx_path)
            return send_file(docx_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
