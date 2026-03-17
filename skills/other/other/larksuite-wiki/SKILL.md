---
name: larksuite-wiki
description: Manage and export Lark Suite (Feishu) Wiki/Knowledge Base documents. Read, search, sync with subdocuments, and incremental export to local Markdown files.
homepage: https://open.larksuite.com
tags: [lark, wiki, knowledge-base, export, sync, markdown]
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "env": ["LARK_APP_ID", "LARK_APP_SECRET"] },
        "primaryEnv": "LARK_APP_ID",
      },
  }
---

# Lark Suite Wiki

Manage and export Lark Suite (Feishu) Wiki/Knowledge Base documents with recursive sync and incremental updates.

## Prerequisites

1. Create a Lark/Feishu app at https://open.larksuite.com/console
2. Enable permissions:
   - `docs:doc:read`
   - `drive:drive:read`
   - `wiki:wiki:read`
3. Publish the app and authorize it to access your wiki
4. Set environment variables (or edit script defaults):
   ```bash
   export LARK_APP_ID="cli_xxxxxxxx"
   export LARK_APP_SECRET="<LARK_APP_SECRET_REDACTED>"
   ```

## Commands

### List Wiki Spaces
```bash
larksuite-wiki spaces
```

### Read Document (with subdocument links)
```bash
larksuite-wiki read <doc_id_or_url>
```

### Export Single Document
```bash
larksuite-wiki export <doc_id_or_url> --output ./docs/
```

### Show Document Tree Structure
```bash
larksuite-wiki tree <doc_id_or_url>
```

### Sync Entire Wiki (Recursive Export)
```bash
# First sync - exports all documents
larksuite-wiki sync <doc_id_or_url> --output ./lark-wiki/

# Incremental sync - only exports changed documents
larksuite-wiki sync <doc_id_or_url> --output ./lark-wiki/

# Force re-export everything
larksuite-wiki sync <doc_id_or_url> --output ./lark-wiki/ --force
```

## Features

### 1. ✅ Batch Export
Export entire knowledge base with one command.

### 2. ✅ Recursive Subdocument Export
Automatically follows and exports all linked subdocuments.

### 3. ✅ Preserves Directory Structure
Creates nested folders matching your wiki structure:
```
lark-wiki/
├── 01_首页/
│   ├── 01_首页.md
│   └── 01_日常复盘/
│       ├── 01_日常复盘.md
│       └── ...
├── 02_云聪金融分析/
│   └── ...
```

### 4. ✅ Incremental Sync
Tracks document revisions and only exports changed documents:
- Saves sync state to `.lark-sync-state.json`
- Compares revision IDs
- Skips unchanged documents

## Quick Start

### Export your entire wiki
```bash
# Get your wiki root document ID from the URL
# https://xxx.larksuite.com/wiki/TDCZweBJ2iMFO4kI1LAlSE62gnd

# Sync everything
python3 larksuite-wiki.py sync TDCZweBJ2iMFO4kI1LAlSE62gnd --output ./my-wiki/
```

### Daily incremental sync
```bash
# Run daily - only exports changed documents
python3 larksuite-wiki.py sync TDCZweBJ2iMFO4kI1LAlSE62gnd --output ./my-wiki/
```

## Output Structure

Each document gets its own folder:
- Main `.md` file
- Subfolders for child documents
- Numbered prefixes for ordering (01_, 02_, etc.)

## API Reference

- Lark Open Platform: https://open.larksuite.com/
- Wiki API: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/wiki-v1/space/overview
- Docx API: https://open.larksuite.com/document/uAjLw4CM/ukTMukTMukTM/reference/docx-v1/document/overview

## Notes

- Documents must be explicitly shared with your app
- Some block types may not convert perfectly to Markdown
- Large wikis with many subdocuments may take time to sync
- Sync state is saved locally for incremental updates
