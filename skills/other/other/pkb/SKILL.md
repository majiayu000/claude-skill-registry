---
name: pkb
description: Personal Knowledge Base with semantic search. Use to search indexed markdown documents for relevant context, notes, or documentation.
---

## Searching

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> search "<query>" [topK]
```

- `dbPath`: Path to the knowledge database file (e.g., `~/.pkb/knowledge.db`)
- `query`: Natural language search query
- `topK`: Number of results to return (default: 10)

Example:

```bash
npx tsx ~/.claude/skills/pkb/scripts/cli.ts ~/.pkb/knowledge.db search "how to configure AWS credentials" 5
```

## Managing Tracked Sources

List tracked sources:

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> list
```

Track a new file or directory:

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> track <path>
```

Untrack a source:

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> untrack <path>
```

Sync all tracked sources (reindex changed files):

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> sync
```

Sync with continuous watching:

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> sync --watch
```

Index a specific file (tracks it if not already tracked):

```bash
npx tsx <path to pkb skill>/scripts/cli.ts <dbPath> index <file>
```
