import os
from langchain_google_genai import ChatGoogleGenerativeAI

def test_chat():
    api_key = os.environ.get("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    try:
        response = llm.invoke("Say hi")
        print(f"Success! Response: {response.content}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_chat()
