---
name: context-map
description: 'Generate a compressed project context map to reduce token waste from codebase exploration. Use before sessions involving heavy file reads.'
version: 1.9.3
category: optimization
tags:
  - context
  - scanning
  - token-conservation
  - exploration
  - import-graph
  - routes
tools: []
complexity: low
model_hint: fast
estimated_tokens: 300
---

# Context Map

Generate a compressed context map for the current project.
The map pre-compiles structural knowledge that AI assistants
would otherwise discover through expensive Read/Grep calls,
saving thousands of tokens per session.

## When to Use

- At the start of a session to understand project layout
- Before implementing features to identify entry points
- When exploring an unfamiliar codebase
- To reduce token waste from Read calls
- To identify hot files (high blast radius) before changes

## What It Detects

| Category | Description |
|----------|-------------|
| Structure | Directory layout with file counts and languages |
| Dependencies | Multi-ecosystem: Python, Node, Rust, Go, Java |
| Frameworks | Framework detection from dependency analysis |
| Entry Points | main.py, index.ts, CLI scripts, etc. |
| **Import Graph** | File-to-file import relationships |
| **Hot Files** | Files imported by 3+ others (high blast radius) |
| **Routes** | FastAPI, Flask, Express, Hono API endpoints |
| **Env Vars** | Environment variable references with defaults |
| **Middleware** | Auth, CORS, rate-limit, logging patterns |
| **Models/Schemas** | SQLAlchemy, Django, Pydantic, Prisma definitions |
| **Token Savings** | Estimated tokens saved vs manual exploration |

## Procedure

1. Run the scanner on the project root:

```bash
PYTHONPATH="$(find . -path '*/conserve/scripts' -type d \
  -print -quit 2>/dev/null || \
  echo 'plugins/conserve/scripts')" \
  python3 -m context_scanner .
```

2. Present the output to the user as the project overview.

3. Use the context map to guide subsequent file reads.
   Prioritize hot files and entry points first.

## Options

### Output

- `--format json` for structured output
- `--max-tokens N` to adjust output size (default: 5000)
- `--output FILE` to save to a file

### Modes

- `--blast FILE` to show blast radius for a specific file
- `--section NAME` to output a single section
  (routes, deps, env, hot-files, models, structure,
  middleware, frameworks)
- `--wiki-only` to generate wiki articles without stdout

### Opt-out

- `--no-cache` to force a fresh scan
- `--no-wiki` to skip wiki article generation

## Wiki Articles

The scanner generates per-topic knowledge articles in
`.codesight/` for selective context loading:

```bash
python3 scanner.py .
# Creates .codesight/INDEX.md, auth.md, database.md, etc.
```

Load only what you need per session instead of the full map:

```bash
python3 scanner.py --section routes .
# ~200 tokens vs ~5,000 for the full map
```

## Example Output

```
# Context Map: myproject
Files: 127

## Structure
  src                  42 files (Python)
  tests                18 files (Python)
  docs                  5 files (Markdown)

## Dependencies (Python)
Package manager: uv
  - fastapi 0.104.0
  - pydantic 2.5.0
  - sqlalchemy 2.0.0
  ...12 more

## Frameworks Detected
  - FastAPI
  - SQLAlchemy
  - Pytest

## Routes
  GET    /users          (src/routes/users.py)
  POST   /users          (src/routes/users.py)
  GET    /users/{id}     (src/routes/users.py)

## Hot Files (high blast radius)
  - src/models/base.py (12 importers)
  - src/utils/auth.py (8 importers)

## Environment Variables
  - DATABASE_URL (required)
  - SECRET_KEY (has default)

## Token Savings: ~12,600 tokens saved
  Routes: ~1,200
  Hot files: ~300
  Env vars: ~200
  File scanning: ~10,200
```
