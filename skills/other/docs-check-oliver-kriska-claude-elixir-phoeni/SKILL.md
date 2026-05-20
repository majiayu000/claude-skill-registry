---
name: docs-check
description: |
  CONTRIBUTOR TOOL - Validate plugin against latest Claude Code documentation.
  Catches breaking changes, deprecations, discovers new features.
  Run before releases or periodically. NOT part of the distributed plugin.
argument-hint: "[--quick|--focus=agents|skills|hooks|config]"
---

# Plugin Documentation Compatibility Check

Validates plugin agents, skills, hooks, and config against the latest
Claude Code documentation to catch breaking changes and discover new features.

## Usage

```text
/docs-check                    # Full validation (all components)
/docs-check --quick            # Structural checks only (no docs fetch, no tokens)
/docs-check --focus=agents     # Validate only agents
/docs-check --focus=skills     # Validate only skills
/docs-check --focus=hooks      # Validate only hooks
/docs-check --focus=config     # Validate only plugin.json/marketplace.json
```

## Architecture (OTP Supervision Pattern)

```text
┌─────────────────────────────────────────────────────────────────┐
│  /docs-check (skill entry point)                                │
│   │                                                             │
│   ├─ Step 1: bash scripts/fetch-claude-docs.sh (zero tokens)    │
│   │          Always fetches all 9 doc pages (~420KB)             │
│   │                                                             │
│   └─ Step 2: delegate to orchestrator (reads from cache only)   │
│       │                                                         │
│       │  docs-validation-orchestrator (opus)                    │
│       │                                                         │
│       │  SCAN → READ CACHE → SPAWN WORKERS → COMPRESS → REPORT │
│       │   │         │              │             │          │   │
│       │   ↓         ↓              ↓             ↓          ↓   │
│       │ inventory  pre-fetched  4 parallel    context    report │
│       │ plugin     docs-cache   subagents     supervisor       │
│       │ components              (sonnet)      (haiku)          │
│       └─────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

## Execution

### Step 1: Fetch Docs (Automatic)

**Always run first.** Downloads all doc pages to cache. Skips pages
already cached within 24h. Zero token cost — pure curl.

```bash
# --quick mode: skip this step entirely (structural checks only)
# All other modes: always fetch
bash scripts/fetch-claude-docs.sh
```

### Step 2: Delegate to Orchestrator

After docs are cached, delegate. The orchestrator reads from cache only
and crashes if cache files are missing.

```text
Task(subagent_type: "docs-validation-orchestrator")
```

Pass the user's flags (--quick, --focus) in the prompt.

## What the Orchestrator Does

1. **Inventory** — scan `plugins/elixir-phoenix/` for existing components
2. **Read cached docs** — from `.claude/docs-check/docs-cache/` (never fetches)
3. **Spawn workers** — one sonnet subagent per component type, in parallel
4. **Compress** — context-supervisor (haiku) if 3+ workers
5. **Structural checks** — fast local checks, always run
6. **Report & Action** — write report, offer PR if issues found

## Iron Laws

1. **Fetch ALL docs upfront** — no conditional fetching, no partial downloads
2. **Use `scripts/fetch-claude-docs.sh`** — single source of truth for doc fetching
3. **Workers get docs IN PROMPT** — no runtime fetching
4. **Workers use sonnet** — opus is wasteful for comparison tasks
5. **Structural checks always run** — even if docs fetch fails
6. **Breaking changes are BLOCKERS** — surface prominently

## References

- `references/validation-rules.md` — Per-component validation checklists
- `references/doc-pages.md` — Component-to-URL mapping
