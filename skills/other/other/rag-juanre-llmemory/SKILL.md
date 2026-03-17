---
name: rag
description: Use when building Retrieval-Augmented Generation systems - covers document ingestion, hybrid search retrieval, reranking results, and prompt augmentation for accurate LLM responses grounded in your knowledge base
version: 0.5.0
---

# LLMemory RAG Systems

## Installation

```bash
uv add llmemory
# For reranking support
uv add "llmemory[reranker-local]"  # Local cross-encoder models
# or configure OpenAI reranking (no extra install needed)
```

## Overview

Retrieval-Augmented Generation (RAG) combines llmemory's document retrieval with LLM generation for accurate, grounded responses.

**RAG Pipeline:**
1. **Ingest**: Add documents to llmemory
2. **Retrieve**: Search for relevant chunks
3. **Rerank**: Improve relevance ordering (optional but recommended)
4. **Augment**: Build prompt with retrieved context
5. **Generate**: Get LLM response

**When to use RAG:**
- Question answering over your documents
- Customer support with knowledge base
- Research assistance
- Code documentation search
- Any application needing accurate, source-backed answers

## Quick Start

```python
from llmemory import LLMemory, SearchType, DocumentType
from openai import AsyncOpenAI

async def rag_system():
    # Initialize
    memory = LLMemory(
        connection_string="postgresql://localhost/mydb",
        openai_api_key="sk-..."
    )
    await memory.initialize()

    # 1. Ingest documents
    await memory.add_document(
        owner_id="workspace-1",
        id_at_origin="kb",
        document_name="product_guide.md",
        document_type=DocumentType.MARKDOWN,
        content="Your product documentation..."
    )

    # 2. Retrieve with reranking
    results = await memory.search(
        owner_id="workspace-1",
        query_text="how to reset password",
        search_type=SearchType.HYBRID,
        query_expansion=True,  # Better retrieval
        rerank=True,           # Better ranking
        rerank_top_k=50,       # Rerank top 50 candidates
        rerank_return_k=10,    # Prefer 10 best after reranking
        limit=5                # Final result count (max of limit and rerank_return_k)
    )

    # 3. Build prompt with context
    context = "\n\n".join([
        f"Source: {r.metadata.get('source', 'unknown')}\n{r.content}"
        for r in results
    ])

    prompt = f"""Answer the question using only the provided context.

Context:
{context}

Question: how to reset password

Answer:"""

    # 4. Generate response
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    print(response.choices[0].message.content)
    await memory.close()

import asyncio
asyncio.run(rag_system())
```

## Query Routing for Production RAG

Production RAG systems should detect when queries cannot be answered from available documents.

**When to use query routing:**
- User queries may be unanswerable from your knowledge base
- Need to route to web search or external APIs
- Want to avoid hallucinated answers
- Building conversational assistants

**Example:**
```python
from llmemory import LLMemory

async with LLMemory(connection_string="...") as memory:
    # Search with automatic routing
    result = await memory.search_with_routing(
        owner_id="workspace-1",
        query_text="What's the current weather in Paris?",
        enable_routing=True,
        limit=5
    )

    if result["route"] == "retrieval":
        # Answer from documents
        return generate_answer(result["results"])
    elif result["route"] == "web_search":
        # Route to web search
        return fetch_from_web(query)
    elif result["route"] == "unanswerable":
        # Honest response
        return "I don't have information to answer that question."
    else:  # clarification
        return "Could you please provide more details?"
```

**API Reference:**

### search_with_routing()

Route queries intelligently before searching.

**Signature:**
```python
async def search_with_routing(
    owner_id: str,
    query_text: str,
    enable_routing: bool = True,
    routing_threshold: float = 0.7,
    **search_kwargs
) -> Dict[str, Any]
```

