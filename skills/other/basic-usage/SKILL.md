---
name: basic-usage
description: Use when getting started with llmemory document storage and search - covers installation, initialization, adding documents, vector search, hybrid search, semantic search, BM25 full-text search, document management, and building RAG systems with multi-tenant support
version: 0.5.0
---

# LLMemory Basic Usage

## Installation

```bash
uv add llmemory
# or
pip install llmemory
```

**Prerequisites:**
- Python 3.10 or higher
- PostgreSQL 14+ (tested up to PostgreSQL 16)
- pgvector extension 0.5.0+
- OpenAI API key (or configure local embeddings)

**Installing pgvector:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-16-pgvector

# macOS with Homebrew
brew install pgvector

# Or using CREATE EXTENSION in PostgreSQL:
psql -d your_database -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

**Verifying pgvector installation:**
```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
-- Should return one row if installed correctly
```

## API Overview

This skill documents core llmemory operations:
- `LLMemory` - Main interface class
- `DocumentType` - Enum for document types
- `SearchType` - Enum for search modes
- `ChunkingStrategy` - Enum for chunking strategies
- `add_document()` - Add and process documents
- `search()` - Search for documents
- `search_with_routing()` - Search with automatic query routing (detects answerable queries)
- `search_with_documents()` - Search and return results with document metadata
- `list_documents()` - List documents with pagination
- `get_document()` - Retrieve a document (owner-scoped)
- `get_document_chunks()` - Get chunks with pagination (owner-scoped)
- `get_chunk_count()` - Get number of chunks for a document (owner-scoped)
- `delete_document()` / `delete_documents()` - Delete documents (owner-scoped)
- `get_statistics()` - Get owner statistics
- `db_manager` - Access underlying database manager
- `initialize()` / `close()` - Lifecycle management

## Quick Start

```python
import asyncio
from llmemory import LLMemory, DocumentType, SearchType

async def main():
    # Initialize
    memory = LLMemory(
        connection_string="postgresql://localhost/mydb",
        openai_api_key="sk-..."
    )
    await memory.initialize()

    # Add a document
    result = await memory.add_document(
        owner_id="workspace-1",
        id_at_origin="user-123",
        document_name="example.txt",
        document_type=DocumentType.TEXT,
        content="Your document content here...",
        metadata={"category": "example"}
    )
    print(f"Created document with {result.chunks_created} chunks")

    # Search
    results = await memory.search(
        owner_id="workspace-1",
        query_text="your search query",
        search_type=SearchType.HYBRID,
        limit=5
    )
    for result in results:
        print(f"[{result.score:.3f}] {result.content[:80]}...")

    # Clean up
    await memory.close()

asyncio.run(main())
```

## Complete API Documentation

### LLMemory

Main interface for document operations.

**Constructor:**
```python
LLMemory(
    connection_string: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    config: Optional[LLMemoryConfig] = None,
    db_manager: Optional[AsyncDatabaseManager] = None
)
```

**Parameters:**
- `connection_string` (str, optional): PostgreSQL connection URL (format: `postgresql://user:pass@host:port/database`). Ignored if `db_manager` provided.
- `openai_api_key` (str, optional): OpenAI API key for embeddings. Can also be set via `OPENAI_API_KEY` environment variable.
- `config` (LLMemoryConfig, optional): Configuration object. Defaults to config from environment if not provided.
- `db_manager` (AsyncDatabaseManager, optional): Existing database manager from shared pool (for production apps with multiple services).

**Raises:**
- `ConfigurationError`: If neither connection_string nor db_manager provided, or if configuration is invalid.

**Example:**
```python
from llmemory import LLMemory

# Simple initialization
memory = LLMemory(
    connection_string="postgresql://localhost/mydb",
    openai_api_key="sk-..."
)
await memory.initialize()
```

### LLMemory.from_db_manager()

Create instance from existing AsyncDatabaseManager (shared pool pattern).

**Signature:**
```python
@classmethod
def from_db_manager(
    cls,
    db_manager: AsyncDatabaseManager,
    openai_api_key: Optional[str] = None,
    config: Optional[LLMemoryConfig] = None
) -> LLMemory
```

**Parameters:**
- `db_manager` (AsyncDatabaseManager, required): Existing database manager with schema already set
- `openai_api_key` (str, optional): OpenAI API key
- `config` (LLMemoryConfig, optional): Configuration object

**Returns:**
- `LLMemory`: Configured instance

**Example:**
```python
from pgdbm import AsyncDatabaseManager, DatabaseConfig
from llmemory import LLMemory

# Create shared pool
config = DatabaseConfig(connection_string="postgresql://localhost/mydb")
shared_pool = await AsyncDatabaseManager.create_shared_pool(config)

# Create llmemory with shared pool
db_manager = AsyncDatabaseManager(pool=shared_pool, schema="llmemory")
memory = LLMemory.from_db_manager(
    db_manager,
    openai_api_key="sk-..."
)
await memory.initialize()
```

### db_manager

Get the underlying database manager for health checks and monitoring.

**Property:**
```python
@property
def db_manager(self) -> Optional[AsyncDatabaseManager]
```

**Returns:**
- `Optional[AsyncDatabaseManager]`: Database manager instance if initialized, None otherwise

**Example:**
```python
from llmemory import LLMemory

memory = LLMemory(connection_string="postgresql://localhost/mydb")
await memory.initialize()

# Access underlying database manager
db_mgr = memory.db_manager
if db_mgr:
    # Check connection pool status
    pool_status = await db_mgr.get_pool_status()
    print(f"Active connections: {pool_status['active']}")
    print(f"Idle connections: {pool_status['idle']}")

    # Run health check
    is_healthy = await db_mgr.health_check()
    print(f"Database healthy: {is_healthy}")
```

**When to use:**
- Health monitoring and observability
- Accessing connection pool metrics
- Database diagnostics
- Integration with monitoring systems

### initialize()

Initialize the library and database schema.

**Signature:**
```python
async def initialize() -> None
```

**Raises:**
- `DatabaseError`: If database initialization fails
- `ConfigurationError`: If configuration is invalid

**Example:**
```python
memory = LLMemory(connection_string="postgresql://localhost/mydb")
await memory.initialize()  # Sets up tables, migrations, indexes
```

### close()

Close all connections and cleanup resources.

**Signature:**
```python
async def close() -> None
```

**Example:**
```python
await memory.close()
```

**Context Manager Pattern (Recommended):**
```python
async with LLMemory(connection_string="...") as memory:
    # Use memory here
    results = await memory.search(...)
# Automatically closed
```

