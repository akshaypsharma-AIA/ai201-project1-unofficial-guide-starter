# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Student reviews of CS professors at the University of Toronto (UofT). 
This knowledge is valuable because official university channels only provide 
formal course descriptions and instructor bios — they don't capture real student 
experiences like teaching quality, exam difficulty, office hour availability, or 
which professors to avoid. Students rely on informal sources like Reddit and Rate 
My Professors to make course selection decisions.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/1694041 |
| 2 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/3121445 |
| 3 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/2340488 |
| 4 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/20260 |
| 5 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/1443534 |
| 6 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/3118690 |
| 7 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/2127391 |
| 8 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/30803 |
| 9 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/30200 |
| 10 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/69474 |
| 11 | Rate My Professors | Web page | https://www.ratemyprofessors.com/professor/3042719 |
| 12 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/n7h98q |
| 13 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/1tirtnu |
| 14 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/1ouc9zd |
| 15 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/11qau12 |
| 16 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/1kjq8ji |
| 17 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/2u8ral |
| 18 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/7kelyu |
| 19 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/4rdqw7 |
| 20 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/1ed0ww |
| 21 | Reddit r/UofT | Forum thread | https://www.reddit.com/r/UofT/comments/1e0xd39 |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**Two strategies used based on source type:
- RMP reviews: chunked by individual review (split on double newline) — each review 
  is already self-contained, averaging 50–150 characters
- Reddit threads: 500 characters with sentence-boundary detection (split at last 
  period or newline within the chunk)


**Overlap:**50 characters applied to Reddit chunks only. RMP reviews are 
self-contained so overlap is not needed.

**Why these choices fit your documents:
RMP reviews are short, independent opinions with one review per professor per student. 
Splitting by review preserves each complete opinion as a single retrievable unit. 
Breaking them by character would split mid-opinion and lose meaning.

Reddit threads are longer and conversational. Character-based chunking with overlap 
prevents mid-sentence splits. Critically, every Reddit comment chunk has the thread 
title and first 200 characters of the original post prepended, this solves the 
orphaned chunk problem where replies like "yeah she's great" have no context about 
which professor is being discussed without the thread header.

Chunk size of 500 characters (~125 tokens) fits comfortably within all-MiniLM-L6-v2's 
256 token limit, avoiding silent truncation.

**Final chunk count:**205 chunks total (167 Reddit + 38 RMP)

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**all-MiniLM-L6-v2 via sentence-transformers (local, free, no API key required)

**Production tradeoff reflection:**
all-MiniLM-L6-v2 is fast, free and runs locally — ideal for a student project. 
In production I would weigh four tradeoffs:

1. Domain specificity — a model trained on or fine-tuned for academic text would 
   likely place terms like "explains well" and "great lecturer" closer in vector 
   space than a general purpose model. Worth evaluating text-embedding-3-large 
   (OpenAI) for higher baseline accuracy, or instructor-xl which can be prompted 
   at inference time to approximate domain-specific embedding without retraining.

2. Multilingual support — UofT has a large international student population who 
   may write in mixed English/Mandarin or other languages. all-MiniLM handles 
   this poorly. A multilingual model like multilingual-e5-large would be worth 
   considering — it handles English just as well as monolingual models while 
   also supporting other languages in a single vector space.

3. Context length — all-MiniLM has a 256 token limit per chunk. At 500 characters 
   (~125 tokens) current chunks fit comfortably. However if chunking strategy 
   changes to larger chunks beyond ~1000 characters, truncation becomes a risk 
   and a model with longer context like text-embedding-3-large (8191 tokens) 
   would be necessary.

4. Latency vs accuracy — all-MiniLM is extremely fast but sacrifices some accuracy. 
   For a real-time student-facing app, that tradeoff is acceptable. For a high-stakes 
   system, a larger slower model would be worth the latency cost.

Fine-tuning the LLM itself is not warranted here — RAG provides the domain knowledge 
and the base model behaviour is sufficient for generating helpful answers from 
retrieved chunks.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are an assistant bot that helps University of Toronto students 
find information about CS professors based on real student reviews.

Answer ONLY using the context provided below. Do not use any outside knowledge.
If the context does not contain enough information to answer the question, say:
"I don't have enough information in my sources to answer that question."

Always mention which professor you are referring to by name.
Keep answers concise and grounded in what students actually said.

Always provide source name as reference followed by text answer on the next line. 
Structure outputs as follows
Example:
[Source: Reddit1.txt]
Text Answer here. 


**How source attribution is surfaced in the response:**
Retrieved chunks are formatted with a source label before being passed to the 
model:

    --- Source 1 (rmp_2.txt) ---
    Marina is one of the nicest profs I've ever had...

    --- Source 2 (redit7.txt) ---
    Thread: Best profs for CSC148...

