---
name: ai-data-engineering
description: Data pipelines, feature stores, and embedding generation for AI/ML systems. Use when building RAG pipelines, ML feature serving, or data transformations. Covers feature stores (Feast, Tecton), embedding pipelines, chunking strategies, orchestration (Dagster, Prefect, Airflow), dbt transformations, data versioning (LakeFS), and experiment tracking (MLflow, W&B).
---

# AI Data Engineering

## Purpose

Build data infrastructure for AI/ML systems including RAG pipelines, feature stores, and embedding generation. Provides architecture patterns, orchestration workflows, and evaluation metrics for production AI applications.

## When to Use

**Use this skill when:**
- Building RAG (Retrieval-Augmented Generation) pipelines
- Implementing semantic search or vector databases
- Setting up ML feature stores for real-time serving
- Creating embedding generation pipelines
- Evaluating RAG quality with RAGAS metrics
- Orchestrating data workflows for AI systems
- Integrating with frontend skills (ai-chat, search-filter)

**Skip this skill if:**
- Building traditional CRUD applications (use databases-relational)
- Simple key-value storage (use databases-nosql)
- No AI/ML components in the application

## RAG Pipeline Architecture

RAG pipelines have 5 distinct stages. Understanding this architecture is critical for production implementations.

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline (5 Stages)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. INGESTION → Load documents (PDF, DOCX, Markdown)        │
│  2. INDEXING → Chunk (512 tokens) + Embed + Store           │
│  3. RETRIEVAL → Query embedding + Vector search + Filters   │
│  4. GENERATION → Context injection + LLM streaming          │
│  5. EVALUATION → RAGAS metrics (faithfulness, relevancy)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**For complete RAG architecture with implementation patterns, see:**
- `references/rag-architecture.md` - Detailed 5-stage breakdown
- `examples/langchain-rag/basic_rag.py` - Working implementation

## Chunking Strategies

Chunking is the most critical decision for RAG quality. Poor chunking breaks retrieval.

**Default Recommendation:**
- **Size:** 512 tokens
- **Overlap:** 50-100 tokens
- **Method:** Fixed token-based

**Why these values:**
- Too small (<256 tokens): Loses context, requires many retrievals
- Too large (>1024 tokens): Includes irrelevant content, hits token limits
- Overlap prevents information loss at chunk boundaries

**Alternative strategies for special cases:**

```python
# Code-aware chunking (preserves functions/classes)
from langchain.text_splitter import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(
    language="python",
    chunk_size=512,
    chunk_overlap=50
)

# Semantic chunking (splits on meaning, not tokens)
from langchain.text_splitter import SemanticChunker

semantic_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile"  # Split at semantic boundaries
)
```

**See:** `references/chunking-strategies.md` for complete decision framework

## Embedding Generation

Embedding quality directly impacts retrieval accuracy. Voyage AI is currently best-in-class.

**Primary Recommendation: Voyage AI voyage-3**
- Dimensions: 1024
- MTEB Score: 69.0 (highest as of Dec 2025)
- Cost: $$$ but 9.74% better than OpenAI
- Use for: Production systems requiring best retrieval quality

**Cost-Effective Alternative: OpenAI text-embedding-3-small**
- Dimensions: 1536
- MTEB Score: 62.3
- Cost: $ (5x cheaper than voyage-3)
- Use for: Development, prototyping, cost-sensitive applications

**Implementation:**

```python
from langchain_voyageai import VoyageAIEmbeddings
from langchain_openai import OpenAIEmbeddings

# Production (best quality)
embeddings = VoyageAIEmbeddings(
    model="voyage-3",
    voyage_api_key="your-api-key"
)

# Development (cost-effective)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key="your-api-key"
)
```

**See:** `references/embedding-strategies.md` for complete provider comparison

## RAGAS Evaluation Metrics

Traditional metrics (BLEU, ROUGE) don't measure RAG quality. RAGAS provides LLM-as-judge evaluation.

**4 Core Metrics:**

| Metric | Measures | Good Score |
|--------|----------|------------|
| **Faithfulness** | Factual consistency with retrieved context | > 0.8 |
| **Answer Relevancy** | Does answer address the user's question? | > 0.7 |
| **Context Precision** | Are retrieved chunks actually relevant? | > 0.6 |
| **Context Recall** | Were all necessary chunks retrieved? | > 0.7 |

