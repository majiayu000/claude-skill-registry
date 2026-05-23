---
name: ripgrep
description: Enhanced code search with custom ripgrep binary supporting ES module extensions and advanced patterns.
version: 1.1.0
model: sonnet
invoked_by: user
user_invocable: true
tools: [Read, Write, Edit]
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Ripgrep Skill

<identity>
Enhanced code search with ripgrep binary. NOTE: Prefer `pnpm search:code` for discovery/ranking and smaller output payloads; prefer raw `rg` for fastest exact literal matching.
</identity>

<capabilities>
- Hybrid code search via `pnpm search:code` (BM25 text + semantic vector ranking)
- Raw ripgrep for exhaustive pattern sweeps (every match, not ranked top-N)
- Advanced regex patterns (PCRE2 with -P flag)
- Custom file type definitions via .ripgreprc
- Integration with .gitignore and custom ignore patterns
</capabilities>

## ⚡ RECOMMENDED: Hybrid Code Search

Use the hybrid search system for day-to-day code discovery:

- **Text search works instantly** with no setup (ripgrep-based BM25)
- **Semantic search** requires a one-time index build: `pnpm code:index:reindex` (~12 min with GPU, ~17 min CPU)
- **GPU-accelerated** embedding via fastembed (NVIDIA CUDA auto-detected)
- **Memory-safe**: embeddings run in isolated subprocess to work around ONNX Runtime memory leak
- **Hybrid scoring**: Reciprocal Rank Fusion (RRF) combines text matches + semantic similarity

### Prerequisites

```bash
# Build the semantic index (one-time, or after major codebase changes)
pnpm code:index:reindex

# Verify .env has embeddings enabled (should be default)
# HYBRID_EMBEDDINGS=on
# LANCEDB_EMBEDDING_MODE=fastembed
```

Without the index build, `pnpm search:code` falls back to text-only matching. Concept queries like "authentication flow" will return poor results without embeddings.

### Search Commands

```bash
# Project structure (directory tree + entry points + dependency graph + Mermaid)
pnpm search:structure

# Token budget analysis (file sizes + token estimates + refactor advice)
pnpm search:tokens .claude/lib          # directory analysis
pnpm search:tokens path/to/file.cjs     # single file analysis

# Semantic + text hybrid search (concept discovery, ranked results)
# Repeated/similar queries served from cache (~5ms hit vs ~800ms miss)
pnpm search:code "authentication logic"
pnpm search:code "export class User"

# One-shot search + compress + dedup pipeline (for large context tasks)
pnpm search:compress "how does routing work"

# Get file content with line numbers
pnpm search:file src/auth.ts 1 50

# Cache observability (daemon must be running)
pnpm search:code --cache-stats          # view hits, misses, entries
pnpm search:code --cache-clear          # flush cached results
```

### `pnpm search:structure` — Know Where Things Are

**Run this FIRST before any edit, refactor, or onboarding task.** It gives a complete map:

1. **Directory Tree** — folder hierarchy up to 3 levels deep (excludes node_modules, .git)
2. **Entry Points** — all ESM `export` and CJS `module.exports` declarations with file:line references
3. **Top Dependencies** — most-imported modules (both `import` and `require`) with counts, split by:
   - `📦` External packages (node:test, path, fs, child_process)
   - `📁` Local modules (which internal files are imported most — these are the architectural hotspots)
4. **Mermaid Diagram** — visual dependency graph with:
   - Directory subgraphs showing export counts per folder
   - External dependency subgraph
   - Most-imported local modules highlighted as hub nodes

**How agents should use this:**

- **Before editing**: run `pnpm search:structure` to find which directory owns the code you need to change
- **To find hotspots**: the `📁` local dependencies with highest counts are the most-connected modules — changes there have the widest blast radius
- **To find entry points**: the exports list shows which files expose public APIs — start reading there
- **To understand architecture**: the Mermaid diagram shows which directories are most interconnected
- **Before refactoring**: the dependency counts tell you how many files will be affected by a rename/move

### `pnpm search:tokens [path]` — Know What Fits in Context

**Run this before deciding HOW to read a file or directory.** It tells you:

- **Token estimates** per file and per directory (~4 chars per token)
- **Actionable advice** on whether to Read directly, use offset/limit, or use search:code instead
- **Largest files** that need special handling
- **Directory rankings** by token size — prioritize which subdirs to explore

```bash
# Check a specific file
pnpm search:tokens .claude/lib/memory/lancedb-client-impl.cjs
# Output: Size: 41.1KB | Tokens: ~10.5K | Advice: △ MEDIUM — use Read with offset/limit

# Check a directory
pnpm search:tokens .claude/lib
# Output: 333 files, 2.0MB, ~527K tokens (too large to read all — use search:code)

# Check the whole project
pnpm search:tokens .
# Output: 12478 files, 61MB, ~16M tokens with per-directory breakdown
```

