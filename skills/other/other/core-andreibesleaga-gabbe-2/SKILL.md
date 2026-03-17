---
name: Knowledge Connectors
description: Manage knowledge integration via MCP, Vector DBs, and A2A connectors.
context_cost: medium
---
# Knowledge Connectors Skill

## Triggers
- "Connect to knowledge base"
- "Ingest documentation"
- "Query vector database"
- "Setup RAG pipeline"
- "Index project files"

## Role
You are a Knowledge Engineer responsible for connecting the agent to external and internal information sources.

## Workflow

1.  **Source Identification**
    -   Identify authoritative sources (Docs, DBs, APIs, PDF/Markdown files).
    -   Map sources to domain entities using `templates/brain/KNOWLEDGE_MAP_TEMPLATE.md`.

2.  **Connector Setup (MCP)**
    -   **Vector DBs**: Configure Qdrant/Chroma/Pinecone via `MCP_CONFIG_TEMPLATE.json`.
    -   **External APIs**: Configure Notion/Linear/GitHub MCPs.
    -   **Local Files**: Use `filesystem-kb` or built-in file reading.

3.  **Ingestion & Indexing**
    -   **Chunking**: Split large documents (Markdown/PDF) into semantic chunks (500-1000 tokens).
    -   **Embedding**: Use local (e.g., all-MiniLM-L6-v2) or remote (OpenAI/Cohere) embeddings.
    -   **Upsert**: Store vectors in the configured Vector DB collection.

4.  **Retrieval (RAG) with Fallback**
    -   **Attempt 1: Vector Search**
        -   Query configured Vector DB.
        -   If successful: Return top-k chunks.
    -   **Attempt 2: SQLite FTS (Fallback)**
        -   If Vector DB fails/timeouts: Query local `knowledge.db` (Full Text Search).
    -   **Attempt 3: Filesystem Grep (Emergency)**
        -   If SQLite fails: `grep -r "keywords" agents/memory/semantic/`
    -   **Context Stuffing**: Inject best available results into Agent context.
    -   **Citation**: Clearly mark source (VectorDB vs Fallback).

## Tools & Commands

```bash
# Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# LangChain / LlamaIndex (Python)
pip install llama-index qdrant-client

# Flowise / LangFlow (No-Code)
npx flowise start
```

## A2A (Agent-to-Agent) Knowledge Exchange
-   **Protocol**: Use `agent-protocol.skill.md` for structured knowledge exchange.
-   **Format**: JSON-LD or Markdown with frontmatter metadata.
-   **Handshake**: Verify agent identity and capability before sharing sensitive knowledge.

## Safety Rules
1.  **Data Privacy**: Never index PII or secrets (API keys, passwords) into Vector DBs.
2.  **Stale Data**: Implement TTL (Time-To-Live) or re-indexing schedules for volatile data.
3.  **Access Control**: Respect source ACLs (e.g., if user can't see Notion page, Agent shouldn't retrieve it).
