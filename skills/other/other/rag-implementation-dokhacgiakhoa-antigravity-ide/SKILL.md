---
version: 4.1.0-fractal
name: rag-implementation
description: Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and semantic search. Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases.
---

# RAG Implementation

Master Retrieval-Augmented Generation (RAG) to build LLM applications that provide accurate, grounded responses using external knowledge sources.

## Use this skill when

- Building Q&A systems over proprietary documents
- Creating chatbots with current, factual information
- Implementing semantic search with natural language queries
- Reducing hallucinations with grounded responses
- Enabling LLMs to access domain-specific knowledge
- Building documentation assistants
- Creating research tools with source citation

## Do not use this skill when

- You only need purely generative writing without retrieval
- The dataset is too small to justify embeddings
- You cannot store or process the source data safely

## Instructions

1. Define the corpus, update cadence, and evaluation targets.
2. Choose embedding models and vector store based on scale.
3. Build ingestion, chunking, and retrieval with reranking.
4. Evaluate with grounded QA metrics and monitor drift.

## Safety

- Redact sensitive data and enforce access controls.
- Avoid exposing source documents in responses when restricted.

## Core Components

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. Vector Databases](./sub-skills/1-vector-databases.md)
### 2. [2. Embeddings](./sub-skills/2-embeddings.md)
### 3. [3. Retrieval Strategies](./sub-skills/3-retrieval-strategies.md)
### 4. [4. Reranking](./sub-skills/4-reranking.md)
### 5. [Pattern 1: Hybrid Search](./sub-skills/pattern-1-hybrid-search.md)
### 6. [Pattern 2: Multi-Query Retrieval](./sub-skills/pattern-2-multi-query-retrieval.md)
### 7. [Pattern 3: Contextual Compression](./sub-skills/pattern-3-contextual-compression.md)
### 8. [Pattern 4: Parent Document Retriever](./sub-skills/pattern-4-parent-document-retriever.md)
### 9. [Recursive Character Text Splitter](./sub-skills/recursive-character-text-splitter.md)
### 10. [Token-Based Splitting](./sub-skills/token-based-splitting.md)
### 11. [Semantic Chunking](./sub-skills/semantic-chunking.md)
### 12. [Markdown Header Splitter](./sub-skills/markdown-header-splitter.md)
### 13. [Pinecone](./sub-skills/pinecone.md)
### 14. [Weaviate](./sub-skills/weaviate.md)
### 15. [Chroma (Local)](./sub-skills/chroma-local.md)
### 16. [1. Metadata Filtering](./sub-skills/1-metadata-filtering.md)
### 17. [2. Maximal Marginal Relevance](./sub-skills/2-maximal-marginal-relevance.md)
### 18. [3. Reranking with Cross-Encoder](./sub-skills/3-reranking-with-cross-encoder.md)
### 19. [Contextual Prompt](./sub-skills/contextual-prompt.md)
### 20. [With Citations](./sub-skills/with-citations.md)
### 21. [With Confidence](./sub-skills/with-confidence.md)
