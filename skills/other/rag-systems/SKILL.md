---
name: rag-systems
description: "Build Retrieval-Augmented Generation systems to enhance LLMs with external knowledge. Use for question answering, document search, knowledge bases, reducing hallucinations, and grounding LLM responses in factual data."
---

# RAG Systems

Build Retrieval-Augmented Generation systems that enhance LLMs with external knowledge.

## Overview

RAG combines information retrieval with language generation, enabling LLMs to access and incorporate external knowledge for more accurate, up-to-date responses.

## Quick Reference

| Scenario | Recommended Approach | Reference File |
|----------|---------------------|----------------|
| Document ingestion and vectorization | Chunking, embedding, indexing | `/references/data-ingestion.md` |
| Finding relevant information | Retrieval strategies and ranking | `/references/retrieval-methods.md` |
| Combining retrieval with generation | Prompt augmentation and generation | `/references/generation-techniques.md` |

## Core Principles

1. **Chunking** - Split documents into semantically coherent pieces
2. **Embedding** - Convert text to dense vector representations
3. **Indexing** - Store vectors for efficient similarity search
4. **Retrieval** - Find most relevant chunks for query
5. **Augmentation** - Inject retrieved context into LLM prompt

## RAG Pipeline

### 1. Data Ingestion
- Load documents from various sources
- Split into chunks (200-500 tokens typical)
- Generate embeddings using embedding model
- Store in vector database

### 2. Retrieval
- Convert user query to embedding
- Perform similarity search in vector database
- Retrieve top-k most relevant chunks
- Optional: Re-rank results for relevance

### 3. Generation
- Construct prompt with retrieved context
- Send to LLM for generation
- Return response with optional citations

## Key Components

**Embedding Models:**
- OpenAI text-embedding-ada-002
- Sentence Transformers (open-source)
- Domain-specific fine-tuned models

**Vector Databases:**
- Pinecone: Managed, scalable
- Weaviate: Open-source, feature-rich
- Chroma: Lightweight, easy to use
- FAISS: Facebook's similarity search library

**Chunking Strategies:**
- Fixed-size with overlap
- Sentence-based
- Paragraph-based
- Semantic chunking

## Using the Reference Files

**`/references/data-ingestion.md`** — Document loading, chunking strategies, embedding generation, vector database setup, and indexing best practices.

**`/references/retrieval-methods.md`** — Similarity search, hybrid search (dense + sparse), re-ranking, metadata filtering, and retrieval optimization.

**`/references/generation-techniques.md`** — Prompt construction, context injection, citation generation, handling long contexts, and response quality improvement.

## Best Practices

- Chunk documents at semantic boundaries
- Use overlap between chunks (10-20%)
- Store metadata with chunks (source, date, etc.)
- Implement hybrid search (semantic + keyword)
- Re-rank retrieved results
- Include source citations in responses
- Monitor and update embeddings regularly
- Handle edge cases (no results, too many results)

## Common Pitfalls to Avoid

- Chunks too large (lose specificity) or too small (lose context)
- Not using overlap between chunks
- Ignoring metadata for filtering
- Only using semantic search (miss exact matches)
- Not re-ranking retrieved results
- Overwhelming LLM with too much context
- Not citing sources
- Stale embeddings (not updating with new data)

