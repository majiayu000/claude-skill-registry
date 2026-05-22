---
name: rag-system-builder
description: Build Retrieval-Augmented Generation (RAG) Q&A systems with Claude or OpenAI. Use for creating AI assistants that answer questions from document collections, technical libraries, or knowledge bases.
version: 1.2.0
last_updated: 2026-01-02
category: document-handling
related_skills:
  - knowledge-base-builder
  - semantic-search-setup
  - pdf-text-extractor
  - document-rag-pipeline
---

# RAG System Builder Skill

## Overview

This skill creates complete RAG (Retrieval-Augmented Generation) systems that combine semantic search with LLM-powered Q&A. Users can ask natural language questions and receive accurate answers grounded in your document collection.

## Quick Start

```python
from sentence_transformers import SentenceTransformer
import anthropic

# Setup
model = SentenceTransformer('all-MiniLM-L6-v2')
client = anthropic.Anthropic()

# Retrieve context (simplified)
query = "What are the safety requirements?"
query_embedding = model.encode(query, normalize_embeddings=True)
# ... search for similar chunks ...

# Generate answer
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}]
)
print(response.content[0].text)
```

## When to Use

- Building AI assistants for technical documentation
- Creating Q&A systems for standards libraries
- Developing chatbots with domain expertise
- Enabling natural language queries over knowledge bases
- Adding AI-powered search to existing document systems

## Architecture

```
User Question
      |
      v
+------------------+
| 1. Embed Query   |  sentence-transformers
+--------+---------+
         v
+------------------+
| 2. Vector Search |  Cosine similarity
+--------+---------+
         v
+------------------+
| 3. Retrieve Top  |  Top-K relevant chunks
+--------+---------+
         v
+------------------+
| 4. Build Prompt  |  Context + Question
+--------+---------+
         v
+------------------+
| 5. LLM Answer    |  Claude/OpenAI
+------------------+
```

## Prerequisites

- Knowledge base with extracted text (see `knowledge-base-builder`)
- Vector embeddings for semantic search (see `semantic-search-setup`)
- API key: `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`

## Implementation

### Step 1: Vector Embeddings Table

```python
import sqlite3
import numpy as np

def setup_embeddings_table(db_path):
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            chunk_id INTEGER UNIQUE,
            embedding BLOB,
            model_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chunk_id) REFERENCES chunks(id)
        )
    ''')

    conn.commit()
    return conn
```

### Step 2: Generate Embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2

    def embed_text(self, text):
        """Generate embedding for text."""
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.astype(np.float32)

    def embed_batch(self, texts, batch_size=100):
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=True
        )
        return embeddings.astype(np.float32)
```

### Step 3: Semantic Search

```python
def semantic_search(db_path, query, model, top_k=5):
    """Find most similar chunks to query."""
    conn = sqlite3.connect(db_path, timeout=30)
    cursor = conn.cursor()

    # Embed query
    query_embedding = model.embed_text(query)

    # Get all embeddings
    cursor.execute('''
        SELECT e.chunk_id, e.embedding, c.chunk_text, d.filename
        FROM embeddings e
        JOIN chunks c ON e.chunk_id = c.id
        JOIN documents d ON c.doc_id = d.id
    ''')

    results = []
    for chunk_id, emb_blob, text, filename in cursor.fetchall():
        embedding = np.frombuffer(emb_blob, dtype=np.float32)
        score = np.dot(query_embedding, embedding)  # Cosine similarity
        results.append({
            'chunk_id': chunk_id,
            'score': float(score),
            'text': text,
            'filename': filename
        })

    # Sort by similarity
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]
```

### Step 4: RAG Query Engine

```python
import anthropic
import openai

class RAGQueryEngine:
    def __init__(self, db_path, embedding_model):
        self.db_path = db_path
        self.model = embedding_model

    def query(self, question, top_k=5, provider='anthropic'):
        """Answer question using RAG."""

        # 1. Retrieve relevant context
        results = semantic_search(self.db_path, question, self.model, top_k)

        # 2. Build context string
        context = "\n\n---\n\n".join([
            f"Source: {r['filename']}\n{r['text']}"
            for r in results
        ])

        # 3. Build prompt
        prompt = f"""Based on the following technical documents, answer the question.
If the answer is not in the documents, say so.

DOCUMENTS:
{context}

QUESTION: {question}

ANSWER:"""

        # 4. Get LLM response
        if provider == 'anthropic':
            return self._query_claude(prompt), results
        else:
            return self._query_openai(prompt), results

    def _query_claude(self, prompt):
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _query_openai(self, prompt):
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### Step 5: CLI Interface