### Document Types

```python
class DocumentType(str, Enum):
    PDF = "pdf"
    MARKDOWN = "markdown"
    CODE = "code"
    TEXT = "text"
    HTML = "html"
    DOCX = "docx"
    EMAIL = "email"
    REPORT = "report"
    CHAT = "chat"
    PRESENTATION = "presentation"
    LEGAL_DOCUMENT = "legal_document"
    TECHNICAL_DOC = "technical_doc"
    BUSINESS_REPORT = "business_report"
    UNKNOWN = "unknown"
```

### Search Types

```python
class SearchType(str, Enum):
    VECTOR = "vector"     # Vector similarity search only
    TEXT = "text"         # Full-text search only
    HYBRID = "hybrid"     # Combines vector + text (recommended)
```

### Chunking Strategies

```python
class ChunkingStrategy(str, Enum):
    HIERARCHICAL = "hierarchical"      # Default - Creates parent and child chunks for better context
    FIXED_SIZE = "fixed_size"          # Fixed-size chunks with overlap
    SEMANTIC = "semantic"              # Chunks based on semantic boundaries (slower, higher quality)
    SLIDING_WINDOW = "sliding_window"  # Sliding window with configurable overlap
```

**Strategy descriptions:**
- **HIERARCHICAL** (default): Creates hierarchical parent and child chunks. Parent chunks provide broader context while child chunks are used for precise retrieval. Best for most use cases.
- **FIXED_SIZE**: Creates fixed-size chunks with configurable overlap. Simple and fast, good for uniform documents.
- **SEMANTIC**: Chunks based on semantic boundaries (paragraphs, sections). Slower but produces higher quality chunks that respect document structure.
- **SLIDING_WINDOW**: Creates overlapping chunks using a sliding window approach. Good for ensuring no information is lost at chunk boundaries.

**Usage:**
```python
from llmemory import ChunkingStrategy

# Use enum value
result = await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="user-123",
    document_name="example.txt",
    document_type=DocumentType.TEXT,
    content="Your document content...",
    chunking_strategy=ChunkingStrategy.SEMANTIC  # Use enum
)

# Or use string value (also valid)
result = await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="user-123",
    document_name="example.txt",
    document_type=DocumentType.TEXT,
    content="Your document content...",
    chunking_strategy="hierarchical"  # String also works
)
```

### Model Classes

#### SearchResult

Search result from any search operation.

**Fields:**
- `chunk_id` (UUID): Chunk identifier
- `document_id` (UUID): Document identifier
- `content` (str): Chunk content
- `metadata` (Dict[str, Any]): Chunk metadata
- `score` (float): Overall relevance score
- `similarity` (float, optional): Vector similarity score (0-1)
- `text_rank` (float, optional): Full-text search rank
- `rrf_score` (float, optional): Reciprocal Rank Fusion score
- `rerank_score` (float, optional): Reranker score (when reranking enabled)
- `summary` (str, optional): Chunk summary if generated
- `parent_chunks` (List[DocumentChunk]): Surrounding chunks if requested

#### EnrichedSearchResult

Extended search result with document metadata (inherits from SearchResult).

**Additional Fields:**
- `document_name` (str): Name of the source document
- `document_type` (str): Type of document
- `document_metadata` (Dict[str, Any]): Document-level metadata

**When used:** Returned by `search_with_documents()`

#### SearchResultWithDocuments

Container for enriched search results.

**Fields:**
- `results` (List[EnrichedSearchResult]): Enriched search results
- `total` (int): Total number of results

#### DocumentAddResult

Result of adding a document.

**Fields:**
- `document` (Document): Created document object with all fields
- `chunks_created` (int): Number of chunks created
- `embeddings_created` (int): Number of embeddings generated
- `processing_time_ms` (float): Processing time in milliseconds

#### DocumentListResult

Result of listing documents with pagination.

**Fields:**
- `documents` (List[Document]): Document objects
- `total` (int): Total matching documents (before pagination)
- `limit` (int): Applied limit
- `offset` (int): Applied offset

#### DocumentWithChunks

Document with optional chunks.

**Fields:**
- `document` (Document): Document object
- `chunks` (Optional[List[DocumentChunk]]): Chunks if requested
- `chunk_count` (int): Total number of chunks

#### OwnerStatistics

Statistics for an owner's documents.

**Fields:**
- `document_count` (int): Total documents
- `chunk_count` (int): Total chunks
- `total_size_bytes` (int): Estimated total size
- `document_type_breakdown` (Optional[Dict[DocumentType, int]]): Count by document type
- `created_date_range` (Optional[Tuple[datetime, datetime]]): (min_date, max_date) of document creation

#### DeleteResult

Result of batch delete operation.

**Fields:**
- `deleted_count` (int): Number of documents deleted
- `deleted_document_ids` (List[UUID]): IDs of deleted documents

#### EmbeddingStatus

Enum for embedding generation status.

```python
class EmbeddingStatus(str, Enum):
    PENDING = "pending"        # Job queued but not started
    PROCESSING = "processing"  # Currently generating embeddings
    COMPLETED = "completed"    # Successfully completed
    FAILED = "failed"          # Failed with error
```

#### EmbeddingJob

Represents a background embedding generation job.

**Fields:**
- `chunk_id` (UUID): Chunk being processed
- `provider_id` (str): Embedding provider ID
- `status` (EmbeddingStatus): Current status
- `retry_count` (int): Number of retries attempted
- `error_message` (Optional[str]): Error details if failed
- `created_at` (datetime): When job was created
- `processed_at` (Optional[datetime]): When processing finished

#### SearchQuery

Internal search query model (rarely used directly).

**Fields:**
- `owner_id` (str): Owner identifier
- `query_text` (str): Search query text
- `search_type` (SearchType): Type of search
- `limit` (int): Maximum results
- `alpha` (float): Hybrid search weight
- `metadata_filter` (Optional[Dict[str, Any]]): Metadata filter
- `id_at_origin` (Optional[str]): Single origin filter
- `id_at_origins` (Optional[List[str]]): Multiple origins filter
- `date_from` (Optional[datetime]): Start date
- `date_to` (Optional[datetime]): End date
- `include_parent_context` (bool): Include parent chunks
- `context_window` (int): Number of parent chunks
- `rerank` (bool): Enable reranking
- `enable_query_expansion` (bool): Enable query expansion
- `max_query_variants` (int): Max query variants

### add_document()

Add a document and process it into searchable chunks.

