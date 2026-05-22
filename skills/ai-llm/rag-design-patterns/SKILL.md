---
name: rag-design-patterns
description: Automatically applies when building RAG (Retrieval Augmented Generation) systems. Ensures proper chunking strategies, vector database patterns, embedding management, reranking, and retrieval optimization.
category: ai-llm
---

# RAG Design Patterns

When building Retrieval Augmented Generation systems, follow these patterns for effective, scalable retrieval.

**Trigger Keywords**: RAG, retrieval, vector database, embeddings, chunking, vector search, semantic search, reranking, vector store, FAISS, Pinecone, Qdrant, ChromaDB, retrieval augmented

**Agent Integration**: Used by `ml-system-architect`, `rag-architect`, `llm-app-engineer`, `performance-and-cost-engineer-llm`

## ✅ Correct Pattern: Document Chunking

```python
from typing import List
from pydantic import BaseModel, Field


class Chunk(BaseModel):
    """A document chunk with metadata."""
    id: str
    content: str
    start_char: int
    end_char: int
    document_id: str
    metadata: dict = Field(default_factory=dict)


class ChunkingStrategy:
    """Base class for chunking strategies."""

    def chunk(self, text: str, document_id: str) -> List[Chunk]:
        """Split text into chunks."""
        raise NotImplementedError


class SemanticChunker(ChunkingStrategy):
    """Chunk by semantic boundaries (paragraphs, sections)."""

    def __init__(
        self,
        max_chunk_size: int = 512,
        overlap: int = 50,
        split_on: List[str] = None
    ):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.split_on = split_on or ["\n\n", "\n", ". "]

    def chunk(self, text: str, document_id: str) -> List[Chunk]:
        """Chunk text at semantic boundaries."""
        chunks = []
        current_pos = 0

        # Split by semantic boundaries first
        for delimiter in self.split_on:
            if delimiter in text:
                segments = text.split(delimiter)
                break
        else:
            segments = [text]

        current_chunk = ""
        chunk_start = 0

        for segment in segments:
            if len(current_chunk) + len(segment) <= self.max_chunk_size:
                current_chunk += segment
            else:
                if current_chunk:
                    chunks.append(Chunk(
                        id=f"{document_id}-{len(chunks)}",
                        content=current_chunk,
                        start_char=chunk_start,
                        end_char=chunk_start + len(current_chunk),
                        document_id=document_id
                    ))
                current_chunk = segment
                chunk_start = chunk_start + len(current_chunk) - self.overlap

        # Add final chunk
        if current_chunk:
            chunks.append(Chunk(
                id=f"{document_id}-{len(chunks)}",
                content=current_chunk,
                start_char=chunk_start,
                end_char=chunk_start + len(current_chunk),
                document_id=document_id
            ))

        return chunks
```

## Vector Database Integration

```python
import numpy as np
from typing import List, Optional
import asyncio


class VectorStore:
    """Abstract vector database interface."""

    async def add_chunks(
        self,
        chunks: List[Chunk],
        embeddings: np.ndarray
    ):
        """Add chunks with their embeddings."""
        raise NotImplementedError

    async def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        filter: Optional[dict] = None
    ) -> List[tuple[Chunk, float]]:
        """Search for similar chunks."""
        raise NotImplementedError


class EmbeddingModel:
    """Generate embeddings for text."""

    async def embed(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts.

        Args:
            texts: List of text strings

        Returns:
            Array of embeddings, shape (len(texts), embedding_dim)
        """
        # Use OpenAI, Anthropic, or local model
        raise NotImplementedError


class RAGPipeline:
    """End-to-end RAG pipeline."""

    def __init__(
        self,
        chunker: ChunkingStrategy,
        embedder: EmbeddingModel,
        vector_store: VectorStore
    ):
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store

    async def index_document(
        self,
        text: str,
        document_id: str,
        metadata: Optional[dict] = None
    ):
        """Index a document into vector store."""
        # Chunk document
        chunks = self.chunker.chunk(text, document_id)

        # Add metadata
        if metadata:
            for chunk in chunks:
                chunk.metadata.update(metadata)

        # Generate embeddings
        texts = [c.content for c in chunks]
        embeddings = await self.embedder.embed(texts)

        # Store in vector DB
        await self.vector_store.add_chunks(chunks, embeddings)

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filter: Optional[dict] = None
    ) -> List[tuple[Chunk, float]]:
        """Retrieve relevant chunks for query."""
        # Embed query
        query_embedding = await self.embedder.embed([query])

        # Search vector store
        results = await self.vector_store.search(
            query_embedding[0],
            top_k=top_k,
            filter=filter
        )

        return results
```

