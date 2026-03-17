---
name: cohere-api
cluster: ai-apis
description: "Cohere API for embeddings, RAG, reranking, and semantic search."
tags: ["ai-apis","api"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "keywords"
---

# cohere-api

## Purpose
This skill integrates the Cohere API to handle AI tasks like generating embeddings, implementing Retrieval-Augmented Generation (RAG), reranking results, and performing semantic search. It's designed for enhancing AI workflows with Cohere's language models, using real-time API calls for efficient processing.

## When to Use
Use this skill when processing text for vector embeddings in ML pipelines, building RAG systems for accurate query responses, reranking search results for relevance, or conducting semantic searches on large datasets. Apply it in scenarios requiring API-based AI enhancements, such as chatbots needing contextual retrieval or applications analyzing text similarity.

## Key Capabilities
- Generate embeddings: Convert text to vectors via the /embed endpoint, supporting models like "embed-english-v3.0" for up to 512 tokens per request.
- RAG implementation: Fetch and augment responses using /generate with external data sources, handling up to 2048 tokens for input and output.
- Reranking: Use the /rerank endpoint to score and reorder lists of texts based on query relevance, with options for top-k results.
- Semantic search: Leverage embeddings for similarity searches, integrating with vector databases like Pinecone or Weaviate.
- Rate limiting: API enforces 60 requests per minute; monitor usage via response headers.
- Model selection: Specify models in requests, e.g., "command" for generation or "embed-multilingual-v2.0" for cross-language embeddings.

## Usage Patterns
To use this skill, first set the environment variable for authentication: export COHERE_API_KEY=your_api_key. Then, make API calls via HTTP requests or the Cohere SDK. For embeddings, structure requests with JSON payloads containing text arrays. In RAG patterns, retrieve documents first, then pass them to /generate for context-aware responses. Always handle asynchronous patterns by checking response status codes. For reranking, pipe search results through the endpoint in a single call. Use try-except blocks in code to wrap API interactions for reliability.

## Common Commands/API
Interact with Cohere API endpoints using curl or Python SDK. Authentication requires the Bearer token from $COHERE_API_KEY.

- Embeddings endpoint: POST https://api.cohere.ai/v1/embed
  Example: curl -X POST https://api.cohere.ai/v1/embed -H "Authorization: Bearer $COHERE_API_KEY" -H "Content-Type: application/json" -d '{"texts": ["Hello world"], "model": "embed-english-v3.0"}'
  
- Generate endpoint (for RAG): POST https://api.cohere.ai/v1/generate
  Code snippet:
  import cohere; import os
  client = cohere.Client(api_key=os.environ['COHERE_API_KEY'])
  response = client.generate(model='command', prompt='Explain AI', max_tokens=50)

- Rerank endpoint: POST https://api.cohere.ai/v1/rerank
  Example: curl -X POST https://api.cohere.ai/v1/rerank -H "Authorization: Bearer $COHERE_API_KEY" -d '{"query": "best AI tools", "documents": ["OpenClaw is great", "Cohere is useful"], "top_n": 1}'

- Semantic search pattern: First generate embeddings, then compute cosine similarity in code.
  Code snippet:
  import numpy as np
  emb1 = response.body['embeddings'][0]  # From embed response
  emb2 = [0.1, 0.2, ...]  # Another embedding
  similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

Config formats: All requests use JSON; for SDK, pass dictionaries like {"model": "command", "prompt": "text"}.

## Integration Notes
Integrate by importing the Cohere SDK in your Python environment: pip install cohere. Set $COHERE_API_KEY as an environment variable for secure handling. In OpenClaw workflows, invoke this skill via function calls, e.g., using the skill ID "cohere-api" in agent prompts. For multi-step integrations, chain outputs: use embeddings from one call as input for RAG. Monitor API usage with Cohere's dashboard to avoid rate limits. Ensure HTTPS for all requests and handle regional endpoints if needed (e.g., us.cohere.ai).

## Error Handling
Common errors include 401 Unauthorized (missing or invalid API key), 429 Too Many Requests (rate limit exceeded), and 400 Bad Request (invalid JSON or parameters). To handle: Check response.status_code in code and retry with exponential backoff for 429 errors. For 401, verify $COHERE_API_KEY and log the issue. Use try-except blocks like this:
Code snippet:
try:
    response = client.embed(texts=["text"])
except cohere.CohereError as e:
    if e.http_status == 429:
        time.sleep(60)  # Wait and retry
    else:
        raise
Always validate inputs before API calls to prevent 400 errors, e.g., ensure text length is under 512 tokens.

## Concrete Usage Examples
**Example 1: Generating Embeddings for Semantic Search**
To create embeddings for a query and compare with documents:
First, set up: export COHERE_API_KEY=your_key
Then, run:
import cohere; import os
client = cohere.Client(api_key=os.environ['COHERE_API_KEY'])
emb_response = client.embed(texts=["What is AI?"])
query_emb = emb_response.body['embeddings'][0]
# Use query_emb for similarity search in a vector DB

**Example 2: Implementing RAG for Question Answering**
For RAG, retrieve context and generate a response:
Prepare documents array, e.g., docs = ["AI is machine intelligence."]
Code:
response = client.generate(
    model='command',
    prompt='What is AI? Context: ' + ' '.join(docs),
    max_tokens=100
)
print(response.body['generations'][0]['text'])  # Output the generated answer

## Graph Relationships
- Related to cluster: ai-apis (e.g., shares dependencies with other API-based skills like openai-api).
- Connected via tags: ai-apis, api (links to skills in similar categories for combined workflows).
- Outgoing: Provides inputs to skills like vector-stores for embedding-based searches.