**Signature:**
```python
async def add_document(
    owner_id: str,
    id_at_origin: str,
    document_name: str,
    document_type: Union[DocumentType, str],
    content: str,
    document_date: Optional[datetime] = None,
    metadata: Optional[Dict[str, Any]] = None,
    chunking_strategy: str = "hierarchical",
    chunking_config: Optional[ChunkingConfig] = None,
    generate_embeddings: bool = True
) -> DocumentAddResult
```

**Parameters:**
- `owner_id` (str, required): Owner identifier for multi-tenancy (e.g., "workspace-123", "tenant-abc")
- `id_at_origin` (str, required): Origin identifier within owner (e.g., "user-456", "thread-789")
- `document_name` (str, required): Name of the document
- `document_type` (DocumentType or str, required): Type of document
- `content` (str, required): Full document content
- `document_date` (datetime, optional): Document date for temporal filtering
- `metadata` (Dict[str, Any], optional): Custom metadata (searchable via `metadata_filter`)
- `chunking_strategy` (str, default: "hierarchical"): Chunking strategy to use
- `chunking_config` (ChunkingConfig, optional): Custom chunking configuration
- `generate_embeddings` (bool, default: True): Generate embeddings immediately

**Returns:**
- `DocumentAddResult` with:
  - `document` (Document): Created document object
  - `chunks_created` (int): Number of chunks created
  - `embeddings_created` (int): Number of embeddings generated
  - `processing_time_ms` (float): Processing time in milliseconds

**Raises:**
- `ValidationError`: If input validation fails (invalid owner_id, empty content, etc.)
- `DatabaseError`: If database operation fails
- `EmbeddingError`: If embedding generation fails

**Example:**
```python
from llmemory import DocumentType
from datetime import datetime

result = await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="user-123",
    document_name="Q4 Report.pdf",
    document_type=DocumentType.PDF,
    content="Full document text here...",
    document_date=datetime(2024, 10, 1),
    metadata={
        "category": "financial",
        "department": "finance",
        "confidential": False
    }
)

print(f"Document ID: {result.document.document_id}")
print(f"Chunks: {result.chunks_created}")
print(f"Embeddings: {result.embeddings_created}")
print(f"Time: {result.processing_time_ms:.2f}ms")
```

### search()

Search for documents.

**Signature:**
```python
async def search(
    owner_id: str,
    query_text: str,
    search_type: Union[SearchType, str] = SearchType.HYBRID,
    limit: int = 10,
    id_at_origin: Optional[str] = None,
    id_at_origins: Optional[List[str]] = None,
    metadata_filter: Optional[Dict[str, Any]] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    include_parent_context: bool = False,
    context_window: int = 2,
    alpha: float = 0.5,
    query_expansion: Optional[bool] = None,
    max_query_variants: Optional[int] = None,
    rerank: Optional[bool] = None,
    rerank_top_k: Optional[int] = None,
    rerank_return_k: Optional[int] = None
) -> List[SearchResult]
```

**Parameters:**
- `owner_id` (str, required): Owner identifier for filtering
- `query_text` (str, required): Search query text
- `search_type` (SearchType or str, default: HYBRID): Type of search to perform
- `limit` (int, default: 10): Maximum number of results
- `id_at_origin` (str, optional): Filter by single origin ID
- `id_at_origins` (List[str], optional): Filter by multiple origin IDs
- `metadata_filter` (Dict[str, Any], optional): Filter by metadata (e.g., `{"category": "financial"}`)
- `date_from` (datetime, optional): Start date filter
- `date_to` (datetime, optional): End date filter
- `include_parent_context` (bool, default: False): Include surrounding chunks
- `context_window` (int, default: 2): Number of surrounding chunks to include
- `alpha` (float, default: 0.5): Hybrid search weight (0=text only, 1=vector only)
- `query_expansion` (bool, optional): Enable query expansion (None = follow config)
- `max_query_variants` (int, optional): Max query variants for expansion
- `rerank` (bool, optional): Enable reranking (None = follow config)
- `rerank_top_k` (int, optional): Candidates for reranker
- `rerank_return_k` (int, optional): Results after reranking

**Returns:**
- `List[SearchResult]` where each result has:
  - `chunk_id` (UUID): Chunk identifier
  - `document_id` (UUID): Document identifier
  - `content` (str): Chunk content
  - `metadata` (Dict[str, Any]): Chunk metadata
  - `score` (float): Overall relevance score
  - `similarity` (float, optional): Vector similarity score
  - `text_rank` (float, optional): Text search rank
  - `rrf_score` (float, optional): Reciprocal Rank Fusion score
  - `rerank_score` (float, optional): Reranker score (when reranking enabled)
  - `summary` (str, optional): Chunk summary if available
  - `parent_chunks` (List[DocumentChunk]): Surrounding chunks if requested

**Raises:**
- `ValidationError`: If input validation fails
- `SearchError`: If search operation fails

**Example:**
```python
from llmemory import SearchType

# Basic search
results = await memory.search(
    owner_id="workspace-1",
    query_text="quarterly revenue trends",
    search_type=SearchType.HYBRID,
    limit=5
)

for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.content[:100]}...")
    print(f"Metadata: {result.metadata}")
    print("---")

# Advanced search with filters
results = await memory.search(
    owner_id="workspace-1",
    query_text="product launch strategy",
    search_type=SearchType.HYBRID,
    limit=10,
    metadata_filter={"category": "strategy", "department": "product"},
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 12, 31),
    alpha=0.7  # Favor vector search slightly
)
```

### search_with_documents()

Search and return results enriched with document metadata.

**Signature:**
```python
async def search_with_documents(
    owner_id: str,
    query_text: str,
    search_type: Union[SearchType, str] = SearchType.HYBRID,
    limit: int = 10,
    metadata_filter: Optional[Dict[str, Any]] = None,
    include_document_metadata: bool = True
) -> SearchResultWithDocuments
```

**Parameters:**
- `owner_id` (str, required): Owner identifier
- `query_text` (str, required): Search query text
- `search_type` (SearchType or str, default: HYBRID): Type of search
- `limit` (int, default: 10): Maximum results
- `metadata_filter` (Dict[str, Any], optional): Filter by metadata
- `include_document_metadata` (bool, default: True): Include document-level metadata

**Returns:**
- `SearchResultWithDocuments` with:
  - `results` (List[EnrichedSearchResult]): Enriched search results
  - `total` (int): Total number of results

**EnrichedSearchResult fields:**
- All fields from `SearchResult` (chunk_id, content, score, etc.)
- `document_name` (str): Name of the source document
- `document_type` (str): Type of document
- `document_metadata` (Dict[str, Any]): Document-level metadata

