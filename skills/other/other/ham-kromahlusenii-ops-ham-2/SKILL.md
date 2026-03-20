---
name: ham
description: Set up and maintain Hierarchical Agent Memory (HAM) for Codex using scoped local memory files. Trigger on "go ham", "set up HAM", "ham commands", "ham help", "ham route", "ham remove", "ham update", "ham status", "ham benchmark", "ham baseline start", "ham baseline stop", "ham metrics clear", "HAM savings", "HAM stats", "HAM dashboard", "HAM sandwich", "HAM insights", "HAM carbon", or "HAM audit".
---

# HAM

Use this skill to apply the file-based HAM workflow from this repo in Codex. Work through `CLAUDE.md`, scoped `CLAUDE.md` files, `.memory/*`, and `.ham/*`. Do not introduce MCP-based behavior into this skill.

Current HAM skill version: `2026.02.28`

## Pro Guard

Before any HAM command, check for Pro signals:

- `.ham/config.json` with `"pro": true`
- `enabledImporters` with more than `"claude"`
- any `**/AGENTS.md` files

If Pro is detected:

- allow `go ham` in Pro-aware mode
- allow `ham remove` because it has its own removal logic
- for all other HAM commands, print `HAM Pro detected — this project is managed by HAM Pro. Manage at goham.dev` and stop

Never create, modify, or delete `AGENTS.md` files from this skill.

## Commands

### ham commands / ham help

List the supported HAM workflows and what each one does:

- `go ham`: set up HAM and detect project structure
- `ham remove`: remove HAM safely while preserving Pro-owned files
- `ham update`: run `bash <skill-dir>/scripts/update.sh` and update `.ham/version`
- `ham status`: show version, update status, memory file count, and last setup signal
- `ham route`: add or update `## Context Routing` in root `CLAUDE.md`
- `ham dashboard`: launch the dashboard on port 7777
- `HAM savings`: show token and cost savings
- `ham carbon`: run the carbon report
- `ham insights`: generate actionable inbox items from session data
- `ham benchmark`: compare baseline and HAM performance
- `ham baseline start`: begin baseline capture
- `ham baseline stop`: stop baseline capture early
- `ham metrics clear`: clear benchmark data after confirmation
- `ham audit`: check memory system health

### go ham

0. Compare `.ham/version` to `2026.02.28`. If outdated, print an update notice. Never block setup.
1. Detect platform signals:
   - `*.xcodeproj` or `Package.swift`: iOS
   - `build.gradle*`: Android
   - `pubspec.yaml`: Flutter
   - `package.json` with framework hints: Web or React Native
   - `pyproject.toml` or `requirements.txt`: Python
   - `Cargo.toml`: Rust
   - `go.mod`: Go
2. Detect maturity:
   - 0-2 code directories: greenfield
   - 3+ code directories: brownfield
3. For large repos, apply a monorepo guard:
   - if there are more than 20 candidate code directories, present a sorted list
   - pre-select the top 15 most likely directories
   - let the user adjust when needed
   - never create more than 20 scoped `CLAUDE.md` files
4. Generate files silently, then confirm what was created.

Pro-aware mode:

- if Pro is detected, skip directories that already have `CLAUDE.md`
- fill gaps only
- never touch `AGENTS.md`

Generated structure:

```text
project/
├── CLAUDE.md
├── .ham/
│   ├── version
│   └── metrics/state.json
├── .memory/
│   ├── decisions.md
│   ├── patterns.md
│   ├── inbox.md
│   └── audit-log.md
└── [major code dirs]/CLAUDE.md
```

Greenfield: create root files only.
Brownfield: also create scoped `CLAUDE.md` files in major code areas.

Append the HAM block to `.gitignore` if missing:

```text
# HAM - AI agent scaffolding (local, do not commit)
.ham/
.memory/
**/CLAUDE.md
!CLAUDE.md
# end HAM
```

Before creating files, capture `.memory/baseline.json`:

```json
{"captured_at":"YYYY-MM-DD","existing_claude_md":{"found":true,"chars":4820,"tokens":1205},"notes":"Migrated from monolithic CLAUDE.md"}
```

If no existing root `CLAUDE.md` exists:

```json
{"captured_at":"YYYY-MM-DD","existing_claude_md":{"found":false},"estimated_baseline_tokens":7500}
```

Create `.ham/metrics/state.json` with baseline mode enabled:

```json
{"mode":"baseline","tasks_completed":0,"tasks_target":10,"started_at":"ISO-8601","memory_reads":0,"total_prompts":0}
```

The next 10 non-trivial tasks should log to baseline mode without HAM memory loading. Auto-transition to active after 10 completed tasks.

If root `CLAUDE.md` is over 3,000 tokens, warn that it is oversized, list sections that should probably move into scoped `CLAUDE.md` files, and offer migration guidance one section at a time.

### Operating Instructions

Embed these ideas in the generated root `CLAUDE.md`:

- read root `CLAUDE.md` before work
- read the target directory `CLAUDE.md` before changes
- if root `CLAUDE.md` has `## Context Routing`, use it to find the right scoped file
- check `.memory/decisions.md` before architectural changes
- check `.memory/patterns.md` before implementing common functionality
- check if audit is due: if 14 or more days or 10 or more sessions have passed since the last audit in `.memory/audit-log.md`, suggest running one
- create `CLAUDE.md` in new directories when they need distinct guidance
- update relevant memory files after work
- keep uncertain inferences in `.memory/inbox.md`
- never record secrets or user data
- never overwrite historical decisions; mark them superseded

### ham route