The model is instructed to answer only from this labelled context. The Groq 
Llama 3.1 model naturally references source numbers and professor names in its 
answers because they appear explicitly in the formatted context. Low-relevance 
chunks are implicitly filtered by the top-k=5 retrieval — only the 5 most 
semantically similar chunks reach the model, reducing noise.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Who is the best professor for first year CS at UofT? | Paul Gries, Danny Heap, Diane Horton mentioned positively | Listed 6 professors with specific course recommendations and student quotes | Relevant | Accurate |
| 2 | What do students say about Paul Gries? | Mixed reviews — mostly positive, some critical | Surfaced both positive and negative reviews with source attribution | Relevant | Accurate |
| 3 | Who should I take for CSC148? | Danny Heap, Paul Gries, Diane Horton, David Liu | Listed correct professors but also showed raw chunk text in answer — generation partially leaked context | Partially relevant | Partially accurate |
| 4 | Which professors should I avoid and why? | CSC401 teaching team described as incompetent | "I don't have enough information" — retrieval failure, wrong chunks returned | Off-target | Inaccurate |
| 5 | What is the best dining hall at UofT? | Should say no information available | Correctly said "I don't have enough information" — grounding worked | Off-target (expected) | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professors should I avoid and why?
**What the system returned:**
I don't have enough information in my sources to answer that question.
**Root cause (tied to a specific pipeline stage):**
This is a retrieval failure at Stage 4. The query uses abstract intent-based language — "avoid" — which did not embed close enough in vector space to the relevant chunks in redit5.txt, a Reddit thread titled "Avoid CSC401 — I'm not even kidding." The embedding model all-MiniLM-L6-v2 is general purpose and did not learn that "avoid" in the context of professor selection maps to complaint vocabulary like "incompetent", "broken tests", and "unexplained deductions". Instead it retrieved chunks about general course recommendations which contained no negative opinions, leaving the model with no basis to answer.

This was confirmed by rephrasing the query to "avoid CSC401 professor" — the system immediately retrieved the correct chunks from redit5.txt and returned a specific, accurate answer about the CSC401 teaching team, citing broken tests, unexplained heavy deductions on assignments, and a lack of response from staff.

The root cause is that all-MiniLM-L6-v2 matches on surface vocabulary, not user intent. The chunks existed — the retriever just could not connect abstract intent to domain-specific complaint language.
**What you would change to fix it:**
Three fixes in order of implementation effort:

1. Query expansion — before embedding the query, use the LLM to rewrite it into multiple phrasings: "professors to avoid", "bad professors at UofT", "CSC courses with poor teaching." Retrieve against all variants and merge results. This costs one extra LLM call but significantly improves recall on intent-based queries.

2. Domain-specific embedding — instructor-xl accepts an instruction string at inference time such as "Represent a student question about professor quality at UofT." This steers the vector space toward academic review vocabulary without any retraining, placing "avoid" closer to "incompetent" and "broken tests."

3. Fine-tune the embedding model — build labelled training pairs marking similar intent: ("avoid this prof" ↔ "incompetent teaching team" = similar). Retrain the embedding model on these pairs so it learns domain-specific semantic relationships. Highest effort but most accurate long-term fix.
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

Planning the chunking strategy upfront in planning.md made a real difference when it came to writing chunk.py. Because I had already thought through the difference between RMP reviews and Reddit threads before touching any code, I naturally ended up with two separate functions — chunk_by_review for RMP and chunk_by_character for Reddit. The spec also pushed me to think about the orphaned chunk problem early, which led to the decision to prepend the thread title and first 200 characters of the original post to every Reddit comment chunk. That detail would probably have been missed if I had just started coding without planning.


**One way your implementation diverged from the spec, and why:**

The divergence was Reddit scraping. The specs assumed automated scraping via requests or PRAW, but Reddit now blocks unauthorized request entirely and getting developer API access requires account approval that takes days. The work around for me was manually downloading the JSON for each thread directly from the browser, which got the same data but required more manual effort than planned. 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* 

My planning.md chunking strategy section describing 
  500 character chunks with 50 character overlap, and the observation that 
  RMP reviews are short and self-contained while Reddit threads are long 
  and conversational.

- *What it produced:*

A chunk.py with two separate functions — chunk_by_character 
  for Reddit and chunk_by_review for RMP — plus a parse_reddit_json function 
  that extracts thread title, original post and comments from raw JSON, 
  prepending the thread title and first 200 characters of the original post 
  to every comment chunk.

- *What I changed or overrode:*

The initial version only prepended the thread 
  title to comments. I directed the AI to also include the first 200 characters 
  of the original post body after understanding that replies without the original 
  question context become orphaned chunks with no retrievable meaning.

**Instance 2**

- *What I gave the AI:*

The retrieval failure observed during evaluation, the query "which professors should I avoid and why?" returned no useful answer despite the corpus containing a relevant thread about CSC401. I described that rephrasing to "avoid CSC401 professor" returned the correct answer immediately.

- *What it produced:*

A detailed root cause analysis identifying this as a Stage 4 retrieval failure — the general purpose all-MiniLM-L6-v2 embedding model did not place abstract intent-based vocabulary like "avoid" close enough in vector space to complaint-specific vocabulary like "incompetent", "broken tests" and "unexplained deductions

- *What I changed or overrode:*

I added three specific fixes in order of implementation effort — query expansion via LLM rewriting, instructor-xl with domain-specific prompting, and full embedding model fine-tuning on labelled pairs. I chose not to implement any of them given the deadline but documented them as production improvements.