**Raises:**
- `ValidationError`: If input validation fails
- `SearchError`: If search operation fails

**Example:**
```python
# Search with document context
results_with_docs = await memory.search_with_documents(
    owner_id="workspace-1",
    query_text="quarterly financial performance",
    search_type=SearchType.HYBRID,
    limit=10
)

print(f"Found {results_with_docs.total} results")

for result in results_with_docs.results:
    print(f"Document: {result.document_name}")
    print(f"Type: {result.document_type}")
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.content[:100]}...")
    print(f"Metadata: {result.document_metadata}")
    print("---")
```

**When to use:**
- When you need document context along with search results
- Building UI that shows source documents
- Grouping results by document
- When document metadata is needed for filtering or display

### list_documents()

List documents with pagination and filtering.

**Signature:**
```python
async def list_documents(
    owner_id: str,
    limit: int = 20,
    offset: int = 0,
    document_type: Optional[DocumentType] = None,
    order_by: Literal["created_at", "updated_at", "document_name"] = "created_at",
    order_desc: bool = True,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> DocumentListResult
```

**Parameters:**
- `owner_id` (str, required): Owner identifier
- `limit` (int, default: 20): Maximum documents to return
- `offset` (int, default: 0): Number of documents to skip (for pagination)
- `document_type` (DocumentType, optional): Filter by document type
- `order_by` (str, default: "created_at"): Field to sort by
- `order_desc` (bool, default: True): Sort descending
- `metadata_filter` (Dict[str, Any], optional): Filter by metadata

**Returns:**
- `DocumentListResult` with:
  - `documents` (List[Document]): Document objects
  - `total` (int): Total matching documents
  - `limit` (int): Applied limit
  - `offset` (int): Applied offset

**Raises:**
- `ValidationError`: If parameters are invalid

**Example:**
```python
# List recent documents
result = await memory.list_documents(
    owner_id="workspace-1",
    limit=20,
    offset=0,
    order_by="created_at",
    order_desc=True
)

print(f"Total documents: {result.total}")
for doc in result.documents:
    print(f"{doc.document_name} - {doc.document_type.value}")

# Filter by type and metadata
result = await memory.list_documents(
    owner_id="workspace-1",
    document_type=DocumentType.PDF,
    metadata_filter={"category": "financial"},
    limit=50
)
```

### get_document()

Retrieve a specific document with optional chunks.

**Signature:**
```python
async def get_document(
    owner_id: str,
    document_id: Union[str, UUID],
    include_chunks: bool = False,
    include_embeddings: bool = False
) -> DocumentWithChunks
```

**Parameters:**
- `owner_id` (str, required): Owner/workspace identifier (required for access control)
- `document_id` (str or UUID, required): Document identifier
- `include_chunks` (bool, default: False): Include all chunks for this document
- `include_embeddings` (bool, default: False): Include embeddings with chunks (requires `include_chunks=True`)

**Returns:**
- `DocumentWithChunks` with:
  - `document` (Document): Document object
  - `chunks` (List[DocumentChunk], optional): Chunks if requested
  - `chunk_count` (int): Total number of chunks

**Raises:**
- `DocumentNotFoundError`: If document doesn't exist
- `PermissionError`: If the document belongs to a different owner

**Example:**
```python
# Get document without chunks
doc_info = await memory.get_document(
    owner_id="workspace-1",
    document_id="uuid-here"
)
print(f"Document: {doc_info.document.document_name}")
print(f"Chunks: {doc_info.chunk_count}")

# Get document with all chunks
doc_with_chunks = await memory.get_document(
    owner_id="workspace-1",
    document_id="uuid-here",
    include_chunks=True
)

for chunk in doc_with_chunks.chunks:
    print(f"Chunk {chunk.chunk_index}: {chunk.content[:50]}...")
```

### get_document_chunks()

Get chunks for a specific document with pagination.

**Signature:**
```python
async def get_document_chunks(
    owner_id: str,
    document_id: Union[str, UUID],
    limit: Optional[int] = None,
    offset: int = 0
) -> List[DocumentChunk]
```

**Parameters:**
- `owner_id` (str, required): Owner/workspace identifier (required for access control)
- `document_id` (str or UUID, required): Document identifier
- `limit` (int, optional): Maximum number of chunks to return (None = all chunks)
- `offset` (int, default: 0): Number of chunks to skip for pagination

**Returns:**
- `List[DocumentChunk]`: List of chunks ordered by chunk_index

**Raises:**
- `DocumentNotFoundError`: If document doesn't exist
- `PermissionError`: If the document belongs to a different owner
- `ValidationError`: If limit or offset are negative

**Example:**
```python
# Get all chunks for a document
chunks = await memory.get_document_chunks(
    owner_id="workspace-1",
    document_id="uuid-here"
)
print(f"Total chunks: {len(chunks)}")
for chunk in chunks:
    print(f"Chunk {chunk.chunk_index}: {chunk.content[:50]}...")

# Paginated retrieval
page_size = 10
offset = 0
while True:
    chunks = await memory.get_document_chunks(
        owner_id="workspace-1",
        document_id="uuid-here",
        limit=page_size,
        offset=offset
    )

    if not chunks:
        break

    for chunk in chunks:
        print(f"Chunk {chunk.chunk_index}: {chunk.content}")

    offset += page_size
```

**When to use:**
- Accessing document chunks without full document
- Paginating through large documents
- Processing chunks in batches
- Inspecting chunking results

### get_chunk_count()

Get the number of chunks for a document.

**Signature:**
```python
async def get_chunk_count(
    owner_id: str,
    document_id: Union[str, UUID]
) -> int
```

**Parameters:**
- `owner_id` (str, required): Owner/workspace identifier (required for access control)
- `document_id` (str or UUID, required): Document identifier

**Returns:**
- `int`: Number of chunks for the document

**Raises:**
- `DocumentNotFoundError`: If document doesn't exist
- `PermissionError`: If the document belongs to a different owner

**Example:**
```python
# Get chunk count
count = await memory.get_chunk_count(owner_id="workspace-1", document_id="uuid-here")
print(f"Document has {count} chunks")

# Check if document needs re-chunking
if count > 1000:
    print("Warning: Very large document, consider splitting")
elif count == 0:
    print("Warning: Document has no chunks")
```

**When to use:**
- Quick check of document size
- Validating chunking results
- Deciding pagination strategy
- Monitoring document processing

### delete_document()

Delete a single document and all its chunks.

**Signature:**
```python
async def delete_document(
    owner_id: str,
    document_id: Union[UUID, str]
) -> None
```

