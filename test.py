import os
import sys
from dotenv import load_dotenv

# Load environment variable (OLLAMA_BASE_URL)
load_dotenv()

# Add the current directory to the system path so that Python recognizes the application package.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from application.rag import embed, respond_rag, load_knowledge_base

def test_ollama_pipeline():
    print("="*50)
    print("START OLLAMA PIPELINE TESTING")
    print(f"OLLAMA_BASE_URL IN USED: {os.getenv('OLLAMA_BASE_URL')}")
    print("="*50)

    # 1. Check loading knowledge base
    try:
        kb = load_knowledge_base()
        print(f" [OK] Loaded Knowledge Base sucessfully! Total docs: {len(kb)}")
    except Exception as e:
        print(f" [X] Error loading Knowledge Base: {e}")
        return

    # 2. Check creating embedding (model: embeddinggemma)
    try:
        print("\n--- Testing Embedding ---")
        sample_text = "Ben Thanh Market is a famous destination."
        vector = embed(sample_text)
        print(f" [OK] Successfully created embedding!")
        print(f"      - Vector's size (Dimensions): {len(vector)}")
        print(f"      - First 5 values: {vector[:5]}")
    except Exception as e:
        print(f" [X] Error calling Embedding API: {e}")

    # 3. Check RAG Chat (Retrieval + generation with qwen3:4b)
    try:
        print("\n--- Testing RAG Chat & LLM ---")
        query = "Tell me about Ben Thanh Market"
        print(f"      - Test question: '{query}'")
        
        answer, sources = respond_rag(query)
        
        print(" [OK] Successfully got RAG response!")
        print(f"      - LLM's answer:\n{answer}")
        print(f"      - Sources:")
        for src in sources:
            print(f"        + ID: {src['id']} | Score: {src['score']:.4f} | Source: {src['source']}")
            
    except Exception as e:
        print(f" [X] Error calling RAG Chat API: {e}")

    print("\n" + "="*50)
    print("TEST DONE")
    print("="*50)

if __name__ == "__main__":
    test_ollama_pipeline()