**Parameters:**
- `owner_id` (str): Owner identifier
- `query_text` (str): Search query
- `enable_routing` (bool, default: True): Enable automatic routing
- `routing_threshold` (float, default: 0.7): Confidence threshold
- `**search_kwargs`: Additional arguments passed to search()

**Returns:**
Dict with:
- `route` (str): "retrieval", "web_search", "unanswerable", or "clarification"
- `confidence` (float): 0-1 confidence in routing decision
- `results` (List[SearchResult]): If route="retrieval"
- `message` (str): If route != "retrieval"
- `reason` (str): Explanation of routing decision

**Example:**
```python
result = await memory.search_with_routing(
    owner_id="support",
    query_text="How do I reset my password?",
    routing_threshold=0.8
)

if result["route"] == "retrieval":
    answer = generate_rag_response(result["results"])
else:
    answer = result["message"]  # Pre-formatted response
```

## Complete RAG Pipeline

### Step 1: Document Ingestion

```python
from llmemory import LLMemory, DocumentType, ChunkingConfig, LLMemoryConfig

async def ingest_knowledge_base(owner_id: str):
    """Ingest documents into RAG system."""

    # Configure chunking for RAG (smaller chunks for precise retrieval)
    chunking_config = ChunkingConfig(
        chunk_size=300,              # Tokens per chunk (smaller for RAG)
        chunk_overlap=50,            # Overlap for context preservation
        strategy="hierarchical",     # Chunking strategy
        min_chunk_size=100,          # Minimum chunk size
        max_chunk_size=500           # Maximum chunk size
    )

    # Enable chunk summaries via LLMemoryConfig
    config = LLMemoryConfig()
    config.chunking.enable_chunk_summaries = True
    config.chunking.summary_max_tokens = 80

    memory = LLMemory(
        connection_string="postgresql://localhost/mydb",
        config=config
    )
    await memory.initialize()

    documents = [
        {
            "name": "product_guide.md",
            "type": DocumentType.MARKDOWN,
            "content": "...",
            "metadata": {"category": "guide", "version": "2.0"}
        },
        {
            "name": "faq.md",
            "type": DocumentType.MARKDOWN,
            "content": "...",
            "metadata": {"category": "faq"}
        },
        {
            "name": "api_docs.md",
            "type": DocumentType.TECHNICAL_DOC,
            "content": "...",
            "metadata": {"category": "api", "language": "python"}
        }
    ]

    for doc in documents:
        result = await memory.add_document(
            owner_id=owner_id,
            id_at_origin="knowledge_base",
            document_name=doc["name"],
            document_type=doc["type"],
            content=doc["content"],
            metadata=doc["metadata"],
            chunking_config=chunking_config,
            generate_embeddings=True
        )
        print(f"Ingested {doc['name']}: {result.chunks_created} chunks")
```

### Step 2: Retrieval Configuration

```python
async def retrieve_for_rag(
    memory: LLMemory,
    owner_id: str,
    query: str,
    top_k: int = 5
) -> List[SearchResult]:
    """Retrieve relevant chunks for RAG."""

    results = await memory.search(
        owner_id=owner_id,
        query_text=query,

        # Hybrid search for best quality
        search_type=SearchType.HYBRID,
        alpha=0.6,  # Slight favor to semantic search

        # Query expansion for better recall
        query_expansion=True,
        max_query_variants=3,

        # Reranking for precision
        rerank=True,
        rerank_top_k=20,        # Consider top 20 candidates
        rerank_return_k=top_k,  # Prefer top_k after reranking

        # Final limit (actual count = max(limit, rerank_return_k))
        limit=top_k
    )

    return results
```

### Step 3: Reranking Configuration

llmemory supports multiple reranking methods:

#### OpenAI Reranking (Recommended for Quality)

```python
# Configure via environment
LLMEMORY_RERANK_PROVIDER=openai
LLMEMORY_RERANK_MODEL=gpt-4.1-mini
LLMEMORY_RERANK_TOP_K=30
LLMEMORY_RERANK_RETURN_K=10
```