**Parameters:**
- `owner_id` (str, required): Owner/workspace identifier (required for access control)
- `document_id` (UUID or str, required): Document ID to delete

**Raises:**
- `ResourceNotFoundError`: If document not found
- `PermissionError`: If the document belongs to a different owner
- `DatabaseError`: If deletion fails

**Example:**
```python
await memory.delete_document(owner_id="workspace-1", document_id="uuid-here")
```

### delete_documents()

Delete multiple documents.

**Signature:**
```python
async def delete_documents(
    owner_id: str,
    document_ids: Optional[List[Union[str, UUID]]] = None,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> DeleteResult
```

**Parameters:**
- `owner_id` (str, required): Owner identifier (safety check)
- `document_ids` (List[UUID or str], optional): Specific documents to delete
- `metadata_filter` (Dict[str, Any], optional): Delete all matching metadata

**Returns:**
- `DeleteResult` with:
  - `deleted_count` (int): Number of documents deleted
  - `deleted_document_ids` (List[UUID]): IDs of deleted documents

**Raises:**
- `ValueError`: If neither document_ids nor metadata_filter provided
- `ValidationError`: If owner_id is invalid

**Example:**
```python
# Delete specific documents
result = await memory.delete_documents(
    owner_id="workspace-1",
    document_ids=["uuid-1", "uuid-2", "uuid-3"]
)
print(f"Deleted {result.deleted_count} documents")

# Delete by metadata
result = await memory.delete_documents(
    owner_id="workspace-1",
    metadata_filter={"category": "temp", "delete_after": "2024-01-01"}
)
```

### get_statistics()

Get statistics for an owner's documents.

**Signature:**
```python
async def get_statistics(
    owner_id: str,
    include_breakdown: bool = False
) -> OwnerStatistics
```

**Parameters:**
- `owner_id` (str, required): Owner identifier
- `include_breakdown` (bool, default: False): Include breakdown by document type

**Returns:**
- `OwnerStatistics` with:
  - `document_count` (int): Total documents
  - `chunk_count` (int): Total chunks
  - `total_size_bytes` (int): Estimated total size
  - `document_type_breakdown` (Dict[DocumentType, int], optional): Count by type
  - `created_date_range` (Tuple[datetime, datetime], optional): Date range

**Example:**
```python
stats = await memory.get_statistics(
    owner_id="workspace-1",
    include_breakdown=True
)

print(f"Documents: {stats.document_count}")
print(f"Chunks: {stats.chunk_count}")
print(f"Size: {stats.total_size_bytes / 1024 / 1024:.2f} MB")

if stats.document_type_breakdown:
    for doc_type, count in stats.document_type_breakdown.items():
        print(f"  {doc_type.value}: {count}")
```

## Common Patterns

### Async Context Manager (Recommended)

```python
async with LLMemory(connection_string="postgresql://localhost/mydb") as memory:
    # Add documents
    await memory.add_document(...)

    # Search
    results = await memory.search(...)
# Automatically closed
```

### Batch Document Processing

```python
documents = [
    {"name": "doc1.txt", "content": "..."},
    {"name": "doc2.txt", "content": "..."},
    {"name": "doc3.txt", "content": "..."},
]

for doc in documents:
    result = await memory.add_document(
        owner_id="workspace-1",
        id_at_origin="batch-import",
        document_name=doc["name"],
        document_type=DocumentType.TEXT,
        content=doc["content"]
    )
    print(f"Added {doc['name']}: {result.chunks_created} chunks")
```

### Filtered Search with Metadata

```python
# Add document with metadata
await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="user-123",
    document_name="report.pdf",
    document_type=DocumentType.PDF,
    content="...",
    metadata={
        "category": "financial",
        "year": 2024,
        "quarter": "Q4",
        "confidential": False
    }
)

# Search with metadata filter
results = await memory.search(
    owner_id="workspace-1",
    query_text="revenue analysis",
    metadata_filter={
        "category": "financial",
        "year": 2024
    },
    limit=10
)
```

### Paginated Document Listing

```python
page_size = 20
offset = 0

while True:
    result = await memory.list_documents(
        owner_id="workspace-1",
        limit=page_size,
        offset=offset
    )

    if not result.documents:
        break

    for doc in result.documents:
        print(f"{doc.document_name}: {doc.chunk_count} chunks")

    offset += page_size
    if offset >= result.total:
        break
```

## Exception Reference

All llmemory exceptions inherit from `LLMemoryError` base class.

### Exception Hierarchy

```
LLMemoryError (base)
├── ConfigurationError
├── ValidationError
├── DatabaseError
│   └── ConnectionError
├── EmbeddingError
├── SearchError
├── ChunkingError
├── ResourceNotFoundError
│   └── DocumentNotFoundError
├── RateLimitError
└── PermissionError
```

### LLMemoryError

Base exception for all llmemory errors.

**When raised:** Never raised directly, use specific subclasses

**Usage:**
```python
from llmemory import LLMemoryError

try:
    await memory.search(...)
except LLMemoryError as e:
    # Catches all llmemory exceptions
    print(f"LLMemory error: {e}")
```

### ConfigurationError

Configuration is invalid or incomplete.

**Common causes:**
- Missing required configuration (connection_string, API key)
- Invalid configuration values (negative pool size, invalid dimensions)
- Incompatible configuration combinations

**When raised:**
- During `LLMemory()` initialization if neither connection_string nor db_manager provided
- During `initialize()` if config validation fails
- When embedding provider configuration is invalid

**Example:**
```python
from llmemory import ConfigurationError

try:
    # Missing connection_string
    memory = LLMemory()  # Raises ConfigurationError
except ConfigurationError as e:
    print(f"Invalid configuration: {e}")
```

### ValidationError

Input validation failed.

**Common causes:**
- owner_id too long or invalid characters
- Empty or too long content
- Invalid document_name
- Negative limit or offset values

**When raised:**
- During `add_document()` if owner_id, id_at_origin, or content invalid
- During `search()` if owner_id or query_text invalid
- During `list_documents()` if pagination parameters invalid

**Example:**
```python
from llmemory import ValidationError

try:
    await memory.add_document(
        owner_id="",  # Empty owner_id - invalid
        id_at_origin="user-123",
        document_name="doc.txt",
        document_type=DocumentType.TEXT,
        content="content"
    )
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Output: "Validation failed: owner_id cannot be empty"
```

### DatabaseError

Database operation failed.

**Common causes:**
- Connection to PostgreSQL failed
- Query execution failed
- Transaction rollback
- Schema migration failed

