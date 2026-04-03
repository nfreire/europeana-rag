import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def test_embed():
    api_key = os.environ.get("GOOGLE_API_KEY")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2-preview")
    try:
        vector = embeddings.embed_query("test")
        print(f"Success! Vector length: {len(vector)}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_embed()