```python
# Or programmatically
from llmemory import LLMemoryConfig

config = LLMemoryConfig()
config.search.enable_rerank = True
config.search.rerank_provider = "openai"
config.search.default_rerank_model = "gpt-4.1-mini"
config.search.rerank_top_k = 30
config.search.rerank_return_k = 10

memory = LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
)
```

#### Local Cross-Encoder Reranking (Faster, No API Calls)

```bash
# Install local reranker dependencies
uv add "llmemory[reranker-local]"
```

```python
# Configure
config = LLMemoryConfig()
config.search.enable_rerank = True
config.search.default_rerank_model = "cross-encoder/ms-marco-MiniLM-L6-v2"
config.search.rerank_device = "cpu"  # or "cuda"
config.search.rerank_batch_size = 16
```

#### Lexical Reranking (Fallback, No Dependencies)

```python
# Automatic fallback when no reranker configured
# Uses token overlap scoring
results = await memory.search(
    owner_id="workspace-1",
    query_text="query",
    rerank=True  # Uses lexical reranking
)
```

## Reranker API Reference

### CrossEncoderReranker

Local cross-encoder model for reranking search results without API calls.

**Constructor:**
```python
CrossEncoderReranker(
    model_name: str = "cross-encoder/ms-marco-MiniLM-L6-v2",
    device: Optional[str] = None,
    batch_size: int = 16
)
```

**Parameters:**
- `model_name` (str, default: "cross-encoder/ms-marco-MiniLM-L6-v2"): Hugging Face cross-encoder model name
  - Available models: "cross-encoder/ms-marco-MiniLM-L6-v2", "cross-encoder/ms-marco-TinyBERT-L2-v2"
- `device` (Optional[str]): Device to run on: "cpu", "cuda", or None (auto-detect)
- `batch_size` (int, default: 16): Batch size for inference

**Methods:**

#### score()

Score query-document pairs for relevance.

**Signature:**
```python
async def score(
    query_text: str,
    results: Sequence[SearchResult]
) -> Sequence[float]
```

**Parameters:**
- `query_text` (str): Search query
- `results` (Sequence[SearchResult]): Search results to score

**Returns:**
- `Sequence[float]`: Relevance scores (same length as results)

**Example:**
```python
from llmemory import CrossEncoderReranker

# Initialize reranker
reranker = CrossEncoderReranker(
    model_name="cross-encoder/ms-marco-MiniLM-L6-v2",
    device="cpu",
    batch_size=32
)

# Get initial search results
results = await memory.search(
    owner_id="workspace-1",
    query_text="machine learning",
    limit=50,
    rerank=False  # Get unranked results
)

# Rerank with cross-encoder
scores = await reranker.score("machine learning", results)

# Sort by new scores
scored_results = list(zip(scores, results))
scored_results.sort(key=lambda x: x[0], reverse=True)
top_results = [r for _, r in scored_results[:10]]
```

**Installation:**
```bash
# Requires sentence-transformers
uv add "llmemory[reranker-local]"
```

### OpenAIResponsesReranker

Use OpenAI GPT models for intelligent reranking with natural language understanding.

**Constructor:**
```python
OpenAIResponsesReranker(
    model: str = "gpt-4.1-mini",
    max_candidates: int = 30,
    temperature: float = 0.0
)
```

**Parameters:**
- `model` (str, default: "gpt-4.1-mini"): OpenAI model name
  - Recommended: "gpt-4.1-mini" (fast, cost-effective), "gpt-4" (higher quality)
- `max_candidates` (int, default: 30): Maximum candidates to send to API
- `temperature` (float, default: 0.0): Model temperature (0 = deterministic)

**Methods:**

#### score()

Score query-document pairs using OpenAI API.

**Signature:**
```python
async def score(
    query_text: str,
    results: Sequence[SearchResult]
) -> Sequence[float]
```

