---
description: Automatic index freshness gate. Called before any query command (search, fetch, refs, explore) to ensure the index exists and is up-to-date. Handles first-run setup, incremental re-indexing, and staleness detection — so users never need to manually index.
---

# Staleness Gate Skill

Ensures the codemunch index is fresh before any query runs. This skill is called automatically — users never invoke it directly.

## Decision flow

```
1. Does .claude/codemunch/index.json exist?
   NO  → First-run: run detect-lsp skill, then full index skill → done
   YES → Continue to step 2

2. Get index timestamp from index.json "generated" field

3. Find files changed since index was built:
   git diff --name-only --diff-filter=ACMRD $(git log -1 --format=%H --before="$GENERATED_TIMESTAMP") HEAD

   Also check for untracked source files:
   git ls-files --others --exclude-standard

4. Filter to source files only (exclude non-code files like .md, .txt, images, etc.)

5. Are there changed source files?
   NO  → Index is fresh, proceed with query
   YES → Run incremental re-index (step 6)

6. Incremental re-index:
   - For each changed/added file: re-extract symbols using the best available engine
   - For each deleted file: remove its symbols from the index
   - Update the "generated" timestamp
   - Update the "file_hashes" manifest
   - Report: "Auto-updated index: +N symbols, -M symbols, K files re-indexed"
```

## Step 1 — Check index exists

```bash
# Check for index
if [ -f .claude/codemunch/index.json ]; then
  echo "INDEX_EXISTS"
else
  echo "NO_INDEX"
fi
```

If `NO_INDEX`:
1. Check if `.claude/codemunch/config.json` exists — if not, run the **detect-lsp** skill first
2. Run the **index** skill with full mode
3. Report: "First-run: auto-built codemunch index (N symbols across M files)"
4. Continue with the original query

## Step 2 — Get index timestamp

```bash
# Extract the generated timestamp from index
python3 -c "
import json
with open('.claude/codemunch/index.json') as f:
    idx = json.load(f)
print(idx.get('generated', ''))
" 2>/dev/null || jq -r '.generated' .claude/codemunch/index.json
```

## Step 3 — Find changed files since index was built

```bash
GENERATED="2026-03-11T02:14:00Z"

# Find the commit closest to when the index was built
BASE_COMMIT=$(git log -1 --format=%H --before="$GENERATED" 2>/dev/null)

if [ -z "$BASE_COMMIT" ]; then
  # No commit found before timestamp — index predates all commits, do full re-index
  echo "FULL_REINDEX_NEEDED"
else
  # Get changed files since that commit
  git diff --name-only --diff-filter=ACMRD "$BASE_COMMIT" HEAD 2>/dev/null
fi

# Also check untracked files (new files not yet committed)
git ls-files --others --exclude-standard 2>/dev/null
```

## Step 4 — Filter to source files

Only consider files with these extensions (adjust per detected languages in config):

```
.ts .tsx .js .jsx .mjs .cjs
.py .pyi
.go
.rs
.rb .rake
.java .kt .kts
.cs
.php
.swift
.c .h .cpp .hpp .cc
.lua .zig .sh .bash
```

Exclude:
- Lock files (`package-lock.json`, `Cargo.lock`, `go.sum`, etc.)
- Generated files (check `.claude/codemunch/config.json` exclude patterns)
- Non-code files (`.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.toml`, images, etc.)

## Step 5 — Decide: fresh or stale

```bash
CHANGED_COUNT=$(echo "$CHANGED_FILES" | grep -c '.')

if [ "$CHANGED_COUNT" -eq 0 ]; then
  echo "INDEX_FRESH"
else
  echo "INDEX_STALE:$CHANGED_COUNT files changed"
fi
```

If fresh: proceed silently — no output to the user.

## Step 6 — Incremental re-index

For each changed file, re-extract symbols using the same engine logic as the index skill:

1. **Remove old symbols** for changed/deleted files from the index
2. **Extract new symbols** for changed/added files
3. **Merge** into the existing index
4. **Update metadata**: `generated` timestamp, `file_hashes`, `stats`

```bash
# Remove symbols for changed files
python3 -c "
import json, sys

changed_files = sys.stdin.read().strip().split('\n')
with open('.claude/codemunch/index.json') as f:
    idx = json.load(f)

# Remove symbols from changed files
idx['symbols'] = [s for s in idx['symbols'] if s['file'] not in changed_files]
print(json.dumps(idx))
" <<< "$CHANGED_FILES"
```

Then run the index skill's engine pipeline (LSP → ctags → rg) on only the changed files, and append the new symbols.

**Report** (brief, inline — not a full index report):
```
🔄 Auto-updated index: 3 files re-indexed, +12 symbols, -8 symbols (1,251 total)
```

## Performance notes

- The staleness check itself is fast: one `git diff` + one JSON field read
- Incremental re-index only processes changed files — not the whole project
- For projects with no changes since last index, this adds <100ms overhead
- If >50 files changed, fall back to full re-index (faster than incremental at that scale)
