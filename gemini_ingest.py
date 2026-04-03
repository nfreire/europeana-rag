import os
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from europeana_processor import EuropeanaDatasetProcessor
from europeana_record import EuropeanaRecord

# Constants
DATA_DIR = os.path.join("data", "europeana_dataset_sample")
PERSIST_DIRECTORY = "chroma_db_gemini"
COLLECTION_NAME = "europeana_collection"

def ingest_data():
    """
    Processes the Europeana dataset and ingests it into ChromaDB using Gemini Embeddings.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    print("Starting Gemini ingestion process...")
    
    documents = []

    def record_handler(rdf_content: str):
        try:
            record = EuropeanaRecord(rdf_content)
            rag_record = record.to_rag_record()
            text_content = rag_record.to_text()
            
            if text_content.strip():
                doc = Document(
                    page_content=text_content,
                    metadata={"source": "europeana_dataset_sample"}
                )
                documents.append(doc)
        except Exception as e:
            # Errors are suppressed/logged as per EuropeanaRecord config
            pass

    # Process dataset
    processor = EuropeanaDatasetProcessor(DATA_DIR)
    
    # Using a subset for demonstration/testing if needed, 
    # but the requirement implies building the full system.
    processor.process(record_handler)

    print(f"Processed {len(documents)} documents. Initializing vector store with Gemini Embeddings...")

    # Initialize Gemini Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")

    # Initialize ChromaDB with the first batch
    import time
    BATCH_SIZE = 1
    total_docs = len(documents)
    
    if not documents:
        print("No documents to ingest.")
        return

    print(f"Ingesting in batches of {BATCH_SIZE} with delay...")
    
    # Create the vectorstore with the first batch
    first_batch = documents[:BATCH_SIZE]
    vectorstore = Chroma.from_documents(
        documents=first_batch,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )
    
    # Add remaining batches
    for i in range(BATCH_SIZE, total_docs, BATCH_SIZE):
        time.sleep(5)  # Avoid rate limits
        batch = documents[i:i + BATCH_SIZE]
        vectorstore.add_documents(batch)
        print(f"Ingested {min(i + BATCH_SIZE, total_docs)}/{total_docs} documents...")

    print(f"Ingestion complete. Vector store persisted at '{PERSIST_DIRECTORY}'.")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found.")
    else:
        ingest_data()
