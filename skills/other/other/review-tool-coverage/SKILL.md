---
name: review-tool-coverage
description: Audit query tools for accuracy, gaps, and retirement candidates
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Audit the query tools in `tools/` for fitness. Use parallelism where possible.

## Context

Query tools (`tools/query_*.ps1`) exist to give structured answers without loading full files into context. CLAUDE.md lists only the most-used tools — niche tools are intentionally omitted to save per-session context, but they're still referenced by skills when relevant. "Unused by CLAUDE.md" does NOT mean unused.

## Current Inventory

| Tool | Purpose |
|------|---------|
| `query_config.ps1` | Config registry search — sections, groups, usage |
| `query_function.ps1` | Extract function body by name |
| `query_function_visibility.ps1` | Function definition, public/private, all callers |
| `query_global_ownership.ps1` | Global declaration, writers, readers, manifest |
| `query_instrumentation.ps1` | Profiler coverage map |
| `query_interface.ps1` | File public surface (functions + globals) |
| `query_ipc.ps1` | IPC message senders/handlers |
| `query_messages.ps1` | Windows message (WM_) handler/sender mapping |
| `query_profile.py` | Speedscope profile analysis |
| `query_state.ps1` | State machine branch extractor |
| `query_timers.ps1` | SetTimer inventory by file |
| `query_visibility.ps1` | Public functions with few external callers |
| `query_callchain.ps1` | Call graph traversal (forward and `-Reverse`) |
| `query_impact.ps1` | Mutation impact analysis |
| `query_includes.ps1` | Cross-file `#Include` analysis |
| `query_mutations.ps1` | Global mutation tracking |

## Audit Steps

### 1. Accuracy — do tools match the codebase?

Run each `query_*.ps1` tool with no args (or a known-good sample query) and check:
- Does the output parse the current file format correctly?
- Have any source files been renamed, restructured, or split since the tool was written?
- Are regex patterns still matching the right constructs?

Flag tools that produce **silently wrong** output (no errors, but stale/incorrect data). A tool that errors loudly is less dangerous than one that lies quietly.

### 2. Gaps — are there new "load big file to find small answer" patterns?

Look for patterns in the codebase that suggest a missing tool:
- Files over 300 lines where agents typically only need a small slice
- Common grep patterns that could return structured answers instead of raw lines
- Questions that require cross-referencing multiple files (e.g., "who sends message X and who handles it" — `query_messages.ps1` already covers this for WM_ messages; is there an equivalent need for other patterns?)

The bar: would a new tool save **>50 lines of context per use**? If not, grep is fine.

### 3. Retirement — are any tools dead weight?

A tool nobody invokes is dead code with maintenance cost. Check:
- Is the tool referenced by any skill in `.claude/skills/`?
- Is the tool listed in CLAUDE.md?
- Does the tool's domain still exist in the codebase? (e.g., if a subsystem was removed, its query tool should go too)

Note: a tool referenced only by skills (not CLAUDE.md) is NOT a retirement candidate — it's a niche tool by design.

### 4. Cross-references — could existing skills benefit from niche tools?

Check each skill in `.claude/skills/` — could any benefit from referencing a query tool they don't currently mention? Skills only load on invocation, so adding a niche tool reference costs zero per-session context.

## Plan Format

**Section 1 — Accuracy issues** (tools producing wrong output):

| Tool | Issue | Fix |
|------|-------|-----|
| `query_config.ps1` | Registry format changed, parser misses `fmt` field | Update regex on line 42 |

**Section 2 — Gap candidates** (potential new tools):

| Pattern | Frequency | Context Saved | Recommendation |
|---------|-----------|--------------|----------------|
| "Which files #Include X" | ~2/session | ~80 lines | New tool: `query_includes.ps1` |

**Section 3 — Retirement candidates** (genuinely unused):

| Tool | Last Relevant Use | Recommendation |
|------|------------------|----------------|
| `query_foo.ps1` | Subsystem removed in v0.7 | Delete |

**Section 4 — Skill cross-references** (niche tools that skills should mention):

| Skill | Tool to Add | Why |
|-------|------------|-----|
| `review-dead-code` | `query_visibility.ps1` | Finds public functions with 0 callers |

Ignore any existing plans — create a fresh one.
