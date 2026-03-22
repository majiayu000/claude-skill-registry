---
name: buff-counterfeit
description: This skill should be used when the user asks to "check my preferences", "show memory", "run /buff:counterfeit", "what does buff remember", "update my preferences", "reset memory", "show session history", "what did I work on", "show graph", "show corrections", or when buff needs to read or write persistent user/project memory. Intelligence engine with 3-tier memory — preferences, patterns, corrections, and project graph. Auto-activates at session start and end.
version: 0.2.0
argument-hint: "[show|reset|prune] [--global] [--project] [--graph] [--corrections]"
allowed-tools: Read, Write, Bash, Glob, Grep
---

# buff-counterfeit v2

Counterfeit is buff's intelligence engine. It maintains a 3-tier memory system — global preferences, cross-project patterns and corrections, and per-project intelligence (dependency graph, decisions, learnings) — so every skill invocation makes the others smarter. Learns across projects, never repeats corrected mistakes.

## Memory architecture

```
~/.buff/memory/                          <- GLOBAL (cross-project)
├── preferences.json                     <- existing: stack, style, communication
├── patterns.json                        <- NEW: architectural patterns, tech decisions
└── corrections.json                     <- NEW: user corrections to buff's output

.buff/memory/                            <- PROJECT (per-project)
├── context.json                         <- existing: session history, plan progress
├── graph.json                           <- NEW: lightweight project model
├── decisions.json                       <- NEW: architectural decisions + rationale
└── learnings.json                       <- NEW: project-specific patterns, mistakes
```

**Resolution rule**: Project-local overrides global. When the same key exists in both, the project value wins.

## Tier 1 — Preferences

`~/.buff/memory/preferences.json` — global preferences that apply everywhere. Schema unchanged from v1:

```json
{
  "stack": {
    "runtime": "bun",
    "language": "typescript",
    "frontend": "react",
    "backend": "elysia",
    "testing": "vitest",
    "package_manager": "bun"
  },
  "code_style": {
    "naming": "camelCase",
    "imports": "named-exports-preferred",
    "error_handling": "result-pattern",
    "file_organization": "feature-colocation"
  },
  "communication": {
    "verbosity": "terse",
    "language": "en",
    "explanations": "code-first"
  },
  "git": {
    "commit_style": "conventional",
    "commit_frequency": "feature"
  }
}
```

## Tier 2 — Patterns & Corrections

Two new global files that capture cross-project intelligence.

### `~/.buff/memory/patterns.json`

What buff learns across ALL projects — architectural patterns, technology decisions, and anti-patterns derived from corrections:

```json
{
  "architecture": [
    {
      "pattern": "repository pattern for DB access",
      "frequency": 3,
      "last_used": "2026-03-20",
      "context": "API projects with relational databases"
    }
  ],
  "tech_decisions": [
    {
      "decision": "Elysia over Express",
      "frequency": 3,
      "last_used": "2026-03-20",
      "rationale": "user prefers performance-focused frameworks"
    }
  ],
  "anti_patterns": [
    {
      "pattern": "default exports",
      "reason": "user corrected: always use named exports",
      "source": "correction"
    }
  ]
}
```

**Promotion rule**: A pattern needs 2+ occurrences across projects to be saved here. Single instances stay in project-level `decisions.json` until repeated elsewhere.

### `~/.buff/memory/corrections.json`

Every time the user corrects buff's output, capture it:

```json
[
  {
    "date": "2026-03-20",
    "skill": "code",
    "what_buff_did": "used default export for AuthService",
    "what_user_wanted": "named export",
    "context": "TypeScript service files",
    "generalized": true
  }
]
```

- `generalized: true` — applies to all projects (e.g., naming conventions, export style)
- `generalized: false` — project-specific only (e.g., domain-specific naming)
- Max 50 entries. When exceeded, prune oldest. Keep high-frequency corrections (3+ occurrences of same correction type) forever.

