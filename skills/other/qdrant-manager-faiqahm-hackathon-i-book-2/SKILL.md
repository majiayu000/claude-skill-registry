---
name: qdrant-manager
description: |
  Manage Qdrant Cloud collections, including vectorization of textbook chapters and metadata tagging for RAG retrieval.
  Agent: AIEngineer
version: 1.0.0
inputs:
  qdrant_url:
    description: Qdrant Cloud cluster URL
    required: true
    example: "https://xxx.qdrant.io"
  qdrant_api_key:
    description: Qdrant API key
    required: true
    example: "your-api-key"
  collection_name:
    description: Name of the collection
    required: false
    default: "textbook_chapters"
    example: "physical_ai_book"
  embedding_model:
    description: OpenAI embedding model to use
    required: false
    default: "text-embedding-3-small"
    example: "text-embedding-3-large"
  vector_size:
    description: Vector dimension size
    required: false
    default: "1536"
    example: "3072"
---

# Qdrant Manager

**Agent:** AIEngineer

Manage Qdrant Cloud collections for the Physical AI textbook RAG system. This skill handles vectorization of textbook chapters, metadata tagging, and collection management for efficient retrieval-augmented generation.

## Quick Setup

```bash
# Set environment variables
export QDRANT_URL="https://xxx.qdrant.io"
export QDRANT_API_KEY="your-api-key"
export OPENAI_API_KEY="sk-..."

# Initialize collection
.claude/skills/qdrant-manager/scripts/setup.sh --init

# Vectorize all chapters
.claude/skills/qdrant-manager/scripts/setup.sh --vectorize docs/

# Query the collection
.claude/skills/qdrant-manager/scripts/setup.sh --query "What is ROS 2?"
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--init` | Initialize/create the collection | - |
| `--vectorize PATH` | Vectorize markdown files in PATH | - |
| `--query TEXT` | Query the collection | - |
| `--delete` | Delete the collection | - |
| `--info` | Show collection info | - |
| `--list` | List all collections | - |
| `--collection NAME` | Collection name | `textbook_chapters` |
| `--model MODEL` | Embedding model | `text-embedding-3-small` |
| `--batch-size N` | Batch size for vectorization | `10` |
| `--top-k N` | Number of results for query | `5` |
| `-h, --help` | Show help message | - |

## What It Does

### 1. Collection Management

Creates and manages Qdrant collections with optimized settings for textbook content:

```python
# Collection schema
{
    "vectors": {
        "size": 1536,  # text-embedding-3-small
        "distance": "Cosine"
    },
    "on_disk_payload": True  # Optimize for large documents
}
```

### 2. Chapter Vectorization

Processes markdown files with intelligent chunking:

