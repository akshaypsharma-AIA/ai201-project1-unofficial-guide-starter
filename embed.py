import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "chunks/all_chunks.json"
CHROMA_DIR = "chroma_store"

def embed_and_store():
    print("Loading chunks...")
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Initialising ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # delete collection if exists so we can re-run cleanly
    try:
        client.delete_collection("professor_reviews")
    except:
        pass

    collection = client.create_collection("professor_reviews")

    print("Embedding and storing chunks...")
    texts = [c["text"] for c in chunks]
    sources = [c["source"] for c in chunks]
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    # embed in batches of 50
    batch_size = 50
    for i in range(0, len(chunks), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_sources = sources[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]

        embeddings = model.encode(batch_texts).tolist()

        collection.add(
            documents=batch_texts,
            embeddings=embeddings,
            metadatas=[{"source": s} for s in batch_sources],
            ids=batch_ids
        )
        print(f"Stored chunks {i} to {i+len(batch_texts)}")

    print(f"\nDone — {len(chunks)} chunks embedded and stored in ChromaDB")

if __name__ == "__main__":
    embed_and_store()