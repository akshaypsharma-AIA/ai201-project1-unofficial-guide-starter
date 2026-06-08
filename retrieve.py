import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_store"
TOP_K = 5

def load_retriever():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection("professor_reviews")
    return model, collection

def retrieve(query, model, collection):
    # embed the query using same model as chunks
    query_vector = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_vector,
        n_results=TOP_K
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    print("Loading retriever...")
    model, collection = load_retriever()

    # test query
    query = "Who is the best professor for first year CS?"
    print(f"\nQuery: {query}\n")
    chunks = retrieve(query, model, collection)

    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} (source: {chunk['source']}, distance: {chunk['distance']:.4f}) ---")
        print(chunk["text"][:300])
        print()