**Token Budget Legend:**

- `✓ OK` (<8K tokens) — safe to `Read` the entire file
- `△ MEDIUM` (8-32K) — use `Read` with `offset`/`limit` parameters, or `search:file`
- `⚠ LARGE` (32-100K) — prefer `search:code` over full Read; only read targeted sections
- `⚠ OVER` (>100K) — MUST use `search:code` or invoke `token-saver-context-compression` skill

**When to invoke `token-saver-context-compression`:**

- Directory total exceeds 100K tokens and you need to understand the whole subsystem
- File exceeds 32K tokens and you need a summary rather than specific lines
- You're building a prompt that would exceed context window limits

**Refactor recommendations** — for source code files >15K tokens, the tool recommends splitting:

```bash
pnpm search:tokens .claude/hooks/routing
# Output includes:
#   ✂ REFACTOR RECOMMENDED: user-prompt-unified.core.cjs (18.2K tokens)
#     Split into ~3 modules of ~8K tokens each:
#       user-prompt-unified.cjs          — thin facade (re-exports)
#       user-prompt-unified-impl.cjs     — main logic
#       user-prompt-unified-helpers.cjs  — extracted helpers
```

This only applies to source code files (`.js`, `.cjs`, `.mjs`, `.ts`, `.py`), not data files or configs. The pattern follows existing splits in the codebase (e.g., `routing-table.cjs` → `routing-table-data.cjs`, `index-manager.cjs` → `index-manager-operations.cjs`).

### `pnpm search:compress "query"` — Search + Compress in One Shot

**Use when `search:tokens` shows a topic spans >32K tokens and you need a compressed summary.**

Combines the full pipeline in a single command:

1. Hybrid search finds relevant files for your query
2. Reads actual file content (not just file paths)
3. Adaptively sets compression ratio based on corpus size (0.8 for small, 0.1 for huge)
4. Compresses via the Python engine with evidence-aware mode
5. Deduplicates extracted insights against existing memory (patterns.json, gotchas.json)
6. Outputs JSON with compressed context + classified memory records

```bash
pnpm search:compress "how does the routing system work"
# Returns JSON:
# {
#   "ok": true,
#   "search": { "query": "...", "hits": 20 },
#   "compression": { "mode": "evidence_aware", "skeletonRatio": 0.5 },
#   "memoryRecords": { "patterns": [...], "gotchas": [...], "issues": [...], "decisions": [...] },
#   "dedupStats": { "total": 24, "kept": 18, "filtered": 6 }
# }
```

**Key features:**

- **Adaptive compression**: small corpus (< 8K tokens) keeps 80%, huge corpus (>100K) keeps only 10%
- **Memory dedup**: won't re-persist patterns/gotchas that already exist in your memory system
- **Evidence gating**: use `--fail-on-insufficient-evidence` to abort if the query doesn't find strong matches

### Automatic Optimizations (No Action Needed)

These features work in the background with no commands required:

**Query Cache** — Repeated or semantically similar `search:code` queries are served from an in-memory cache (~5ms vs ~800ms). The cache uses cosine similarity (threshold: 0.95) so "routing system" and "how routing works" share cached results. Entries expire after 5 minutes. The cache lives in the daemon process for persistence across queries.

**BM25 Auto-Update** — When you edit a file, the BM25 text index updates incrementally (~10ms per file). This means `search:code` always reflects your latest changes without needing `code:index:reindex`. Only the text index updates; semantic embeddings require a full reindex.

**Cache observability:**

```bash
pnpm search:code --cache-stats    # entries, hits, misses, hit rate
pnpm search:code --cache-clear    # flush all cached results
```

### Search Mode Contract (Deterministic)

| Mode                           | Use when                                                         | Latency                          | Output                                    |
| ------------------------------ | ---------------------------------------------------------------- | -------------------------------- | ----------------------------------------- |
| `pnpm search:structure`        | First step: understand project layout, find where to edit        | Fast                             | Directory tree + exports + deps + Mermaid |
| `pnpm search:tokens [path]`    | Before reading: check if file/dir fits in context                | Fast                             | Token estimates + refactor advice         |
| `pnpm search:code "query"`     | Concept discovery, find unknown paths. Auto-cached (~5ms repeat) | ~0.2-0.8s (first), ~5ms (cached) | Compact ranked top-20                     |
| `pnpm search:compress "query"` | Large context: search + compress + dedup in one shot             | ~2-5s                            | JSON: compressed context + memory records |
| `rg -F "literal"`              | Exact symbol/literal lookup and anchor checks before edits       | Fastest (~35ms)                  | ALL matches (not ranked)                  |
| `Grep` (built-in)              | Exhaustive pattern sweeps for audits                             | Fast                             | ALL matches with context                  |

Required selection behavior:

