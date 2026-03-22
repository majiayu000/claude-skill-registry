---
name: review-ownership-manifest
description: Review ownership.manifest for coupling that can be reduced
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Review `ownership.manifest` for coupling that can be reduced. Use maximum parallelism where possible.

The manifest lists all files that write to each global (alphabetical, no file is special by position). The pre-gate validates freshness against actual code, so all entries reflect real mutations. Focus on whether coupling is **necessary**, not whether entries are accurate.

## Tools

**Ownership tools** (all in `tools/query_global_ownership.ps1`):

| Flag | Purpose |
|------|---------|
| `-Discover` | Full coupling landscape with `[SHARED]` / `[MOVABLE]` / `[MOVABLE -> target]` classification per hotspot. Add `-Detail` for per-file mutation counts. |
| `<name>` (positional) | Investigate a specific global — declaring file, fn-body write counts per file |
| `-Generate` | Preview manifest diff after changes |

**Semantic tools** (reduce context bloat vs full file reads):

| Tool | Purpose |
|------|---------|
| `query_interface.ps1 <file>` | What a file exports (public functions + globals) |
| `query_function_visibility.ps1 <funcName>` | Where defined, public/private, all callers |
| `query_function.ps1 <funcName>` | Extract full function body without loading entire file |
| `query_mutations.ps1 <globalName>` | Detailed per-function mutation sites with assignment operators and values |

## What to Look For

### 1. Movable declarations

Globals tagged `[MOVABLE -> target]` by `-Discover`. The declaring file has no function-body writes; a single external file is the sole writer. Moving the declaration to that file eliminates the manifest entry with zero risk.

**Skip** `[MOVABLE]` without a target — multiple files write, so moving the declaration doesn't reduce the manifest (all writers stay listed regardless of who declares).

**NEVER** move a `[SHARED]` global. The declaring file has real function-body writes. Moving it just flips which file needs a manifest entry.

### 2. Misplaced logic

A file writing globals that belong to another module's domain. Not "wrap it in a function to hide the write" but "this logic is in the wrong file." Function extraction is a side effect of putting code where it belongs.

### 3. Writer clusters

The same set of files appearing together on many variables. Does this suggest shared state that could be narrowed, or a missing module boundary?

### 4. Writer count reduction on high-fanout entries

A global with 5 writers means 5 files to read when debugging. Use the query tool on specific globals to check write counts — sometimes one writer's mutation is a 2-line operation that naturally belongs in the declaring file. Not "wrap it to hide the write" — genuinely "this 2-line reset belongs in the state machine, not the store handler." Even narrowing from 5 writers to 3 saves loading 2 files.

## What to Skip

Entries where coupling is inherent to the architecture (e.g., `cfg` across processes, GUI data flow between state/store/input). The goal isn't zero entries — it's removing coupling that forces loading extra files to understand a change.

## Methodology

1. Start with `-Discover` to get the full landscape
2. For each `[MOVABLE -> target]`, verify the move is safe (query the specific global, read the declaration site)
3. For `[SHARED]` entries with high writer counts, query each and look for reducible writers
4. For each proposed change, validate by reading the actual code — cite specific line ranges
5. Run `-Generate` to preview what the manifest would look like after proposed changes

## Plan Format

**Section 1 — Movable declarations** (zero-risk moves):

| Global | Current Declarer | Move To | Why |
|--------|-----------------|---------|-----|
| `gFoo` | `bar.ahk` | `baz.ahk` | Sole writer, no decl-file writes |

**Section 2 — Logic relocations** (misplaced writes):

| Global | File with Misplaced Write | Belongs In | Lines | What the Write Does |
|--------|--------------------------|-----------|-------|-------------------|
| `gFoo` | `bar.ahk:42` | `foo_state.ahk` | 40–45 | 2-line reset after transition |

**Section 3 — Cluster observations** (architectural notes, may or may not warrant action):

Narrative form — describe the pattern and whether it suggests a missing boundary.

Ignore any existing plans — create a fresh one.