## Tier 3 — Project Intelligence

Three new project-local files that build per-project awareness.

### `.buff/memory/graph.json`

Lightweight project dependency model. NOT a full AST — just exports, imports, line counts, and coverage. Enough for cross-file awareness without token bloat:

```json
{
  "files": {
    "src/auth.ts": {
      "exports": ["AuthService", "validateToken", "createSession"],
      "imports_from": ["src/db.ts", "src/types.ts"],
      "imported_by": ["src/router.ts", "src/middleware.ts"],
      "lines": 142,
      "last_modified": "2026-03-20",
      "test_file": "src/auth.test.ts",
      "coverage": {
        "functions": 3,
        "tested": 2,
        "untested": ["createSession"]
      }
    }
  },
  "updated_at": "2026-03-20T14:00:00Z"
}
```

### `.buff/memory/decisions.json`

Architectural decisions made during planning and development:

```json
[
  {
    "decision": "Use repository pattern for all DB access",
    "rationale": "Separates persistence from business logic, easier testing",
    "date": "2026-03-20",
    "skill": "plan",
    "affects": ["src/repositories/"]
  }
]
```

### `.buff/memory/learnings.json`

Project-specific patterns and mistakes captured during work:

```json
[
  {
    "learning": "Middleware order matters — auth must come before rate limiter",
    "source": "user correction during code review",
    "date": "2026-03-20",
    "applies_to": "middleware ordering"
  }
]
```

## Graph update triggers

The graph is updated at two points only — no polling, no watchers.

### (a) Session start — staleness check

The `session-start.sh` hook checks if `graph.json` exists and whether `graph.updated_at` is older than the last git commit. If stale, it sets the `.buff/memory/.graph-stale` flag file. The SessionStart prompt hook then detects this flag and runs the incremental update algorithm (below) to rebuild the graph.

### (b) Post-skill lazy update

Any skill that writes files (`code`, `test`) updates `graph.json` entries for the files it touched at the end of its execution. This is a prompt instruction in each skill's SKILL.md, not a hook.

### Incremental update algorithm

Never do a full re-scan. Always incremental:

1. Run `git log --name-only --since="<graph.updated_at>" --pretty=format:""` to get files changed since last update, plus `git diff --name-only HEAD` to catch uncommitted changes
2. For each changed file: re-read exports, imports, line count with Grep/Read. Update the file's entry in `graph.json`
3. For deleted files: remove their entries from `graph.json`
4. For new files: add minimal entry (exports, imports, lines)
5. Write updated `graph.json` with new `updated_at` timestamp
6. Expected time: 2-5 seconds for a medium project (~100 files changed)

## Token budget

Max 3,000 tokens total counterfeit payload at session start. The graph is NOT injected at session start — it is read on-demand by individual skills.

| When | What | Tokens |
|---|---|---|
| **Session start** | preferences.json (full) | ~200 |
| **Session start** | corrections.json (recent 10) | ~300 |
| **Session start total** | | **~500** |
| On-demand (plan) | decisions.json (relevant subset) | ~200 |
| On-demand (code) | patterns.json (relevant subset) | ~300 |
| On-demand (any skill) | graph.json (per-file entries, as needed) | ~100 per file |

Skills request only the slices they need. No skill loads the full graph into context.

## Correction capture

Prompt-based detection mechanism — no hooks or external tooling required. Each upgraded skill includes a "Correction Detection" instruction block in its own SKILL.md.

### Detection signals

Watch for these indicators that the user is correcting buff's output:

- **Explicit rejection**: "no", "not like that", "wrong", "don't do that"
- **Code replacement**: user provides alternative code immediately after buff's output
- **Approach redirect**: "instead, do X", "use Y not Z", "I prefer..."
- **Style correction**: "always use...", "never use...", formatting changes

### On detection

