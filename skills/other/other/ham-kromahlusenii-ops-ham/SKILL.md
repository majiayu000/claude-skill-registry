---
name: ham
ham_version: "2026.02.28"
description: Set up Hierarchical Agent Memory (HAM) — scoped CLAUDE.md files per directory that reduce token spend. Trigger on "go ham", "set up HAM", "ham commands", "ham help", "ham route", "ham remove", "ham update", "ham status", "ham benchmark", "ham baseline start", "ham baseline stop", "ham metrics clear", "HAM savings", "HAM stats", "HAM dashboard", "HAM sandwich", "HAM insights", or "HAM carbon".
---

## Pro Guard — run FIRST

Before ANY command, check for Pro signals: `.ham/config.json` with `"pro": true`, `enabledImporters` with more than `"claude"`, or any `**/AGENTS.md` files.

- **If Pro detected:** allow `go ham` (Pro-aware mode) and `ham remove` (has own Pro logic). All other commands → print `HAM Pro detected — this project is managed by HAM Pro. Manage at goham.dev` and STOP.
- **Pro rules:** NEVER create/modify/delete AGENTS.md files. CLAUDE.md = HAM-owned. AGENTS.md = Pro-owned.

## Commands

**Trigger:** "ham commands" or "ham help" — list all commands:

| Command | What it does |
|---|---|
| `go ham` | Set up HAM (auto-detects stack and structure) |
| `ham remove` | Remove HAM safely (preserves Pro files) |
| `ham update` | Run `bash <skill-dir>/scripts/update.sh`, update `.ham/version` |
| `ham status` | Show version, update status, memory file count, last setup date |
| `ham route` | Add/update Context Routing in root CLAUDE.md |
| `ham dashboard` | Launch web dashboard at :7777 via `node <skill-dir>/dashboard/launch.js --port 7777` |
| `ham savings` | Show token and cost savings report |
| `ham carbon` | Run `node <skill-dir>/dashboard/carbon-cli.js [--last] [--days 30]` |
| `ham insights` | Generate insights → write actionable items to `.memory/inbox.md` |
| `ham benchmark` | Run `node <skill-dir>/dashboard/benchmark-cli.js [--days 30] [--model name] [--json]` |
| `ham baseline start` | Begin 10-task baseline capture |
| `ham baseline stop` | End baseline early, keep partial data |
| `ham metrics clear` | Delete all benchmark data (confirm first) |
| `ham audit` | Check memory system health |

## go ham — Setup

0. **Update check** — compare `.ham/version` against `ham_version` in frontmatter. If outdated, print update notice. Never block.
1. **Detect platform** — scan for: `*.xcodeproj`/`Package.swift` (iOS), `build.gradle*` (Android), `pubspec.yaml` (Flutter), `package.json` + framework (Web/RN), `pyproject.toml`/`requirements.txt` (Python), `Cargo.toml` (Rust), `go.mod` (Go).
2. **Detect maturity** — count subdirs with code: 0-2 = greenfield, 3+ = brownfield.
3. **Monorepo guard** — if >20 code dirs: present sorted list, pre-select top 15, let user adjust. Hard cap: never create >20 subdirectory CLAUDE.md files.
4. **Generate files** silently, then confirm.

**Pro-aware mode:** if Pro detected, skip directories with existing CLAUDE.md (Pro-created). Fill gaps only. Never touch AGENTS.md.

### Generated Structure

```
project/
├── CLAUDE.md              # Root (~200 tokens)
├── .ham/
│   ├── version
│   └── metrics/state.json # {mode, tasks_completed, tasks_target, started_at, memory_reads, total_prompts}
├── .memory/
│   ├── decisions.md       # ADRs
│   ├── patterns.md        # Reusable patterns
│   ├── inbox.md           # Inferred items (brownfield only)
│   └── audit-log.md       # Audit history (last 5 entries)
└── [src dirs]/CLAUDE.md   # Per-directory (brownfield only)
```

