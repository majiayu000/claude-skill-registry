---
name: trioexplorer
description: Search clinical notes using the Trioexplorer CLI. Use when the user wants to search patient notes, list cohorts, view search history, or explore the clinical notes database.
allowed-tools: Bash
---

# Trioexplorer CLI

Search clinical notes using the `trioexplorer` CLI. The CLI requires `TRIOEXPLORER_API_KEY` to be set.

## Commands

### Search clinical notes
```bash
trioexplorer search "query" [options]
```

Options:
- `-k N` — Number of results (default: 10)
- `--type TYPE` — Search type: `keyword`, `semantic`, or `hybrid` (default)
- `--cohort-ids IDS` — Comma-separated cohort IDs to search
- `--format FORMAT` — Output: `table` (default), `json`, or `csv`
- `--full-text` — Show full note text
- `--rerank false` — Disable semantic reranking
- `--vector-weight N` — Weight for vector vs keyword (0.0-1.0)

### List resources
```bash
trioexplorer list cohorts [--limit N]
trioexplorer list notetypes [--search TEXT]
trioexplorer list history [--page N] [--user-id ID]
trioexplorer list entities
trioexplorer list filters [--field NAME]
```

### Statistics
```bash
trioexplorer stats history [--date-from DATE] [--date-to DATE]
```

### Global options
- `--debug` — Enable request/response logging
- `--help` — Show help for any command

## Examples

Search for diabetes-related notes:
```bash
trioexplorer search "diabetes management" -k 20
```

Semantic search with JSON output:
```bash
trioexplorer search "patient having trouble with blood sugar" --type semantic --format json
```

Search within specific cohorts:
```bash
trioexplorer search "chest pain" --cohort-ids abc123,def456
```

## Task: $ARGUMENTS
