---
name: doc-to-qra
description: >
  Convert a document (PDF, URL, text) into Q&A pairs stored in memory.
allowed-tools: Bash, Read
triggers:
  - convert to QRA
  - document to QRA
  - pdf to QRA
  - create QRA from
  - extract QRA from document
  - turn this into Q&A
  - make Q&A from this
  - remember this document
  - learn from this pdf
metadata:
  short-description: Document to Q&A pairs in memory
---

# doc-to-qra

Convert a document into Question-Reasoning-Answer pairs stored in memory.

## Usage

```bash
./run.sh <document> <scope> [context] [--dry-run]
```

## Examples

```bash
# PDF → QRA
./run.sh paper.pdf research

# URL → QRA
./run.sh https://example.com/article web

# With domain focus
./run.sh paper.pdf research "ML researcher"

# Preview first
./run.sh paper.pdf research --dry-run
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| document | Yes | PDF file, URL, or text file |
| scope | Yes | Memory scope to store QRAs |
| context | No | Domain focus (e.g. "security expert") |
| --dry-run | No | Preview without storing |

No other flags. Defaults handle everything.
