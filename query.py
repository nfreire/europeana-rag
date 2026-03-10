import sys
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Constants
PERSIST_DIRECTORY = "chroma_db"
COLLECTION_NAME = "europeana_collection"

PROMPT_TEMPLATE = """
You are an expert on cultural heritage objects. Use ONLY the provided Context to answer the question.
If the answer isn't there, say "I don't find a matching work in the database."

Constraints:
- When mentioning a book, always format it as: Title by Author (Year).
- If the user asks for 'meat-based' or 'non-vegetarian' recipes, politely inform them that this database focuses on plant-based and vegetarian resources.
- If multiple books match, list them in a bulleted list.

Context:
{context}

Question: {question}

Answer:
"""

def query_rag(query_text: str):
    """
    Queries the RAG system.
    """
    # Embeddings
    embeddings = OllamaEmbeddings(model="mistral")

    # Load Vector Store
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    # LLM
    llm = OllamaLLM(model="mistral")

    # Prompt
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # Retrieval Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": vectorstore.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Execute
    response = rag_chain.invoke(query_text)
    print(f"\nQuery: {query_text}")
    print(f"Response:\n{response}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query.py \"your question\"")
    else:
        query_rag(sys.argv[1])
