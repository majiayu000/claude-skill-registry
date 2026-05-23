---
name: gemini-embeddings
description: Generate text embeddings using Gemini Embedding API via scripts/. Use for creating vector representations of text, semantic search, similarity matching, clustering, and RAG applications. Triggers on "embeddings", "semantic search", "vector search", "text similarity", "RAG", "retrieval".
license: MIT
version: 1.0.0
keywords: embeddings, semantic search, vector, similarity, clustering, RAG, retrieval, cosine similarity, gemini-embedding-001
---

# Gemini Embeddings

Generate high-quality text embeddings for semantic search, similarity analysis, clustering, and RAG (Retrieval Augmented Generation) applications through executable scripts.

## When to Use This Skill

Use this skill when you need to:
- Find semantically similar documents or texts
- Build semantic search engines
- Implement RAG (Retrieval Augmented Generation)
- Cluster or group similar documents
- Calculate text similarity scores
- Power recommendation systems
- Enable semantic document retrieval
- Create vector databases for AI applications

## Available Scripts

### scripts/embed.py
**Purpose**: Generate embeddings and calculate similarity

**When to use**:
- Creating vector representations of text
- Comparing text similarity
- Building semantic search systems
- Implementing RAG pipelines
- Clustering documents

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `texts` | Text(s) to embed (required) | `"Your text here"` |
| `--model`, `-m` | Embedding model | `gemini-embedding-001` |
| `--task`, `-t` | Task type | `SEMANTIC_SIMILARITY` |
| `--dim`, `-d` | Output dimensionality | `768`, `1536`, `3072` |
| `--similarity`, `-s` | Calculate pairwise similarity | Flag |
| `--json`, `-j` | Output as JSON | Flag |

**Output**: Embedding vectors or similarity scores

## Workflows

### Workflow 1: Single Text Embedding
```bash
python scripts/embed.py "What is the meaning of life?"
```
- Best for: Basic embedding generation
- Output: Vector with 3072 dimensions (default)
- Use when: Storing single document vectors

### Workflow 2: Semantic Search
```bash
# 1. Generate embedding for query
python scripts/embed.py "best practices for coding" --task RETRIEVAL_QUERY > query.json

# 2. Generate embeddings for documents (batch)
python scripts/embed.py "Coding best practices include version control" "Clean code is essential" --task RETRIEVAL_DOCUMENT > docs.json

# 3. Compare and find most similar (calculate similarity separately)
```
- Best for: Building search functionality
- Task types: `RETRIEVAL_QUERY`, `RETRIEVAL_DOCUMENT`
- Combines with: Similarity calculation for ranking

### Workflow 3: Text Similarity Comparison
```bash
python scripts/embed.py "What is the meaning of life?" "What is the purpose of existence?" "How do I bake a cake?" --similarity
```
- Best for: Comparing multiple texts, finding duplicates
- Output: Pairwise similarity scores (0-1)
- Use when: Need to rank text similarity

### Workflow 4: Dimensionality Reduction for Efficiency
```bash
python scripts/embed.py "Text to embed" --dim 768
```
- Best for: Faster storage and comparison
- Options: `768`, `1536`, or `3072` (default)
- Trade-off: Lower dimensions = less accuracy but faster

### Workflow 5: Document Clustering
```bash
# 1. Generate embeddings for multiple documents
python scripts/embed.py "Machine learning is AI" "Deep learning is a subset" "Neural networks power AI" --json > embeddings.jsonl

# 2. Process embeddings with clustering algorithm (your code)
# Use scikit-learn, KMeans, etc.
```
- Best for: Grouping similar documents, topic discovery
- Task type: `CLUSTERING`
- Combines with: Clustering libraries (scikit-learn)

### Workflow 6: RAG Implementation
```bash
# 1. Create document embeddings (one-time setup)
python scripts/embed.py "Document 1 content" "Document 2 content" --task RETRIEVAL_DOCUMENT --dim 1536

# 2. For each query, find similar documents
python scripts/embed.py "User query here" --task RETRIEVAL_QUERY

# 3. Use retrieved documents in prompt to LLM (gemini-text)
python skills/gemini-text/scripts/generate.py "Context: [retrieved docs]. Answer: [user query]"
```
- Best for: Building knowledge-based AI systems
- Combines with: gemini-text for generation with context

### Workflow 7: JSON Output for API Integration
```bash
python scripts/embed.py "Text to process" --json
```
- Best for: API responses, database storage
- Output: JSON array of embedding vectors
- Use when: Programmatic processing required

### Workflow 8: Batch Document Processing
```bash
# 1. Create JSONL with documents
echo '{"text": "Document 1"}' > docs.jsonl
echo '{"text": "Document 2"}' >> docs.jsonl

# 2. Process with script or custom code
python3 << 'EOF'
import json
from google import genai

client = genai.Client()

texts = []
with open("docs.jsonl") as f:
    for line in f:
        texts.append(json.loads(line)["text"])

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
    task_type="RETRIEVAL_DOCUMENT"
)

embeddings = [e.values for e in response.embeddings]
print(f"Generated {len(embeddings)} embeddings")
EOF
```
- Best for: Large document collections
- Combines with: Vector databases (Pinecone, Weaviate)

