---
name: building-rag-systems
description: Build production RAG systems with LangChain orchestration and Qdrant vector store. Covers 8 RAG architectures (Simple, HyDE, CRAG, Self-RAG, Agentic), document processing, semantic chunking, retrieval chains, and evaluation with LangSmith/RAGAS. Use when implementing RAG pipelines, semantic search, or AI knowledge systems. NOT for simple keyword search.
---

# Building RAG Systems

Production-grade RAG with LangChain, Qdrant, and advanced retrieval patterns.

## Quick Start (LangChain)

```bash
# Dependencies
pip install langchain langchain-qdrant langchain-openai langchain-text-splitters
pip install qdrant-client fastembed  # For hybrid search

# Start Qdrant
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

```python
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load and split documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)
splits = text_splitter.split_documents(docs)

# Create vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = QdrantVectorStore.from_documents(
    splits,
    embeddings,
    url="http://localhost:6333",
    collection_name="my_docs",
)

# Search
results = vector_store.similarity_search("query", k=4)
```

---

## RAG Architectures (8 Patterns)

| Pattern | When to Use | Key Feature |
|---------|-------------|-------------|
| **Simple RAG** | FAQ, known scope | Single retrieval → generate |
| **+Memory** | Conversations | Context-aware retrieval |
| **Branched** | Multi-domain | Route to specialized retrievers |
| **HyDE** | Vague queries | Generate hypothetical answer first |
| **Adaptive** | Variable complexity | Adjust strategy dynamically |
| **CRAG** | High accuracy | Grade docs, fallback to web |
| **Self-RAG** | Research | Self-assess and re-retrieve |
| **Agentic** | Complex reasoning | Multi-tool agent orchestration |

See [references/rag-architectures.md](references/rag-architectures.md) for implementations.

---

## Quick Start (Raw Qdrant)

```bash
# Dependencies
pip install qdrant-client openai pydantic python-frontmatter

# Core components
# 1. Crawler → discovers files, extracts path metadata
# 2. Parser → extracts frontmatter, computes file hash
# 3. Chunker → semantic split on ## headers, 400 tokens, 15% overlap
# 4. Embedder → batched OpenAI embeddings
# 5. Uploader → Qdrant upsert with indexed payloads
```

---

## Ingestion Pipeline

### Architecture

```
┌──────────┐    ┌────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐
│ Crawler  │ -> │ Parser │ -> │ Chunker │ -> │ Embedder │ -> │ Uploader │
└──────────┘    └────────┘    └─────────┘    └──────────┘    └──────────┘
     │              │              │              │              │
Discovers      Extracts       Splits by     Generates      Upserts to
files          frontmatter    semantic      vectors        Qdrant
               + file hash    boundaries    (batched)      (batched)
```

### Semantic Chunking (NOT Fixed-Size)

```python
class SemanticChunker:
    """
    Production chunking:
    - Split on ## headers (semantic boundaries)
    - Target 400 tokens (NVIDIA benchmark optimal)
    - 15% overlap for context continuity
    - Track prev/next for context expansion
    """
    SECTION_PATTERN = re.compile(r"(?=^## )", re.MULTILINE)
    TOKENS_PER_WORD = 1.3

    def __init__(
        self,
        target_tokens: int = 400,
        max_tokens: int = 512,
        overlap_percent: float = 0.15,
    ):
        self.target_words = int(target_tokens / self.TOKENS_PER_WORD)
        self.overlap_words = int(self.target_words * overlap_percent)

    def chunk(self, content: str, file_hash: str) -> list[Chunk]:
        sections = self.SECTION_PATTERN.split(content)
        chunks = []

        for idx, section in enumerate(sections):
            content_hash = hashlib.sha256(section.encode()).hexdigest()[:16]
            chunk_id = f"{file_hash[:8]}_{content_hash}_{idx}"

            chunks.append(Chunk(
                id=chunk_id,
                text=section,
                chunk_index=idx,
                total_chunks=len(sections),
                prev_chunk_id=chunks[-1].id if chunks else None,
                content_hash=content_hash,
                source_file_hash=file_hash,
            ))

            # Set next_chunk_id on previous
            if len(chunks) > 1:
                chunks[-2].next_chunk_id = chunk_id

        return chunks
