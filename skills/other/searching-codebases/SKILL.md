---
name: searching-codebases
description: >
  Find code by regex pattern or natural language concept in any codebase.
  Auto-routes between n-gram indexed regex search (2-20x faster than ripgrep)
  and TF-IDF semantic search. Expands results to full functions via AST maps.
  Accepts GitHub URLs, local directories, uploaded files/archives, or project
  knowledge. Use when asked to find implementations, search for patterns,
  explore unfamiliar repos, or answer "where is X" / "how does Y work" about
  code. Triggers on "search this repo", "find where X is", "grep for",
  "what handles Y", regex patterns, or natural-language questions about code.
metadata:
  version: 1.0.0
---

# Searching Codebases

Find code in any codebase by pattern or concept. One entry point, two
search strategies, automatic routing.

## Prerequisites

```bash
uv tool install ripgrep
```

Tree-sitter (for structural maps) installs automatically when needed.

## Primary Command

```bash
SKILL_DIR=/mnt/skills/user/searching-codebases

python3 $SKILL_DIR/scripts/search.py SOURCE "query1" ["query2" ...] [OPTIONS]
```

SOURCE is any of:
- Local directory path
- GitHub URL (downloads tarball automatically)
- `uploads` (uses `/mnt/user-data/uploads/`)
- `project` (uses `/mnt/project/`)
- Path to a `.zip` or `.tar.gz` archive

## Search Modes

**Regex mode** (patterns, identifiers, literal text):
```bash
python3 $SKILL_DIR/scripts/search.py ./repo "def handle_error"
python3 $SKILL_DIR/scripts/search.py ./repo "class.*Exception" --regex
python3 $SKILL_DIR/scripts/search.py ./repo "TODO|FIXME|HACK"
```

**Semantic mode** (concepts, natural language):
```bash
python3 $SKILL_DIR/scripts/search.py ./repo "retry logic with backoff" --semantic
python3 $SKILL_DIR/scripts/search.py ./repo "authentication flow"
python3 $SKILL_DIR/scripts/search.py ./repo "error handling strategy"
```

Auto-detection: short queries and code-like tokens → regex. Multi-word
natural language → semantic. Override with `--regex` or `--semantic`.

## Options

- `--regex` / `--semantic`: Force search mode
- `--expand`: Return full function bodies instead of matching lines
- `--map-only`: Generate structural maps only (delegates to mapping-codebases)
- `--benchmark`: Compare indexed regex vs brute-force ripgrep
- `--branch NAME`: Git branch for GitHub URLs (default: main)
- `--skip DIRS`: Comma-separated directories to skip
- `--json`: Machine-readable output
- `-v`: Show index stats and query routing decisions

## How It Works

**Regex search** builds a sparse n-gram inverted index over all files.
Queries are decomposed into literal fragments, looked up in the index
to identify candidate files (typically 90-99% reduction), then verified
with ripgrep. Frequency-weighted n-grams make rare character sequences
more selective.

**Semantic search** builds a TF-IDF index over code chunks (functions,
classes, map entries). Queries are ranked by cosine similarity. Structural
maps from mapping-codebases enrich the index when available.

**Context expansion** (`--expand`) uses `_MAP.md` files to identify function
boundaries, returning complete structural units rather than line fragments.

**Small codebases** (< 20 files) skip indexing entirely — direct ripgrep is
faster when there's nothing to narrow.

## Mixed Queries

Multiple queries can use different modes in a single invocation. Each query
is auto-routed independently, and indexes are built once per mode:

```bash
python3 $SKILL_DIR/scripts/search.py ./repo \
  "class.*Error" \
  "error recovery strategy" \
  "def retry"
```

## Dependencies

- **mapping-codebases**: Generates `_MAP.md` files for context expansion and
  TF-IDF enrichment. Not required — search works without maps, just with
  less context in results.
- **ripgrep**: Required for regex verification. Install via `uv tool install ripgrep`.
- **scikit-learn**: Required for semantic mode. Installs automatically.

## When NOT to Use

- Repos under ~10 files: just read them directly
- Exact identifier known: `rg "identifier" /path` is simpler
- Need AST-precise extraction (complete function bodies via tree-sitter):
  use exploring-codebases with `--expand-full` instead

## Files

- `scripts/search.py` — Entry point, query routing, output formatting
- `scripts/resolve.py` — Input source resolution (GitHub, uploads, archives)
- `scripts/context.py` — AST/map-based context expansion
- `scripts/ngram_index.py` — Sparse n-gram inverted index, regex decomposition
- `scripts/sparse_ngrams.py` — Core n-gram algorithms, frequency weights
- `scripts/code_rag.py` — TF-IDF semantic search over code chunks
