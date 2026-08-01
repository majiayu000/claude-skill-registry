# Embeddings

Text embeddings convert text into numerical vectors for semantic similarity, search, classification, and clustering.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Batch Embeddings](#batch-embeddings)
- [Task Types](#task-types)
- [Output Dimensionality](#output-dimensionality)
- [Normalizing Embeddings](#normalizing-embeddings)
- [Use Cases](#use-cases)

---

## Basic Usage

### Python
```python
from google import genai

client = genai.Client()

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?"
)

print(result.embeddings)
```

### JavaScript
```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: 'What is the meaning of life?',
});

console.log(response.embeddings);
```

### REST
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "model": "models/gemini-embedding-001",
        "content": {
            "parts": [{"text": "What is the meaning of life?"}]
        }
    }'
```

---

## Batch Embeddings

Generate embeddings for multiple texts at once.

### Python
```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=[
        "What is the meaning of life?",
        "What is the purpose of existence?",
        "How do I bake a cake?"
    ]
)

for embedding in result.embeddings:
    print(embedding)
```

### JavaScript
```javascript
const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: [
        'What is the meaning of life?',
        'What is the purpose of existence?',
        'How do I bake a cake?'
    ],
});

console.log(response.embeddings);
```

---

## Task Types

Specify task type to optimize embeddings for your use case.

| Task Type | Description | Use For |
|-----------|-------------|---------|
| `SEMANTIC_SIMILARITY` | Assess text similarity | Recommendations, duplicate detection |
| `CLASSIFICATION` | Classify by preset labels | Sentiment analysis, spam detection |
| `CLUSTERING` | Cluster by similarities | Document organization, anomaly detection |
| `RETRIEVAL_DOCUMENT` | Optimize for document search | Indexing articles, books, web pages |
| `RETRIEVAL_QUERY` | Optimize for search queries | Custom search (pair with RETRIEVAL_DOCUMENT) |
| `CODE_RETRIEVAL_QUERY` | Code search from natural language | Code suggestions (pair with RETRIEVAL_DOCUMENT) |
| `QUESTION_ANSWERING` | Find docs answering questions | Chatbots (pair with RETRIEVAL_DOCUMENT) |
| `FACT_VERIFICATION` | Retrieve evidence for statements | Fact-checking (pair with RETRIEVAL_DOCUMENT) |

### Example: Semantic Similarity

```python
from google.genai import types
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

texts = [
    "What is the meaning of life?",
    "What is the purpose of existence?",
    "How do I bake a cake?",
]

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
    config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
)

# Compute cosine similarity matrix
similarity = cosine_similarity([e.values for e in result.embeddings])
```

```javascript
const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: texts,
    taskType: 'SEMANTIC_SIMILARITY'
});
```

---

## Output Dimensionality

Control embedding size using Matryoshka Representation Learning. Default is 3072 dimensions.

**Recommended dimensions:** 768, 1536, 3072

### Python
```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?",
    config=types.EmbedContentConfig(output_dimensionality=768)
)

print(f"Length: {len(result.embeddings[0].values)}")  # 768
```

### JavaScript
```javascript
const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    content: 'What is the meaning of life?',
    outputDimensionality: 768,
});

console.log(`Length: ${response.embedding.values.length}`);  // 768
```

### REST
```bash
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent" \
    -H 'Content-Type: application/json' \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "content": {"parts":[{"text": "What is the meaning of life?"}]},
        "output_dimensionality": 768
    }'
```

---

## Normalizing Embeddings

The 3072-dimension output is normalized. For other dimensions (768, 1536), normalize manually for accurate cosine similarity:

```python
import numpy as np

embedding_values = np.array(result.embeddings[0].values)
normed_embedding = embedding_values / np.linalg.norm(embedding_values)

print(f"Norm: {np.linalg.norm(normed_embedding):.6f}")  # ~1.0
```

---

## Use Cases

| Use Case | Description |
|----------|-------------|
| **RAG** | Retrieve relevant context for generation |
| **Information Retrieval** | Search semantically similar documents |
| **Search Reranking** | Score initial results by semantic relevance |
| **Anomaly Detection** | Identify outliers in embedding clusters |
| **Classification** | Categorize text (sentiment, spam) |
| **Clustering** | Group related documents |

---

## Model Info

| Property | Value |
|----------|-------|
| Model | `gemini-embedding-001` |
| Input token limit | 2,048 |
| Output dimensions | 128-3072 (default: 3072) |
| Recommended dimensions | 768, 1536, 3072 |

---

## Resources

- [Embeddings Quickstart](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Embeddings.ipynb)
- [Document Search Tutorial](https://github.com/google-gemini/cookbook/blob/main/examples/Talk_to_documents_with_embeddings.ipynb)
- [Classification Tutorial](https://github.com/google-gemini/cookbook/blob/main/examples/Classify_text_with_embeddings.ipynb)
- [Clustering Tutorial](https://github.com/google-gemini/cookbook/blob/main/examples/clustering_with_embeddings.ipynb)