**Parameters:**
- `query_text` (str): Search query
- `results` (Sequence[SearchResult]): Search results to score

**Returns:**
- `Sequence[float]`: Relevance scores between 0 and 1

**Example:**
```python
from llmemory import OpenAIResponsesReranker
import os

# Initialize reranker (uses OPENAI_API_KEY from env)
reranker = OpenAIResponsesReranker(
    model="gpt-4.1-mini",
    max_candidates=20,
    temperature=0.0
)

# Get initial search results
results = await memory.search(
    owner_id="workspace-1",
    query_text="customer retention strategies",
    limit=50,
    rerank=False
)

# Rerank with OpenAI
scores = await reranker.score("customer retention strategies", results)

# Sort by scores
scored_results = list(zip(scores, results))
scored_results.sort(key=lambda x: x[0], reverse=True)
top_results = [r for _, r in scored_results[:10]]

print(f"Top result score: {scores[0]:.3f}")
```

**Cost Considerations:**
- Each rerank call makes one API request
- Costs depend on model and number of candidates
- Consider caching reranked results for repeated queries

**When to use:**
- Need highest quality reranking
- Willing to pay API costs
- Latency tolerance (100-300ms overhead)

### RerankerService

Internal service that wraps reranker implementations (rarely used directly).

**Usage:** Automatically created by LLMemory when reranking is enabled via configuration. Generally not instantiated directly by users.

## SearchResult Fields Reference

Search results contain multiple score fields depending on the search configuration. Understanding these fields helps optimize RAG retrieval quality.

### Core Fields

**chunk_id** (UUID)
- Unique identifier for the chunk

**document_id** (UUID)
- Parent document identifier

**content** (str)
- Full chunk text content

**metadata** (Dict[str, Any])
- Chunk metadata (may include title, section, page number, etc.)

**score** (float)
- Primary relevance score
- For hybrid search: combined score from vector and text search
- For vector search: same as similarity
- For text search: same as text_rank
- After reranking: same as rerank_score

### Optional Score Fields

**similarity** (Optional[float])
- Vector similarity score (cosine distance)
- Range: 0.0 to 1.0 (higher = more similar)
- Populated when search_type is VECTOR or HYBRID
- Example: 0.87 indicates 87% semantic similarity

**text_rank** (Optional[float])
- BM25 full-text search rank
- Higher values indicate better keyword matches
- Populated when search_type is TEXT or HYBRID
- Not normalized to [0,1] range

**rrf_score** (Optional[float])
- Reciprocal Rank Fusion score
- Populated when query_expansion=True (multi-query search)
- Combines rankings from multiple query variants
- Higher values indicate consistent ranking across variants

**rerank_score** (Optional[float])
- Reranker relevance score
- Populated when rerank=True
- Range and interpretation depends on reranker:
  - OpenAI reranker: 0.0 to 1.0 (normalized probability)
  - Cross-encoder: typically -10 to +10 (raw logit score)
  - Lexical reranker: 0.0 to 1.0 (token overlap ratio)
- Higher values indicate higher relevance according to reranker

**summary** (Optional[str])
- Concise chunk summary (30-50% of original length)
- Populated when ChunkingConfig.enable_chunk_summaries=True
- Generated during document ingestion
- Use for prompts to reduce token usage: `text = result.summary or result.content`
- See "Enable and Use Chunk Summaries" section below

### Using Score Fields

