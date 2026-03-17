---
name: compact-docs
description: Compress, reduce, optimize, or shrink documentation files. Use when docs are verbose, redundant, or need consolidation for clarity.
disable-model-invocation: true
allowed-tools: Read, Edit
---

# Compact Docs

Compress and optimize documentation files.

## Arguments

Path to the markdown file to be compressed (e.g., `docs/README.md`, `CONTRIBUTING.md`).

$ARGUMENTS

## Process

### 1. Read and Analyze Target Document

- Understand overall structure and content
- Comprehend relationships between sections

### 2. Apply Compression Techniques

**A. Reduce Duplicate Information**
- Identify content repeated across sections
- Convert duplicates to cross-references
- Unify different expressions of the same concept

**B. Simplify Verbose Explanations**
- Convert long text to bullet points
- Summarize excessive details while retaining important information
- Prioritize concise expressions over detailed explanations

**C. Detect Contradictions**
- Identify inconsistencies between sections
- Report contradictory statements (do not auto-fix)

**D. Remove Historical Information**
- Remove change history and update timestamps
- Delete historical descriptions like "Added ~" or "Changed to ~"
- Git tracks history, so documentation doesn't need to

### 3. Generate Compression Report

Include:
- Applied compression techniques and examples
- Line count before/after and reduction rate
- Detected contradictions (if any)
- Recommended next actions

## Guidelines

- **Preserve Meaning** - Don't sacrifice information quality for brevity
- **Maintain Structure** - Keep the original document organization
- **Be Explicit** - Show what was changed and why
- **Don't Auto-fix Contradictions** - Report them for manual review