## Parameters Reference

### Task Types

| Task Type | Best For | When to Use |
|-----------|----------|-------------|
| `SEMANTIC_SIMILARITY` | Comparing text similarity | General comparison tasks |
| `RETRIEVAL_DOCUMENT` | Embedding documents | Storing documents for retrieval |
| `RETRIEVAL_QUERY` | Embedding search queries | Finding similar documents |
| `CLASSIFICATION` | Text classification | Categorizing text |
| `CLUSTERING` | Grouping similar texts | Document clustering |

### Dimensionality Options

| Dimensions | Use Case | Trade-off |
|------------|----------|-----------|
| 768 | High-volume, real-time | Lower accuracy, faster |
| 1536 | Balanced performance | Good accuracy/speed balance |
| 3072 | Highest accuracy | Slower, more storage |

### Similarity Scores

| Score | Interpretation |
|-------|---------------|
| 0.8 - 1.0 | Very similar (likely duplicates) |
| 0.6 - 0.8 | Highly related (same topic) |
| 0.4 - 0.6 | Moderately related |
| 0.2 - 0.4 | Weakly related |
| 0.0 - 0.2 | Unrelated |

## Output Interpretation

### Embedding Vector
- Format: List of float values (768, 1536, or 3072)
- Range: Typically -1.0 to 1.0
- Normalized for cosine similarity
- Can be stored in vector databases

### Similarity Output
```
Pairwise Similarity:
  'What is the meaning of life?...' <-> 'What is the purpose of existence?...': 0.8742
  'What is the meaning of life?...' <-> 'How do I bake a cake?...': 0.1234
```
- Higher scores = more similar
- Use threshold (e.g., 0.7) for matching

### JSON Output
```json
[[0.123, -0.456, 0.789, ...], [0.234, -0.567, 0.890, ...]]
```
- Array of embedding vectors
- One per input text
- Ready for database storage

## Common Issues

### "google-genai not installed"
```bash
pip install google-genai numpy
```

### "numpy not installed" (for similarity)
```bash
pip install numpy
```

### "Invalid task type"
- Use available tasks: SEMANTIC_SIMILARITY, RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, CLASSIFICATION, CLUSTERING
- Check spelling (case-sensitive)
- Use correct task for your use case

### "Invalid dimension"
- Options: 768, 1536, or 3072 only
- Check model supports requested dimension
- Default to 3072 if unsure

### "No similarity calculated"
- Need multiple texts for similarity comparison
- Use `--similarity` flag
- Check that at least 2 texts provided

### "Embedding size mismatch"
- All embeddings must have same dimensionality
- Use consistent `--dim` parameter
- Recompute if dimensions differ

## Best Practices

### Task Selection
- **SEMANTIC_SIMILARITY**: General text comparison
- **RETRIEVAL_DOCUMENT**: Storing documents for search
- **RETRIEVAL_QUERY**: Querying for similar documents
- **CLASSIFICATION**: Categorization tasks
- **CLUSTERING**: Grouping similar content

### Dimensionality Choice
- **768**: Real-time applications, high volume
- **1536**: Balanced choice for most use cases
- **3072**: Maximum accuracy, offline processing

### Performance Optimization
- Use lower dimensions for speed
- Batch multiple texts in one request
- Cache embeddings for repeated queries
- Precompute document embeddings for search

### Storage Tips
- Use vector databases (Pinecone, Weaviate, Chroma)
- Normalize vectors for consistent comparison
- Store metadata with embeddings
- Index for fast retrieval

### RAG Implementation
- Precompute document embeddings
- Use RETRIEVAL_DOCUMENT for docs
- Use RETRIEVAL_QUERY for user questions
- Combine top results with gemini-text

### Similarity Thresholds
- **0.9+**: Exact duplicates or near-duplicates
- **0.7-0.9**: Same topic/subject
- **0.5-0.7**: Related concepts
- **<0.5**: Different topics

## Related Skills

- **gemini-text**: Generate text with retrieved context (RAG)
- **gemini-batch**: Process embeddings in bulk
- **gemini-files**: Upload documents for embedding
- **gemini-search**: Implement semantic search (if available)

## Quick Reference

```bash
# Basic embedding
python scripts/embed.py "Your text here"

# Semantic search
python scripts/embed.py "Query" --task RETRIEVAL_QUERY

# Document embedding
python scripts/embed.py "Document text" --task RETRIEVAL_DOCUMENT

# Similarity comparison
python scripts/embed.py "Text 1" "Text 2" "Text 3" --similarity

# Dimensionality reduction
python scripts/embed.py "Text" --dim 768

# JSON output
python scripts/embed.py "Text" --json
```

## Reference

- Get API key: https://aistudio.google.com/apikey
- Documentation: https://ai.google.dev/gemini-api/docs/embeddings
- Vector databases: Pinecone, Weaviate, Chroma, Qdrant
- Cosine similarity: Standard for embedding comparison