- **FIRST**: `pnpm search:structure` to orient — know the directory layout and dependency hotspots.
- **CHECK SIZE**: `pnpm search:tokens` before reading — know if the file fits in context.
- **THEN**: `pnpm search:code` for concept discovery — find files related to your task. Repeat queries are cached automatically.
- **FOR LARGE CONTEXT**: `pnpm search:compress` when you need compressed understanding of a broad topic. Combines search + adaptive compression + memory dedup in one command.
- **BEFORE EDITS**: `rg -F` to validate exact anchors — confirm the symbol/function exists where you think.
- **FOR AUDITS**: `Grep` (built-in) for exhaustive sweeps — need ALL matches, not top-N.
- BM25 text index auto-updates when files are edited (no manual action needed).
- `fzf` stays optional for human-in-the-loop workflows; do not require it for automation.

### Locate Before You Edit (MANDATORY workflow for agents)

Before writing or editing ANY file, agents must locate it first. Blind edits waste tokens and cause errors.

**Step 1 — Orient** (run once per task):

```bash
pnpm search:structure
```

Read the output to understand:

- Which directories exist and what they contain
- Which modules are most-imported (`📁` local deps with high counts)
- Where the public APIs are (Entry Points list)

**Step 2 — Check token budget** (before reading files):

```bash
# Is this file safe to Read in full, or do I need search:code?
pnpm search:tokens .claude/lib/memory/lancedb-client-impl.cjs
# Output: △ MEDIUM (10.5K tokens) — use Read with offset/limit

# How big is this directory? Can I read all files?
pnpm search:tokens .claude/lib/routing
# If >32K total → use search:code for discovery, don't try to read everything
```

**Step 3 — Discover** (per subtask):

```bash
# Find files related to your task concept
pnpm search:code "hook validation pre-tool"
```

This returns ranked files most relevant to the concept. Note the file paths.

**Step 4 — Pinpoint** (before each edit):

```bash
# Confirm exact symbol location with line numbers
rg -F "validateHookInput" -g "*.cjs" -n

# Read the file to understand context (use offset/limit for MEDIUM+ files)
pnpm search:file .claude/lib/utils/hook-input.cjs 1 50
```

**Step 5 — Check blast radius** (before refactors):

```bash
# How many files import the module you're about to change?
rg -F "hook-input.cjs" -g "*.cjs" -c
# If 40+ files import it, consider backward-compatible changes
```

This workflow prevents:

- Wasting tokens on files too large for context (check tokens first)
- Editing the wrong file (there may be similarly-named files in different directories)
- Missing callsites during refactors (rg -c shows exact counts)
- Breaking high-import modules without knowing the blast radius
- Triggering context compression unnecessarily (know sizes upfront)

### Interactive Narrowing with fzf (Operator UX)

When result sets are large, use `fzf` to interactively narrow `rg`/`rga` output.

```bash
# rg + fzf + file preview
rg --line-number --no-heading --color=always "auth|token|session" . \
  | fzf --ansi --delimiter ":" \
    --preview "bat --color=always --style=numbers --highlight-line {2} {1}"

# rga (documents/archives) + fzf
rga --line-number --no-heading --color=always "invoice|receipt|policy" . \
  | fzf --ansi --delimiter ":" \
    --preview "bat --color=always --style=numbers --line-range=:300 {1}"
```

Advanced interactive ripgrep launcher pattern:

```bash
: | rg_prefix='rg --column --line-number --no-heading --color=always --smart-case' \
  fzf --ansi --disabled \
      --bind 'start:reload:$rg_prefix ""' \
      --bind 'change:reload:$rg_prefix {q} || true'
```

Usage contract:

- Use `fzf` for operator selection/narrowing, not as a replacement for search backends.
- Keep `pnpm search:code` as default for agent discovery/ranking workflows.
- Use `rg`/`rga` + `fzf` for interactive triage and manual result picking.

Structural + interactive workflow (human triage):

```bash
# Structural candidates (ast-grep)
ast-grep -p 'function $NAME($$$) { $$$ }' --lang javascript --files-with-matches .

# Narrow candidates interactively
ast-grep -p 'function $NAME($$$) { $$$ }' --lang javascript --files-with-matches . \
  | fzf --ansi --delimiter ":" \
    --preview "bat --color=always --style=numbers --line-range=:220 {}"
```

### How It Works

1. `pnpm code:index:reindex` builds BM25 text index + LanceDB vector embeddings
2. Embedding generation runs in an isolated subprocess (GPU-accelerated when available)
3. Subprocess is restarted every 50 batches to reclaim ONNX native memory leaks
4. `search:code` checks the query cache first (~5ms hit); on miss, queries BM25 + vector indexes
5. RRF merges text and semantic rankings into a single ordered result set
6. Results are cached for future similar queries (cosine > 0.95 = cache hit)
7. Post-edit hooks incrementally update the BM25 text index (~10ms per file)
8. `search:compress` combines search + adaptive compression + memory dedup in one pipeline