- **Chunk Strategy**: Split by headers (##, ###) for semantic coherence
- **Overlap**: 100 tokens overlap between chunks
- **Max Chunk Size**: 500 tokens per chunk
- **Metadata Extraction**: Title, chapter, section, language, keywords

### 3. Metadata Schema

Each vector point includes rich metadata for filtered retrieval:

```json
{
    "id": "uuid-v4",
    "vector": [0.1, 0.2, ...],
    "payload": {
        "content": "The actual text content...",
        "source": "docs/chapter-1/index.md",
        "chapter": 1,
        "section": "Introduction",
        "title": "Introduction to Physical AI & ROS 2",
        "language": "en",
        "locale": "en-US",
        "keywords": ["ros2", "physical-ai", "robotics"],
        "word_count": 245,
        "created_at": "2026-01-02T00:00:00Z",
        "chunk_index": 0,
        "total_chunks": 5
    }
}
```

### 4. RAG Query Support

Semantic search with metadata filtering:

```python
# Example: Query with language filter
results = client.search(
    collection_name="textbook_chapters",
    query_vector=embed("What is ROS 2?"),
    query_filter={
        "must": [
            {"key": "language", "match": {"value": "en"}}
        ]
    },
    limit=5
)
```

## Bundled Resources

### 1. Python Dependencies

**File**: `requirements.txt`

```
qdrant-client>=1.7.0
openai>=1.0.0
tiktoken>=0.5.0
python-dotenv>=1.0.0
rich>=13.0.0
```

### 2. Collection Configuration

**File**: `assets/collection_config.json`

```json
{
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    },
    "optimizers_config": {
        "indexing_threshold": 20000
    },
    "on_disk_payload": true,
    "replication_factor": 1
}
```

### 3. Chunking Configuration

**File**: `assets/chunking_config.json`

```json
{
    "chunk_size": 500,
    "chunk_overlap": 100,
    "separators": ["## ", "### ", "\n\n", "\n"],
    "length_function": "tiktoken",
    "model": "text-embedding-3-small"
}
```

### 4. Vectorization Script

**File**: `scripts/vectorize.py`

```python
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from openai import OpenAI
import tiktoken
import uuid
import json
from pathlib import Path

class TextbookVectorizer:
    def __init__(self, qdrant_url, qdrant_api_key, openai_api_key):
        self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.openai = OpenAI(api_key=openai_api_key)
        self.encoder = tiktoken.encoding_for_model("text-embedding-3-small")

    def create_collection(self, name: str, vector_size: int = 1536):
        self.qdrant.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    def chunk_markdown(self, content: str, source: str) -> list:
        # Split by headers for semantic coherence
        chunks = []
        current_chunk = ""
        current_section = "Introduction"

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_chunk:
                    chunks.append({"content": current_chunk, "section": current_section})
                current_section = line[3:].strip()
                current_chunk = line + "\n"
            else:
                current_chunk += line + "\n"
                if len(self.encoder.encode(current_chunk)) > 500:
                    chunks.append({"content": current_chunk, "section": current_section})
                    current_chunk = ""

        if current_chunk:
            chunks.append({"content": current_chunk, "section": current_section})

        return chunks

    def embed(self, text: str) -> list:
        response = self.openai.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def vectorize_file(self, filepath: Path, collection: str):
        content = filepath.read_text()
        chunks = self.chunk_markdown(content, str(filepath))

        points = []
        for i, chunk in enumerate(chunks):
            vector = self.embed(chunk["content"])
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "content": chunk["content"],
                    "source": str(filepath),
                    "section": chunk["section"],
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            ))

        self.qdrant.upsert(collection_name=collection, points=points)
        return len(points)
```

### 5. Input Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `qdrant_url` | Yes | - | Qdrant Cloud cluster URL |
| `qdrant_api_key` | Yes | - | Qdrant API key |
| `collection_name` | No | `textbook_chapters` | Collection name |
| `embedding_model` | No | `text-embedding-3-small` | OpenAI embedding model |
| `vector_size` | No | `1536` | Vector dimension |

## Usage Instructions

### Step 1: Set Environment Variables

```bash
# Add to .env file
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key
OPENAI_API_KEY=sk-...
```

### Step 2: Initialize Collection

```bash
.claude/skills/qdrant-manager/scripts/setup.sh --init --collection textbook_chapters
```

### Step 3: Vectorize Chapters

```bash
# Vectorize English chapters
.claude/skills/qdrant-manager/scripts/setup.sh --vectorize docs/

# Vectorize Urdu translations
.claude/skills/qdrant-manager/scripts/setup.sh --vectorize i18n/ur/docusaurus-plugin-content-docs/current/
```

### Step 4: Query for RAG

```bash
# Simple query
.claude/skills/qdrant-manager/scripts/setup.sh --query "How do I install ROS 2?"

# Query with top-k
.claude/skills/qdrant-manager/scripts/setup.sh --query "Gazebo simulation" --top-k 10
```

### Step 5: Verify Collection

```bash
# Show collection info
.claude/skills/qdrant-manager/scripts/setup.sh --info

# List all collections
.claude/skills/qdrant-manager/scripts/setup.sh --list
```

## Verification Checklist

- [ ] `QDRANT_URL` environment variable set
- [ ] `QDRANT_API_KEY` environment variable set
- [ ] `OPENAI_API_KEY` environment variable set
- [ ] Collection created successfully
- [ ] Chapters vectorized without errors
- [ ] Query returns relevant results
- [ ] Metadata filtering works correctly

## Integration with RAG Chatbot

This skill provides the vector storage for the RAG chatbot (Feature 002). The chatbot queries this collection to retrieve relevant context for answering user questions.

```python
# In RAG chatbot
from qdrant_client import QdrantClient

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def get_context(query: str, language: str = "en") -> list:
    query_vector = embed(query)
    results = client.search(
        collection_name="textbook_chapters",
        query_vector=query_vector,
        query_filter={"must": [{"key": "language", "match": {"value": language}}]},
        limit=5
    )
    return [hit.payload["content"] for hit in results]
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Connection refused** | Check QDRANT_URL is correct and cluster is running |
| **Authentication failed** | Verify QDRANT_API_KEY is valid |
| **Embedding rate limit** | Reduce --batch-size or add delays |
| **Collection not found** | Run --init first to create collection |
| **Out of memory** | Use smaller --batch-size |
| **Slow vectorization** | Use --batch-size 20 for faster processing |

## Requirements

- Python 3.9+
- Qdrant Cloud account (or self-hosted Qdrant)
- OpenAI API key (for embeddings)
- pip packages: qdrant-client, openai, tiktoken

## Cost Considerations

| Resource | Cost |
|----------|------|
| **Qdrant Cloud Free Tier** | 1GB storage, 1M vectors |
| **OpenAI text-embedding-3-small** | $0.02 / 1M tokens |
| **Estimated for 3 chapters** | ~$0.01 (one-time) |

## Related

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- Skill: `vercel-fastapi-link` - Backend API with RAG endpoints
- Feature: `002-rag-chatbot` - RAG chatbot specification

## Changelog

### v1.0.0 (2026-01-02)
**Initial Release**

- Collection creation and management
- Markdown chunking with header-based splitting
- OpenAI embedding integration (text-embedding-3-small)
- Metadata extraction (chapter, section, language, keywords)
- Query support with filtering
- Batch vectorization with progress tracking
