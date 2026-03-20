---
name: searching-codebases
description: >
  Semantic code search with full pipeline: download, map, index, search, extract
  in a single invocation. Finds implementations by concept when identifiers are
  unknown — "retry logic" finds TokenBucketRateLimiter. Use when exploring GitHub
  repos, searching by intent rather than exact name, evaluating unfamiliar
  codebases, or answering "how does X work in this repo". Triggers on "search
  this repo", "find where X is implemented", "what handles Y", "evaluate this
  codebase", "explore this repo", or any natural-language question about code in
  a repository.
---

# Searching Codebases

Run the pipeline. Read the report. Synthesize.

## Primary Command

```bash
python3 SKILL_DIR/scripts/pipeline.py REPO_PATH_OR_URL "query1" ["query2" ...] [OPTIONS]
```

Replace `SKILL_DIR` with this skill's installed path. The pipeline runs the
full sequence internally — download, structural mapping, TF-IDF indexing,
search, context extraction — and outputs a single structured report to stdout.

**One tool call. One report. No manual step-by-step.**

Examples:

```bash
# Explore a GitHub repo with targeted queries
python3 SKILL_DIR/scripts/pipeline.py https://github.com/org/repo \
  "authentication flow" "error handling" "rate limiting"

# Local repo, single query
python3 SKILL_DIR/scripts/pipeline.py ./local-repo "retry logic with backoff"

# Structure overview only (no search queries)
python3 SKILL_DIR/scripts/pipeline.py https://github.com/org/repo --map-only

# Skip mapping for faster search (loses _MAP.md enrichment)
python3 SKILL_DIR/scripts/pipeline.py ./repo "query" --no-map

# Custom branch
python3 SKILL_DIR/scripts/pipeline.py https://github.com/org/repo "query" --branch develop
```

Options: `--skip DIRS` (comma-separated, default covers common noise),
`--top N` (results per query, default 5), `--map-only`, `--no-map`,
`--branch NAME`.

## What the Pipeline Does

```
resolve_repo ──┐
               ├──→ generate_maps ──→ search_and_extract ──→ compile_report
install_deps ──┘
```

0. **resolve_repo**: Downloads tarball from GitHub (with retry) or validates
   local path. Parallelizes with dependency installation.
1. **install_deps**: Ensures tree-sitter-language-pack is available for mapping.
2. **generate_maps**: Runs codemap.py (from mapping-codebases) to produce
   `_MAP.md` files. These dense signature files enrich the search index.
3. **search_and_extract**: Builds TF-IDF index once, runs all queries,
   extracts implementation context via line-targeted reads for top hits.
4. **compile_report**: Assembles README summary + structural map + ranked
   search results + extracted code into a single markdown report.

## Reading the Report

The report contains four sections:

1. **Overview** — README excerpt for project context
2. **Code Structure** — Root `_MAP.md` showing directory layout, exports, signatures
3. **Search Results** — Per-query ranked matches with scores and file locations
4. **Extracted Implementations** — Actual code for the highest-scoring matches

Scores above 0.3 are strong matches. Scores 0.1–0.3 are plausible leads.
Below 0.1 is noise — rephrase the query with more domain-specific terms.

## Follow-Up Searches

After reading the pipeline report, use `code_rag.py` directly for targeted
follow-up queries against the already-downloaded repo:

```bash
python3 SKILL_DIR/scripts/code_rag.py search /path/to/repo "specific query" --grouped
```

This reuses the local repo without re-downloading. The index rebuilds in
~50ms–2s depending on repo size. Use this for refinement, not as the primary
search method.

## When NOT to Use This

Skip this for repos under ~10 files — just read them directly. Skip this when
the exact identifier is already known — grep directly. For AST-precise
structural extraction (complete function bodies via tree-sitter), use
exploring-codebases instead.

## Limitations

TF-IDF has no morphological awareness — "clean" won't match "cleaning" unless
both forms appear in the corpus. Enrich sparse queries with synonyms:
"retry exponential backoff error recovery" beats "retry" alone.

Covers: Python, JS/JSX, TS/TSX, MJS/MTS, YAML/YML, Markdown, `_MAP.md`.
Dot-directories and common build artifacts are skipped by default.
