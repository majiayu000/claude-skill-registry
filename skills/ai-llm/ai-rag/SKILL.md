---
name: ai-rag
description: Complete RAG and search engineering skill. Covers chunking strategies, hybrid retrieval (BM25 + vector), cross-encoder reranking, query rewriting, ranking pipelines, nDCG/MRR evaluation, and production search systems. Modern patterns for retrieval-augmented generation and semantic search.
---

# RAG & Search Engineering — Complete Reference

Build production-grade retrieval systems with **hybrid search**, **grounded generation**, and **measurable quality**.

This skill covers:

- **RAG**: Chunking, contextual retrieval, grounding, adaptive/self-correcting systems
- **Search**: BM25, vector search, hybrid fusion, ranking pipelines
- **Evaluation**: recall@k, nDCG, MRR, groundedness metrics

**Modern Best Practices (December 2025)**:

- Separate **retrieval quality** from **answer quality**; evaluate both (RAG paper: https://arxiv.org/abs/2005.11401).
- Default to **hybrid retrieval** (sparse + dense) with **reranking** when precision matters (DPR: https://arxiv.org/abs/2004.04906).
- Treat **freshness/invalidation** as first-class; staleness is a correctness bug, not a UX issue.
- Add **grounding gates**: answerability checks, citation coverage checks, and refusal-on-missing-context defaults.
- Threat-model RAG: retrieved text is untrusted input (OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/).

**Default posture**: deterministic pipeline, bounded context, explicit failure handling, and telemetry for every stage.

**Scope note**: For prompt structure and output contracts used in the generation phase, see [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md).

---

---

## Quick Reference

| Task | Tool/Framework | Command/Pattern | When to Use |
|------|----------------|-----------------|-------------|
| Decide RAG vs alternatives | Decision framework | RAG if: freshness + citations + corpus size; else: fine-tune/caching | Avoid unnecessary retrieval latency/complexity |
| Chunking & parsing | Chunker + parser | Start simple; add structure-aware chunking per doc type | Ingestion for docs, code, tables, PDFs |
| Retrieval | Sparse + dense (hybrid) | Fusion (e.g., RRF) + metadata filters + top-k tuning | Mixed query styles; high recall requirements |
| Precision boost | Reranker | Cross-encoder/LLM rerank of top-k candidates | When top-k contains near-misses/noise |
| Grounding | Output contract + citations | Quote/ID citations; answerability gate; refuse on missing evidence | Compliance, trust, and auditability |
| Evaluation | Offline + online eval | Retrieval metrics + answer metrics + regression tests | Prevent silent regressions and staleness failures |

---

## Decision Tree: RAG Architecture Selection

```text
Building RAG system: [Architecture Path]
    ├─ Document type?
    │   ├─ Page/section-structured? → Structure-aware chunking (pages/sections + metadata)
    │   ├─ Technical docs/code? → Structure-aware + code-aware chunking (symbols, headers)
    │   └─ Simple content? → Fixed-size token chunking with overlap (baseline)
    │
    ├─ Retrieval accuracy low?
    │   ├─ Query ambiguity? → Query rewriting + multi-query expansion + filters
    │   ├─ Noisy results? → Add reranker + better metadata filters
    │   └─ Mixed queries? → Hybrid retrieval (sparse + dense) + reranking
    │
    ├─ Dataset size?
    │   ├─ <100k chunks? → Flat index (exact search)
    │   ├─ 100k-10M? → HNSW (low latency)
    │   └─ >10M? → IVF/ScaNN/DiskANN (scalable)
    │
    └─ Production quality?
        └─ Add: ACLs, freshness/invalidation, eval gates, and telemetry (end-to-end)
```

---

## Core Concepts (Vendor-Agnostic)

- **Pipeline stages**: ingest → chunk → embed → index → retrieve → rerank → pack context → generate → verify.
- **Two evaluation planes**: retrieval relevance (did we fetch the right evidence?) vs generation fidelity (did we use it correctly?).
- **Freshness model**: staleness budget, invalidation triggers, and rebuild strategy (incremental vs full).
- **Trust boundaries**: retrieved content is untrusted; apply the same rigor as user input (OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/).

## Implementation Practices (Tooling Examples)

- Use a **retrieval API contract**: query, filters, top_k, trace_id, and returned evidence IDs.
- Instrument each stage with tracing/metrics (OpenTelemetry GenAI semantic conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/).
- Add **caches** deliberately: embeddings cache, retrieval cache (query+filters), and response cache (with invalidation).

## Do / Avoid

**Do**
- Do keep retrieval deterministic: fixed top_k, stable ranking, explicit filters.
- Do enforce document-level ACLs at retrieval time (not only at generation time).
- Do include citations with stable IDs and verify citation coverage in tests.

**Avoid**
- Avoid shipping RAG without a test set and regression gate.
- Avoid “stuff everything” context packing; it increases cost and can reduce accuracy.
- Avoid mixing corpora without metadata and tenant isolation.

## When to Use This Skill

Claude should invoke this skill when the user asks:

- "Help me design a RAG pipeline."
- "How should I chunk this document?"
- "Optimize retrieval for my use case."
- "My RAG system is hallucinating — fix it."
- "Choose the right vector database / index type."
- "Create a RAG evaluation framework."
- "Debug why retrieval gives irrelevant results."

---

## Related Skills

For adjacent topics, reference these skills:

- **[ai-llm](../ai-llm/SKILL.md)** - Prompting, fine-tuning, instruction datasets
- **[ai-agents](../ai-agents/SKILL.md)** - Agentic RAG workflows and tool routing
- **[ai-llm-inference](../ai-llm-inference/SKILL.md)** - Serving performance, quantization, batching
- **[ai-mlops](../ai-mlops/SKILL.md)** - Deployment, monitoring, security, privacy, and governance
- **[ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)** - Prompt patterns for RAG generation phase

---

## Detailed Guides

### Core RAG Architecture

- **[Pipeline Architecture](resources/pipeline-architecture.md)** - End-to-end RAG pipeline structure, ingestion, freshness, index hygiene, embedding selection
- **[Chunking Strategies](resources/chunking-strategies.md)** - Chunking tradeoffs, evaluation approach, and production pitfalls
- **[Index Selection Guide](resources/index-selection-guide.md)** - Vector database configuration, HNSW/IVF/Flat selection, parameter tuning

### Advanced Retrieval Techniques

- **[Retrieval Patterns](resources/retrieval-patterns.md)** - Dense retrieval, hybrid search, query preprocessing, reranking workflow, metadata filtering
- **[Contextual Retrieval Guide](resources/contextual-retrieval-guide.md)** - Chunk context augmentation technique; validate impact on your corpus
- **[Grounding Checklists](resources/grounding-checklists.md)** - Context compression, hallucination control, citation patterns, answerability validation

### Production & Evaluation

- **[RAG Evaluation Guide](resources/rag-evaluation-guide.md)** - Recall@K, nDCG, groundedness, RAGAS/TruLens, A/B testing, sliced evaluation
- **[Advanced RAG Patterns](resources/advanced-rag-patterns.md)** - Graph/multimodal RAG, online evaluation, telemetry, shadow/canary testing, adaptive retrieval
- **[RAG Troubleshooting](resources/rag-troubleshooting.md)** - Failure mode triage, debugging irrelevant results, hallucination fixes

### Existing Detailed Patterns

- **[Chunking Patterns](resources/chunking-patterns.md)** - Technical implementation details for all chunking approaches
- **[Retrieval Patterns](resources/retrieval-patterns.md)** - Low-level retrieval implementation patterns

---

## Templates

### System Design (Start Here)

- [RAG System Design](templates/design/rag-system-design.md)

### Chunking & Ingestion

- [Basic Chunking](templates/chunking/template-basic-chunking.md)
- [Code Chunking](templates/chunking/template-code-chunking.md)
- [Long Document Chunking](templates/chunking/template-long-doc-chunking.md)

### Embedding & Indexing

- [Index Configuration](templates/indexing/template-index-config.md)
- [Metadata Schema](templates/indexing/template-metadata-schema.md)

### Retrieval & Reranking

- [Retrieval Pipeline](templates/retrieval/template-retrieval-pipeline.md)
- [Hybrid Search](templates/retrieval/template-hybrid-search.md)
- [Reranking](templates/retrieval/template-reranking.md)

### Context Packaging & Grounding

- [Context Packing](templates/context/template-context-packing.md)
- [Grounding](templates/context/template-grounding.md)

### Evaluation

- [RAG Evaluation](templates/eval/template-rag-eval.md)
- [RAG Test Set](templates/eval/template-rag-testset.jsonl)

## Navigation

**Resources**
- [resources/rag-evaluation-guide.md](resources/rag-evaluation-guide.md)
- [resources/rag-troubleshooting.md](resources/rag-troubleshooting.md)
- [resources/contextual-retrieval-guide.md](resources/contextual-retrieval-guide.md)
- [resources/pipeline-architecture.md](resources/pipeline-architecture.md)
- [resources/advanced-rag-patterns.md](resources/advanced-rag-patterns.md)
- [resources/chunking-strategies.md](resources/chunking-strategies.md)
- [resources/grounding-checklists.md](resources/grounding-checklists.md)
- [resources/index-selection-guide.md](resources/index-selection-guide.md)
- [resources/retrieval-patterns.md](resources/retrieval-patterns.md)
- [resources/chunking-patterns.md](resources/chunking-patterns.md)

**Templates**
- [templates/context/template-context-packing.md](templates/context/template-context-packing.md)
- [templates/context/template-grounding.md](templates/context/template-grounding.md)
- [templates/design/rag-system-design.md](templates/design/rag-system-design.md)
- [templates/chunking/template-basic-chunking.md](templates/chunking/template-basic-chunking.md)
- [templates/chunking/template-code-chunking.md](templates/chunking/template-code-chunking.md)
- [templates/chunking/template-long-doc-chunking.md](templates/chunking/template-long-doc-chunking.md)
- [templates/retrieval/template-retrieval-pipeline.md](templates/retrieval/template-retrieval-pipeline.md)
- [templates/retrieval/template-hybrid-search.md](templates/retrieval/template-hybrid-search.md)
- [templates/retrieval/template-reranking.md](templates/retrieval/template-reranking.md)
- [templates/eval/template-rag-eval.md](templates/eval/template-rag-eval.md)
- [templates/eval/template-rag-testset.jsonl](templates/eval/template-rag-testset.jsonl)
- [templates/indexing/template-index-config.md](templates/indexing/template-index-config.md)
- [templates/indexing/template-metadata-schema.md](templates/indexing/template-metadata-schema.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references

---

## External Resources

See [data/sources.json](data/sources.json) for:

- Embedding models (OpenAI, Cohere, Sentence Transformers, Voyage AI, Jina)
- Vector DBs (FAISS, Pinecone, Qdrant, Weaviate, Milvus, Chroma, pgvector, LanceDB)
- Hybrid search libraries (Elasticsearch, OpenSearch, Typesense, Meilisearch)
- Reranking models (Cohere Rerank, Jina Reranker, RankGPT, Flashrank)
- Evaluation frameworks (RAGAS, TruLens, DeepEval, BEIR)
- RAG frameworks (LlamaIndex, LangChain, Haystack, txtai)
- Advanced techniques (RAG Fusion, CRAG, Self-RAG, Contextual Retrieval)
- Production platforms (Vectara, AWS Kendra)

---

Use this skill whenever the user needs **retrieval-augmented system design or debugging**, not prompt work or deployment.