```python
# Example: Analyzing search result scores
results = await memory.search(
    owner_id="workspace-1",
    query_text="machine learning algorithms",
    search_type=SearchType.HYBRID,
    query_expansion=True,
    rerank=True,
    limit=5
)

for result in results:
    print(f"Chunk ID: {result.chunk_id}")
    print(f"  Final score: {result.score:.3f}")

    # Vector component (if hybrid/vector search)
    if result.similarity is not None:
        print(f"  Vector similarity: {result.similarity:.3f}")

    # Text component (if hybrid/text search)
    if result.text_rank is not None:
        print(f"  BM25 rank: {result.text_rank:.3f}")

    # Multi-query fusion (if query_expansion=True)
    if result.rrf_score is not None:
        print(f"  RRF score: {result.rrf_score:.3f}")

    # Reranking (if rerank=True)
    if result.rerank_score is not None:
        print(f"  Rerank score: {result.rerank_score:.3f}")

    # Summary (if enabled during ingestion)
    if result.summary:
        print(f"  Summary: {result.summary[:100]}...")
```

### Reranking Parameters

**rerank_top_k** (int, default: 50)
- Number of initial candidates to send to reranker
- Retrieve this many results from base search before reranking
- Larger values: better quality but slower and more expensive
- Recommended range: 20-100

**rerank_return_k** (int, default: 15)
- Preferred number of results after reranking
- Results are prioritized by rerank score
- Actual result count: `max(limit, rerank_return_k)`
- Set higher than limit to ensure best reranked results

**limit** (int, default: 10)
- Final result count returned to user
- Works with rerank_return_k: `final_count = max(limit, rerank_return_k)`
- Example: limit=5, rerank_return_k=10 → returns 10 results
- Example: limit=20, rerank_return_k=10 → returns 20 results

```python
# Example: Reranking parameter interactions
results = await memory.search(
    owner_id="workspace-1",
    query_text="database optimization",
    search_type=SearchType.HYBRID,
    rerank=True,
    rerank_top_k=50,      # Consider top 50 from base search
    rerank_return_k=10,   # Prefer 10 best after reranking
    limit=5               # But return max(5, 10) = 10 results
)
# Returns 10 results (max of limit and rerank_return_k)
assert len(results) == 10

results = await memory.search(
    owner_id="workspace-1",
    query_text="database optimization",
    search_type=SearchType.HYBRID,
    rerank=True,
    rerank_top_k=50,      # Consider top 50 from base search
    rerank_return_k=5,    # Prefer 5 best after reranking
    limit=20              # But return max(20, 5) = 20 results
)
# Returns 20 results (max of limit and rerank_return_k)
assert len(results) == 20
```

### Step 4: Prompt Augmentation

```python
def build_rag_prompt(
    query: str,
    results: List[SearchResult],
    system_instructions: str = "Answer based only on the provided context."
) -> str:
    """Build RAG prompt with retrieved context."""

    # Format context from search results
    context_parts = []
    for i, result in enumerate(results, 1):
        # Include source information
        source = result.metadata.get("source", "Unknown")
        doc_name = result.metadata.get("document_name", "")

        # Use summary if available (more concise for prompts)
        # Summary is populated when ChunkingConfig.enable_chunk_summaries=True
        text = result.summary or result.content

        context_parts.append(
            f"[Source {i}: {doc_name or source}]\n{text}"
        )

    context = "\n\n".join(context_parts)

    # Build final prompt
    prompt = f"""{system_instructions}

Context:
{context}

Question: {query}

Answer:"""

    return prompt
```

#### Advanced Prompt Patterns

**With Citation Requirements:**
```python
def build_prompt_with_citations(query: str, results: List[SearchResult]) -> str:
    context_parts = []
    for i, result in enumerate(results, 1):
        source = result.metadata.get("document_name", f"Source {i}")
        # Use summary if enabled (see enabling summaries section below)
        text = result.summary or result.content
        context_parts.append(f"[{i}] {source}: {text}")

    context = "\n\n".join(context_parts)

    prompt = f"""Answer the question using the provided context. Cite sources using [number] format.

Context:
{context}

Question: {query}

Answer (with citations):"""

    return prompt
```

