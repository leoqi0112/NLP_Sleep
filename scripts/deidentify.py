from docx import Document
import pandas as pd
import os
import re
from uuid import uuid4
from tqdm import tqdm

DATA_DIR = 'data'
OUTPUT_DIR = 'output'
MAPPING_FILE = 'name_map.csv'

id_map = []

# Fixed Patient name and Birth date label format
name_pattern = re.compile(r'(Patient name:\s*)(.+)')
dob_pattern = re.compile(r'(Birth date:\s*)(\d{2}/\d{2}/\d{4})')

for filename in tqdm(os.listdir(DATA_DIR)):
    if filename.endswith('.docx'):
        doc_path = os.path.join(DATA_DIR, filename)
        doc = Document(doc_path)
        new_id = str(uuid4())[:8]
        name_found = None


        # Replace name with id and remove birth date
        for para in doc.paragraphs:
            if 'Patient name:' in para.text:
                match = name_pattern.search(para.text)
                if match:
                    name_found = match.group(2).strip()
                    para.text = f"Unique ID: {new_id}"
            
            if 'Birth date:' in para.text:
                para.text = dob_pattern.sub(r'\1[REMOVED]', para.text)

        if name_found:
            id_map.append({'patient_id': new_id, 'name': name_found})
            output_path = os.path.join(OUTPUT_DIR, f"{new_id}.docx")
            doc.save(output_path)

# Save to CSV
df = pd.DataFrame(id_map)
df.to_csv(MAPPING_FILE, index=False)

    