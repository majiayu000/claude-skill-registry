---
name: ai-vector-brain
description: Builds vector-brain implementations for repos, docs hubs, and compliance corpora. Use when creating pgvector retrieval brains with scripts, SQL, manifests, and evals.
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.2"
last_validated: 2026-07-11
---

# AI Vector Brain

Build a vector brain implementation. V1 default: Postgres + pgvector. Pick a corpus playbook.

Use this skill when the user asks to:

- build a vector brain, RAG brain, LLM brain, repo brain, docs brain, or compliance brain
- turn a repo, docs hub, policy corpus, guide set, or generated context artifacts into a repeatable retrieval layer
- choose a vector-brain backend and produce a concrete implementation path
- create SQL, manifests, ingestion scripts, eval seeds, or an agent retrieval tool contract

## Boundary Contract

| Skill | Owns | Does Not Own |
|---|---|---|
| `ai-context-layer` | Where context lives: memory vs retrieval vs tools, grounding, provenance, lifecycle, app context architecture | Paste-ready SQL, vector DB schemas, embedding pipelines, ingest scripts |
| `ai-rag` | Retrieval theory: chunking principles, hybrid fusion concepts, reranking concepts, eval theory, when retrieval is wrong | Operational DDL, backend-specific SQL, concrete ingest scripts |
| `ai-agents` | Agent topology, tool use, planner/critic flows, agent vs workflow decisions | Retrieval backend implementation |
| `ai-bot-builder` | Bot UX, conversation flows, escalation, channel integration, KB use in a bot surface | KB/vector-brain construction |
| `ai-vector-brain` | How to build: corpus inventory, manifests, DDL, ingest scripts, embeddings, hybrid search, eval seeds, backend recipes | Broad RAG theory, app context strategy, agent topology, bot UX |

## Quick Reference

