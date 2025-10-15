import chromadb
from sentence_transformers import SentenceTransformer
import hashlib

# создаем persistent-клиент и коллекцию в папке data/chroma
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_or_create_collection("liuba_knowledge")

# модель для преобразования текста в векторы
model = SentenceTransformer("all-MiniLM-L6-v2")

def _make_id(fact: str) -> str:
    # Детерминированный ID по содержимому факта, чтобы избежать конфликтов и дубликатов
    return hashlib.sha1(fact.encode("utf-8")).hexdigest()

def add_fact(fact: str):
    """Добавить текстовый факт в базу знаний (id по содержимому, upsert)."""
    embedding = model.encode([fact]).tolist()
    fid = _make_id(fact)
    # upsert не упадёт, если такой id уже существует
    collection.upsert(documents=[fact], embeddings=embedding, ids=[fid])

def search_fact(query: str, top_k: int = 5, max_distance: float = 0.4):
    """Поиск по смыслу. Возвращает уникальные релевантные документы (строки).

    max_distance — порог косинусной дистанции (чем меньше, тем ближе). 0.4 ~ умеренно релевантно.
    """
    query_emb = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_emb,
        n_results=top_k,
        include=["documents", "distances"],
    )

    docs_batches = results.get("documents") or []
    dist_batches = results.get("distances") or []
    if not docs_batches:
        return []

    docs = docs_batches[0]
    dists = dist_batches[0] if dist_batches else [None] * len(docs)

    # Фильтрация по порогу дистанции и удаление дублей, сохранение порядка
    seen = set()
    filtered: list[str] = []
    for doc, dist in zip(docs, dists):
        if dist is not None and dist > max_distance:
            continue
        if doc in seen:
            continue
        seen.add(doc)
        filtered.append(doc)

    return filtered


