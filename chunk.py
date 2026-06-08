import os
import json

DOCUMENTS_DIR = "documents"
CHUNKS_DIR = "chunks"
os.makedirs(CHUNKS_DIR, exist_ok=True)

CHUNK_SIZE = 500
OVERLAP = 50

def chunk_by_character(text, source_name):
    """For Reddit — character based chunking with overlap"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        if end < len(text):
            last_break = max(chunk.rfind(". "), chunk.rfind("\n"))
            if last_break > 100:
                end = start + last_break + 1
                chunk = text[start:end]
        chunk = chunk.strip()
        if len(chunk) > 50:
            chunks.append({"text": chunk, "source": source_name})
        start = end - OVERLAP
    return chunks

def chunk_by_review(text, source_name):
    """For RMP — each review is one chunk, split by double newline"""
    chunks = []
    reviews = text.split("\n\n")
    for review in reviews:
        review = review.strip()
        if len(review) > 50:
            chunks.append({"text": review, "source": source_name})
    return chunks

def parse_reddit_json(raw, filename):
    try:
        data = json.loads(raw)
        post = data[0]["data"]["children"][0]["data"]
        title = post["title"]
        body = post.get("selftext", "")
        comments = []
        for child in data[1]["data"]["children"]:
            comment = child["data"].get("body", "")
            if comment and comment not in ["[deleted]", "[removed]"]:
                # prepend thread title AND original post to every comment
                # this ensures no chunk is an orphan — every chunk carries full context
                comments.append(f"Thread: {title}\nContext: {body[:200]}\n{comment}")
        full_text = f"Thread: {title}\n\n{body}\n\n" + "\n\n".join(comments)
        return full_text
    except Exception as e:
        print(f"Could not parse {filename} as JSON: {e}")
        return None

def process_all():
    all_chunks = []

    for filename in os.listdir(DOCUMENTS_DIR):
        if filename == ".gitkeep":
            continue
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            raw = f.read()

        if len(raw) < 100:
            print(f"Skipping {filename} — too small")
            continue

        if filename.startswith("redit"):
            # Reddit — parse JSON then chunk by character with overlap
            text = parse_reddit_json(raw, filename)
            if not text:
                continue
            chunks = chunk_by_character(text, filename)

        else:
            # RMP — each review is its own chunk
            chunks = chunk_by_review(raw, filename)

        all_chunks.extend(chunks)
        print(f"{filename} → {len(chunks)} chunks")

    output_path = os.path.join(CHUNKS_DIR, "all_chunks.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    process_all()