import os
import hashlib

# Lazy optional imports to support low-memory deployments without embeddings
_WITH_EMBEDDINGS = os.getenv("WITH_EMBEDDINGS", "false").lower() == "true"
_chroma_client = None
_collection = None
_model = None

def _ensure_embeddings_stack_loaded():
    global _chroma_client, _collection, _model
    if not _WITH_EMBEDDINGS:
        raise RuntimeError("Embeddings stack disabled. Set WITH_EMBEDDINGS=true to enable KB.")
    if _chroma_client is None:
        import chromadb  # heavy
        _chroma_client = chromadb.PersistentClient(path="data/chroma")
        _collection = _chroma_client.get_or_create_collection("liuba_knowledge")
    if _model is None:
        from sentence_transformers import SentenceTransformer  # heavy
        _model = SentenceTransformer("all-MiniLM-L6-v2")

def _make_id(fact: str) -> str:
    # Детерминированный ID по содержимому факта, чтобы избежать конфликтов и дубликатов
    return hashlib.sha1(fact.encode("utf-8")).hexdigest()

def add_fact(fact: str):
    """Добавить факт. Ничего не делает, если WITH_EMBEDDINGS=false."""
    if not _WITH_EMBEDDINGS:
        return
    _ensure_embeddings_stack_loaded()
    embedding = _model.encode([fact]).tolist()
    fid = _make_id(fact)
    _collection.upsert(documents=[fact], embeddings=embedding, ids=[fid])

def search_fact(query: str, top_k: int = 5, max_distance: float = 0.4):
    """Семантический поиск. Возвращает [] если WITH_EMBEDDINGS=false."""
    if not _WITH_EMBEDDINGS:
        return []
    _ensure_embeddings_stack_loaded()
    query_emb = _model.encode([query]).tolist()
    results = _collection.query(
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


