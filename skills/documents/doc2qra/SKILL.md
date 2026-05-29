---
name: doc2qra
description: >
  Convert any document (PDF, URL, text) into Question-Reasoning-Answer pairs
  with a document summary. Stores to memory for later recall.
allowed-tools: Bash, Read, WebFetch
triggers:
  - convert to QRA
  - document to QRA
  - pdf to QRA
  - extract QRA
  - extract Q&A
  - extract knowledge
  - create Q&A pairs
  - distill this
  - distill this pdf
  - distill this paper
  - remember this paper
  - store this research
  - learn from this document
  - ingest this pdf
  - turn this into Q&A
  - make Q&A from this
metadata:
  short-description: "Document → QRA pairs + summary (PDF, URL, text)"
---

# doc2qra

**Convert any document into Question-Reasoning-Answer pairs with a summary.**

Input → Summary + QRA pairs → Memory

## Quick Start

```bash
# PDF → QRA with summary
./run.sh --file paper.pdf --scope research

# With domain focus (recommended for better relevance)
./run.sh --file paper.pdf --scope research --context "ML researcher"

# Preview before storing
./run.sh --file paper.pdf --dry-run

# URL → QRA
./run.sh --url https://example.com/article --scope web

# Text file → QRA
./run.sh --file notes.txt --scope project
```

## What It Does

1. **Extract** content from PDF/URL/text
2. **Summarize** the document (2-3 paragraph overview)
3. **Split** into logical sections
4. **Generate** Q&A pairs via LLM (parallel batch)
5. **Validate** answers are grounded in source
6. **Store** summary + QRAs to memory

## Parameters

| Flag | Description |
|------|-------------|
| `--file` | PDF, markdown, or text file |
| `--url` | URL to fetch and convert |
| `--scope` | Memory scope (default: research) |
| `--context` | Domain focus, e.g. "security expert" |
| `--dry-run` | Preview without storing |
| `--json` | JSON output (includes summary) |
| `--sections-only` | Extract sections only (no Q&A) |
| `--summary-only` | Generate only the summary |

## Output Format

When using `--json`, output includes:

```json
{
  "summary": "A 2-3 paragraph summary of the document...",
  "extracted": 15,
  "stored": 15,
  "sections": 8,
  "source": "paper.pdf",
  "scope": "research",
  "qra_pairs": [
    {"problem": "What is...", "solution": "The document explains..."},
    ...
  ]
}
```

## Examples

```bash
# Research paper with context
./run.sh --file arxiv_paper.pdf --scope research --context "ML researcher"

# Technical documentation
./run.sh --file api_docs.md --scope project --context "backend developer"

# Just get the summary
./run.sh --file paper.pdf --summary-only

# From extractor output (pipeline integration)
./run.sh --from-extractor /path/to/extractor/results --scope research
```

## Environment Variables (Optional Tuning)

| Variable | Default | Description |
|----------|---------|-------------|
| `DOC2QRA_PDF_MODE` | fast | PDF mode: fast, accurate, auto |
| `DOC2QRA_CONCURRENCY` | 6 | Parallel LLM requests |
| `DOC2QRA_GROUNDING_THRESH` | 0.6 | Grounding similarity threshold |
| `DOC2QRA_NO_GROUNDING` | - | Set to 1 to skip validation |

## Migration from distill/qra/doc-to-qra

This skill consolidates the functionality of:
- `distill` → Use `doc2qra` instead
- `qra` → Use `doc2qra` instead
- `doc-to-qra` → Use `doc2qra` instead

All three legacy skills now redirect to `doc2qra` with deprecation warnings.
