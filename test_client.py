import os
from europeana_processor import EuropeanaDatasetProcessor

from europeana_record import EuropeanaRecord

def rdf_handler(rdf_content: str):
    """
    Parses the RDF content and prints it as a RAG-friendly JSON.
    """
    try:
        record = EuropeanaRecord(rdf_content)
        rag_record = record.to_rag_record()
        print("-" * 40)
        print("RAG RECORD JSON:")
        print(rag_record.to_json())
        print("-" * 40)
    except Exception as e:
        print(f"Error processing record: {e}")

if __name__ == "__main__":
    data_folder = os.path.join("data", "europeana_dataset_sample")
    
    # Check if folder exists
    if not os.path.exists(data_folder):
        print(f"Error: Data folder '{data_folder}' not found.")
    else:
        processor = EuropeanaDatasetProcessor(data_folder)
        
        print(f"Starting to process ZIP files in {data_folder}...")
        
        # We'll use a counter to stop after a few records for the demonstration
        # so it doesn't print 1000s of records.
        count = 0
        MAX_RECORDS = 5
        
        def limited_handler(content):
            global count
            if count < MAX_RECORDS:
                rdf_handler(content)
                count += 1
            elif count == MAX_RECORDS:
                print(f"\n... Stopped after {MAX_RECORDS} records for demonstration.")
                count += 1

        processor.process(limited_handler)
        print("Processing finished.")
