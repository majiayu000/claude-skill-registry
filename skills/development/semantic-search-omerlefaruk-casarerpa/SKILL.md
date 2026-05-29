---
name: semantic-search
description: Semantic search the CasareRPA codebase using the local ChromaDB index and MCP server. Use when: locating code by intent, finding classes/functions without exact names, exploring patterns across layers.
---

# Semantic Search

Use the local ChromaDB index for intent-based discovery. Prefer semantic search for concepts and `rg` for exact symbols.

## Quick Start

1. Build or refresh the index:
   `python scripts/index_codebase.py`
2. Query via the MCP tool:
   `python scripts/chroma_search_mcp.py`
3. Call `search_codebase(query, top_k)` with a natural-language query.

## Direct Python Query

```python
from fastembed import TextEmbedding
from casare_rpa.infrastructure.ai.vector_store import get_vector_store

store = get_vector_store(persist_path=".chroma")
model = TextEmbedding("sentence-transformers/all-MiniLM-L6-v2")
emb = list(model.embed(["browser automation click"]))[0].tolist()
results = await store.search(
    query="browser automation click",
    collection="casare_codebase",
    top_k=5,
    query_embedding=emb,
)
```

## Notes

- Index scope: `src/` Python files only.
- Index location: `.chroma/` in repo root.
- Re-run indexing if results look stale.