1. Extract: what buff did wrong + what the user wanted + context (file type, skill, domain)
2. Write to `.buff/memory/learnings.json` (project-specific learning)
3. If generalizable (applies beyond this project): also write to `~/.buff/memory/corrections.json` with `generalized: true`
4. If generalized (step 3 applied) and same correction appears 2+ times in `corrections.json`: promote the pattern to `patterns.json` anti_patterns array

### Example flow

User says: "No, use named exports here, not default" after `code` skill outputs a default export.

1. Capture: `what_buff_did: "default export"`, `what_user_wanted: "named export"`, `context: "TypeScript files"`
2. Write to `learnings.json`: `{"learning": "Use named exports, not default", ...}`
3. Write to `corrections.json`: `{"what_buff_did": "used default export", "what_user_wanted": "named export", "generalized": true, ...}`
4. Check frequency in `corrections.json` — if 2+ similar: add to `patterns.json` anti_patterns

## Skill integration map

Every upgraded skill both reads from and writes to counterfeit memory:

| Skill | Reads from | Writes to |
|---|---|---|
| `plan` | patterns, decisions, graph | decisions |
| `code` | patterns, corrections, graph, decisions | graph, learnings |
| `validate` | patterns, corrections, graph | learnings, graph |
| `test` | graph, corrections | graph (coverage) |
| `forge` | everything (via decision engine) | everything (via cycle results) |

`forge` integration is out of scope for this upgrade — listed for completeness only.

## Pruning rules

| File | Rule |
|---|---|
| `corrections.json` | Max 50 entries. Prune oldest first. Keep high-frequency corrections (3+ same type) forever. |
| `patterns.json` `anti_patterns` | Permanent. Sourced from corrections, never auto-pruned. Removed only via `reset --corrections` or manually. |
| `patterns.json` | Entries with frequency 1 and `last_used` older than 30 days are deleted. |
| `decisions.json` | Max 50 entries. When exceeded, prune oldest entries that don't overlap with current source directories. Decisions overridden by newer ones on the same `affects` path are removed. |
| `learnings.json` | Max 30 entries. Prune oldest first. Keep entries referenced by active corrections. |
| `graph.json` | No pruning. Entries removed only when corresponding files are deleted from the project. |
| `context.json` history | Max 10 entries. Prune oldest. Entries older than 30 days are deleted. |
| `preferences.json` | Never pruned. Permanent until explicitly changed by the user. |

## Session start

Auto-invoked by the SessionStart hook. Flow:

1. **Check memory files exist** — for all 7 files (preferences, patterns, corrections, context, graph, decisions, learnings). Create with empty defaults if missing.
2. **Merge global + project** — project values override global on conflicts.
3. **Check graph staleness** — if `.buff/memory/.graph-stale` flag exists, run the incremental update algorithm to rebuild `graph.json`, then delete the flag.
4. **Inject payload** — load preferences (full) + recent 10 corrections into context. Max 3,000 tokens total. Do NOT load graph, decisions, patterns, or learnings at start — skills load these on-demand.
5. **Print greeting** — only if `context.json` history has entries:

```
buff · Last session: [summary of most recent history entry]
Plan: [N]% complete · [N] tests passing
```

If no history exists, print nothing — no greeting for new projects.

## Session end

Auto-invoked by the Stop hook. Flow:

1. Read `.buff/session.log` for this session's activity
2. Build session summary (1-2 sentences)
3. Append to `history` array in `context.json`
4. Update `last_active`, `last_active_files`, `plan_progress`
5. Check for corrections captured this session — if any correction's type now has frequency 2+ in `corrections.json`, promote to `patterns.json`
6. Prune all files per pruning rules (see table above)
7. Write updated files

## Live capture

Counterfeit learns from patterns observed during development. Update memory immediately when detected — do not wait for session end.

