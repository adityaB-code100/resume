from flask import Flask, render_template, request
import os

from flask_sqlalchemy import SQLAlchemy
from utils import extract_text, extract_info  # ✅ Importing Step 3 & 4

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
# MySQL config (XAMPP uses 'root' user with no password by default)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/resume'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    education = db.Column(db.Text)
    projects = db.Column(db.Text)
    skills = db.Column(db.Text)
    responsibilities = db.Column(db.Text)






@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        resume_file = request.files['resume']
        if resume_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(file_path)
            extracted_text = extract_text(file_path)
            extracted_info = extract_info(extracted_text)
            resume = Resume(
                name=extracted_info['Name'],
                email=extracted_info['Email'],
                phone=extracted_info['Phone'],
                education=extracted_info['Education'],
                projects=extracted_info['Projects'],
                skills=extracted_info['Skills & Interests'],
                responsibilities=extracted_info['Responsibilities']
            )
            db.session.add(resume)
            db.session.commit()
            return render_template('result.html', info=extracted_info)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