**With Metadata Filtering:**
```python
async def rag_with_filters(
    memory: LLMemory,
    owner_id: str,
    query: str,
    category: str
):
    """RAG with metadata filtering."""
    results = await memory.search(
        owner_id=owner_id,
        query_text=query,
        search_type=SearchType.HYBRID,
        metadata_filter={"category": category},  # Filter by category
        rerank=True,
        limit=5
    )

    return build_rag_prompt(query, results)
```

### Step 5: LLM Generation

```python
from openai import AsyncOpenAI

async def generate_rag_response(
    query: str,
    results: List[SearchResult],
    model: str = "gpt-4"
) -> dict:
    """Generate LLM response with RAG context."""

    # Build prompt
    prompt = build_rag_prompt(query, results)

    # Generate with OpenAI
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,  # Lower temperature for factual answers
        max_tokens=500
    )

    # Extract response
    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": [
            {
                "content": r.content[:200] + "...",
                "score": r.score,
                "metadata": r.metadata
            }
            for r in results
        ],
        "model": model
    }
```

## Complete RAG System Example

```python
from llmemory import LLMemory, SearchType, DocumentType
from openai import AsyncOpenAI
from typing import List, Dict, Any

class RAGSystem:
    """Complete RAG system with llmemory."""

    def __init__(self, connection_string: str, openai_api_key: str):
        self.memory = LLMemory(
            connection_string=connection_string,
            openai_api_key=openai_api_key
        )
        self.client = AsyncOpenAI(api_key=openai_api_key)
        self.initialized = False

    async def initialize(self):
        """Initialize the RAG system."""
        await self.memory.initialize()
        self.initialized = True

    async def ingest_document(
        self,
        owner_id: str,
        document_name: str,
        content: str,
        document_type: DocumentType = DocumentType.TEXT,
        metadata: Dict[str, Any] = None
    ):
        """Add a document to the knowledge base."""
        result = await self.memory.add_document(
            owner_id=owner_id,
            id_at_origin="rag_kb",
            document_name=document_name,
            document_type=document_type,
            content=content,
            metadata=metadata or {},
            generate_embeddings=True
        )
        return {
            "document_id": str(result.document.document_id),
            "chunks_created": result.chunks_created
        }

    async def answer_question(
        self,
        owner_id: str,
        question: str,
        top_k: int = 5,
        model: str = "gpt-4"
    ) -> Dict[str, Any]:
        """Answer a question using RAG."""

        # Retrieve relevant chunks
        results = await self.memory.search(
            owner_id=owner_id,
            query_text=question,
            search_type=SearchType.HYBRID,
            query_expansion=True,
            max_query_variants=3,
            rerank=True,
            rerank_top_k=20,
            rerank_return_k=top_k,
            limit=top_k
        )

        if not results:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": [],
                "confidence": "low"
            }

        # Build prompt
        context = "\n\n".join([
            f"[Source: {r.metadata.get('document_name', 'Unknown')}]\n{r.summary or r.content}"
            for r in results
        ])

        prompt = f"""Answer the question using only the provided context. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {question}

Answer:"""

        # Generate response
        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        # Determine confidence based on scores
        avg_score = sum(r.score for r in results) / len(results)
        confidence = "high" if avg_score > 0.5 else "medium" if avg_score > 0.3 else "low"

        return {
            "answer": answer,
            "sources": [
                {
                    "document_name": r.metadata.get("document_name"),
                    "content_preview": r.content[:150] + "...",
                    "score": r.score,
                    "similarity": r.similarity,
                    "rerank_score": r.rerank_score  # Populated when rerank=True
                }
                for r in results
            ],
            "confidence": confidence,
            "model": model
        }

    async def close(self):
        """Clean up resources."""
        await self.memory.close()

# Usage
async def main():
    rag = RAGSystem(
        connection_string="postgresql://localhost/mydb",
        openai_api_key="sk-..."
    )
    await rag.initialize()

    # Ingest documents
    await rag.ingest_document(
        owner_id="user-123",
        document_name="product_guide.md",
        content="...",
        document_type=DocumentType.MARKDOWN,
        metadata={"category": "guide"}
    )

    # Answer questions
    result = await rag.answer_question(
        owner_id="user-123",
        question="How do I reset my password?",
        top_k=5
    )

    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Sources: {len(result['sources'])}")

    await rag.close()
```

