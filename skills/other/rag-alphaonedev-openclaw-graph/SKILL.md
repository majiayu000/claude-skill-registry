---
name: rag
cluster: aimlops
description: "Implements Retrieval-Augmented Generation for AI models to fetch and use external knowledge."
tags: ["rag","aiml","nlp"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "retrieval augmented generation ai ml nlp"
---

# rag

## Purpose
This skill implements Retrieval-Augmented Generation (RAG) for OpenClaw, enabling AI models to query external knowledge bases and integrate results into responses, enhancing accuracy for tasks like question-answering.

## When to Use
Use this skill when your AI needs dynamic access to external data, such as querying a vector database for real-time information in NLP tasks, handling knowledge gaps in models, or augmenting responses in chatbots. Avoid it for purely generative tasks without external dependencies.

## Key Capabilities
- Fetches documents from vector databases (e.g., Pinecone, FAISS) using similarity search.
- Integrates retrieved content into AI prompts for generation.
- Supports embedding models for query vectorization (e.g., via Hugging Face transformers).
- Handles chunking of large documents and relevance scoring.
- Configurable via JSON files for custom sources and thresholds.

## Usage Patterns
Always set the API key via environment variable: `export OPENCLAW_API_KEY=$SERVICE_API_KEY`. For CLI, use `openclaw rag` with required flags. In code, import the skill and call methods like `rag.retrieve()`. Pattern: Query -> Retrieve -> Augment -> Generate. Ensure queries are under 512 tokens to avoid truncation.

## Common Commands/API
- CLI Command: `openclaw rag query --db pinecone --index myindex --query "What is RAG?" --top-k 5`
  - Flags: `--db` specifies database (e.g., pinecone, faiss), `--index` for collection name, `--top-k` for result count, `--query` for search string.
- API Endpoint: POST /v1/rag/retrieve with JSON body: `{"query": "Explain AI", "db": "pinecone", "top_k": 3}`
  - Response: JSON object with keys like `"results"` (array of documents) and `"scores"`.
- Code Snippet (Python):
  ```python
  import openclaw
  client = openclaw.Client(api_key=os.environ['OPENCLAW_API_KEY'])
  results = client.rag.retrieve(query="What is NLP?", db="faiss", top_k=4)
  ```
- Config Format: JSON file (e.g., rag_config.json):
  ```
  {
    "db": "pinecone",
    "api_endpoint": "https://api.pinecone.io",
    "embedding_model": "text-embedding-ada-002"
  }
  ```
  Load it via: `openclaw rag config load --file rag_config.json`.

## Integration Notes
Integrate by wrapping RAG calls around your AI pipeline: First, call `rag.retrieve()` to get context, then pass it to your model's prompt. For multi-skill workflows, chain with "aiml" skills by piping outputs (e.g., use RAG results as input to a generation skill). Handle asynchronous calls with `await client.rag.retrieve_async()` in async environments. Test integrations in a sandbox with mock databases to verify data flow.

## Error Handling
Check for common errors like authentication failures (e.g., "401 Unauthorized" if $OPENCLAW_API_KEY is invalid) by verifying env vars first. For query errors, catch exceptions like `RetrievalError` and retry with exponential backoff: 
```python
try:
    results = client.rag.retrieve(query=query)
except openclaw.RetrievalError as e:
    if e.status_code == 404:
        print("Database not found; create index first.")
    else:
        raise
```
Log all errors with details (e.g., error codes, messages) and use `--debug` flag in CLI for verbose output. Always validate inputs (e.g., ensure query is a string) before calling.

## Concrete Usage Examples
1. **Example 1: CLI Query for Knowledge Retrieval**  
   Use to answer user questions: Run `openclaw rag query --db faiss --index docs_index --query "Summarize RAG technique" --top-k 3`. This retrieves top 3 documents from the "docs_index" database and outputs them. Pipe the result: `openclaw rag query ... | openclaw aiml generate --prompt "Use this context:"`.
   
2. **Example 2: Code Integration for AI Response**  
   In a Python script, augment a chatbot: 
   ```python
   query = "What is machine learning?"
   context = client.rag.retrieve(query=query, db="pinecone", top_k=2)
   full_prompt = f"Context: {context}\nAnswer: {query}"
   response = client.aiml.generate(prompt=full_prompt)
   print(response)
   ```
   This fetches relevant context and passes it to the AI for a informed response.

## Graph Relationships
- Related to: aiml (for generation integration), nlp (for text processing), vector-db (for data storage dependencies).
- Depends on: embedding skills for vectorization.
- Used by: knowledge-base skills for external data access.