1. Find all scoped `CLAUDE.md` files excluding the root file.
2. Build a `## Context Routing` section in root `CLAUDE.md`.
3. Add or update entries without deleting unrelated user-written content.

### ham status

Report:

- installed version from `.ham/version` if present
- whether root HAM files exist
- scoped memory file count
- last setup signal if discoverable
- whether baseline tracking is active
- whether an update appears available

### ham audit

Check:

- root `CLAUDE.md` size
- oversized scoped `CLAUDE.md` files
- missing scoped memory in major code directories
- `.memory/` entry counts
- unreviewed inbox items

Append a short result to `.memory/audit-log.md`.

### HAM savings / HAM stats

Read `.memory/baseline.json`, estimate token load from all `CLAUDE.md` and `.memory/*.md` files, and compare baseline versus current HAM setup. If no baseline exists, show raw counts and tell the user savings percentage requires a real baseline.

Use this calculation model:

```python
root_tokens = count_tokens(read("CLAUDE.md"))
subdir_files = glob("**/CLAUDE.md", exclude="root")
avg_subdir = sum(count_tokens(read(f)) for f in subdir_files) / len(subdir_files) if subdir_files else 0

memory_tokens = sum(count_tokens(read(f)) for f in glob(".memory/*.md"))
state = read_json(".ham/metrics/state.json")
memory_weight = state["memory_reads"] / state["total_prompts"] if state.get("total_prompts", 0) >= 10 else 0.30
ham_tokens = root_tokens + avg_subdir + (memory_tokens * memory_weight)

if exists(".memory/baseline.json"):
    baseline_mid = baseline_data["old_claude_md_tokens"] + max(500, len(subdir_files) * 300)
    baseline_is_measured = True
else:
    code_dirs = count_dirs_with_code()
    baseline_mid = max(1000, ham_tokens * 1.5) if code_dirs <= 2 else max(3000, ham_tokens * 2.5) if code_dirs <= 10 else max(5000, ham_tokens * 3.5)
    baseline_is_measured = False
```

Display rules:

- if baseline is estimated, show raw token counts only
- do not show savings percentage or monthly projections without a real baseline
- label `.memory/` weighting as estimated until at least 10 prompts are tracked

### ham baseline start / ham baseline stop

- `start`: write `.ham/metrics/state.json` with `mode: "baseline"`
- `stop`: set `mode: "active"` and report captured tasks

## Task Metrics Logging

Each non-trivial task should log two JSONL entries to `.ham/metrics/tasks.jsonl`, or `baseline.jsonl` while baseline mode is active:

```json
{"id":"task-<hex8>","type":"task_start","timestamp":"ISO-8601","description":"...","ham_active":true,"model":"codex","files_read":0,"memory_files_loaded":0,"estimated_tokens":0}
{"id":"task-<hex8>","type":"task_end","timestamp":"ISO-8601","status":"completed"}
```

Skip trivial queries such as HAM commands, yes or no answers, and clarifications.

Baseline mode rules:

1. If `mode = "baseline"`, write to `baseline.jsonl`, set `ham_active: false`, skip scoped `CLAUDE.md` and `.memory/` reads, and increment `tasks_completed` only for completed tasks.
2. If `mode = "active"`, or the state file is missing or unparseable, write to `tasks.jsonl`, set `ham_active: true`, and use HAM memory normally.
3. If the state file is corrupt, warn once and treat the repo as active mode.

### ham benchmark

Run `node <skill-dir>/dashboard/benchmark-cli.js [--days 30] [--model name] [--json]`.

### ham dashboard / HAM sandwich

Run `node <skill-dir>/dashboard/launch.js --port 7777` from the project root and tell the user to open `http://localhost:7777`.

### ham carbon

Run `node <skill-dir>/dashboard/carbon-cli.js [--last] [--days 30]`.

### ham insights

Run `node <skill-dir>/dashboard/insights-cli.js --days 30`, extract actionable items, deduplicate against `.memory/inbox.md`, append new items, and log the audit event.

### ham update

Run `bash <skill-dir>/scripts/update.sh`, then update `.ham/version`.

### ham metrics clear

Require confirmation before deleting benchmark data.

### ham remove

1. Detect Pro state.
2. Inventory HAM-owned versus Pro-owned files.
3. Show a dry run.
4. Confirm with the user.
5. Remove only HAM-owned files and sections:
   - `.memory/*`
   - `.ham/*` except Pro-owned config
   - scoped `CLAUDE.md` files created by HAM
   - HAM sections from root `CLAUDE.md`
   - HAM block from `.gitignore`
6. Preserve user content and Pro files.

## Templates

See [references/templates.md](references/templates.md) for starter file shapes and [references/platforms.md](references/platforms.md) for platform-specific source roots and brownfield analysis cues.

## Writing Rules

- Write memory into the narrowest scope that will still be useful.
- Keep root `CLAUDE.md` short and global.
- Use scoped `CLAUDE.md` files for purpose, conventions, integrations, patterns, and gotchas that only apply in one subtree.
- Never overwrite existing memory blindly; read first and merge carefully.
- Never store secrets, API keys, tokens, or user data.
- Never promote uncertain findings from `.memory/inbox.md` into canonical memory without user confirmation.

## Session Discipline

- For non-trivial work, read memory before coding and write back durable learnings after coding.
- Skip memory churn for trivial one-shot asks.
- Record accepted architecture changes in `.memory/decisions.md`.
- Record reusable implementation rules in `.memory/patterns.md`.
- Keep speculation, cleanup ideas, and uncertain inferences in `.memory/inbox.md`.

Read [references/setup-and-scopes.md](references/setup-and-scopes.md) when deciding where scoped `CLAUDE.md` files belong.
