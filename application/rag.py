import json
import os
import numpy as np
import ollama
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_ollama_client():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return ollama.Client(host=base_url)

def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
    with open(kb_path, "r", encoding="utf-8") as f:
        return json.load(f)

def embed(text):
    response = get_ollama_client().embeddings(model="embeddinggemma", prompt=text)
    return response["embedding"]

def cosine_simi(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Global knowledge base embedded cache
@st.cache_resource
def get_cached_kb():
    kb = load_knowledge_base()
    kb_cache = []
    for doc in kb:
        doc_emb = embed(doc["text"])
        kb_cache.append({"doc": doc, "embedding": doc_emb})
    print("Finished caching Knowledge Base embeddings!")
    return kb_cache

def retrieve_top_k(query, k=3):
    kb_data = get_cached_kb()
    query_emb = embed(query)
    
    scored_docs = []
    for item in kb_data:
        # Generate embeddings for each text segment in the knowledge base (can be cached for optimization)
        score = cosine_simi(query_emb, item["embedding"])
        scored_docs.append((score, item["doc"]))
        
    # Sort in decreasing order
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return scored_docs[:k]

def respond_rag(query):
    top_docs = retrieve_top_k(query, k=2)
    
    context = ""
    sources = []
    for score, doc in top_docs:
        context += f"ID: {doc['id']}\nText: {doc['text']}\nSource: {doc['source']}\nScore: {score:.4f}\n\n"
        sources.append({"id": doc["id"], "score": score, "source": doc["source"]})

    system_prompt = (
        "You are a helpful travel assistant. You should quickly answer the user's question strictly using the provided context."
        "If you recommend a place, make sure to give them the location and opening hours of it."
        "You must cite the source IDs (e.g., [G01]) for every piece of information used."
        "If the answer cannot be found in the context, you must strictly output: 'I don't know'."
    )

    prompt = f"Context:\n{context}\nUser Question: {query}"

    print(f"Prompt sent to qwen3:4b:\n{query}")

    response = get_ollama_client().chat(
        model="qwen3:4b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    print(f"qwen3:4b answered:\n{response['message']['content']}")
    
    return response['message']['content'], sources