| Observation | Action |
|---|---|
| User corrects stack detection | Update `stack` in global preferences |
| User prefers different naming | Update `code_style.naming` in preferences |
| User says "don't explain, just code" | Set `communication.verbosity` to `"minimal"` |
| User runs `--yolo` in forge | Note autonomy preference in preferences |
| User consistently uses `--patch` | Flag discipline drift in session log |
| Plan progress milestone reached | Update `plan_progress` in context |
| User corrects buff's code output | Capture in corrections.json + learnings.json |
| User redirects architectural approach | Capture in decisions.json + potentially patterns.json |
| Same correction appears 2+ times | Promote to patterns.json anti_patterns |
| User overrides a previous decision | Update decisions.json, mark old decision as superseded |

## Commands

### `show`

```
/buff:counterfeit show
```

Print current memory (all tiers, merged):

```
## Counterfeit memory

### Global preferences
Stack: bun · typescript · react · elysia
Style: camelCase · named exports · result-pattern errors
Communication: terse · en · code-first

### Patterns (3 architectural, 2 tech, 1 anti-pattern)
Top: repository pattern (3x) · Elysia over Express (3x)
Anti: default exports (from correction)

### Recent corrections (3 of 12 total)
- code: used default export -> named export (TypeScript files)
- plan: suggested monolith -> user wanted modular (API projects)
- test: skipped edge cases -> user wants exhaustive (validators)

### Project context
Plan: 60% complete (Phase 2 of 3 done)
Last session: 2026-03-20 · implemented auth middleware
Decisions: 4 recorded · Learnings: 2 captured
```

### `show --graph`

```
/buff:counterfeit show --graph
```

Print graph summary:

```
## Project graph

Files tracked: 24
Coverage: 78% (19/24 have tests)
Top untested: src/middleware.ts, src/utils/cache.ts, src/config.ts
Last updated: 2026-03-20T14:00:00Z
```

### `show --corrections`

```
/buff:counterfeit show --corrections
```

List recent corrections:

```
## Corrections (12 total, showing recent 10)

1. [2026-03-20] code: default export -> named export (TypeScript files) [generalized]
2. [2026-03-19] plan: monolith -> modular architecture (API projects) [generalized]
3. [2026-03-18] test: basic tests -> exhaustive edge cases (validators) [project-only]
...
```

### `reset`

```
/buff:counterfeit reset --global       # wipe global: preferences, patterns, corrections
/buff:counterfeit reset --project      # wipe project: context, graph, decisions, learnings
/buff:counterfeit reset --graph        # wipe graph.json only
/buff:counterfeit reset --corrections  # wipe corrections.json only
/buff:counterfeit reset                # wipe everything (confirm first)
```

### `prune`

```
/buff:counterfeit prune
```

Manually trigger pruning on all files per the pruning rules table. Report what was removed.

## Initialization

On first use (no memory files exist):

1. Create `~/.buff/memory/` directory
2. Write `preferences.json` with empty template: `{"stack": {}, "code_style": {}, "communication": {}, "git": {}}`
3. Write `patterns.json` with empty template: `{"architecture": [], "tech_decisions": [], "anti_patterns": []}`
4. Write `corrections.json` with empty template: `[]`
5. Create `.buff/memory/` in project root
6. Write `context.json` with empty template: `{"project": {"name": "", "type": "", "stack": {}, "plan_path": ".buff/plan.md", "plan_progress": 0}, "session": {"last_active": "", "last_active_files": [], "recent_decisions": [], "unresolved_todos": []}, "tech": {"test_framework": "", "test_conventions": "", "doc_style": ""}, "history": []}`
7. Write `graph.json` with empty template: `{"files": {}, "updated_at": ""}`
8. Write `decisions.json` with empty template: `[]`
9. Write `learnings.json` with empty template: `[]`
10. Add `.buff/memory/` to project `.gitignore` (project memory is machine-local)
11. Print: "Counterfeit v2 initialized. Intelligence engine active — preferences, patterns, and project graph will build as you work."