### Configuration

```bash
# Semantic search (default: on after running code:index:reindex)
HYBRID_EMBEDDINGS=on

# Embedding engine (fastembed recommended for speed + GPU support)
LANCEDB_EMBEDDING_MODE=fastembed

# Subprocess isolation for ONNX memory safety (default: on)
EMBED_SUBPROCESS=on

# Query cache (auto-caches repeated/similar queries)
SEARCH_CACHE_ENABLED=on            # Kill switch: set to off to disable
SEARCH_CACHE_TTL_MS=300000          # Cache TTL: 5 minutes
SEARCH_CACHE_SIMILARITY=0.95        # Cosine threshold for semantic cache hit

# BM25 incremental update after file edits
BM25_INCREMENTAL_UPDATE=on          # Kill switch: set to off to disable

# Disable semantic search (text-only, fastest, no index needed)
# HYBRID_EMBEDDINGS=off

# Daemon transport for repeated queries (cache lives here)
HYBRID_SEARCH_DAEMON=on
HYBRID_DAEMON_PREWARM=true
HYBRID_DAEMON_IDLE_MS=600000

# Query cache (caches repeated/similar queries by embedding similarity)
SEARCH_CACHE_ENABLED=on          # set to off to disable
SEARCH_CACHE_TTL_MS=300000       # cache entry TTL (5 min)
SEARCH_CACHE_SIMILARITY=0.95     # cosine threshold for cache hit

# BM25 incremental update after file edits
BM25_INCREMENTAL_UPDATE=on       # set to off to disable
```

### Daemon + Prewarm Runbook

```bash
# Start, verify, prewarm
pnpm search:daemon:start
pnpm search:daemon:status
pnpm search:daemon:prewarm

# Search (daemon path)
pnpm search:code "authentication logic"

# Stop daemon
pnpm search:daemon:stop
```

Expected latency profile on this repository:

- Cold daemon first query (no prewarm): ~1.35s avg
- First query after prewarm: ~0.40s avg
- Warm repeated daemon queries: ~0.18-0.19s
- Direct mode (`HYBRID_SEARCH_DAEMON=off`): ~0.73s avg for repeated CLI calls

### Index Build Performance

| Metric                       | With GPU (RTX 4070)           | CPU-only |
| ---------------------------- | ----------------------------- | -------- |
| Index time (2843 files)      | ~12 min                       | ~17 min  |
| Main process memory          | ~200MB                        | ~200MB   |
| Subprocess memory (isolated) | ~500MB                        | ~300MB   |
| Heap allocation needed       | 4GB                           | 4GB      |
| Index size on disk           | ~6MB (BM25) + ~10MB (vectors) | Same     |

### Measured Performance and Output (This Repo)

Using the same 5 queries on this repository:

| Mode                                         | Avg Latency | Avg Output Bytes | Best Use Case                      |
| -------------------------------------------- | ----------- | ---------------- | ---------------------------------- |
| `pnpm search:code` (`HYBRID_EMBEDDINGS=off`) | ~227ms      | ~461 bytes       | Fast discovery with compact output |
| `pnpm search:code` (`HYBRID_EMBEDDINGS=on`)  | ~734ms      | ~512 bytes       | Semantic/concept queries           |
| Raw `rg` literal search                      | ~35ms       | ~2478 bytes      | Exact symbol/literal lookup        |

Interpretation:

- Raw `rg` is fastest for exact literal/symbol lookups
- Hybrid search returns significantly smaller output payloads (often lower token pressure)
- Embeddings improve semantic recall, but add latency

### Decision Rule (Practical)

Use `pnpm search:code` when:

- Query is conceptual/natural language (`"auth flow for refresh tokens"`)
- You need ranked results and concise context for agent prompts
- You want lower output volume by default

Use raw `rg` when:

- Query is an exact symbol/literal (`TaskUpdate(`, `HybridLazyIndexer`, exact export names)
- You need the fastest possible lookup time
- You need advanced regex/PCRE2 behavior

### Measured by File Size (This Repo)

Sample size: 4 small files (0.5-5KB), 4 large files (30-109KB), literal token queries.

| Bucket      | `search:code` off | `search:code` on | `rg_repo`       | `rg_file`      |
| ----------- | ----------------- | ---------------- | --------------- | -------------- |
| Small files | ~230ms / ~2707B   | ~600ms / ~2965B  | ~34ms / ~17075B | ~15ms / ~1156B |
| Large files | ~228ms / ~2354B   | ~475ms / ~2847B  | ~35ms / ~17811B | ~15ms / ~6564B |

Takeaways:

- `rg_file` is fastest and best for targeted file-level checks.
- `rg_repo` remains fastest for repo-wide literal scans, but emits much larger output payloads.
- `search:code` has steadier latency across file sizes and typically lower output volume for prompt usage.

### Real-World Scenario Playbook (Tested Patterns)

