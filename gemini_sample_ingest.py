import os
from europeana_processor import EuropeanaDatasetProcessor
from europeana_record import EuropeanaRecord

# Constants
DATA_DIR = os.path.join("data", "europeana_dataset_sample")
OUTPUT_DIR = os.path.join("data", "records_txt")
MAX_RECORDS = 10

def sample_ingest():
    """
    Processes a sample of 10 Europeana records and saves their plain text versions.
    """
    print(f"Starting sample ingestion (limit: {MAX_RECORDS})...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        print(f"Created directory: {OUTPUT_DIR}")

    records_count = 0

    def record_handler(rdf_content: str):
        nonlocal records_count
        if records_count >= MAX_RECORDS:
            return

        try:
            record = EuropeanaRecord(rdf_content)
            rag_record = record.to_rag_record()
            text_content = rag_record.to_text()
            
            if text_content.strip():
                records_count += 1
                filename = f"record_{records_count}.txt"
                file_path = os.path.join(OUTPUT_DIR, filename)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text_content)
                
                print(f"Saved {filename}")
        except Exception as e:
            # Silently skip bad records as per existing patterns
            pass

    # Process dataset
    processor = EuropeanaDatasetProcessor(DATA_DIR)
    
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found.")
        return

    # The processor doesn't have an easy way to 'break' early, 
    # but the handler will ignore records after the limit.
    processor.process(record_handler)

    print(f"\nSample ingestion complete. Processed {records_count} records.")
    print(f"Files saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    sample_ingest()
