---
name: vector-db
cluster: aimlops
description: "Handles vector databases for efficient storage and querying of high-dimensional vectors in AI/ML applications."
tags: ["vector-db","ai","ml"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "vector database ai ml search similarity"
---

# vector-db

## Purpose
This skill enables the management of vector databases for storing, indexing, and querying high-dimensional vectors, optimizing AI/ML workflows for tasks like similarity searches and embeddings.

## When to Use
Use this skill for AI/ML applications requiring fast vector similarity queries, such as building recommendation engines, semantic search in NLP, or image retrieval systems. Apply it when dealing with large-scale vector data (e.g., embeddings from models like BERT) to avoid brute-force comparisons.

## Key Capabilities
- Store vectors with metadata and perform efficient nearest-neighbor searches using indexes.
- Support distance metrics like cosine, Euclidean, and dot product for similarity calculations.
- Handle vector dimensions up to 2048 and scale to millions of entries.
- Integrate with embedding models for real-time vector generation and querying.

## Usage Patterns
Invoke this skill via CLI for quick operations or through API calls in code. Always set the environment variable `$VECTOR_DB_API_KEY` for authentication before use. For CLI, prefix commands with `vector-db` and use JSON config files for complex setups (e.g., `config.json` with `{ "dimension": 768, "metric": "cosine" }`). In code, use HTTP requests to the API endpoint, ensuring error checking on responses. Pattern: First, create an index; then, insert vectors; finally, query them.

## Common Commands/API
Use the CLI tool `vector-db` or the API at `https://api.openclaw.com/vector-db/v1`. Authentication requires `$VECTOR_DB_API_KEY` in headers.

- CLI Command: Create an index  
  `vector-db create index --name myindex --dimension 768 --metric cosine --file config.json`  
  This initializes a new index; ensure config.json specifies additional options like shards.

- CLI Command: Insert vectors  
  `vector-db insert --index myindex --vectors "[0.1, 0.2, 0.3]" --id vec1`  
  Vectors must be in JSON array format; use `--batch` flag for multiple inserts.

- API Endpoint: Query vectors  
  POST https://api.openclaw.com/vector-db/v1/indexes/myindex/query  
  Body: `{ "vector": [0.1, 0.2, 0.3], "top_k": 5 }`  
  Response: JSON array of nearest neighbors.

- API Endpoint: Delete index  
  DELETE https://api.openclaw.com/vector-db/v1/indexes/myindex  
  Include header: `Authorization: Bearer $VECTOR_DB_API_KEY`

Config format: Use JSON files like `{ "index_name": "myindex", "vector_size": 768, "distance": "cosine" }` for CLI operations.

## Integration Notes
Integrate with AI/ML tools by exporting vectors from models and using this skill for storage. Set `$VECTOR_DB_API_KEY` in your environment or .env file. For Python integration, use requests library:  
```python
import requests  
headers = {'Authorization': f'Bearer {os.environ.get("VECTOR_DB_API_KEY")}' }  
response = requests.post('https://api.openclaw.com/vector-db/v1/indexes/myindex/insert', json={'vectors': [[0.1, 0.2]]}, headers=headers)  
```  
Ensure the API base URL matches your deployment; handle rate limits by adding retries. For clustering with aimlops, link via shared IDs (e.g., use skill ID "vector-db" in workflows).

## Error Handling
Common errors include authentication failures (HTTP 401) from missing `$VECTOR_DB_API_KEY`, invalid vector dimensions (e.g., mismatch with index), or network issues. To handle:  
- Check for 401 errors and prompt user to set `$VECTOR_DB_API_KEY`.  
- For invalid inputs, use try-except in code:  
  ```python
  try:  
      response = requests.post(url, json=data)  
      response.raise_for_status()  
  except requests.exceptions.HTTPError as e:  
      print(f"Error: {e} - Check vector dimensions.")  
  ```  
- CLI errors show as "Error: Invalid metric specified"; fix by verifying command flags. Always validate inputs before sending requests.

## Concrete Usage Examples
1. **Example: Building a simple search engine**  
   First, create an index: `vector-db create index --name searchindex --dimension 512`.  
   Insert embeddings: `vector-db insert --index searchindex --vectors '[[0.5, 0.6], [0.7, 0.8]]' --ids 'doc1,doc2'`.  
   Query for similarities: Use API POST to `/indexes/searchindex/query` with body `{ "vector": [0.5, 0.6], "top_k": 3 }`.  
   This pattern is ideal for NLP, e.g., searching similar documents based on embeddings.

2. **Example: Image similarity in ML pipeline**  
   Generate image embeddings with a model, then store: `vector-db insert --index imageindex --vectors '[[0.1, 0.2, 0.3]]' --metadata '{"url": "image1.jpg"}'`.  
   Query for similar images: CLI `vector-db query --index imageindex --vector [0.1, 0.2, 0.3] --top_k 5`.  
   Integrate in code by fetching results and filtering by metadata, useful for recommendation systems.

## Graph Relationships
- Connected to cluster: aimlops (e.g., shares data pipelines with data-processing skills).
- Relates to: embedding-generation skills (for vector creation) and query-optimization tools (for enhancing searches).
- Links with: ai skills for ML model integration and ml skills for training data storage.
