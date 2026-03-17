---
name: agent-optimize
description: Optimize a document for AI agent consumption. Restructures prose into formats that agents parse efficiently while preserving meaning.
argument-hint: <file|folder>...
---

Optimize the target document(s) at `$ARGUMENTS` for agent consumption.

**Stop after each stage and have changes reviewed with user.**

> **Note**: The goal is agent efficiency, not stripping all prose. Some content is genuinely better as narrative — context-setting introductions, nuanced trade-offs, philosophy notes. Optimize the structure agents need to parse; preserve the prose humans need to understand intent.

0. **Read and assess the document** (developer confirms)
   - Read the target document and identify its current structure
   - What sections are prose-heavy and could benefit from structured formats?
   - What relationships between concepts are buried in narrative?
   - Confirm understanding and optimization targets before proceeding

1. **Replace verbose prose with structured formats** (agent leads with approval)
   - Are there narrative paragraphs that would be clearer as tables, diagrams, or bullet lists?
   - Convert where meaning is preserved — don't force structure where prose is genuinely better
   - Use structured formats agents parse well (clear headers, consistent patterns)

2. **Compress token usage** (agent leads with approval)
   - Is there redundant phrasing that can be removed without losing information?
   - Are there verbose explanations that could be stated more directly?
   - Prefer concise, direct language over verbose explanation

3. **Make relationships explicit** (agent leads with approval)
   - Are there implicit references between sections that should be explicit cross-references?
   - Add hierarchy indicators to show parent/child relationships
   - Prefer visual structure over narrative explanation

## Pipeline Position

This skill sits at the end of the composition pipeline: **flesh-out** -> **review-steps** -> **strong-edit** -> **agent-optimize**. Run it after the content is complete and reviewed — it restructures for consumption, not correctness.

## When to Use This vs Other Skills

| Goal | Use |
|------|-----|
| Raw notes need structure and expansion | **flesh-out** |
| Draft needs polish and consistency | **review-steps** |
| Complete draft needs critical evaluation | **strong-edit** |
| Finalized document needs agent-friendly restructuring | **agent-optimize** |