**Quick evaluation script:**

```bash
# Run RAGAS evaluation (TOKEN-FREE script execution)
python scripts/evaluate_rag.py --dataset eval_data.json --output results.json
```

**Manual implementation:**

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

dataset = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["France's capital is Paris."]],
    "ground_truth": ["Paris"]
}

result = evaluate(dataset, metrics=[faithfulness, answer_relevancy])
print(f"Faithfulness: {result['faithfulness']}")
print(f"Answer Relevancy: {result['answer_relevancy']}")
```

**See:** `references/evaluation-metrics.md` for complete RAGAS implementation guide

## Feature Stores

Feature stores solve the "training-serving skew" problem by providing consistent feature computation.

**Primary Recommendation: Feast** - Open source, works with any backend (PostgreSQL, Redis, DynamoDB, S3, BigQuery, Snowflake)

**Basic usage:**

```python
from feast import FeatureStore
store = FeatureStore(repo_path="feature_repo/")

# Online serving (low-latency)
features = store.get_online_features(
    features=["user_features:total_orders"],
    entity_rows=[{"user_id": 1001}]
).to_dict()
```

**See:** `references/feature-stores.md` for complete Feast setup and alternatives (Tecton, Hopsworks)

## LangChain Orchestration

LangChain is the primary framework for LLM orchestration with the largest ecosystem (24,215+ API reference snippets).

**Context7 Library ID:** `/websites/langchain_oss_python_langchain` (Trust: High, Snippets: 435)

**Basic RAG Chain:**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_qdrant import QdrantVectorStore
from langchain_voyageai import VoyageAIEmbeddings

# Setup retriever
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    embedding=VoyageAIEmbeddings(model="voyage-3")
)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# Build chain
prompt = ChatPromptTemplate.from_template(
    "Answer based on context:\n{context}\n\nQuestion: {question}"
)
chain = {"context": retriever, "question": lambda x: x} | prompt | ChatOpenAI() | StrOutputParser()

# Stream response
for chunk in chain.stream("What is the capital of France?"):
    print(chunk, end="", flush=True)
```

**See:** `references/langchain-patterns.md` - Complete LangChain 0.3+ patterns with streaming and hybrid search

## Orchestration Tools

Modern AI pipelines require workflow orchestration beyond cron jobs.

**Primary Recommendation: Dagster (for ML/AI pipelines)** - Asset-centric design, best lineage tracking, perfect for RAG

**Example: Embedding Pipeline**

```python
from dagster import asset
from langchain_voyageai import VoyageAIEmbeddings

@asset
def raw_documents():
    """Load documents from S3."""
    return documents

@asset
def chunked_documents(raw_documents):
    """Split into 512-token chunks with 50-token overlap."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.split_documents(raw_documents)

@asset
def embedded_documents(chunked_documents):
    """Generate embeddings with Voyage AI."""
    embeddings = VoyageAIEmbeddings(model="voyage-3")
    return embeddings.embed_documents([doc.page_content for doc in chunked_documents])
```

**See:** `references/orchestration-tools.md` for complete Dagster patterns and alternatives (Prefect, Airflow 3.0, dbt)

## Integration with Frontend Skills

### ai-chat Skill → RAG Backend

The ai-chat skill consumes RAG pipeline outputs for streaming responses.

**Backend API (FastAPI):**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

@app.post("/api/rag/stream")
async def stream_rag(query: str):
    async def generate():
        chain = RetrievalQA.from_chain_type(llm=OpenAI(streaming=True), retriever=vectorstore.as_retriever())
        async for chunk in chain.astream(query):
            yield chunk
    return StreamingResponse(generate(), media_type="text/plain")
```

**See:** `references/rag-architecture.md` for complete frontend integration patterns

### search-filter Skill → Semantic Search

The search-filter skill uses semantic search backends for vector similarity.

**Backend (Qdrant + Voyage AI):**

```python
from qdrant_client import QdrantClient
from langchain_voyageai import VoyageAIEmbeddings

@app.post("/api/search/semantic")
async def semantic_search(query: str, filters: dict):
    query_vector = VoyageAIEmbeddings(model="voyage-3").embed_query(query)
    results = QdrantClient().search(
        collection_name="documents",
        query_vector=query_vector,
        query_filter=filters,
        limit=10
    )
    return {"results": results}