Greenfield: root + .memory/ + .ham/ only. Brownfield: also subdirectory CLAUDE.md files.

### .gitignore

Append (idempotent — check for `# HAM` marker first):
```
# HAM — AI agent scaffolding (local, do not commit)
.ham/
.memory/
**/CLAUDE.md
!CLAUDE.md
# end HAM
```

### Capture Baseline

Before creating files, save `.memory/baseline.json`:
```json
{"captured_at":"YYYY-MM-DD","existing_claude_md":{"found":true,"chars":4820,"tokens":1205},"notes":"Migrated from monolithic CLAUDE.md"}
```
If no existing CLAUDE.md: `{"captured_at":"...","existing_claude_md":{"found":false},"estimated_baseline_tokens":7500}`.

### Initialize Benchmarking

Create `.ham/metrics/state.json`: `{"mode":"baseline","tasks_completed":0,"tasks_target":10,"started_at":"ISO-8601","memory_reads":0,"total_prompts":0}`. Next 10 tasks log to `baseline.jsonl` without HAM memory loading. Auto-transitions to active after 10.

### Confirm Setup

Report files created. If root CLAUDE.md >3,000 tokens: warn, list sections that may belong in subdirectory files, offer interactive migration (present each candidate one at a time, move only on user confirmation).

## Operating Instructions

Embed in every root CLAUDE.md:

```markdown
## Agent Memory System

### Before Working
- Read this file for global context, then read the target directory's CLAUDE.md before changes
- If this file has a ## Context Routing section, use it to find the right subdirectory CLAUDE.md
- Check .memory/decisions.md before architectural changes
- Check .memory/patterns.md before implementing common functionality
- Check if audit is due: if 14+ days or 10+ sessions since last audit in .memory/audit-log.md, suggest running one

### During Work
- Create CLAUDE.md in any new directory you create

### After Work
- Update relevant CLAUDE.md if conventions changed
- Log decisions to .memory/decisions.md (ADR format)
- Log patterns to .memory/patterns.md
- Uncertain inferences → .memory/inbox.md (never canonical files)

### Safety
- Never record secrets, API keys, or user data
- Never overwrite decisions — mark as [superseded]
- Never promote from inbox without user confirmation
```

## Task Metrics Logging

Each non-trivial task logs two JSONL entries to `.ham/metrics/tasks.jsonl` (or `baseline.jsonl` in baseline mode):

```json
{"id":"task-<hex8>","type":"task_start","timestamp":"ISO-8601","description":"...","ham_active":true,"model":"claude-opus-4-6","files_read":0,"memory_files_loaded":0,"estimated_tokens":0}
{"id":"task-<hex8>","type":"task_end","timestamp":"ISO-8601","status":"completed"}
```

Skip trivial queries (HAM commands, yes/no, clarifications). Increment `total_prompts` in state.json for every non-trivial task; increment `memory_reads` when `.memory/` files are loaded.

### Baseline Mode

Check `.ham/metrics/state.json` before each task:

1. **mode = "baseline":** write to `baseline.jsonl`, set `ham_active: false`, skip subdir CLAUDE.md and .memory/ files. Only increment `tasks_completed` for `status: "completed"` (not "error"/"skipped"). Transition to active when `tasks_completed >= tasks_target`.

2. **mode = "active", or state.json missing, or state.json unparseable:** write to `tasks.jsonl`, set `ham_active: true`, load all files normally. If state.json was corrupt, warn user once: `⚠ .ham/metrics/state.json is corrupted. Treating as active mode.`

## ham savings

**Trigger:** "HAM savings" or "HAM stats"

Read `.memory/baseline.json`, count tokens in all CLAUDE.md and .memory/ files (chars ÷ 4), then display: baseline section, current HAM setup, tokens per prompt, savings, and monthly projection (1,500 prompts at $3/M Sonnet, $15/M Opus).

### Calculation

