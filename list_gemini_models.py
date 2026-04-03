import os
import google.generativeai as genai

def list_models():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set")
        return
    
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(m.name)

if __name__ == "__main__":
    list_models()