**When raised:**
- During `initialize()` if database setup fails
- During any CRUD operation if database query fails
- During `add_document()` if insert fails

**Example:**
```python
from llmemory import DatabaseError

try:
    await memory.add_document(...)
except DatabaseError as e:
    print(f"Database error: {e}")
    # Possible causes: connection lost, disk full, constraint violation
```

### ConnectionError

Cannot connect to database (subclass of DatabaseError).

**Common causes:**
- PostgreSQL not running
- Wrong connection string
- Network issues
- Firewall blocking connection

**When raised:**
- During `initialize()` if connection fails
- During operations if connection is lost

**Example:**
```python
from llmemory import ConnectionError

try:
    memory = LLMemory(connection_string="postgresql://invalid:5432/db")
    await memory.initialize()
except ConnectionError as e:
    print(f"Cannot connect to database: {e}")
```

### EmbeddingError

Embedding generation failed.

**Common causes:**
- OpenAI API key invalid or missing
- OpenAI rate limit exceeded
- Local embedding model failed to load
- Invalid embedding dimensions

**When raised:**
- During `add_document()` if generate_embeddings=True and embedding fails
- During `process_pending_embeddings()` if batch processing fails

**Example:**
```python
from llmemory import EmbeddingError

try:
    await memory.add_document(
        owner_id="workspace-1",
        id_at_origin="user-123",
        document_name="doc.txt",
        document_type=DocumentType.TEXT,
        content="content",
        generate_embeddings=True  # Will fail if no API key
    )
except EmbeddingError as e:
    print(f"Embedding generation failed: {e}")
```

### SearchError

Search operation failed.

**Common causes:**
- Invalid search query syntax
- Vector index not built
- Embedding provider not configured for vector search
- Search timeout exceeded

**When raised:**
- During `search()` if query execution fails
- During vector search if embeddings table doesn't exist
- During hybrid search if either vector or text search fails

**Example:**
```python
from llmemory import SearchError

try:
    results = await memory.search(
        owner_id="workspace-1",
        query_text="test",
        search_type=SearchType.VECTOR  # Fails if no embeddings
    )
except SearchError as e:
    print(f"Search failed: {e}")
```

### ChunkingError

Document chunking failed.

**Common causes:**
- Invalid chunking configuration
- Document too large to chunk
- Chunking strategy not supported for document type

**When raised:**
- During `add_document()` if chunking fails
- During `process_document()` if chunker fails

**Example:**
```python
from llmemory import ChunkingError

try:
    await memory.add_document(
        owner_id="workspace-1",
        id_at_origin="user-123",
        document_name="huge.txt",
        document_type=DocumentType.TEXT,
        content="x" * 100_000_000  # Too large
    )
except ChunkingError as e:
    print(f"Chunking failed: {e}")
```

### ResourceNotFoundError

Requested resource doesn't exist.

**Common causes:**
- Document ID doesn't exist
- Chunk ID not found
- Owner has no documents

**When raised:**
- During `delete_document()` if document not found
- During `get_document()` if document doesn't exist

### DocumentNotFoundError

Specific document doesn't exist (subclass of ResourceNotFoundError).

**When raised:**
- During `get_document()` if document_id doesn't exist
- During `delete_document()` if document not found

**Example:**
```python
from llmemory import DocumentNotFoundError
from uuid import UUID

try:
    doc = await memory.get_document(
        owner_id="workspace-1",
        document_id=UUID("00000000-0000-0000-0000-000000000000")
    )
except DocumentNotFoundError as e:
    print(f"Document not found: {e}")
```

### RateLimitError

API rate limit exceeded.

**Common causes:**
- OpenAI API rate limit hit
- Too many embedding requests in short time
- Exceeded configured rate limits

**When raised:**
- During embedding generation if API rate limited
- During query expansion if LLM API rate limited

**Example:**
```python
from llmemory import RateLimitError
import asyncio

try:
    # Batch process with rate limiting
    for doc in documents:
        await memory.add_document(...)
except RateLimitError as e:
    print(f"Rate limited: {e}")
    await asyncio.sleep(60)  # Wait before retry
```

### PermissionError

Permission denied for operation.

**Common causes:**
- Attempting to access document owned by different owner_id
- Database permission denied

**When raised:**
- During operations if user doesn't have permission
- During delete if document belongs to different owner

**Example:**
```python
from llmemory import PermissionError as LLMemoryPermissionError

try:
    # Trying to access another owner's document
    doc = await memory.get_document(owner_id="workspace-1", document_id="...")
except LLMemoryPermissionError as e:
    print(f"Permission denied: {e}")
```

## Error Handling Patterns

### Basic Error Handling

```python
from llmemory import (
    LLMemoryError, ConfigurationError, ValidationError, DatabaseError,
    DocumentNotFoundError, EmbeddingError, SearchError, ChunkingError,
    ResourceNotFoundError, RateLimitError, ConnectionError
)

try:
    memory = LLMemory(connection_string="postgresql://localhost/mydb")
    await memory.initialize()

    result = await memory.add_document(
        owner_id="workspace-1",
        id_at_origin="user-123",
        document_name="test.txt",
        document_type=DocumentType.TEXT,
        content="Test content"
    )

    results = await memory.search(
        owner_id="workspace-1",
        query_text="test query"
    )

except ConfigurationError as e:
    print(f"Configuration error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except ConnectionError as e:
    print(f"Cannot connect to database: {e}")
except DatabaseError as e:
    print(f"Database error: {e}")
except DocumentNotFoundError as e:
    print(f"Document not found: {e}")
except EmbeddingError as e:
    print(f"Embedding error: {e}")
except SearchError as e:
    print(f"Search error: {e}")
except ChunkingError as e:
    print(f"Chunking error: {e}")
except RateLimitError as e:
    print(f"Rate limit hit: {e}")
    await asyncio.sleep(60)  # Wait before retry
except LLMemoryError as e:
    print(f"Unexpected llmemory error: {e}")
finally:
    await memory.close()
```

### Granular Error Handling

```python
# Handle specific errors differently
try:
    result = await memory.add_document(...)
except ValidationError as e:
    # User input error - return 400
    return {"error": str(e), "code": 400}
except EmbeddingError as e:
    # Embedding failed but document added - return partial success
    logger.error(f"Embedding failed: {e}")
    return {"warning": "Document added but embeddings pending", "code": 202}
except DatabaseError as e:
    # System error - return 500
    logger.error(f"Database error: {e}")
    return {"error": "Internal server error", "code": 500}
```

### Retry Logic for Transient Errors

