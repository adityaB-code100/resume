import fitz  # PyMuPDF
import docx2txt
import re

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    else:
        return ""

import re

def extract_info(text):
    name = text.split('\n')[0].strip()

    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.findall(r'\+?\d[\d\s]{9,}', text)

    education = re.search(r'EDUCATIOn(.*?)(PROjECTs|$)', text, re.IGNORECASE | re.DOTALL)
    projects = re.search(r'PROjECTs(.*?)(TEChnICAL|$)', text, re.IGNORECASE | re.DOTALL)
    skills = re.search(r'TEChnICAL SKILLs.*?InTEREsTs(.*?)(PosITIOns|$)', text, re.IGNORECASE | re.DOTALL)
    positions = re.search(r'PosITIOns of REsPOnsIBILITy(.*)', text, re.IGNORECASE | re.DOTALL)

    return {
        'Name': name,
        'Email': email[0] if email else "Not found",
        'Phone': phone[0] if phone else "Not found",
        'Education': education.group(1).strip() if education else "Not found",
        'Projects': projects.group(1).strip() if projects else "Not found",
        'Skills & Interests': skills.group(1).strip() if skills else "Not found",
        'Responsibilities': positions.group(1).strip() if positions else "Not found"
    }
