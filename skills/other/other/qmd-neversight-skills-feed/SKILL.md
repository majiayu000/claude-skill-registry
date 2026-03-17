---
name: qmd
description: Search and retrieve documents from local markdown knowledge bases using the qmd CLI (Quick Markdown Search). This skill should be used when searching notes, documentation, meeting transcripts, or any indexed markdown content. Triggers on requests like "search my notes for...", "find in my knowledge base...", "what do my notes say about...", or any query that needs to search local markdown files.
---

# QMD - Quick Markdown Search

## Overview

QMD is an on-device search engine for markdown-based knowledge bases. It provides three search modes with increasing quality/latency tradeoffs, plus document retrieval capabilities. All processing runs locally using embedded GGUF models.

## Search Modes

Choose the appropriate search mode based on the query type:

### 1. BM25 Search (`qmd search`) - Fast Keyword Search

```bash
qmd search "<query>" -n 10 --json
```

**When to use:**
- Exact keyword or phrase searches
- Technical terms, function names, specific identifiers
- When speed matters more than semantic understanding

### 2. Vector Search (`qmd vsearch`) - Semantic Search

```bash
qmd vsearch "<query>" -n 10 --json
```

**When to use:**
- Conceptual queries ("how do I...", "what about...")
- When exact keywords are unknown
- Finding related content with different wording

### 3. Hybrid Search (`qmd query`) - Highest Quality

```bash
qmd query "<query>" -n 10 --json
```

**When to use:**
- Important searches where accuracy matters
- Complex queries requiring understanding
- Default choice when unsure which mode to use

## Document Retrieval

After searching, retrieve full document content:

```bash
# By file path
qmd get "collection/path/to/file.md" --json

# By document ID (from search results)
qmd get "#a1b2c3" --json

# Multiple documents
qmd multi-get "collection/*.md" -l 500 --json
```

## Typical Workflow

1. **Search** to find relevant documents:
   ```bash
   qmd query "quarterly planning" -n 5 --json
   ```

2. **Review** search results (docids, scores, snippets)

3. **Retrieve** full content of relevant documents:
   ```bash
   qmd get "#abc123" --json
   ```

4. **Synthesize** information from retrieved documents to answer the user's question

## Common Options

| Option | Description |
|--------|-------------|
| `-n <num>` | Number of results (default: 5) |
| `--json` | JSON output for parsing |
| `--files` | TSV format: docid, score, filepath |
| `-c <name>` | Restrict to specific collection |
| `--min-score <n>` | Minimum relevance threshold (0-1) |
| `-l <lines>` | Max lines per document |

## Index Status

Check available collections and index health:

```bash
qmd status
```

## Critical Constraints

**Never run these commands automatically:**
- `qmd collection add` - Expensive indexing operation
- `qmd embed` - Generates embeddings (slow, resource-intensive)
- `qmd update` - Re-indexes all collections

These operations should only be run when explicitly requested by the user.

## Score Interpretation

| Score Range | Meaning |
|-------------|---------|
| 0.8 - 1.0 | Highly relevant |
| 0.5 - 0.8 | Moderately relevant |
| 0.2 - 0.5 | Somewhat relevant |
| 0.0 - 0.2 | Low relevance |

## Resources

### references/

- `cli_reference.md` - Complete CLI API documentation with all commands, options, and examples