```python
import asyncio
from llmemory import RateLimitError, ConnectionError

async def robust_search(memory, owner_id, query, max_retries=3):
    """Search with retry logic for transient errors."""
    for attempt in range(max_retries):
        try:
            return await memory.search(
                owner_id=owner_id,
                query_text=query
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
        except ConnectionError:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)
                continue
            raise
```

## Complete Environment Variable Reference

### Database Configuration

```bash
DATABASE_URL=postgresql://localhost/mydb  # PostgreSQL connection string
LLMEMORY_DB_MIN_POOL_SIZE=5              # Minimum connection pool size (default: 5)
LLMEMORY_DB_MAX_POOL_SIZE=20             # Maximum connection pool size (default: 20)
```

### Embedding Configuration

```bash
# Provider selection
OPENAI_API_KEY=sk-...                    # OpenAI API key (required for OpenAI embeddings)
LLMEMORY_EMBEDDING_PROVIDER=openai       # Provider: "openai" or "local-minilm" (default: "openai")

# Local embedding models
LLMEMORY_LOCAL_MODEL=all-MiniLM-L6-v2    # Local model name (default: all-MiniLM-L6-v2)
LLMEMORY_LOCAL_DEVICE=cpu                # Device: "cpu" or "cuda" (default: cpu)
LLMEMORY_LOCAL_CACHE_DIR=/path/to/cache  # Cache directory for local models
```

### Search Configuration

```bash
# HNSW Index tuning
LLMEMORY_HNSW_PROFILE=balanced           # Profile: "fast", "balanced", "accurate" (default: balanced)

# Search defaults
LLMEMORY_DEFAULT_SEARCH_TYPE=hybrid      # Default search type (default: hybrid)
LLMEMORY_SEARCH_CACHE_TTL=300            # Search cache TTL in seconds (default: 300)
```

### Query Expansion Configuration

```bash
LLMEMORY_ENABLE_QUERY_EXPANSION=1        # Enable query expansion: 1 or 0 (default: 0)
LLMEMORY_MAX_QUERY_VARIANTS=3            # Max query variants to generate (default: 3)
```

### Reranking Configuration

```bash
LLMEMORY_ENABLE_RERANK=1                 # Enable reranking: 1 or 0 (default: 0)
LLMEMORY_RERANK_PROVIDER=openai          # Provider: "openai", "lexical" (default: lexical)
LLMEMORY_RERANK_MODEL=gpt-4.1-mini       # Reranking model name
LLMEMORY_RERANK_TOP_K=50                 # Candidates to consider (default: 50)
LLMEMORY_RERANK_RETURN_K=15              # Results to return after reranking (default: 15)
LLMEMORY_RERANK_DEVICE=cpu               # Device for local rerankers: "cpu" or "cuda"
LLMEMORY_RERANK_BATCH_SIZE=16            # Batch size for local reranking (default: 16)
```

### Chunking Configuration

```bash
LLMEMORY_ENABLE_CHUNK_SUMMARIES=1        # Enable chunk summaries: 1 or 0 (default: 0)
```

### Feature Flags

```bash
LLMEMORY_DISABLE_CACHING=1               # Disable search caching (default: enabled)
LLMEMORY_DISABLE_METRICS=1               # Disable Prometheus metrics (default: enabled)
```

### Logging

```bash
LLMEMORY_LOG_LEVEL=INFO                  # Log level: DEBUG, INFO, WARNING, ERROR (default: INFO)
```

## Complete Configuration Reference

### LLMemoryConfig

Main configuration class containing all subsystem configurations.

**Constructor:**
```python
LLMemoryConfig(
    embedding: EmbeddingConfig = EmbeddingConfig(),
    chunking: ChunkingConfig = ChunkingConfig(),
    search: SearchConfig = SearchConfig(),
    database: DatabaseConfig = DatabaseConfig(),
    validation: ValidationConfig = ValidationConfig(),
    enable_caching: bool = True,
    enable_metrics: bool = True,
    enable_background_processing: bool = True,
    log_level: str = "INFO",
    log_slow_queries: bool = True,
    slow_query_threshold: float = 1.0
)
```

**Creating and using config:**
```python
from llmemory import LLMemoryConfig

# Use default configuration
config = LLMemoryConfig()

# Modify specific settings
config.embedding.default_provider = "openai"
config.chunking.default_parent_size = 1000
config.search.enable_query_expansion = True

# Use with LLMemory
memory = LLMemory(
    connection_string="postgresql://localhost/mydb",
    config=config
)
```

**Loading from environment:**
```python
# Automatically reads from environment variables
config = LLMemoryConfig.from_env()
memory = LLMemory(connection_string="...", config=config)
```

### EmbeddingConfig

Configuration for embedding generation.

**Fields:**
- `default_provider` (str, default: "openai"): Default embedding provider
- `providers` (Dict[str, EmbeddingProviderConfig]): Available providers
- `auto_create_tables` (bool, default: True): Auto-create provider tables

**Example:**
```python
config = LLMemoryConfig()
config.embedding.default_provider = "local-minilm"
```

### EmbeddingProviderConfig

Configuration for a single embedding provider.

**Fields:**
- `provider_type` (str): "openai" or "local"
- `model_name` (str): Model name
- `dimension` (int): Embedding dimensions
- `api_key` (Optional[str]): API key (for OpenAI)
- `device` (str, default: "cpu"): Device for local models ("cpu" or "cuda")
- `cache_dir` (Optional[str]): Cache directory for local models
- `batch_size` (int, default: 100): Batch size for processing
- `max_retries` (int, default: 3): Max retries on failure
- `retry_delay` (float, default: 1.0): Delay between retries in seconds
- `timeout` (float, default: 30.0): Request timeout in seconds
- `max_tokens_per_minute` (int, default: 1,000,000): Rate limit for tokens
- `max_requests_per_minute` (int, default: 3,000): Rate limit for requests

### ChunkingConfig

Configuration for document chunking (in `config.py`).

