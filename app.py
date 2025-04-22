from flask import Flask, render_template, request
import os
from utils import extract_text, extract_info  # ✅ Importing Step 3 & 4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        resume_file = request.files['resume']
        if resume_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(file_path)
            extracted_text = extract_text(file_path)
            extracted_info = extract_info(extracted_text)
            return render_template('result.html', info=extracted_info)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
