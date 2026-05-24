---
name: distill
description: >
  Distill PDF, URL, or text into Q&A pairs stored in memory.
  Use --context for domain-focused extraction.
allowed-tools: Bash, Read, WebFetch
triggers:
  - distill this
  - distill this pdf
  - distill this paper
  - extract knowledge from
  - remember this paper
  - store this research
  - learn from this document
  - ingest this pdf
metadata:
  short-description: Distill content into Q&A pairs for memory
---

# Distill Skill

Distill PDF, URL, or text into Q&A pairs and store in memory.

## Happy Path

```bash
# Distill a PDF into memory
./run.sh --file paper.pdf --scope research

# With domain focus (recommended for better relevance)
./run.sh --file paper.pdf --scope research --context "ML researcher"

# Preview before storing
./run.sh --file paper.pdf --dry-run

# From URL
./run.sh --url https://example.com/article --scope web
```

## Parameters

| Flag | Description |
|------|-------------|
| `--file` | PDF, markdown, or text file |
| `--url` | URL to fetch and distill |
| `--scope` | Memory scope (default: research) |
| `--context` | Domain focus, e.g. "security expert" |
| `--dry-run` | Preview without storing |
| `--json` | JSON output |
| `--sections-only` | Extract sections only (no Q&A) |

## What It Does

1. **Extract** content from PDF/URL/text
2. **Split** into logical sections
3. **Generate** Q&A pairs via LLM
4. **Validate** answers are grounded in source
5. **Store** to memory via `memory-agent learn`

## Examples

```bash
# Research paper
./run.sh --file arxiv_paper.pdf --scope research --context "ML researcher"

# Technical documentation
./run.sh --file api_docs.md --scope project --context "backend developer"

# Just extract sections (no Q&A)
./run.sh --file paper.pdf --sections-only --json
```

## Environment Variables (Optional Tuning)

| Variable | Default | Description |
|----------|---------|-------------|
| `DISTILL_PDF_MODE` | fast | PDF mode: fast, accurate, auto |
| `DISTILL_CONCURRENCY` | 6 | Parallel LLM requests |
| `DISTILL_GROUNDING_THRESH` | 0.6 | Grounding similarity threshold |
| `DISTILL_NO_GROUNDING` | - | Set to 1 to skip validation |