Use these scenario patterns to choose the right search path quickly.

#### Scenario 1: Incident Triage (Unknown Root Cause)

Goal: find likely hotspots for a production symptom quickly without flooding context.

```bash
# 1) Start broad and semantic
pnpm search:code "task status not updating after completion"

# 2) Pivot to exact symbol checks once candidates appear
pnpm search:code "TaskUpdate("
```

Pattern:

- Start with `search:code` for intent-level recall.
- Narrow with literal/symbol queries once candidate files are identified.

#### Scenario 2: Fast Exact Lookup (You Know the Identifier)

Goal: locate exact definitions/usages as fast as possible.

```bash
# Repo-wide exact literal (stable example in this repo)
rg -F "TaskUpdate(" -g "*.cjs" -g "*.js" -g "*.ts" .

# Single-file exact lookup (fastest path)
rg -F "spawnSync" .claude/skills/skill-creator/scripts/create.cjs
```

Pattern:

- Use raw `rg -F` for exact symbol searches, especially for large files or known paths.

#### Scenario 3: Safe Refactor Prep

Goal: enumerate callsites and assess blast radius before renaming or behavior changes.

```bash
# 1) Check blast radius — how many files import this module?
pnpm search:structure
# Look at 📁 local deps: "📁 router-state (22)" = 22 files affected by changes

# 2) Gather broad callsites with semantic search
pnpm search:code "TaskUpdate completed status workflow"

# 3) Get EXACT callsite inventory (every match, not ranked)
rg -F "TaskUpdate(" -g "*.cjs" -g "*.js" -g "*.ts" -c
# Shows count per file — plan your edits across all files

# 4) Verify the specific lines before editing
rg -F "TaskUpdate(" -g "*.cjs" -n -C 2
```

Pattern:

- `search:structure` first to check dependency counts (blast radius).
- Hybrid search to find semantic variants you might miss.
- Raw `rg -c` for exact callsite count per file.
- Raw `rg -n -C 2` for line numbers + context before making edits.

#### Scenario 4: Security Audit Sweep

Goal: detect risky patterns and confirm exact high-confidence matches.

**For exhaustive sweeps (auditing), use `rg` or `Grep` (built-in) as primary tool.**
Hybrid search returns ranked top-N results, which is great for discovery but can miss matches.
Security audits need ALL instances of a pattern, not a ranked sample.

```bash
# EXHAUSTIVE sweep first (every match, not ranked)
rg -F "shell: true" -g "*.cjs" -g "*.js" -g "*.mjs"
rg -F "JSON.parse(" -g "*.cjs" -g "*.js" --no-heading
rg "eval\(|new Function\(" -g "*.cjs" -g "*.js"
rg -F "child_process" -g "*.cjs" -g "*.js"

# THEN use hybrid for concept discovery (find patterns you didn't think to grep for)
pnpm search:code "command injection shell execution security"
pnpm search:code "prototype pollution unsafe parsing"

# Verify specific findings with file-level rg
rg -F "exec(" .claude/lib/tools/standard-tools.cjs
```

Pattern:

- `rg`/`Grep` for exhaustive sweeps where completeness matters (security, compliance).
- Hybrid search for concept discovery to find patterns you didn't know to grep for.
- Never rely solely on hybrid top-N results for security claims.

#### Scenario 5: Architecture Onboarding (New Contributor/Agent)

Goal: understand structure and know where to make changes.

```bash
# 1) Get the full project map (directory tree + exports + deps + Mermaid)
pnpm search:structure

# From the output, you'll see:
#   - Directory tree: which folders exist and their nesting
#   - Entry points: which files export APIs (with file:line)
#   - Top dependencies: most-imported local modules (📁) = architectural hotspots
#     e.g. "📁 memory-manager.cjs (56)" means 56 files import it — high blast radius
#   - Mermaid diagram: visual module graph

# 2) Drill into subsystems by concept
pnpm search:code "routing guard task lifecycle"
pnpm search:code "memory scheduler session context"

# 3) Once you find candidate files, read them
pnpm search:file .claude/lib/routing/router-state.cjs 1 50

# 4) Before editing, confirm exact locations with rg
rg -F "resetToRouterMode" -g "*.cjs" -n
```

Pattern:

- `search:structure` first — know the landscape before touching anything.
- Look at `📁` local dependencies with highest counts — those are the modules where changes have the widest impact.
- Use `search:code` to find files related to your concept.
- Use `search:file` to read specific files with line numbers.
- Use `rg -F` to confirm exact symbol locations before editing.

#### Scenario 6: Codebase Audit / Deep Dive

Goal: systematic audit of a codebase for bugs, security issues, and dead code.