```

### Change Detection (Incremental Updates)

```python
def compute_file_hash(file_path: str) -> str:
    """SHA-256 for change detection."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

class QdrantStateTracker:
    """Query Qdrant payloads directly - no external state DB needed."""

    def get_indexed_files(self, book_id: str) -> dict[str, str]:
        """Returns {file_path: file_hash} from Qdrant."""
        indexed = {}
        offset = None

        while True:
            points, next_offset = self.client.scroll(
                collection_name=self.collection,
                scroll_filter=Filter(must=[
                    FieldCondition(key="book_id", match=MatchValue(value=book_id))
                ]),
                limit=100,
                offset=offset,
                with_payload=["source_file", "source_file_hash"],
                with_vectors=False,
            )

            for point in points:
                indexed[point.payload["source_file"]] = point.payload["source_file_hash"]

            if next_offset is None:
                break
            offset = next_offset

        return indexed

    def detect_changes(self, current: dict[str, str], indexed: dict[str, str]):
        """Compare filesystem vs index."""
        new = [p for p in current if p not in indexed]
        deleted = [p for p in indexed if p not in current]
        modified = [p for p in current if p in indexed and current[p] != indexed[p]]
        return new, modified, deleted
```

### Batched Embeddings

```python
class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small", batch_size: int = 20):
        self.client = OpenAI()
        self.model = model
        self.batch_size = batch_size  # OpenAI recommendation

    def embed_chunks(self, chunks: list[Chunk]) -> list[EmbeddedChunk]:
        embedded = []
        for i in range(0, len(chunks), self.batch_size):
            batch = chunks[i:i + self.batch_size]
            response = self.client.embeddings.create(
                input=[c.text for c in batch],
                model=self.model,
            )
            for chunk, data in zip(batch, response.data):
                embedded.append(EmbeddedChunk(**chunk.dict(), embedding=data.embedding))
        return embedded
```

### Qdrant Collection with Payload Indexes

```python
def create_collection(self, recreate: bool = False):
    """Create collection with proper indexes for filtered retrieval."""
    self.client.create_collection(
        collection_name=self.collection,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

    # Index ALL fields you filter by
    indexes = [
        ("book_id", PayloadSchemaType.KEYWORD),      # Tenant isolation
        ("module", PayloadSchemaType.KEYWORD),       # Content filter
        ("chapter", PayloadSchemaType.INTEGER),      # Range filter
        ("hardware_tier", PayloadSchemaType.INTEGER),# Personalization
        ("proficiency_level", PayloadSchemaType.KEYWORD),
        ("parent_doc_id", PayloadSchemaType.KEYWORD),# Context expansion
        ("source_file_hash", PayloadSchemaType.KEYWORD),  # Change detection
    ]

    for field, schema in indexes:
        self.client.create_payload_index(
            collection_name=self.collection,
            field_name=field,
            field_schema=schema,
        )
```

---

## Retrieval Patterns

### Comprehensive Filter Builder

```python
def build_filter(self, query: SearchQuery) -> Filter:
    """Build Qdrant filter with all conditions (AND logic)."""
    conditions = []

    # Required: Tenant isolation
    conditions.append(FieldCondition(
        key="book_id", match=MatchValue(value=query.book_id)
    ))

    # Required: Hardware tier (lte = "tier X or lower")
    conditions.append(FieldCondition(
        key="hardware_tier", range=Range(lte=query.hardware_tier)
    ))

    # Optional: Module exact match
    if query.module:
        conditions.append(FieldCondition(
            key="module", match=MatchValue(value=query.module)
        ))

    # Optional: Chapter range
    if query.chapter_min or query.chapter_max:
        chapter_range = Range()
        if query.chapter_min:
            chapter_range.gte = query.chapter_min
        if query.chapter_max:
            chapter_range.lte = query.chapter_max
        conditions.append(FieldCondition(key="chapter", range=chapter_range))

    # Optional: Proficiency OR logic
    if query.proficiency_levels:
        conditions.append(FieldCondition(
            key="proficiency_level",
            match=MatchAny(any=query.proficiency_levels),
        ))

    return Filter(must=conditions)
```

### Context Expansion (Walk Chunk Chain)

```python
def expand_context(self, chunk_id: str, prev: int = 1, next: int = 1) -> list[Chunk]:
    """Walk prev_chunk_id/next_chunk_id chain for surrounding context."""
    current = self.get_chunk_by_id(chunk_id)
    if not current:
        return []

    # Walk backwards
    prev_chunks = []
    prev_id = current.prev_chunk_id
    for _ in range(prev):
        if not prev_id:
            break
        chunk = self.get_chunk_by_id(prev_id)
        if not chunk:
            break
        prev_chunks.insert(0, chunk)
        prev_id = chunk.prev_chunk_id

    # Walk forwards
    next_chunks = []
    next_id = current.next_chunk_id
    for _ in range(next):
        if not next_id:
            break
        chunk = self.get_chunk_by_id(next_id)
        if not chunk:
            break
        next_chunks.append(chunk)
        next_id = chunk.next_chunk_id

    return prev_chunks + [current] + next_chunks
```

### Full Document Retrieval

```python
def get_document_chunks(self, parent_doc_id: str) -> list[Chunk]:
    """Get all chunks for a document, ordered by chunk_index."""
    points, _ = self.client.scroll(
        collection_name=self.collection,
        scroll_filter=Filter(must=[
            FieldCondition(key="parent_doc_id", match=MatchValue(value=parent_doc_id))
        ]),
        limit=100,
        with_payload=True,
        with_vectors=False,
    )

    chunks = [self._to_chunk(p) for p in points]
    chunks.sort(key=lambda c: c.chunk_index)
    return chunks
```

---

## Payload Schema

```python
class ChunkPayload(BaseModel):
    """Complete payload for filtered retrieval and context expansion."""

    # Tenant isolation
    book_id: str

    # Content filters (all indexed)
    module: str
    chapter: int
    lesson: int
    hardware_tier: int
    proficiency_level: str

    # Display content
    text: str
    section_title: Optional[str]
    source_file: str

    # Context expansion
    parent_doc_id: str
    chunk_index: int
    total_chunks: int
    prev_chunk_id: Optional[str]
    next_chunk_id: Optional[str]

    # Change detection
    content_hash: str
    source_file_hash: str
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Fixed character chunking | Semantic boundaries (## headers) |
| Position-based chunk IDs | Content hash for stable IDs |
| No overlap between chunks | 10-20% overlap for continuity |
| Full re-index on every change | Incremental with file hash detection |
| Missing payload indexes | Index every field you filter by |
| Synchronous embedding | Batch with background jobs |
| External state database | Qdrant-native state tracking |

---

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `scaffolding-fastapi-dapr` - API patterns for search endpoints
- `streaming-llm-responses` - Streaming RAG responses

## References

### LangChain Patterns
- [references/langchain-patterns.md](references/langchain-patterns.md) - LangChain RAG with Qdrant integration
- [references/rag-architectures.md](references/rag-architectures.md) - 8 RAG patterns (Simple to Agentic)
- [references/evaluation-patterns.md](references/evaluation-patterns.md) - LangSmith + RAGAS evaluation

### Raw Implementation
- [references/ingestion-patterns.md](references/ingestion-patterns.md) - Full ingestion pipeline
- [references/retrieval-patterns.md](references/retrieval-patterns.md) - Filter strategies, context expansion