```

## Data Versioning

**Primary Recommendation: LakeFS** (acquired DVC team November 2025)

Git-like operations on data lakes: branch, commit, merge, time travel. Works with S3/Azure/GCS.

```python
import lakefs

branch = lakefs.Branch("main").create("experiment-voyage-3")
branch.commit("Updated embeddings to voyage-3")
branch.merge_into("main")
```

**See:** `references/data-versioning.md` for complete LakeFS setup

## Quick Start Workflow

**1. Set up vector database:**

```bash
# Run Qdrant setup script (TOKEN-FREE execution)
python scripts/setup_qdrant.py --collection docs --dimension 1024
```

**2. Chunk and embed documents:**

```bash
# Chunk documents (TOKEN-FREE execution)
python scripts/chunk_documents.py \
  --input data/documents/ \
  --chunk-size 512 \
  --overlap 50 \
  --output data/chunks/
```

**3. Implement RAG pipeline:**

See `examples/langchain-rag/basic_rag.py` for complete working example.

**4. Evaluate with RAGAS:**

```bash
# Run evaluation (TOKEN-FREE execution)
python scripts/evaluate_rag.py \
  --dataset data/eval_qa.json \
  --output results/ragas_metrics.json
```

**5. Deploy with orchestration:**

See `examples/dagster-pipelines/embedding_pipeline.py` for production deployment.

## Dependencies

**Required Python packages:**

```bash
# Core RAG
pip install langchain langchain-core langchain-openai langchain-voyageai langchain-qdrant

# Vector database
pip install qdrant-client

# Evaluation
pip install ragas datasets

# Feature stores
pip install feast

# Orchestration
pip install dagster dagster-webserver

# Data versioning
pip install lakefs-client
```

**Optional for alternatives:**

```bash
# LlamaIndex (alternative to LangChain)
pip install llama-index

# dbt (SQL transformations)
pip install dbt-core dbt-postgres

# Prefect (alternative orchestration)
pip install prefect
```

## Troubleshooting

**Common Issues:**

**1. Poor retrieval quality** - Check chunk size (try 512 tokens), increase overlap (50-100), try hybrid search, re-rank with Cohere

**2. Slow embedding generation** - Batch documents (100-1000), use async APIs, cache with Redis, use smaller model for dev

**3. High LLM costs** - Reduce retrieved chunks (k=3), use cheaper re-ranking models, cache frequent queries

**See:** `references/rag-architecture.md` for complete troubleshooting guide

## Best Practices

**Chunking:** Default to 512 tokens with 50-token overlap. Use semantic chunking for complex documents. Preserve code structure for source code.

**Embeddings:** Use Voyage AI voyage-3 for production, OpenAI text-embedding-3-small for development. Never mix embedding models (re-embed everything if changing).

**Evaluation:** Run RAGAS metrics on every pipeline change. Maintain test dataset of 50+ question-answer pairs. Track metrics over time.

**Orchestration:** Use Dagster for ML/AI pipelines, dbt for SQL transformations only. Version control all pipeline code.

**Frontend Integration:** Always stream LLM responses. Implement retry logic. Show citations/sources to users. Handle empty results gracefully.

## Additional Resources

**Reference Documentation:**
- `references/rag-architecture.md` - Complete RAG pipeline guide
- `references/chunking-strategies.md` - Decision framework for chunking
- `references/embedding-strategies.md` - Embedding model comparison
- `references/langchain-patterns.md` - LangChain 0.3+ patterns
- `references/feature-stores.md` - Feast setup and alternatives
- `references/evaluation-metrics.md` - RAGAS implementation guide

**Working Examples:**
- `examples/langchain-rag/basic_rag.py` - Simple RAG chain
- `examples/langchain-rag/streaming_rag.py` - Streaming responses
- `examples/langchain-rag/hybrid_search.py` - Vector + BM25
- `examples/llamaindex-agents/query_engine.py` - LlamaIndex alternative
- `examples/feast-features/` - Complete feature store setup
- `examples/dagster-pipelines/embedding_pipeline.py` - Production pipeline

**Executable Scripts (TOKEN-FREE):**
- `scripts/evaluate_rag.py` - RAGAS evaluation runner
- `scripts/chunk_documents.py` - Document chunking utility
- `scripts/benchmark_retrieval.py` - Retrieval quality benchmark
- `scripts/setup_qdrant.py` - Qdrant collection setup
