import os
from typing import List
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from europeana_processor import EuropeanaDatasetProcessor
from europeana_record import EuropeanaRecord

# Constants
DATA_DIR = os.path.join("data", "europeana_dataset_sample")
PERSIST_DIRECTORY = "chroma_db"
COLLECTION_NAME = "europeana_collection"

def ingest_data():
    """
    Processes the Europeana dataset and ingests it into ChromaDB.
    """
    print("Starting ingestion process...")
    
    documents = []

    def record_handler(rdf_content: str):
        try:
            # Parse RDF
            record = EuropeanaRecord(rdf_content)
            # Map to RAG record
            rag_record = record.to_rag_record()
            # Convert to text
            text_content = rag_record.to_text()
            
            if text_content.strip():
                # Create LangChain Document
                doc = Document(
                    page_content=text_content,
                    metadata={"source": "europeana_dataset_sample"}
                )
                documents.append(doc)
        except Exception as e:
            print(f"Error processing a record: {e}")

    # Process dataset
    processor = EuropeanaDatasetProcessor(DATA_DIR)
    processor.process(record_handler)

    print(f"Processed {len(documents)} documents. Initializing vector store...")

    # Initialize Embeddings
    embeddings = OllamaEmbeddings(model="mistral")

    # Initialize ChromaDB
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )

    print(f"Ingestion complete. Vector store persisted at '{PERSIST_DIRECTORY}'.")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory '{DATA_DIR}' not found.")
    else:
        ingest_data()
