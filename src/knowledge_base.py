import chromadb
from sentence_transformers import SentenceTransformer

# создаем клиент и коллекцию
client = chromadb.Client()
collection = client.get_or_create_collection("liuba_knowledge")

# модель для преобразования текста в векторы
model = SentenceTransformer("all-MiniLM-L6-v2")

def add_fact(fact: str):
    """Добавить текстовый факт в базу знаний"""
    embedding = model.encode([fact]).tolist()
    collection.add(documents=[fact], embeddings=embedding, ids=[str(len(collection.get()['ids']) + 1)])

def search_fact(query: str, top_k: int = 3):
    """Поиск по смыслу"""
    query_emb = model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_emb, n_results=top_k)
    return results["documents"][0] if results["documents"] else []