## RAG Best Practices

### 1. Chunk Size Optimization

```python
from llmemory import ChunkingConfig, LLMemoryConfig

# For RAG, use smaller chunks (better precision)
chunking_config = ChunkingConfig(
    chunk_size=300,              # 300 tokens (vs 1000 default)
    chunk_overlap=50,            # 50 tokens overlap
    strategy="hierarchical",     # Create parent/child chunks
    min_chunk_size=100,          # Minimum chunk size
    max_chunk_size=500           # Maximum chunk size
)

# Enable summaries via LLMemoryConfig (set when creating LLMemory)
# config = LLMemoryConfig()
# config.chunking.enable_chunk_summaries = True
# config.chunking.summary_max_tokens = 80

await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="kb",
    document_name="doc.md",
    document_type=DocumentType.MARKDOWN,
    content="...",
    chunking_config=chunking_config
)

# Smaller chunks:
# - More precise retrieval
# - Better for prompts (fit more sources)
# - Less noise in context
#
# Larger chunks:
# - More context per chunk
# - Better for broad questions
# - Fewer chunks needed
```

### 2. Use Parent Context for Broader Context

```python
# Retrieve with parent context
results = await memory.search(
    owner_id="workspace-1",
    query_text="API authentication",
    search_type=SearchType.HYBRID,
    include_parent_context=True,  # Include surrounding chunks
    context_window=2,              # ±2 chunks
    limit=5
)

# Build prompt with parent context
for result in results:
    print(f"Main chunk: {result.content}")
    if result.parent_chunks:
        print(f"Context from {len(result.parent_chunks)} parent chunks")
        for parent in result.parent_chunks:
            print(f"  - {parent.content[:100]}...")
```

### 3. Reranking for Quality

Always use reranking in RAG for better relevance:

```python
# Without reranking (lower quality)
results = await memory.search(
    owner_id="workspace-1",
    query_text="query",
    rerank=False,
    limit=5
)

# With reranking (higher quality)
results = await memory.search(
    owner_id="workspace-1",
    query_text="query",
    rerank=True,
    rerank_top_k=20,    # Consider top 20 candidates
    rerank_return_k=10,  # Prefer 10 best after reranking
    limit=5             # Final count = max(5, 10) = 10 results
)

# Reranking improves:
# - Relevance of top results
# - Precision for RAG prompts
# - Reduces hallucination (better context)
```

### 4. Query Expansion for Recall

```python
# Use multi-query for better recall
results = await memory.search(
    owner_id="workspace-1",
    query_text="reduce latency",
    query_expansion=True,  # Generates variants like "improve response time"
    max_query_variants=3,
    rerank=True,           # Rerank after fusion
    limit=5
)

# Good for:
# - Vague queries
# - Different terminology in docs
# - Comprehensive answers
```

### 5. Metadata for Filtering

```python
# Add rich metadata during ingestion
await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="kb",
    document_name="api_v2_docs.md",
    document_type=DocumentType.TECHNICAL_DOC,
    content="...",
    metadata={
        "category": "api",
        "version": "2.0",
        "language": "python",
        "last_updated": "2024-10-01"
    }
)

# Filter during retrieval
results = await memory.search(
    owner_id="workspace-1",
    query_text="authentication",
    metadata_filter={
        "category": "api",
        "version": "2.0"
    },
    limit=5
)
```

### 6. Enable and Use Chunk Summaries

Chunk summaries provide concise representations of chunks, making prompts more efficient by reducing token usage while preserving key information.

**Enabling Summaries:**

