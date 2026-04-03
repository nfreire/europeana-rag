import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Constants
PERSIST_DIRECTORY = "chroma_db_gemini"
COLLECTION_NAME = "europeana_collection"

PROMPT_TEMPLATE = """
You are an expert on cultural heritage objects. Use ONLY the provided Context to answer the question.
If the answer isn't there, say "I don't find a matching work in the database."

Constraints:
- When mentioning a book, always format it as: Title by Author (Year).
- If multiple books match, list them in a bulleted list.

Context:
{context}

Question: {question}

Answer:
"""

def query_rag(query_text: str):
    """
    Queries the Gemini RAG system.
    """
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    # Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")

    # Load Vector Store
    if not os.path.exists(PERSIST_DIRECTORY):
        print(f"Error: Vector store '{PERSIST_DIRECTORY}' not found. Run gemini_ingest.py first.")
        return

    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

    # LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    # Prompt
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # Retrieval Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Execute
    print(f"\nGemini Query: {query_text}")
    print("Thinking...")
    response = rag_chain.invoke(query_text)
    print(f"\nResponse:\n{response}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gemini_query.py \"your question\"")
    else:
        query_rag(sys.argv[1])
