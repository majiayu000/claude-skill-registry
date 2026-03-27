---
name: mpep-search
description: Expert system for searching USPTO MPEP, 35 USC statutes, 37 CFR regulations, and post-Jan 2024 updates.
---

# MPEP Search Skill

Search MPEP corpus through hybrid RAG (FAISS vector + BM25 keyword + HyDE + cross-encoder reranking).

**Sources:**
- MPEP: Manual of Patent Examining Procedure
- 35 USC: United States Code Title 35
- 37 CFR: Code of Federal Regulations Title 37
- Subsequent Publications: Federal Register updates (post-Jan 2024)

## Core Operations

### 1. `search_mpep`

**Inputs:**
- `query` (string, required): Search query (minimum 3 characters)
- `top_k` (int, optional): Number of results (default: 5, max: 20)
- `retrieve_k` (int | None, optional): Candidates before reranking (default: top_k * 4, max: 100)
- `source_filter` (string | None, optional): Filter by source (`"MPEP"`, `"35_USC"`, `"37_CFR"`, `"SUBSEQUENT"`, or `None`)
- `is_statute` (bool | None, optional): Filter for statute content
- `is_regulation` (bool | None, optional): Filter for regulation content
- `is_update` (bool | None, optional): Filter for recent updates

**Outputs:**
```python
{
    "rank": int,
    "source": str,
    "section": str,
    "file": str,
    "page": int,
    "has_statute": bool,
    "has_mpep_ref": bool,
    "has_rule_ref": bool,
    "is_statute": bool,
    "is_regulation": bool,
    "is_update": bool,
    "relevance_score": float,
    "text": str,
    # Optional for SUBSEQUENT:
    "doc_type": str,
    "fr_citation": str,
    "effective_date": str
}
```

**Examples:**
```python
# Basic search
search_mpep("enablement requirement 35 USC 112", top_k=5)

# Search only statutes
search_mpep("written description", top_k=10, is_statute=True)

# Search recent updates
search_mpep("AI inventorship", is_update=True)

# Filter by source
search_mpep("fee schedule", source_filter="37_CFR")
```

### 2. `get_mpep_section`

Retrieve all content from specific MPEP section.

**Inputs:**
- `section_number` (string, required): MPEP section number (e.g., `"2100"`, `"608.01"`)
- `max_chunks` (int, optional): Maximum chunks to return (default: 50)

**Outputs:**
```python
{
    "section": str,
    "total_chunks": int,
    "chunks": [
        {
            "text": str,
            "metadata": {
                "source": str,
                "file": str,
                "page": int,
                "section": str,
                "has_statute": bool,
                "has_mpep_ref": bool,
                "has_rule_ref": bool,
                "is_statute": bool,
                "is_regulation": bool,
                "is_update": bool
            }
        }
    ]
}
```

**Error Response:**
```python
{"error": "No content found for MPEP section {section_number}"}
```

**Examples:**
```python
# Get MPEP 2100 (Patentability)
get_mpep_section("2100", max_chunks=50)

# Get subsection
get_mpep_section("608.01")
```

## Input Validation

**Query validation:**
- Minimum 3 characters
- Case-insensitive
- No empty/whitespace-only queries

**Section number validation:**
- Numeric with optional decimal (e.g., "100", "2100", "608.01")

**Limits:**
- `top_k` capped at 20
- `retrieve_k` capped at 100

## Implementation Notes

**Index Location:**
- FAISS index: `mcp_server/index/mpep_index.faiss`
- Metadata: `mcp_server/index/mpep_metadata.json`
- BM25 index: `mcp_server/index/mpep_bm25.json`

**Search Architecture:**
1. HyDE Query Expansion (hypothetical documents)
2. Hybrid Retrieval (FAISS vector + BM25 keyword via RRF)
3. Cross-Encoder Reranking (final relevance scores)
4. Metadata Filtering (source/type filters)

**Dependencies:**
- sentence-transformers (BGE-base-en-v1.5)
- FAISS (vector search)
- rank-bm25 (keyword search)
- Cross-encoder (reranking)
- HyDE (optional, graceful degradation)

**Error Handling:**
- Clear error messages for missing index/invalid queries
- Graceful degradation if HyDE fails
- Input validation before processing
