---
name: RAG Pipeline
description: Details on the Retrieval Augmented Generation pipeline, Ingestion, and Vector Search.
---

# RAG Pipeline Logic

## Ingestion
- **Script**: `backend/ingest.py`
- **Process**:
    1. Scans `docs/`.
    2. Cleans MDX (removes frontmatter/imports).
    3. Chunks text (1000 chars, 100 overlap).
    4. Embeds using `models/text-embedding-004`.
    5. Upserts to Qdrant collection `physical_ai_book`.
- **Run**: `python backend/ingest.py`

## Vector Search (Qdrant)
- **Client**: `qdrant-client`
- **Collection**: `physical_ai_book`
- **Vector Size**: 768 (Gecko-004)
- **Similarity**: Cosine

## Prompt Engineering
- **File**: `backend/utils/helpers.py`.
- **RAG Prompt**: Constructs a prompt containing retrieved context chunks.
- **Personalization**: `backend/personalization.py` creates system instructions based on `software_background` and `hardware_background` of the user.

## Agentic Flow
We use a custom `Agent` class (`backend/agents.py`) that wraps the LLM calls, allowing for future expansion into multi-agent workflows.
