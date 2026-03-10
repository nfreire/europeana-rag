# Europeana RAG System Setup

This system uses LangChain, ChromaDB, and Ollama (Mistral) to answer cultural heritage questions.

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

## Constraints
The system follows these rules from `Requirements.txt`:
- Uses ONLY provided context.
- Formats books as `Title by Author (Year)`.
- Rejects non-vegetarian recipe requests.
- Returns bulleted lists for multiple matches.