```python
#!/usr/bin/env python3
"""RAG Query CLI - Ask questions about your documents."""

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='RAG Q&A System')
    parser.add_argument('question', nargs='?', help='Question to ask')
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-k', '--top-k', type=int, default=5)
    parser.add_argument('--provider', choices=['anthropic', 'openai'], default='anthropic')

    args = parser.parse_args()

    engine = RAGQueryEngine(DB_PATH, EmbeddingGenerator())

    if args.interactive:
        print("RAG Q&A System (type 'quit' to exit)")
        while True:
            question = input("\nQuestion: ").strip()
            if question.lower() == 'quit':
                break
            answer, sources = engine.query(question, args.top_k, args.provider)
            print(f"\nAnswer: {answer}")
            print(f"\nSources: {[s['filename'] for s in sources]}")
    else:
        answer, sources = engine.query(args.question, args.top_k, args.provider)
        print(f"Answer: {answer}")
        print(f"\nSources:")
        for s in sources:
            print(f"  - {s['filename']} (score: {s['score']:.3f})")

if __name__ == '__main__':
    main()
```

## Prompt Engineering Tips

### System Prompt Template

```python
SYSTEM_PROMPT = """You are a technical expert assistant. Your role is to:
1. Answer questions based ONLY on the provided documents
2. Cite specific sources when possible
3. Acknowledge when information is not available
4. Be precise with technical terminology
5. Provide practical, actionable answers

If asked about topics not covered in the documents, say:
"I don't have information about that in the available documents."
"""
```

### Multi-Turn Conversations

```python
def query_with_history(self, question, history=[]):
    """Support follow-up questions."""
    context = self.get_relevant_context(question)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history
    for h in history[-4:]:  # Last 4 turns
        messages.append({"role": "user", "content": h['question']})
        messages.append({"role": "assistant", "content": h['answer']})

    # Add current question with context
    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {question}"
    })

    return self.llm.query(messages)
```

## Execution Checklist

- [ ] Set up knowledge base with text extraction
- [ ] Generate vector embeddings for all chunks
- [ ] Configure API keys (ANTHROPIC_API_KEY or OPENAI_API_KEY)
- [ ] Test semantic search independently
- [ ] Build and test RAG pipeline end-to-end
- [ ] Tune top_k parameter for answer quality
- [ ] Add source attribution to responses
- [ ] Implement error handling for API failures

## Error Handling

### Common Errors

**Error: anthropic.APIError (rate limit)**
- Cause: Too many API requests
- Solution: Add exponential backoff retry logic

**Error: Empty search results**
- Cause: No relevant documents in knowledge base
- Solution: Expand search with lower similarity threshold

**Error: Context too long**
- Cause: Top-k chunks exceed model context window
- Solution: Reduce top_k or chunk size

**Error: API key not found**
- Cause: Environment variable not set
- Solution: Export ANTHROPIC_API_KEY or OPENAI_API_KEY

**Error: Low quality answers**
- Cause: Poor retrieval or insufficient context
- Solution: Tune chunk size, overlap, and top_k parameters

## Metrics

| Metric | Typical Value |
|--------|---------------|
| Query latency (end-to-end) | 2-5 seconds |
| Retrieval time | <100ms |
| LLM response time | 1-4 seconds |
| Token usage per query | 500-2000 tokens |
| Answer relevance | 85-95% with good tuning |

## Performance Optimization

### 1. Cache Embeddings
```python
# Load all embeddings into memory at startup
self.embedding_cache = self._load_all_embeddings()
```

### 2. Use FAISS for Large Collections
```python
import faiss

# Build FAISS index for fast similarity search
index = faiss.IndexFlatIP(dimension)  # Inner product for cosine sim
index.add(embeddings)
```

