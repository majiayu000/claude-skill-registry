---
name: faion-rag-engineer
description: "RAG engineering: embeddings, chunking, vector databases, hybrid search, reranking."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# RAG Engineer Skill

**Communication: User's language. Code: English.**

## Purpose

Specializes in RAG (Retrieval Augmented Generation) systems. Covers document processing, embeddings, vector search, and retrieval optimization.

## Context Discovery

### Auto-Investigation

Check these project signals before asking questions:

| Signal | Where to Check | What to Look For |
|--------|----------------|------------------|
| **Dependencies** | package.json, requirements.txt | langchain, llamaindex, qdrant-client, chromadb, weaviate-client |
| **Vector DB** | docker-compose.yml, .env | Qdrant, Weaviate, Chroma config/containers |
| **Document dirs** | /docs, /data, /content | Documents to index (PDF, MD, TXT) |
| **Existing embeddings** | Grep for "embed", "vector", "retriever" | Current RAG implementation |

### Discovery Questions

```yaml
question: "What's your RAG use case?"
header: "RAG Goal"
multiSelect: false
options:
  - label: "Documentation Q&A"
    description: "Answer questions from internal docs"
  - label: "Knowledge base search"
    description: "Semantic search over articles/guides"
  - label: "Code search/retrieval"
    description: "Find relevant code snippets"
  - label: "Customer support"
    description: "Context-aware support responses"
```

```yaml
question: "Which vector database?"
header: "Vector DB"
multiSelect: false
options:
  - label: "Qdrant (recommended for production)"
    description: "Fast, scalable, rich filtering"
  - label: "Chroma (recommended for dev/prototyping)"
    description: "Simple, local, easy setup"
  - label: "Weaviate (for knowledge graphs)"
    description: "Hybrid search, graph features"
  - label: "pgvector (for PostgreSQL projects)"
    description: "Vector extension for existing Postgres"
```

```yaml
question: "Document volume and type?"
header: "Data Characteristics"
multiSelect: false
options:
  - label: "Small (<1000 docs, mostly text)"
    description: "Simple chunking sufficient"
  - label: "Medium (1000-10000 docs)"
    description: "Consider hybrid search + reranking"
  - label: "Large (>10000 docs, mixed formats)"
    description: "Advanced chunking + metadata filtering"
  - label: "Code repository"
    description: "AST-aware chunking needed"
```

```yaml
question: "Do you need hybrid search (vector + keyword)?"
header: "Search Strategy"
multiSelect: false
options:
  - label: "Yes - combine semantic + exact matching"
    description: "Hybrid search for best results"
  - label: "No - semantic search only"
    description: "Vector similarity sufficient"
```

## Scope

| Area | Coverage |
|------|----------|
| **Chunking** | Text splitting, semantic chunking, overlap strategies |
| **Embeddings** | Text vectorization, similarity search, models |
| **Vector DBs** | Qdrant, Weaviate, Chroma, pgvector |
| **Retrieval** | Hybrid search, reranking, metadata filtering |
| **RAG Systems** | Architecture, evaluation, agentic RAG |

## Quick Start

| Task | Files |
|------|-------|
| Basic RAG | chunking-basics.md → embedding-basics.md → rag-architecture.md |
| Vector DB setup | db-comparison.md → db-qdrant.md (recommended) |
| Advanced retrieval | hybrid-search-basics.md → reranking-basics.md |
| RAG evaluation | rag-eval-metrics.md → rag-eval-methods.md |
| Agentic RAG | agentic-rag.md |

## Methodologies (22)

**Chunking (2):**
- chunking-basics: Size, overlap, delimiters
- chunking-advanced: Semantic, recursive, custom

**Embeddings (4):**
- embedding-basics: Fundamentals, similarity
- embedding-generation: API usage, batching
- embedding-models: Comparison, selection
- embedding-applications: Use cases, patterns

**Vector Databases (4):**
- db-comparison: Feature comparison, selection
- db-qdrant: Setup, indexing, search (recommended)
- db-weaviate: Knowledge graphs, hybrid search
- db-chroma: Local dev, prototyping
- vector-database-setup: General setup patterns

**Retrieval (4):**
- hybrid-search-basics: Vector + keyword search
- hybrid-search-implementation: Production patterns
- reranking-basics: Cross-encoder fundamentals
- reranking-models: Cohere, MixedBread, custom

**RAG Systems (7):**
- rag: RAG overview, fundamentals
- rag-architecture: System design, components
- rag-implementation: Production patterns
- rag-eval-metrics: Relevance, faithfulness, correctness
- rag-eval-methods: Evaluation frameworks
- agentic-rag: Agent-driven retrieval
- graph-rag-advanced-retrieval: Knowledge graphs

## Architecture

```
Document Ingestion
    ↓
Chunking (semantic/fixed)
    ↓
Embedding Generation
    ↓
Vector Database Storage
    ↓
Query Processing
    ↓
Retrieval (vector + hybrid)
    ↓
Reranking
    ↓
Context Assembly
    ↓
LLM Generation
```

## Code Examples

### Basic RAG Pipeline

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Chunk documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = splitter.split_documents(docs)

# Generate embeddings and store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)

# Retrieve
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)
results = retriever.invoke("query")
```

### Hybrid Search with Qdrant

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, Filter

client = QdrantClient("localhost", port=6333)

# Create collection
client.create_collection(
    collection_name="docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Hybrid search
results = client.search(
    collection_name="docs",
    query_vector=query_embedding,
    query_filter=Filter(...),
    limit=10
)
```

### Reranking

```python
from cohere import Client

co = Client(api_key="...")

# Rerank retrieved docs
reranked = co.rerank(
    query="query text",
    documents=[doc.text for doc in results],
    top_n=3,
    model="rerank-english-v3.0"
)
```

## Evaluation Metrics

| Metric | Measures |
|--------|----------|
| **Retrieval Precision** | Relevant docs in results |
| **Retrieval Recall** | Coverage of relevant docs |
| **MRR** | Mean reciprocal rank |
| **NDCG** | Ranking quality |
| **Faithfulness** | Grounding in context |
| **Answer Relevance** | Response matches query |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-llm-integration | Uses embedding APIs |
| faion-ai-agents | Agentic RAG patterns |
| faion-ml-ops | RAG evaluation |

---

*RAG Engineer v1.0 | 22 methodologies*
