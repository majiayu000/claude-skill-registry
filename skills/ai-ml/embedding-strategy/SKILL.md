---
name: embedding-strategy
version: "0.1"
description: >
  [STUB - Not implemented] Asymmetric embedding strategy with RETRIEVAL_DOCUMENT for ingestion and RETRIEVAL_QUERY for queries.
  PROACTIVELY activate for: [TODO: Define on implementation].
  Triggers: [TODO: Define on implementation]
core-integration:
  techniques:
    primary: ["[TODO]"]
    secondary: []
  contracts:
    input: "[TODO]"
    output: "[TODO]"
  patterns: "[TODO]"
  rubrics: "[TODO]"
---

# Embedding Strategy

> **STUB: This skill is not yet implemented**
>
> This placeholder preserves the documented plugin structure.
> See parent plugin README for planned capabilities.

## Planned Capabilities

- **Asymmetric Embedding Strategy**:
  - RETRIEVAL_DOCUMENT task_type for document ingestion
  - RETRIEVAL_QUERY task_type for query embeddings
  - Semantic mismatch prevention
- Concurrent online embeddings (never use batch API for documents)
- Embedding model selection and configuration
- Asymmetric task_type validation and enforcement

## Critical Pattern

Documents and queries must use different task_types for optimal semantic search. Batch API defaults to RETRIEVAL_QUERY which causes semantic mismatch and poor retrieval quality.

## Implementation Status

- [ ] Core implementation
- [ ] References documentation
- [ ] Output templates
- [ ] Integration tests