## Reranking for Improved Precision

```python
from typing import List, Tuple


class Reranker:
    """Rerank retrieved chunks for better relevance."""

    async def rerank(
        self,
        query: str,
        chunks: List[Chunk],
        top_k: int = 5
    ) -> List[Tuple[Chunk, float]]:
        """
        Rerank chunks using cross-encoder or LLM.

        Args:
            query: Search query
            chunks: Retrieved chunks
            top_k: Number of top results to return

        Returns:
            Reranked chunks with new scores
        """
        # Use cross-encoder model or LLM for reranking
        scores = await self._compute_relevance_scores(query, chunks)

        # Sort by score
        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]

    async def _compute_relevance_scores(
        self,
        query: str,
        chunks: List[Chunk]
    ) -> List[float]:
        """Compute relevance scores."""
        # Implementation using cross-encoder or LLM
        raise NotImplementedError


class RAGWithReranking(RAGPipeline):
    """RAG pipeline with reranking."""

    def __init__(self, *args, reranker: Reranker, **kwargs):
        super().__init__(*args, **kwargs)
        self.reranker = reranker

    async def retrieve(
        self,
        query: str,
        initial_k: int = 20,
        final_k: int = 5,
        filter: Optional[dict] = None
    ) -> List[tuple[Chunk, float]]:
        """Retrieve with reranking."""
        # Get initial results (over-retrieve)
        initial_results = await super().retrieve(
            query,
            top_k=initial_k,
            filter=filter
        )

        # Extract chunks
        chunks = [chunk for chunk, _ in initial_results]

        # Rerank
        reranked = await self.reranker.rerank(query, chunks, top_k=final_k)

        return reranked
```

## Query Rewriting and Expansion

```python
class QueryRewriter:
    """Rewrite queries for better retrieval."""

    async def rewrite(self, query: str) -> List[str]:
        """
        Generate multiple query variations.

        Args:
            query: Original query

        Returns:
            List of query variations
        """
        # Use LLM to generate variations
        prompt = f"""Generate 3 variations of this query for better search:

Original: {query}

Variations (one per line):"""

        response = await llm_complete(prompt)
        variations = [
            line.strip()
            for line in response.strip().split("\n")
            if line.strip()
        ]

        return [query] + variations  # Include original


class HybridRetriever:
    """Combine multiple retrieval strategies."""

    def __init__(
        self,
        vector_store: VectorStore,
        embedder: EmbeddingModel,
        query_rewriter: QueryRewriter
    ):
        self.vector_store = vector_store
        self.embedder = embedder
        self.query_rewriter = query_rewriter

    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[tuple[Chunk, float]]:
        """Hybrid retrieval with query expansion."""
        # Generate query variations
        queries = await self.query_rewriter.rewrite(query)

        # Retrieve for each variation
        all_results = []
        for q in queries:
            results = await self._retrieve_for_query(q, top_k=top_k * 2)
            all_results.extend(results)

        # Deduplicate and merge scores
        merged = self._merge_results(all_results)

        # Return top k
        return sorted(merged, key=lambda x: x[1], reverse=True)[:top_k]

    def _merge_results(
        self,
        results: List[tuple[Chunk, float]]
    ) -> List[tuple[Chunk, float]]:
        """Merge and deduplicate results."""
        chunk_scores = {}
        for chunk, score in results:
            if chunk.id in chunk_scores:
                # Average or max score
                chunk_scores[chunk.id] = max(chunk_scores[chunk.id], score)
            else:
                chunk_scores[chunk.id] = score

        return [(chunk, chunk_scores[chunk.id]) for chunk, _ in results
                if chunk.id in chunk_scores]
```