| Need | Start Here |
|------|------------|
| Decide vector vs relational vs graph (upstream choice) | [../software-database-design/SKILL.md#storage-paradigm-matrix-relational-vs-graph-vs-vector](../software-database-design/SKILL.md#storage-paradigm-matrix-relational-vs-graph-vs-vector) |
| Build the default brain | [references/postgres-pgvector-default.md](references/postgres-pgvector-default.md) |
| Choose backend (matrix + decision flow) | [references/backend-selection.md](references/backend-selection.md) |
| Per-backend deep dive (S3 Vectors, Turbopuffer, Pinecone Serverless, Bedrock KB, OpenSearch, Vertex, Azure, edge) | [references/backend-selection-extended.md](references/backend-selection-extended.md) |
| S3 Vectors cost, limits (2B vectors/index GA limit, 14-region GA Dec 2025), direct API vs Bedrock KB | [references/s3-vectors-backend.md](references/s3-vectors-backend.md) |
| Estimate cost (formulas, sizing, worked examples for hot vs object-backed vs managed) | [references/cost-calculation.md](references/cost-calculation.md) |
| Pick corpus recipe | [references/corpus-playbooks.md](references/corpus-playbooks.md) |
| Define portable manifest | [references/framework.md](references/framework.md) |
| Expose brain to agents | [references/agent-tool-contract.md](references/agent-tool-contract.md) |
| Choose eval gates | [references/eval-by-corpus-type.md](references/eval-by-corpus-type.md) |
| Prove retrieval before ANN | [../ai-rag/scripts/exact_search_baseline.py](../ai-rag/scripts/exact_search_baseline.py) + [../ai-rag/assets/eval/golden-retrieval-cases.jsonl](../ai-rag/assets/eval/golden-retrieval-cases.jsonl) |
| Compare backends fairly | [../ai-rag/references/backend-comparison-fixtures.md](../ai-rag/references/backend-comparison-fixtures.md) |
| Trace production retrieval | [../ai-rag/references/observability-tracing-contract.md](../ai-rag/references/observability-tracing-contract.md) |
| Debug quality drops | [../ai-rag/references/retrieval-debugging-runbook.md](../ai-rag/references/retrieval-debugging-runbook.md) |
| Red-team retrieval security | [../ai-rag/references/security-red-team-cases.md](../ai-rag/references/security-red-team-cases.md) |
| Lift retrieval with contextual summaries | [references/contextual-retrieval.md](references/contextual-retrieval.md) |
| Add cross-encoder reranking | [references/reranking-recipe.md](references/reranking-recipe.md) |
| Decide the retrieval leg (lexical vs vector vs hybrid vs plain SQL, per query) | [references/lexical-vs-vector-vs-hybrid.md](references/lexical-vs-vector-vs-hybrid.md) |
| Add real BM25 when ts_rank's missing IDF/length-saturation fails evals | [references/bm25-when-ts_rank-isnt-enough.md](references/bm25-when-ts_rank-isnt-enough.md) |
| Add a learned-sparse/SPLADE leg when dense misses rare-term precision and tsvector is too brittle | [references/learned-sparse-splade-leg.md](references/learned-sparse-splade-leg.md) |
| Ship a local/notebook/single-binary brain (no server) | [references/embedded-local-brain.md](references/embedded-local-brain.md) |
| Tune the lexical layer (tsvector weighting, exact tokens, multilingual, debug) | [references/postgres-fts-tuning.md](references/postgres-fts-tuning.md) |
| Turn a dev-context compiled hub or repo artifact set into a vector brain | [references/dev-context-hub-vector-recipe.md](references/dev-context-hub-vector-recipe.md) |
| Scale past ~10M vectors (HNSW tuning, DiskANN, quantization, sharding, graph-augmented retrieval) | [references/graph-theory-at-scale.md](references/graph-theory-at-scale.md) |
| Cut vector RAM/latency at the default tier (quantize + rescore) | [references/quantization-and-rescore.md](references/quantization-and-rescore.md) |
| Run the embedder yourself (cost/residency bars a hosted API) | [references/embedding-runtime.md](references/embedding-runtime.md) |
| Know what v1 doesn't ship and when to add it | [references/deferred-extensions.md](references/deferred-extensions.md) |
| Ship to production (backups, RLS, observability, migration drills) | [references/production-runbook.md](references/production-runbook.md) |
| Handle model drift and corpus drift without full re-embedding | [references/embedding-drift-mitigation.md](references/embedding-drift-mitigation.md) |
| Validate inventory | `scripts/check_brain_manifest.py` |
| Embed and load a corpus | `scripts/embed_and_load.py` |
| Query the brain from the CLI | `scripts/retrieve.py` |

The bundled SQL assets default to **1024-dimensional embeddings**. If the chosen
embedding model uses a different output dimension, update every `vector(N)` and
`bit(N)` occurrence in `assets/sql/001_schema.sql`, `003_hybrid_search_function.sql`,
`005_eval_tables.sql`, and `011_quantize_rescore.sql` before loading data.

## V1 Workflow

## ASCII Flow

```text
Vector-brain implementation request
  -> Inventory corpus and classify repo, docs hub, or compliance material
  -> Normalize, chunk, deduplicate, and anchor source documents
  -> Choose retrieval unit, backend, schema, and indexes
  -> Embed, load, and query through the provided scripts
  -> Evaluate retrieval quality, citations, cost, and rerun path
```

1. **Inventory the corpus** with `scripts/inventory_corpus.py`.
2. **Classify corpus type**: repo/codebase, docs hub, or compliance/policy.
3. **Prepare normalized documents** with `scripts/prepare_documents.py`.
4. **Chunk with stable anchors** using `scripts/chunk_corpus_files.py` for mixed repo/context corpora or `scripts/chunk_markdown.py` for Markdown-only corpora.
5. **Choose retrieval unit**: source chunk, parent-child chunk, or typed knowledge packet.
6. **Deduplicate canonical facts** before embedding when the corpus has repeated versions, copied procedures, or near-duplicate docs.
7. **Create schema and indexes** from `assets/sql/`.
8. **Embed and load retrieval units** with `scripts/embed_and_load.py` (provider-agnostic; swap the `Embedder` class for a new backend).
9. **Optionally contextualize chunks** at index time per [contextual-retrieval.md](references/contextual-retrieval.md) when retrieval-failure rate is the bottleneck.
10. **Run hybrid retrieval** with `scripts/retrieve.py` (lexical + vector + RRF; sets the required `hnsw.iterative_scan` session knob).
11. **Optionally rerank** the top-N candidates with a cross-encoder per [reranking-recipe.md](references/reranking-recipe.md) before passing top-K to the generator.
12. **Seed evals** with `scripts/build_eval_seed.py`, then hand-label expected evidence.
13. **Expose retrieval** through the `retrieve_context` contract.
14. **Operate freshness** with ingest ledgers, corpus versions, tombstones, query logs (`assets/sql/007_query_logs.sql`), and metric gates.
15. **Promote to production** following [production-runbook.md](references/production-runbook.md) (backups, RLS, SLOs, embedding migration drill).

## Backend Stance

Postgres + pgvector is the V1 default because it is durable, scriptable, easy to inspect, and sufficient for most repo/docs/compliance brains. It is not the identity of the skill.

**On-device iOS / Swift is out of scope here.** When the retrieval target is an iPhone/iPad app running fully offline (sqlite-vec / `NLEmbedding` / Core Spotlight semantic index feeding an Apple Foundation Models or sentence-bank composer), this skill's pgvector + server scripts don't apply. Route to [`../software-ios-ai-engine/SKILL.md`](../software-ios-ai-engine/SKILL.md) for the on-device retrieval-stitch composer (Option C) and the shared `{ answer, grounding, followUps[], safetyBoundary }` contract. Use this skill only for the *upstream* knowledge build (chunking, anchors, eval seeds) that ships into the bundle.

**Dual-deployment pattern (server pgvector + on-device sqlite-vec mirror with shared `content_hash` so citations resolve identically across paths)** plus full four-skill composition for natural conversational iOS surfaces is documented in [composition-with-rag-context-vector.md](../software-ios-ai-engine/references/composition-with-rag-context-vector.md) — covers Path A (Foundation Models) and Path B (vector-DB-only) for three generic domain shapes (consumer reflection, regulated copilot, multi-turn emotional companion).

**For non-iOS conversational surfaces** (Android with Gemini Nano / AICore, web browser with Chrome `window.ai` or WebLLM, Telegram/Discord/WhatsApp/Slack bots via LangGraph + Mem0, voice surfaces), see [`conversational-surfaces-cross-platform.md`](../ai-context-layer/references/conversational-surfaces-cross-platform.md) — same composition skeleton, per-platform composer matrix (with-model and without-model paths), per-platform retrieval backend choice (ObjectBox Android, IndexedDB+WASM sqlite-vec web, server pgvector for bots).

Use [backend-selection.md](references/backend-selection.md) before choosing an alternative. The matrix covers four tiers:

- **SQL-native**: pgvector, pgvectorscale, ParadeDB
- **Dedicated services**: Qdrant, Weaviate, Milvus/Zilliz, Vespa, LanceDB, Chroma
- **Serverless / object-storage-backed (cost-driven)**: AWS S3 Vectors, Turbopuffer, Pinecone Serverless, Cloudflare Vectorize, Upstash Vector
- **Hyperscaler managed**: AWS Bedrock Knowledge Bases, Azure AI Search, Vertex AI Vector Search, OpenAI File Search
- **Search-engine k-NN (lift-and-shift)**: Elasticsearch / OpenSearch, Redis Stack, MongoDB Atlas Vector

For per-backend deep dives and look-alike comparisons (S3 Vectors vs Turbopuffer vs Pinecone Serverless, Bedrock KB vs Vertex vs Azure vs OpenAI File Search), see [backend-selection-extended.md](references/backend-selection-extended.md).

## Corpus Playbooks

V1 ships three playbooks:

- **Repo/codebase brain**: exact path, symbol, module, ownership, structured profile, schema, and selected source retrieval.
- **Docs hub brain**: architecture, guides, generated docs, and cross-page navigation.
- **Compliance/policy brain**: authority, effective-time, citation precision, and refusal-on-no-evidence.

Support KB, note-vault, and generated graph + markdown playbooks are later increments unless the user explicitly asks for them.

## Operational Defaults

- Keep source truth separate from chunks and embeddings.
- Store stable evidence IDs, source URIs, content hashes, freshness, ACL scope, and citation anchors.
- Treat chunks as a default transport unit, not always the best knowledge unit. For policies, docs, support, and repeated business knowledge, consider typed claim or question-answer packets with source anchors, version state, and access scope.
- Collapse near-duplicate units into canonical records before embedding when duplicate versions would crowd top-k results.
- Use lexical + vector hybrid retrieval from the first production version.
- Contextualize chunks at index time (not query time) when adopting contextual retrieval; embed the contextualized form, keep the original `content` for display and citation.
- Rerank in the app layer with a cross-encoder, never inside the database; oversample candidates (N ≈ 5–10x final K) before reranking.
- Add `model_id` to embeddings from day one; never overwrite embeddings in place during live migration.
- Keep the manifest `embedding_model` dimension aligned with the SQL assets and CLI `--dim`.
- Tombstone stale or deleted content; do not silently hard-delete normal corpus history.
- Build a corpus-specific eval set before tuning chunk size, model, backend, or index parameters.
- Treat retrieved chunks as untrusted external content until assembled into a grounded context bundle.

## Common Anti-Patterns

- vector database first, source-of-truth model later
- one chunking or retrieval-unit recipe for code, docs, and policies
- treating arbitrary token windows as facts when the corpus needs atomic claims, obligations, decisions, or Q&A records
- letting duplicate versions compete in embedding space instead of canonicalizing current/deprecated records
- embeddings and raw source text in one undifferentiated table
- pure vector search with no lexical leg for code, policy, or proper-noun-heavy docs
- treating HNSW as infinite scale; quantizing without a rescore step; rebuilding PPR/Louvain inside the brain instead of reusing dev-context-code-graph / dev-context-multi-repo runners
- contextualizing chunks at query time instead of index time (loses the precompute + prompt-caching cost win)
- embedding the contextualized form but discarding the original chunk so citations can no longer point at the source text
- reranking inside the database instead of app-layer; running rerank with N == K so there is nothing to rerank
- mixing rerank scores across reranker models in the same eval cohort
- no deletion, tombstone, or supersession path
- semantic cache without corpus-version invalidation
- tuning by vibes instead of labeled retrieval evals
- citing chunks without stable source anchors
- hiding operational SQL in theory skills where it drifts
- **no re-indexing line in the FinOps model** — re-embedding a corpus is recurring, not one-time. May 2026 going rates: ~$12–$40 per 10M vectors, ~$120–$400 per 100M, billed every time the embedding model or chunking strategy changes (quarterly is standard for serious products). Budget it at architecture-design time, not after the first surprise invoice.
- **no `embedding_model` column on the vectors table** — providers silently upgrade models behind a stable API alias; one documented case on Pinecone + `text-embedding-3-large` saw a **14% retrieval-precision drop** after a transparent backend bump. Pin model name and version on every row, monitor cosine-similarity distribution between query embeddings and top-k results (rolling avg + stdev), alert when the mean drifts more than 2σ from baseline.
- **assuming "same model" means "same neighbourhood" forever** — even with a frozen embedding model, corpus drift (new docs, expired docs, evolving terminology) reshapes the semantic landscape of the index over months. Schedule a quarterly drift check against a held-out labeled eval; trigger re-embed when recall@k falls below threshold. When full re-embed is too expensive, consider Drift-Adapter (see `references/embedding-drift-mitigation.md`) — recovers 95–99% of fresh-index recall at ~100× lower compute cost than a full re-embedding or dual-index migration.
- **picking a vector DB on raw k-NN throughput when the workload is filter-heavy** — Pinecone has been observed to choke on metadata-filtered queries where Qdrant's payload index delivered ~10× better latency on the same workload. Benchmark with realistic filter cardinality and selectivity, not unfiltered top-k.
- **ingesting tens of millions of vectors because storage is cheap** — published production telemetry consistently shows ~80% of queries hit ~5% of the corpus. Premature scale inflates RAM, re-embed cost, and tail latency for queries that would have been fine on 100k vectors. Measure query-corpus concentration before sizing.
- **single-config `english` `fts_vector` for code/policy/proper-noun corpora** — `english_stem` destroys exact identifiers (`ERR_5012` → `err`). Layer a weight-A `simple`+`unaccent` contribution; see `references/postgres-fts-tuning.md`.
- **`unaccent()` wrapped `IMMUTABLE` to fit a generated column** — index goes silently stale when the unaccent ruleset changes. Use a text-search configuration instead.
- **tuning `ts_rank` normalization to fix ranking while RRF is downstream** — RRF consumes rank position, not raw score; pre-fusion score shaping is wasted. Tune at the right layer.
- **assuming "it indexed" means "it ranked"** — positions past 16383 are silently clamped (lexeme still matches; `ts_rank_cd` proximity degrades), and positions beyond 256 per lexeme are discarded; tsvector caps at 1 MB. Guard chunk size.
- **per-row language via a generated column** — a generated column cannot pick its `regconfig` from a column; per-row language needs a trigger.
- **trigram GIN on full body text** — `pg_trgm` GIN bloats on long text; index only the identifier/symbol column.

## Fact-Checking

- Verify backend capabilities, index behavior, hosted-service support, pricing, and benchmark claims against current primary vendor docs before making a hard recommendation.
- Treat model rankings, embedding dimensions, reranker quality, and managed-vector-store features as volatile.
- Prefer official docs, release notes, and primary project repositories over blog summaries.
- If live verification is unavailable, present backend guidance as a default pattern, not as a current market ranking.
- MTEB v1 and v2 scores are not directly comparable; confirm benchmark version when comparing embedding models.

## Navigation

### References

- [references/framework.md](references/framework.md)
- [references/backend-selection.md](references/backend-selection.md)
- [references/backend-selection-extended.md](references/backend-selection-extended.md)
- [references/s3-vectors-backend.md](references/s3-vectors-backend.md) — S3 Vectors cost model, GA limits, direct API vs Bedrock KB, anti-patterns
- [references/cost-calculation.md](references/cost-calculation.md)
- [references/postgres-pgvector-default.md](references/postgres-pgvector-default.md)
- [references/corpus-playbooks.md](references/corpus-playbooks.md)
- [references/eval-by-corpus-type.md](references/eval-by-corpus-type.md)
- [references/agent-tool-contract.md](references/agent-tool-contract.md)
- [references/contextual-retrieval.md](references/contextual-retrieval.md)
- [references/reranking-recipe.md](references/reranking-recipe.md)
- [references/lexical-vs-vector-vs-hybrid.md](references/lexical-vs-vector-vs-hybrid.md) — per-query leg decision matrix, smell test, worked examples, patterns/anti-patterns/traps
- [references/bm25-when-ts_rank-isnt-enough.md](references/bm25-when-ts_rank-isnt-enough.md) — real BM25 (pg_search/OpenSearch/Vespa) vs ts_rank; per-backend verdict matrix
- [references/learned-sparse-splade-leg.md](references/learned-sparse-splade-leg.md) — learned-sparse/SPLADE 4th leg (sparsevec/Qdrant/ELSER); per-backend verdict matrix
- [references/embedded-local-brain.md](references/embedded-local-brain.md) — embedded/local brain (DuckDB-VSS, sqlite-vec); per-backend tier verdicts
- [references/quantization-and-rescore.md](references/quantization-and-rescore.md) — binary_quantize + two-pass rescore (default tier); per-backend verdict matrix
- [references/embedding-runtime.md](references/embedding-runtime.md) — self-hosted embedding runtime (TEI/Infinity/vLLM/Ollama/llama.cpp); per-runtime verdict matrix
- [references/postgres-fts-tuning.md](references/postgres-fts-tuning.md) — tsvector weighting, exact-token, multilingual, debug, snippet, RUM toolkit
- [references/graph-theory-at-scale.md](references/graph-theory-at-scale.md)
- [references/deferred-extensions.md](references/deferred-extensions.md)
- [references/production-runbook.md](references/production-runbook.md)
- [references/embedding-drift-mitigation.md](references/embedding-drift-mitigation.md) — detect model drift vs corpus drift; Drift-Adapter and dual-index alternatives to full re-embedding

### SQL Assets

- [assets/sql/001_schema.sql](assets/sql/001_schema.sql)
- [assets/sql/002_indexes_hnsw.sql](assets/sql/002_indexes_hnsw.sql)
- [assets/sql/003_hybrid_search_function.sql](assets/sql/003_hybrid_search_function.sql)
- [assets/sql/004_ingest_ledger.sql](assets/sql/004_ingest_ledger.sql)
- [assets/sql/005_eval_tables.sql](assets/sql/005_eval_tables.sql)
- [assets/sql/006_rls_multitenant.sql](assets/sql/006_rls_multitenant.sql) — optional, multi-tenant only
- [assets/sql/007_query_logs.sql](assets/sql/007_query_logs.sql) — observability
- [assets/sql/008_fts_hardening.sql](assets/sql/008_fts_hardening.sql) — reversible weighted unaccent fts_vector (supersedes 001's v1 column)
- [assets/sql/009_bm25_pg_search.sql](assets/sql/009_bm25_pg_search.sql) — reversible pg_search BM25 lexical-leg alternative to 008
- [assets/sql/010_sparsevec.sql](assets/sql/010_sparsevec.sql) — reversible sparsevec column + HNSW inner-product index for the learned-sparse/SPLADE leg
- [assets/sql/011_quantize_rescore.sql](assets/sql/011_quantize_rescore.sql) — binary_quantize expression index + two-pass rescore (reversible)

### Scripts

- `scripts/inventory_corpus.py`
- `scripts/prepare_documents.py`
- `scripts/chunk_corpus_files.py`
- `scripts/chunk_markdown.py`
- `scripts/embed_and_load.py`
- `scripts/retrieve.py`
- `scripts/build_eval_seed.py`
- `scripts/check_brain_manifest.py`
- `scripts/test_sql_asset_contracts.py` — regression checks for SQL asset examples and reversible migration contracts
- `../ai-rag/scripts/exact_search_baseline.py` — backend-neutral exact-search proof before index tuning
- `../ai-rag/scripts/hybrid_rrf_demo.py` — portable hybrid/RRF smoke comparison for prediction files

### Sources

- [data/sources.json](data/sources.json) — curated primary docs for freshness validation

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