```bash
# 1) Map the project — identify architectural hotspots FIRST
pnpm search:structure
# Key things to note from the output:
#   - 📁 local deps with high counts = audit priority (most connected = most risk)
#   - Entry points list = public API surface to review
#   - Directory tree = scope of what needs auditing

# 2) Exhaustive pattern sweeps with rg (need ALL matches, not top-N)
rg -F "JSON.parse(" -g "*.cjs" -g "*.js" --no-heading
rg -F "shell: true" -g "*.cjs" -g "*.js"
rg "eval\(|new Function\(" -g "*.cjs" -g "*.js"
rg "DEPRECATED|LEGACY|WARN" -g "*.cjs" -g "*.js" -g "*.mjs"
rg -F "catch" -A1 -g "*.cjs" | rg "^\s*\}"  # empty catch blocks

# 3) Concept discovery for patterns you didn't think to grep
pnpm search:code "prototype pollution unsafe parsing"
pnpm search:code "race condition concurrent file write"
pnpm search:code "hardcoded secret credential password"

# 4) Cross-reference: find what calls a specific module
pnpm search:code "routing-table-intent"
rg -F "standard-tools" -g "*.cjs" -c  # exact import count per file

# 5) Check for dead code: find exports that are never imported
# Compare entry points from search:structure against rg import counts
rg -F "orchestrator-tool.cjs" -g "*.cjs" -c  # 0 results = dead module
```

Pattern:

