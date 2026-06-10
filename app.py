import gradio as gr
from generate import ask, load_retriever, retrieve, generate_answer

# load model and collection once at startup — not on every query
model, collection = load_retriever()

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    # retrieve relevant chunks
    chunks = retrieve(question, model, collection)
    
    # generate answer
    answer = generate_answer(question, chunks)
    
    # format sources for display
    sources = "\n".join(f"• {c['source']} (distance: {c['distance']:.4f})" 
                        for c in chunks)
    
    return answer, sources

with gr.Blocks(title="UofT CS Professor Review Bot") as demo:
    gr.Markdown("# UofT CS Professor Review Bot")
    gr.Markdown("Ask me anything about CS professors at the University of Toronto based on real student reviews.")
    
    inp = gr.Textbox(label="Your question", placeholder="e.g. Who is the best professor for CSC148?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()