### 3. Batch Queries
```python
# Process multiple questions efficiently
questions = ["Q1", "Q2", "Q3"]
query_embeddings = model.embed_batch(questions)
```

## Best Practices

1. **Chunk size matters** - 500-1500 chars optimal for context
2. **Retrieve enough context** - top_k=5-10 for comprehensive answers
3. **Include source attribution** - Always show which documents were used
4. **Handle edge cases** - Empty results, API errors, timeouts
5. **Monitor token usage** - Track costs and optimize prompts
6. **Use SQLite timeout** - `timeout=30` for concurrent access

## Example Usage

```bash
# Single question
./rag "What are the fatigue design requirements for risers?"

# Interactive mode
./rag -i

# With OpenAI
./rag --provider openai "Explain API 2RD requirements"
```

## Advanced: Hybrid Search (BM25 + Vector)

Combine keyword and semantic search for better results:

```python
import sqlite3
from rank_bm25 import BM25Okapi
import numpy as np

class HybridSearch:
    def __init__(self, db_path, embedding_model):
        self.db_path = db_path
        self.model = embedding_model
        self._build_bm25_index()

    def _build_bm25_index(self):
        """Build BM25 index from chunks."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, chunk_text FROM chunks')

        self.chunk_ids = []
        tokenized_corpus = []
        for chunk_id, text in cursor.fetchall():
            self.chunk_ids.append(chunk_id)
            tokenized_corpus.append(text.lower().split())

        self.bm25 = BM25Okapi(tokenized_corpus)
        conn.close()

    def search(self, query, top_k=10, alpha=0.5):
        """Hybrid search with alpha weighting.

        alpha=0.0: Pure BM25 (keyword)
        alpha=1.0: Pure vector (semantic)
        alpha=0.5: Balanced hybrid
        """
        # BM25 scores
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        bm25_scores = bm25_scores / (bm25_scores.max() + 1e-6)  # Normalize

        # Vector scores
        vector_results = semantic_search(self.db_path, query, self.model, top_k=len(self.chunk_ids))
        vector_scores = {r['chunk_id']: r['score'] for r in vector_results}

        # Combine scores
        combined = []
        for i, chunk_id in enumerate(self.chunk_ids):
            score = (1 - alpha) * bm25_scores[i] + alpha * vector_scores.get(chunk_id, 0)
            combined.append((chunk_id, score))

        combined.sort(key=lambda x: x[1], reverse=True)
        return combined[:top_k]
```

## Advanced: Reranking

Add a reranking step for improved precision:

```python
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, candidates, top_k=5):
        """Rerank candidates using cross-encoder."""
        pairs = [(query, c['text']) for c in candidates]
        scores = self.model.predict(pairs)

        for i, score in enumerate(scores):
            candidates[i]['rerank_score'] = float(score)

        reranked = sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
        return reranked[:top_k]

# Usage in RAG pipeline
def query_with_rerank(self, question, initial_k=20, final_k=5):
    # First pass: retrieve more candidates
    candidates = semantic_search(self.db_path, question, self.model, top_k=initial_k)

    # Second pass: rerank for precision
    reranked = self.reranker.rerank(question, candidates, top_k=final_k)

    return reranked
```

## Streaming Responses

For better UX with long answers:

```python
def query_streaming(self, question, top_k=5):
    """Stream RAG response for real-time display."""
    context = self.get_context(question, top_k)
    prompt = self.build_prompt(context, question)

    # Anthropic streaming
    with anthropic.Anthropic().messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text
```

## Related Skills

- `knowledge-base-builder` - Build the document database first
- `semantic-search-setup` - Generate vector embeddings
- `pdf-text-extractor` - Extract text from PDFs
- `document-rag-pipeline` - Complete end-to-end pipeline

## Dependencies

```bash
pip install sentence-transformers anthropic openai numpy
```

Optional:
- faiss-cpu (for large-scale vector search)
- rank-bm25 (for hybrid search)

---

## Version History

- **1.2.0** (2026-01-02): Added Quick Start, Execution Checklist, Error Handling, Metrics sections; updated frontmatter with version, category, related_skills
- **1.1.0** (2025-12-30): Added hybrid search (BM25+vector), reranking, streaming responses
- **1.0.0** (2025-10-15): Initial release with basic RAG implementation
