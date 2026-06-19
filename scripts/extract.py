import os
import json
from pathlib import Path
import pdfplumber
import docx

# Define directories based on the identified paths
CURRICULUM_DIR = Path("/Users/shyam/Desktop/A2000/Curriculum")
CAPSTONE_DIR = Path("/Users/shyam/Desktop/A2000/Capstone projects")

# Define output directory for Phase 0
OUTPUT_DIR = Path(__file__).parent / "extracted"

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}")
    return text

def process_directory(input_dir, category_name):
    print(f"Processing directory: {input_dir}")
    category_output_dir = OUTPUT_DIR / category_name
    category_output_dir.mkdir(parents=True, exist_ok=True)
    
    if not input_dir.exists():
        print(f"Directory {input_dir} does not exist.")
        return

    for root, _, files in os.walk(input_dir):
        for file in files:
            file_path = Path(root) / file
            output_filename = file_path.stem + ".txt"
            output_filepath = category_output_dir / output_filename
            
            extracted_text = ""
            if file.lower().endswith(".pdf"):
                print(f"Extracting PDF: {file}")
                extracted_text = extract_text_from_pdf(file_path)
            elif file.lower().endswith(".docx"):
                print(f"Extracting DOCX: {file}")
                extracted_text = extract_text_from_docx(file_path)
            else:
                continue
            
            if extracted_text.strip():
                with open(output_filepath, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                print(f"Saved extracted text to {output_filepath}")

def main():
    print("Starting Phase 0: Knowledge Extraction")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Extract from Curriculum
    process_directory(CURRICULUM_DIR, "curriculum")
    
    # Extract from Capstone Projects
    # We will specifically target the AI project first as per our Phase 1 plan
    ai_project_dir = CAPSTONE_DIR / "AI"
    process_directory(ai_project_dir, "capstone_projects/ai")
    
    print("Phase 0 Extraction Complete. Check the 'data/structured_knowledge' directory.")

if __name__ == "__main__":
    main()
