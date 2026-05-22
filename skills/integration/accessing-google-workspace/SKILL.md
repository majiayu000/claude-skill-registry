---
name: accessing-google-workspace
description: >
  Access Google Sheets and Docs via gcloud CLI.
  Use when user shares a Google Sheets/Docs URL or mentions
  スプレッドシート, Sheets, Docs, Google ドキュメント.
allowed-tools:
  - Bash
  - Read
user-invocable: false
---

# Accessing Google Workspace

Access Google Sheets and Docs via CLI.

## URL Detection

| Pattern                           | Type          |
| --------------------------------- | ------------- |
| `docs.google.com/spreadsheets/d/` | Google Sheets |
| `docs.google.com/document/d/`     | Google Docs   |

## Commands

### Google Sheets

```bash
# CSV format
gsheet "URL"

# JSONL format (for structured data)
gsheet "URL" json
```

### Google Docs

```bash
# Text format
gdoc "URL"

# Markdown format
gdoc "URL" md
```

## Format Selection

| Data Type        | Recommended Format |
| ---------------- | ------------------ |
| Tabular data     | `json` (JSONL)     |
| Documents/Specs  | `md` (Markdown)    |
| Simple retrieval | Default (CSV/txt)  |
