# Europeana RAG System Setup

A retrieval-augmented generation (RAG) prototype over cultural heritage data from Europeana.eu, combining semantic data modeling with LLM-based question answering.
This system uses LangChain, ChromaDB, and Ollama (Mistral or Gemini) to answer cultural heritage questions.

## Prerequisites

1.  **Ollama**: Install Ollama from [ollama.com](https://ollama.com/).
2.  **Pull Mistral**: Run the following command in your terminal:
    ```bash
    ollama pull mistral
    ```
3.  **Run Ollama**: Ensure the Ollama service is running.

## How to Use

1.  **Ingest Data**: Process the SIP archives and populate the vector store.
    ```bash
    python ingest.py
    ```
    *(Note: The current script has a limit of 10 records for testing. You can modify `ingest.py` to process more.)*

2.  **Query the System**:
    ```bash
    python query.py "What can you tell me about the objects in the database?"
    ```

### Option 2: Gemini (Cloud)

1.  **Ingest Data**:
    ```bash
    python gemini_ingest.py
    ```
   
2.  **Query the System**: 
    ```bash
    python gemini_query.py "What can you tell me about the objects in the database?"
    ```

## Constraints