## Context Assembly for LLM

```python
class ContextBuilder:
    """Build context from retrieved chunks."""

    def build_context(
        self,
        chunks: List[Chunk],
        max_tokens: int = 4000,
        include_metadata: bool = True
    ) -> str:
        """
        Assemble context from chunks within token limit.

        Args:
            chunks: Retrieved chunks
            max_tokens: Maximum context tokens
            include_metadata: Include chunk metadata

        Returns:
            Formatted context string
        """
        context_parts = []
        total_tokens = 0

        for i, chunk in enumerate(chunks):
            # Format chunk
            chunk_text = f"[Source {i+1}]\n{chunk.content}\n"

            if include_metadata and chunk.metadata:
                meta_str = ", ".join(
                    f"{k}: {v}" for k, v in chunk.metadata.items()
                )
                chunk_text += f"Metadata: {meta_str}\n"

            # Estimate tokens (rough: 1 token ≈ 4 chars)
            chunk_tokens = len(chunk_text) // 4

            if total_tokens + chunk_tokens > max_tokens:
                break

            context_parts.append(chunk_text)
            total_tokens += chunk_tokens

        return "\n".join(context_parts)


async def rag_complete(
    query: str,
    pipeline: RAGPipeline,
    context_builder: ContextBuilder
) -> str:
    """Complete RAG workflow."""
    # Retrieve
    chunks, scores = zip(*await pipeline.retrieve(query, top_k=5))

    # Build context
    context = context_builder.build_context(chunks)

    # Generate with LLM
    prompt = f"""Answer this question using the provided context.

Context:
{context}

Question: {query}

Answer:"""

    return await llm_complete(prompt)
```

## ❌ Anti-Patterns

```python
# ❌ Fixed-size chunking ignoring semantics
chunks = [text[i:i+512] for i in range(0, len(text), 512)]  # Breaks mid-sentence!

# ✅ Better: Semantic chunking
chunks = chunker.chunk(text, document_id)


# ❌ No overlap between chunks
chunks = split_by_size(text, 512)  # Context loss!

# ✅ Better: Add overlap
chunks = semantic_chunker.chunk(text, overlap=50)


# ❌ Embed and search without reranking
results = vector_store.search(query_embedding)  # Approximate!

# ✅ Better: Rerank top results
initial = vector_store.search(query_embedding, top_k=20)
results = reranker.rerank(query, initial, top_k=5)


# ❌ No metadata for filtering
chunk = Chunk(content=text)  # Can't filter!

# ✅ Better: Rich metadata
chunk = Chunk(
    content=text,
    metadata={
        "source": "docs",
        "date": "2025-01-15",
        "category": "technical"
    }
)
```

## Best Practices Checklist

- ✅ Use semantic chunking (paragraphs/sections, not arbitrary splits)
- ✅ Add overlap between chunks (50-100 tokens)
- ✅ Include rich metadata for filtering
- ✅ Implement reranking for top results
- ✅ Use query rewriting/expansion
- ✅ Respect token limits when building context
- ✅ Track retrieval metrics (precision, recall)
- ✅ Embed chunks asynchronously in batches
- ✅ Cache embeddings for frequently accessed documents
- ✅ Test different chunk sizes for your use case

## Auto-Apply

When building RAG systems:
1. Implement semantic chunking with overlap
2. Add comprehensive metadata to chunks
3. Use async for all embedding/retrieval operations
4. Implement reranking for top results
5. Build context within token limits
6. Log retrieval quality metrics

## Related Skills

- `llm-app-architecture` - For LLM integration
- `async-await-checker` - For async patterns
- `pydantic-models` - For data validation
- `observability-logging` - For retrieval logging
- `performance-profiling` - For optimization