**Fields:**
- `enable_chunk_summaries` (bool, default: False): Generate summaries for chunks
- `summary_max_tokens` (int, default: 120): Max tokens for summaries
- `min_chunk_size` (int, default: 50): Minimum chunk size in tokens
- `max_chunk_size` (int, default: 2000): Maximum chunk size in tokens
- `enable_contextual_retrieval` (bool, default: False): Prepend document context to chunks before embedding (Anthropic's approach)
- `context_template` (str): Template for contextual retrieval format (default: "Document: {document_name}\nType: {document_type}\n\n{content}")

**Contextual Retrieval Example:**
```python
config = LLMemoryConfig()
config.chunking.enable_contextual_retrieval = True

memory = LLMemory(connection_string="...", config=config)

# Chunks are embedded with document context prepended:
# "Document: Q3 Report\nType: report\n\nRevenue increased 15%"
#
# But chunk.content remains original for display:
# "Revenue increased 15%"

await memory.add_document(
    owner_id="workspace-1",
    id_at_origin="kb",
    document_name="Q3 Report",
    document_type=DocumentType.REPORT,
    content="Revenue increased 15% QoQ..."
)
```

**Example:**
```python
config = LLMemoryConfig()
config.chunking.enable_chunk_summaries = True
config.chunking.summary_max_tokens = 100
```

### SearchConfig

Configuration for search operations.

**Fields:**
- `default_limit` (int, default: 10): Default result limit
- `max_limit` (int, default: 100): Maximum allowed limit
- `default_search_type` (str, default: "hybrid"): Default search type
- `hnsw_profile` (str, default: "balanced"): HNSW index profile
- `rrf_k` (int, default: 50): RRF constant for fusion
- `enable_query_expansion` (bool, default: False): Enable query expansion
- `max_query_variants` (int, default: 3): Max query variants
- `query_expansion_model` (Optional[str]): Model for expansion
- `include_keyword_variant` (bool, default: True): Include keyword variant
- `enable_rerank` (bool, default: False): Enable reranking
- `default_rerank_model` (Optional[str]): Reranking model
- `rerank_provider` (str, default: "lexical"): Reranker provider
- `rerank_top_k` (int, default: 50): Candidates for reranking
- `rerank_return_k` (int, default: 15): Results after reranking
- `rerank_device` (Optional[str]): Device for local rerankers
- `rerank_batch_size` (int, default: 16): Batch size for reranking
- `hnsw_ef_search` (int, default: 100): HNSW ef_search parameter
- `vector_search_limit` (int, default: 100): Internal vector search limit
- `text_search_limit` (int, default: 100): Internal text search limit
- `cache_ttl` (int, default: 3600): Cache TTL in seconds
- `cache_max_size` (int, default: 10000): Max cache entries
- `search_timeout` (float, default: 5.0): Search timeout in seconds
- `min_score_threshold` (float, default: 0.0): Minimum score threshold

**Example:**
```python
config = LLMemoryConfig()
config.search.enable_query_expansion = True
config.search.enable_rerank = True
config.search.rerank_provider = "openai"
config.search.hnsw_profile = "accurate"
```

### DatabaseConfig

Configuration for database operations.

**Fields:**
- `min_pool_size` (int, default: 5): Minimum connection pool size
- `max_pool_size` (int, default: 20): Maximum connection pool size
- `connection_timeout` (float, default: 10.0): Connection timeout in seconds
- `command_timeout` (float, default: 30.0): Command timeout in seconds
- `schema_name` (str, default: "llmemory"): PostgreSQL schema name
- `documents_table` (str, default: "documents"): Documents table name
- `chunks_table` (str, default: "document_chunks"): Chunks table name
- `embeddings_queue_table` (str, default: "embedding_queue"): Queue table name
- `search_history_table` (str, default: "search_history"): Search history table
- `embedding_providers_table` (str, default: "embedding_providers"): Providers table
- `chunk_embeddings_prefix` (str, default: "chunk_embeddings_"): Embedding table prefix
- `hnsw_index_name` (str, default: "document_chunks_embedding_hnsw"): HNSW index name
- `hnsw_m` (int, default: 16): HNSW M parameter
- `hnsw_ef_construction` (int, default: 200): HNSW ef_construction parameter

**Example:**
```python
config = LLMemoryConfig()
config.database.schema_name = "my_app_llmemory"
config.database.min_pool_size = 10
config.database.max_pool_size = 50
```

### ValidationConfig

Configuration for input validation.

**Fields:**
- `max_owner_id_length` (int, default: 255): Max owner_id length
- `max_id_at_origin_length` (int, default: 255): Max id_at_origin length
- `max_document_name_length` (int, default: 500): Max document name length
- `max_content_length` (int, default: 10,000,000): Max content length (10MB)
- `max_metadata_size` (int, default: 65536): Max metadata size (64KB)
- `min_content_length` (int, default: 10): Minimum content length
- `valid_owner_id_pattern` (str): Regex for valid owner_id
- `valid_id_at_origin_pattern` (str): Regex for valid id_at_origin

**Example:**
```python
config = LLMemoryConfig()
config.validation.max_content_length = 20_000_000  # 20MB
config.validation.min_content_length = 50  # Require at least 50 chars
```

## Common Mistakes

❌ **Wrong: Not calling initialize()**
```python
memory = LLMemory(connection_string="...")
results = await memory.search(...)  # Error: not initialized
```

✅ **Right: Always call initialize()**
```python
memory = LLMemory(connection_string="...")
await memory.initialize()  # Required!
results = await memory.search(...)
```

❌ **Wrong: Not closing connections**
```python
memory = LLMemory(connection_string="...")
await memory.initialize()
# ... use memory ...
# Missing: await memory.close()
```

✅ **Right: Use context manager**
```python
async with LLMemory(connection_string="...") as memory:
    # ... use memory ...
# Automatically closed
```

❌ **Wrong: Forgetting owner_id filtering**
```python
results = await memory.search(
    owner_id="workspace-1",
    query_text="sensitive data"
)
# Results only from workspace-1 (good!)
# But need to verify owner_id matches current user
```

✅ **Right: Always validate owner_id**
```python
current_workspace = get_current_workspace()
results = await memory.search(
    owner_id=current_workspace,  # Validated owner
    query_text="sensitive data"
)
```

## Related Skills

- `hybrid-search` - Vector + BM25 hybrid search patterns
- `multi-query` - Query expansion and multi-query retrieval
- `multi-tenant` - Multi-tenant isolation patterns for SaaS
- `rag` - Building complete RAG systems with reranking

## Important Notes

**Multi-Tenancy:**
Always provide `owner_id` for proper data isolation. llmemory automatically filters all operations by owner.

**Connection Pooling:**
For production applications with multiple services, use `from_db_manager()` with a shared connection pool (see `pgdbm-shared-pool` skill).

**Chunking:**
Documents are automatically chunked during `add_document()`. Default strategy is hierarchical chunking which creates parent and child chunks for better retrieval.

**Embeddings:**
Embeddings are generated automatically unless `generate_embeddings=False`. For batch operations, consider using background processing.

**Search Types:**
- `VECTOR`: Best for semantic similarity
- `TEXT`: Best for exact keyword matching
- `HYBRID`: Best for most use cases (combines both)
