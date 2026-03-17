---
name: pytidb
description: PyTiDB (pytidb) setup and usage for TiDB from Python. Covers connecting, table modeling (TableModel), CRUD, raw SQL, transactions, vector/full-text/hybrid search, auto-embedding, custom embedding functions, and reference templates/snippets (vector/hybrid/image) plus agent-oriented examples (RAG/memory/text2sql).
allowed-tools: ["bash", "write", "read_file"]
---

# PyTiDB (pytidb)

Use this skill to connect to TiDB from Python via `pytidb`, define tables, and build search / AI features on top.

## When to Use This Skill

- You want a Python ORM-like experience on TiDB via `pytidb` (built on SQLAlchemy).
- You want vector search / full-text search / hybrid search on TiDB with high-level APIs.
- You want runnable starter templates (scripts + small examples) you can adapt.

**Need to provision a TiDB Cloud cluster first?** Use `tidbx` (TiDB X) for cluster lifecycle guidance.

## Code Generation Rules (Python)

- Never hardcode credentials; use env vars (`.env`) and document required variables.
- Prefer `python -m venv .venv` and pinned deps for reproducibility.
- When editing requirements.txt, do not invent pytidb versions, use an unpinned pytidb by default unless the user explicitly requests it and the version has been verified to exist.
- Keep examples minimal and runnable; avoid framework-specific assumptions unless the user asks.
- Use parameterized SQL for any dynamic value (SQL injection safety).
- For interactive environments, avoid “table already defined” errors (use `extend_existing` / `open_table` / `if rows()==0` patterns).

## Available Guides

Each guide is a self-contained walkthrough with a checklist and phases:

- `guides/quickstart.md` — one-file “connect → create table → insert → vector search”
- `guides/search.md` — vector / full-text / hybrid: when to use which, plus gotchas
- `guides/demos.md` — examples playbook (vector/hybrid/image)
- `guides/agent-apps.md` — agent-ish examples (RAG / memory / text2sql)
- `guides/troubleshooting.md` — connection, TLS, embedding, and index/search issues
- `guides/custom-embedding.md` — implement a custom embedding function (example: BGE-M3)

I’ll infer your intent (CRUD vs search vs “agent app”), then point you to the smallest guide and template set that gets you running.

## Templates & Scripts

Each template is a complete file you can copy into your project. Choose the smallest one that matches your goal.

### Core usage

- `templates/quickstart.py` — minimal end-to-end: connect → create table → insert → vector search
- `templates/crud.py` — basic table modeling + CRUD lifecycle (create/truncate/insert/query/update/delete)
- `templates/auto_embedding.py` — auto embedding with pluggable providers (env-driven)
- `templates/vector_search.py` — vector search example (optional metadata filter + threshold)
- `templates/hybrid_search.py` — hybrid search example (FullTextField + vector field) with fused scoring

### Image search

- `templates/image_search.py` — image-to-image or text-to-image search (requires multimodal embedding + Pillow)
- `templates/image_search_data_loader.py` — loads Oxford Pets dataset into TiDB (used by `image_search.py`)

### Custom embeddings

- `templates/custom_embedding_function.py` — example `BaseEmbeddingFunction` implementation (BGE-M3 via FlagEmbedding)
- `templates/custom_embedding.py` — uses the custom embedder with auto embedding + vector search

### Agent-ish examples

- `templates/rag.py` — minimal RAG: retrieve via vector search, then generate via local LLM (Ollama via LiteLLM)
- `templates/memory_lib.py` — reusable “memory” library (extract facts → store → retrieve)
- `templates/memory.py` — CLI memory chat example using `memory_lib.py`
- `templates/text2sql.py` — interactive Text2SQL (generates SQL via OpenAI; asks before executing)

### Scripts

- `scripts/validate_connection.py` — quick connection + `SELECT 1` smoke test (supports params or `DATABASE_URL`)

## Related Skills

- `tidbx` — provision/manage TiDB Cloud (TiDB X) clusters

---

## Workflow

I will:
1. Confirm your TiDB deployment (Cloud Starter vs self-managed) and how you want to connect (params vs `DATABASE_URL`).
2. Help you set env vars, validate the connection, and choose the right path:
   - CRUD/table modeling
   - vector/full-text/hybrid search (and embedding provider)
   - example templates
3. Generate the minimal set of files and commands to get you running.
