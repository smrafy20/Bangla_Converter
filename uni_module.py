from flask import Flask, request, render_template_string, send_file
import pdfplumber
from docx import Document
import os
import uuid
from unicodeconverter import convert_bijoy_to_unicode  # use wrapper module

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>PDF to Unicode DOCX Converter</title>
</head>
<body>
    <h2>Upload a Bangla PDF (Bijoy) to Convert to Unicode DOCX</h2>
    <form action="/convert" method="post" enctype="multipart/form-data">
        <input type="file" name="pdf_file" accept="application/pdf" required><br><br>
        <input type="submit" value="Convert">
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return "No file part"

    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file"

    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    extracted_text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            extracted_text += page.extract_text() + "\n"

    unicode_text = convert_bijoy_to_unicode(extracted_text)

    doc = Document()
    doc.add_paragraph(unicode_text)
    output_filename = f"converted_{uuid.uuid4()}.docx"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    doc.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