```python
from llmemory import LLMemory, ChunkingConfig, LLMemoryConfig, DocumentType

# Enable summaries via LLMemoryConfig
config = LLMemoryConfig()
config.chunking.enable_chunk_summaries = True
config.chunking.summary_max_tokens = 80  # Control summary length

memory = LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
)
await memory.initialize()

# Use custom chunking config for chunk size settings
chunking_config = ChunkingConfig(
    chunk_size=300,
    chunk_overlap=50,
    strategy="hierarchical"
)

await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="kb",
    document_name="doc.md",
    document_type=DocumentType.MARKDOWN,
    content="...",
    chunking_config=chunking_config
)
```

**Using Summaries in Prompts:**

```python
def build_prompt_with_summaries(query: str, results: List[SearchResult]):
    """Build prompt using chunk summaries when available."""
    context_parts = []
    for result in results:
        # SearchResult.summary is populated when enable_chunk_summaries=True
        # Falls back to full content if summaries weren't generated
        text = result.summary or result.content
        context_parts.append(text)

    context = "\n".join(context_parts)
    return f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
```

**Benefits:**
- Reduced prompt token usage (summaries are ~30-50% of original size)
- More chunks fit in context window
- Faster LLM processing
- Preserved key information for accurate answers

## RAG Evaluation

### Measuring Retrieval Quality

```python
async def evaluate_retrieval(
    memory: LLMemory,
    owner_id: str,
    test_queries: List[Dict[str, Any]]
):
    """Evaluate retrieval quality."""

    metrics = {
        "precision_at_5": [],
        "recall": [],
        "mrr": []  # Mean Reciprocal Rank
    }

    for test in test_queries:
        query = test["query"]
        relevant_doc_ids = set(test["relevant_docs"])

        # Retrieve
        results = await memory.search(
            owner_id=owner_id,
            query_text=query,
            rerank=True,
            limit=10
        )

        # Calculate precision@5
        top_5_docs = {str(r.document_id) for r in results[:5]}
        precision = len(top_5_docs & relevant_doc_ids) / 5
        metrics["precision_at_5"].append(precision)

        # Calculate recall
        retrieved_docs = {str(r.document_id) for r in results}
        recall = len(retrieved_docs & relevant_doc_ids) / len(relevant_doc_ids)
        metrics["recall"].append(recall)

        # Calculate MRR
        for rank, result in enumerate(results, 1):
            if str(result.document_id) in relevant_doc_ids:
                metrics["mrr"].append(1.0 / rank)
                break
        else:
            metrics["mrr"].append(0.0)

    return {
        "avg_precision_at_5": sum(metrics["precision_at_5"]) / len(test_queries),
        "avg_recall": sum(metrics["recall"]) / len(test_queries),
        "mean_reciprocal_rank": sum(metrics["mrr"]) / len(test_queries)
    }
```


## Related Skills

- `basic-usage` - Core document and search operations
- `hybrid-search` - Vector + BM25 hybrid search fundamentals
- `multi-query` - Query expansion for improved retrieval
- `multi-tenant` - Multi-tenant isolation patterns for SaaS

## Important Notes

**RAG Pipeline Optimization:**
The complete RAG pipeline (retrieve → rerank → generate) typically takes 200-500ms:
- Retrieval: 50-150ms
- Reranking: 50-200ms (depending on provider)
- LLM generation: 500-2000ms

**Chunk Size for RAG:**
Smaller chunks (200-400 tokens) work better for RAG than larger chunks:
- More precise retrieval
- Less noise in context
- More chunks fit in prompt
- Better for specific questions

**Multi-Tenant RAG:**
Always use `owner_id` for data isolation in multi-tenant RAG systems. Never expose one tenant's documents to another.

**Reranking ROI:**
Reranking adds 50-200ms but significantly improves answer quality by ensuring the most relevant chunks appear first in the prompt, reducing hallucination and improving accuracy.
