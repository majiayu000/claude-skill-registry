---
name: alphaear-search
description: Perform web searches and local context searches. Use when the user needs general info from the web (Jina/DDG/Baidu) or needs to retrieve information from a local document store (RAG).
---

# AlphaEar Search Skill

## Overview

This skill provides unified search capabilities: web search (via DuckDuckGo, Jina, or Baidu) and local hybrid search (BM25 + Vector) for RAG applications.

## Capabilities

### 1. Web Search

Use `scripts/search_tools.py` to perform web searches.

**Key Methods:**

-   `search(query, engine, max_results)`: Execute a search.
    -   **Engines**: `jina`, `ddg`, `baidu`.
    -   **Returns**: Dictionary with `results` (JSON string) and metadata.
-   `aggregate_search(query)`: Search across multiple engines and aggregate results.

**Example Usage (Python):**

```python
from scripts.database_manager import DatabaseManager
from scripts.search_tools import SearchTools

db = DatabaseManager()
tools = SearchTools(db)

# Simple Search
results = tools.search("NVIDIA Earnings", engine="ddg")
print(results)
```

### 2. Local Hybrid Search (RAG)

Use `scripts/hybrid_search.py` for in-memory document retrieval.

**Key Features:**
-   Add documents.
-   Search with weighted keyword matching (simple algorithm).

**Example Usage (Python):**

```python
from scripts.hybrid_search import InMemoryRAG

rag = InMemoryRAG()
rag.add({"id": "doc1", "content": "Apple released Vision Pro.", "title": "Tech News"})
rag.add({"id": "doc2", "content": "Tesla cybertruck delivery.", "title": "Auto News"})

# Search
hits = rag.search("Vision Pro")
print(hits)
```

## Dependencies

-   `duckduckgo-search`
-   `requests`
-   `sqlite3` (built-in)

Ensure `DatabaseManager` is initialized correctly.
