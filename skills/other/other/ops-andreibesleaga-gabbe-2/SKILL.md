---
name: memory-optimization
description: Summarizing context, pruning history, and managing token budget efficiency.
role: orch-researcher
triggers:
  - prune context
  - summarize
  - forget
  - compress memory
  - token budget
---

# memory-optimization Skill

This skill prevents "Context Overflow" and reduces API costs.

## 1. Summarization Strategies
- **Rolling Summary**: Keep the last 10 messages + a summary of everything before.
- **Entity Extraction**: Extract key facts ("User chose Redis", "App is on port 3000") and store in `semantic/`.

## 2. Context Pruning
- **Irrelevant Files**: Only keep file definitions in context if actively editing. Use `grep` for others.
- **Old Logs**: Truncate logs > 50 lines.

## 3. The "Forget" Protocol
- When a task is done:
  1.  **Summarize**: Write outcome to `AUDIT_LOG.md`.
  2.  **Clear**: Remove task-specific context from working memory.
  3.  **Retain**: Keep only global constraints and active file list.

## 4. Semantic Memory Integration
- Use **Qdrant** or **PGVector** (via MCP) to store embeddings of documentation.
- **Retrieval**: Retrieve only the Top-3 relevant chunks for the current query.