- `search:structure` first to identify hotspots (high-import modules = audit priority).
- `rg`/`Grep` for exhaustive sweeps (security, dead code, pattern matching).
- `search:code` for concept discovery (find things you didn't know to grep for).
- Cross-reference `search:structure` entry points against `rg` import counts to find dead code.
- Never rely solely on hybrid search for audit completeness; it returns ranked top-N, not all matches.

#### Scenario 7: Token-Constrained Agent Workflow

Goal: minimize prompt/context bloat while maintaining retrieval quality.

```bash
# Default: semantic search on (compact ranked output, good for agents)
pnpm search:code "workflow task completion guard"

# For fastest possible response when you know exact terms
HYBRID_EMBEDDINGS=off pnpm search:code "TaskUpdate completed"

# For intent-heavy queries where exact terms are unknown
pnpm search:code "why does the task get stuck after agent finishes"
```

Pattern:

- Default to `HYBRID_EMBEDDINGS=on` (compact ranked output is already token-efficient).
- Use `HYBRID_EMBEDDINGS=off` override only when exact keyword match is sufficient and speed is critical.
- Hybrid search output is typically smaller than raw `rg` output (ranked top-N vs all matches).

### Reusable Query Patterns

- Concept query: `"authentication flow refresh token validation"`
- Mixed query: `"TaskUpdate completed status"`
- Exact query: `"TaskUpdate("` (prefer `rg -F` when speed is critical)
- Structure query: use `pnpm search:structure` before large edits
- File drill-down: `pnpm search:file <path> <startLine> <endLine>`

**Only use raw ripgrep (below) for:**

- Advanced PCRE2 regex patterns (lookahead/lookbehind)
- Custom file type filtering not supported by `search:code`
- Pipeline integration with other CLI tools

<instructions>
<execution_process>

## Overview

This skill provides access to ripgrep (rg) via the `@vscode/ripgrep` npm package, which automatically downloads the correct binary for your platform (Windows, Linux, macOS). Enhanced file type support for modern JavaScript/TypeScript projects.

**Binary Source**: `@vscode/ripgrep` npm package (cross-platform, auto-installed)

- Automatically handles Windows, Linux, macOS binaries
- No manual binary management required

**Optional Config**: `bin/.ripgreprc` (if present, automatically used)

## When to Use What

| Tool                 | Best for                                              | Tradeoff                                               |
| -------------------- | ----------------------------------------------------- | ------------------------------------------------------ |
| `pnpm search:code`   | Concept discovery, ranked results, agent workflows    | Top-N ranked, not exhaustive; needs index for semantic |
| Built-in `Grep` tool | Exhaustive pattern sweeps, audits, exact counts       | Returns ALL matches; higher token output               |
| Raw `rg` via Bash    | PCRE2 regex, pipeline integration, `.ripgreprc` types | Requires Bash tool; larger raw output                  |
| Built-in `Glob` tool | Finding files by name pattern                         | No content search                                      |

**For audits and security sweeps**: prefer `Grep` (built-in) — it returns every match, not ranked top-N. You need completeness, not ranking.

**For discovery and onboarding**: prefer `pnpm search:code` — compact ranked output, semantic understanding, low token pressure.

**For exact symbol lookups before edits**: prefer raw `rg -F` — fastest possible, deterministic.

## Quick Start Commands

### Basic Search

```bash
# Search for pattern in all files
node .claude/skills/ripgrep/scripts/search.mjs "pattern"

# Search specific file types
node .claude/skills/ripgrep/scripts/search.mjs "pattern" -tjs
node .claude/skills/ripgrep/scripts/search.mjs "pattern" -tts

# Case-insensitive search
node .claude/skills/ripgrep/scripts/search.mjs "pattern" -i

# Search with context lines
node .claude/skills/ripgrep/scripts/search.mjs "pattern" -C 3
```

### Quick Search Presets

```bash
# Search JavaScript files (includes .mjs, .cjs)
node .claude/skills/ripgrep/scripts/quick-search.mjs js "pattern"

# Search TypeScript files (includes .mts, .cts)
node .claude/skills/ripgrep/scripts/quick-search.mjs ts "pattern"

# Search all .mjs files specifically
node .claude/skills/ripgrep/scripts/quick-search.mjs mjs "pattern"

# Search .claude directory for hooks
node .claude/skills/ripgrep/scripts/quick-search.mjs hooks "pattern"

# Search .claude directory for skills
node .claude/skills/ripgrep/scripts/quick-search.mjs skills "pattern"

# Search .claude directory for tools
node .claude/skills/ripgrep/scripts/quick-search.mjs tools "pattern"

# Search .claude directory for agents
node .claude/skills/ripgrep/scripts/quick-search.mjs agents "pattern"

# Search all files (no filter)
node .claude/skills/ripgrep/scripts/quick-search.mjs all "pattern"
```

## Common Patterns

### File Type Searches

```bash
# JavaScript files (includes .js, .mjs, .cjs)
rg "function" -tjs

# TypeScript files (includes .ts, .mts, .cts)
rg "interface" -tts

# Config files (.yaml, .yml, .toml, .ini)
rg "port" -tconfig

# Markdown files (includes .md, .mdc)
rg "# Heading" -tmd
```

### Advanced Regex

```bash
# Word boundary search
rg "\bfoo\b"

# Case-insensitive
rg "pattern" -i

# Smart case (case-insensitive unless uppercase present)
rg "pattern" -S  # Already default in .ripgreprc

# Multiline search
rg "pattern.*\n.*another" -U

# PCRE2 lookahead/lookbehind
rg -P "foo(?=bar)"        # Positive lookahead
rg -P "foo(?!bar)"        # Negative lookahead
rg -P "(?<=foo)bar"       # Positive lookbehind
rg -P "(?<!foo)bar"       # Negative lookbehind
```

### Filtering

```bash
# Exclude directories
rg "pattern" -g "!node_modules/**"
rg "pattern" -g "!.git/**"

# Include only specific directories
rg "pattern" -g ".claude/**"

# Exclude specific file types
rg "pattern" -Tjs  # Exclude JavaScript

# Search hidden files
rg "pattern" --hidden

# Search binary files
rg "pattern" -a
```

### Context and Output

```bash
# Show 3 lines before and after match
rg "pattern" -C 3

# Show 2 lines before
rg "pattern" -B 2

# Show 2 lines after
rg "pattern" -A 2

# Show only filenames with matches
rg "pattern" -l

# Show count of matches per file
rg "pattern" -c

# Show line numbers (default in .ripgreprc)
rg "pattern" -n
```

## PCRE2 Advanced Patterns

Enable PCRE2 mode with `-P` for advanced features:

### Lookahead and Lookbehind

```bash
# Find "error" only when followed by "critical"
rg -P "error(?=.*critical)"

# Find "test" not followed by ".skip"
rg -P "test(?!\.skip)"

# Find words starting with capital after "Dr. "
rg -P "(?<=Dr\. )[A-Z]\w+"

# Find function calls not preceded by "await "
rg -P "(?<!await )\b\w+\("
```

### Backreferences

```bash
# Find repeated words
rg -P "\b(\w+)\s+\1\b"

# Find matching HTML tags
rg -P "<(\w+)>.*?</\1>"
```

### Conditionals

```bash
# Match IPv4 or IPv6
rg -P "(\d{1,3}\.){3}\d{1,3}|([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}"
```

## Integration with Other Tools

### With fzf (Interactive Search)

```bash
# Search and interactively select file
rg --files | fzf

# Search pattern and open in editor
rg "pattern" -l | fzf | xargs code
```

### With vim

```bash
# Set ripgrep as grep program in .vimrc
set grepprg=rg\ --vimgrep\ --smart-case\ --follow
```

### Pipeline with Other Commands

```bash
# Search and count unique matches
rg "pattern" -o | sort | uniq -c

# Search and replace preview
rg "old" -l | xargs sed -i 's/old/new/g'
```

## Performance Optimization

### Tips for Large Codebases

1. **Use file type filters**: `-tjs` is faster than searching all files
2. **Exclude large directories**: `-g "!node_modules/**"`
3. **Use literal strings when possible**: `-F "literal"` (disables regex)
4. **Enable parallel search**: Ripgrep uses all cores by default
5. **Use .gitignore**: Ripgrep respects .gitignore automatically

### Benchmarks

Ripgrep is typically:

- **10-100x faster** than grep
- **5-10x faster** than ag (The Silver Searcher)
- **3-5x faster** than git grep

## Custom Configuration

The optional `.ripgreprc` file at `bin/.ripgreprc` (if present) contains:

```
# Extended file types
--type-add=js:*.mjs
--type-add=js:*.cjs
--type-add=ts:*.mts
--type-add=ts:*.cts
--type-add=md:*.mdc
--type-add=config:*.yaml
--type-add=config:*.yml
--type-add=config:*.toml
--type-add=config:*.ini

# Default options
--smart-case
--follow
--line-number
```

## Framework-Specific Patterns

### Searching .claude Directory

```bash
# Find all hooks
rg "PreToolUse\|PostToolUse" .claude/hooks/

# Find all skills
rg "^# " .claude/skills/ -tmd

# Find agent definitions
rg "^name:" .claude/agents/ -tmd

# Find workflow steps
rg "^### Step" .claude/workflows/ -tmd
```

### Common Agent Studio Searches

```bash
# Find all TaskUpdate calls
rg "TaskUpdate\(" -tjs -tts

# Find all skill invocations
rg "Skill\(\{" -tjs -tts

# Find all memory protocol sections
rg "## Memory Protocol" -tmd

# Find all BLOCKING enforcement comments
rg "BLOCKING|CRITICAL" -C 2
```

</execution_process>

<best_practices>

1. **Use file type filters** (`-tjs`, `-tts`) for faster searches
2. **Respect .gitignore** patterns (automatic by default)
3. **Use smart-case** for case-insensitive search (default in config)
4. **Enable PCRE2** (`-P`) only when advanced features needed
5. **Exclude large directories** with `-g "!node_modules/**"`
6. **Use literal search** (`-F`) when pattern has no regex
7. **Binary automatically managed** via `@vscode/ripgrep` npm package
8. **Use quick-search presets** for common .claude directory searches
   </best_practices>
   </instructions>

<examples>
<usage_example>
**Search for all TaskUpdate calls in the project:**

```bash
node .claude/skills/ripgrep/scripts/search.mjs "TaskUpdate" -tjs -tts
```

**Find all security-related hooks:**

```bash
node .claude/skills/ripgrep/scripts/quick-search.mjs hooks "security|SECURITY" -i
```

**Search for function definitions with PCRE2:**

```bash
node .claude/skills/ripgrep/scripts/search.mjs -P "^function\s+\w+\(" -tjs
```

</usage_example>
</examples>

## Binary Management

The search scripts use `@vscode/ripgrep` npm package which automatically:

- Detects your platform (Windows, Linux, macOS)
- Downloads the correct binary during `pnpm install`
- Handles all architecture variants (x64, ARM64, etc.)

No manual binary management required - the npm package handles everything automatically.

## Related Skills

- [`grep`](../grep/SKILL.md) - Built-in Claude Code grep (simpler, less features)
- [`glob`](../glob/SKILL.md) - File pattern matching

## Iron Laws

1. **ALWAYS** run `pnpm search:structure` first to orient before any edit task — editing without understanding directory layout and import hotspots causes missed callsites and blast radius surprises.
2. **NEVER** use ranked/top-N hybrid search output for security audits — completeness matters for audits; use `rg` or built-in `Grep` to get every match, not a ranked sample.
3. **ALWAYS** validate exact symbol anchors with `rg -F` before editing code — editing based on semantic matches alone misses similarly-named functions and causes wrong-file edits.
4. **NEVER** make `fzf` a blocking dependency in automated or agent workflows — interactive selection is operator UX only; unattended agent flows must stay non-interactive and reproducible.
5. **ALWAYS** scope repo-wide searches with file type filters or path globs — unscoped searches flood context with irrelevant matches and inflate token costs.

## Anti-Patterns

| Anti-Pattern                                                       | Why It Fails                                                                                       | Correct Approach                                                                                       |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Starting an edit task without running `search:structure`           | Missing directory layout knowledge causes edits to the wrong file and missed callsites             | Always run `pnpm search:structure` first to understand directory hierarchy and import hotspots         |
| Using hybrid search for security audit completeness                | Hybrid search returns ranked top-N, not all matches; security audits need every instance           | Use `rg`/`Grep` (exhaustive) for security sweeps; use hybrid search only for concept discovery         |
| Editing code without confirming exact symbol location with `rg -F` | Semantic matches include similarly-named symbols; editing the wrong function is silent             | Run `rg -F "exact_symbol"` to confirm location and callsite count before any code edit                 |
| Making `fzf` a required step in agent automation pipelines         | `fzf` requires interactive input; agents cannot proceed when the pipeline blocks on user selection | Keep `fzf` optional and operator-only; agent workflows must use deterministic `rg`/`search:code`       |
| Running unscoped repo-wide regex searches                          | Large monorepos return thousands of matches; token costs spike and context floods                  | Always constrain scope with `-g "*.cjs"`, `-tjs`, or a path argument before running repo-wide patterns |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
