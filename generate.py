import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import load_retriever, retrieve

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are RulesBot — an assistant that helps University of Toronto students 
find information about CS professors based on real student reviews.

Answer ONLY using the context provided below. Do not use any outside knowledge.
If the context does not contain enough information to answer the question, say:
"I don't have enough information in my sources to answer that question."

Always mention which professor you are referring to by name.
Keep answers concise and grounded in what students actually said.

Always show source of the answer followed by text on the next line
eg.
[Source: Redit1.txt]
Text answer here  
"""

def generate_answer(query, chunks):
    # format retrieved chunks as context
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"\n--- Source {i+1} ({chunk['source']}) ---\n"
        context += chunk["text"] + "\n"

    prompt = f"""Context from student reviews:
{context}

Question: {query}

Answer based only on the context above:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    return response.choices[0].message.content

def ask(query):
    print(f"\nQuestion: {query}")
    print("Retrieving relevant chunks...")
    model, collection = load_retriever()
    chunks = retrieve(query, model, collection)
    print(f"Retrieved {len(chunks)} chunks from: {set(c['source'] for c in chunks)}")
    print("\nGenerating answer...")
    answer = generate_answer(query, chunks)
    print(f"\nAnswer:\n{answer}")
    return {"answer": answer, "sources": [c['source'] for c in chunks]}

if __name__ == "__main__":
    ask("Who is the best professor for first year CS at UofT?")