```python
root_tokens = count_tokens(read("CLAUDE.md"))
subdir_files = glob("**/CLAUDE.md", exclude="root")
avg_subdir = sum(count_tokens(read(f)) for f in subdir_files) / len(subdir_files) if subdir_files else 0

# .memory/ weighted by tracked read frequency
memory_tokens = sum(count_tokens(read(f)) for f in glob(".memory/*.md"))
state = read_json(".ham/metrics/state.json")
memory_weight = state["memory_reads"] / state["total_prompts"] if state.get("total_prompts", 0) >= 10 else 0.30
ham_tokens = root_tokens + avg_subdir + (memory_tokens * memory_weight)

# Baseline: measured if baseline.json exists, tiered estimate otherwise
if exists(".memory/baseline.json"):
    baseline_mid = baseline_data["old_claude_md_tokens"] + max(500, len(subdir_files) * 300)
    baseline_is_measured = True
else:
    code_dirs = count_dirs_with_code()
    baseline_mid = max(1000, ham_tokens * 1.5) if code_dirs <= 2 else max(3000, ham_tokens * 2.5) if code_dirs <= 10 else max(5000, ham_tokens * 3.5)
    baseline_is_measured = False
```

**Display rules:** when `baseline_is_measured = False`, show raw token counts only — no savings percentage or cost projections. Add: `⚠ No baseline captured — savings % requires a real baseline. Run "go ham" to capture one.` Show "(estimated)" next to .memory/ frequency until 10+ prompts tracked.

## ham remove

**Trigger:** "ham remove" — EXEMPT from Pro guard.

1. Detect Pro (same checks as guard)
2. Inventory: skill-owned (.memory/\*, .ham/\*, subdir CLAUDE.md, HAM sections in root) vs Pro-owned (.ham/config.json, AGENTS.md) vs user files (root CLAUDE.md content)
3. Show dry-run listing what will be deleted/edited/kept
4. Confirm with user
5. Execute: delete skill files, strip `## Agent Memory System` and `## Context Routing` from root CLAUDE.md, remove HAM block from .gitignore
6. Report results

## ham route

**Trigger:** "ham route"

1. Find all `**/CLAUDE.md` (excluding root)
2. Build entries: `→ [label]: [path]` (label = directory name)
3. Append or update `## Context Routing` in root CLAUDE.md. Never remove existing entries.

## ham dashboard

**Trigger:** "HAM dashboard" or "HAM sandwich"

Check for updates, then run `node <skill-dir>/dashboard/launch.js --port 7777` from the project root. Dashboard reads session JSONL from `~/.claude/projects/` — no database. Tell user to open http://localhost:7777.

## ham insights

**Trigger:** "HAM insights"

Run `node <skill-dir>/dashboard/insights-cli.js --days 30`. Parse JSON output, filter to actionable items, deduplicate against existing `.memory/inbox.md`, write new items in format:
```markdown
### Insight: [title] ([date])
**Confidence:** [severity] | **Observed:** [detail] | **Proposed Action:** [action]
```
Log to `.memory/audit-log.md` (keep last 5 entries). Report summary to user.

## ham audit

**Trigger:** "HAM audit" or "HAM health"

Check: root CLAUDE.md size (recommend <60 lines, <250 tokens), subdirectory file count and oversized files (>75 lines), missing CLAUDE.md in code dirs, .memory/ entry counts, unreviewed inbox items. Present results, append to `.memory/audit-log.md`.

## ham baseline start / stop

**start:** Create `.ham/metrics/state.json` with `mode: "baseline"`, `tasks_target: 10`. Tell user next 10 tasks capture baseline.

**stop:** Set `mode: "active"` in state.json. Report tasks captured.

## Templates

See `templates.md` for full templates. Summary:

- **Root CLAUDE.md:** Project name, Stack, Rules, Agent Memory System (operating instructions above)
- **Subdirectory CLAUDE.md:** Purpose (1 sentence), Conventions, Patterns
- **decisions.md:** ADR format (status, decision, context, alternatives)
- **inbox.md:** Header + review instructions
