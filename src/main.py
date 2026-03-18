import os
import pandas as pd
from extractor import extract_text_from_pdf
from llm_parser import parse_lease_data

# Define relative paths based on the repository structure
RAW_PDF_DIR = os.path.join(os.path.dirname(__file__), "../data/raw_pdfs/")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "../data/processed_data/lease_summary.csv")

def process_all_leases():
    """Orchestrates the extraction and parsing pipeline."""
    print("Starting DocuParse AI Pipeline...")
    results = []
    
    if not os.path.exists(RAW_PDF_DIR):
        print(f"Directory {RAW_PDF_DIR} does not exist. Please create it.")
        return

    pdf_files = [f for f in os.listdir(RAW_PDF_DIR) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the raw data directory. Add sample leases to begin.")
        return

    for filename in pdf_files:
        file_path = os.path.join(RAW_PDF_DIR, filename)
        print(f"Processing: {filename}")
        
        # Step 1: Extract Text
        raw_text = extract_text_from_pdf(file_path)
        
        # Step 2: Parse with LLM
        if raw_text.strip():
            extracted_data = parse_lease_data(raw_text)
            extracted_data['source_file'] = filename
            results.append(extracted_data)
            print(f"Success: Extracted {extracted_data.get('tenant_name')} | ${extracted_data.get('rent_amount')}")
        else:
            print(f"Warning: No text extracted from {filename}")

    # Step 3: Save to CSV
    if results:
        df = pd.DataFrame(results)
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\nPipeline Complete. Data saved to {OUTPUT_CSV}")
        print("\nOutput Preview:")
        print(df.head())

if __name__ == "__main__":
    process_all_leases()