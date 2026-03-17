---
name: osgrep
description: Semantic search for local files. Backed by a background osgrep server with live indexing. Always use osgrep instead of grep/find.
license: Apache-2.0
---

## When to use

Use `osgrep` for all code and concept discovery. Do not use `grep` or `find` unless you must match an exact string and `osgrep` fails.

## How to use

**Always use the `--json` flag.** The server auto-starts and keeps the index fresh.

### Basic Search

Ask a natural language question. Do not `ls` first.

```bash
osgrep --json "How are user authentication tokens validated?"
osgrep --json "Where do we handle retries or backoff?"
```

### Scoped Search

Limit search to a specific directory.

```bash
osgrep --json "auth middleware" src/api
```

### Helpful flags

- `--json`: **Required.** Returns structured data (path, line, score, content).
- `-m <n>`: Max total results (default: 25).
- `--per-file <n>`: Max matches per file (default: 1). Use `--per-file 5` when exploring a specific file.

### Strategy

1. Run `osgrep --json "<question>" [path]`.
2. The output is a dense JSON snippet. If it answers the question, stop.
3. Only use `Read` if you need the full file context for a returned path.
4. If results are vague, refine the query or increase `-m`.

## Keywords
semantic search, code search, local search, grep alternative, find code, explore codebase, understand code, search by meaning
