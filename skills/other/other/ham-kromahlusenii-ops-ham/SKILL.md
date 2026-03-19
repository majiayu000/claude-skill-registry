---
name: ham
ham_version: "2026.02.28"
description: Set up Hierarchical Agent Memory (HAM) — scoped CLAUDE.md files per directory that reduce token spend. Trigger on "go ham", "set up HAM", "ham commands", "ham help", "ham route", "ham remove", "ham update", "ham status", "ham benchmark", "ham baseline start", "ham baseline stop", "ham metrics clear", "HAM savings", "HAM stats", "HAM dashboard", "HAM sandwich", "HAM insights", or "HAM carbon".
---

## ⛔ HAM Pro Guard — run FIRST, before any command

Before executing ANY HAM command, check for HAM Pro signals in the project:

1. Check if `.ham/config.json` exists and contains `"pro": true`
2. Check if `.ham/config.json` exists and `enabledImporters` contains more than just `"claude"`
3. Check if any `AGENTS.md` files exist anywhere in the project (`**/AGENTS.md`)

**If ANY of these conditions are true:**

- If the command is **`go ham`**: allow it to proceed, but in **Pro-aware mode** (see Quick Start § Pro-Aware Mode below). Do NOT overwrite Pro-created files.
- If the command is **`ham remove`**: allow it to proceed — it has its own Pro-aware logic that preserves Pro-owned files (see HAM Remove Command below).
- For **all other commands**: print the following message and **STOP — do not execute the command**:

```
HAM Pro detected — this project is managed by HAM Pro.
The HAM skill is disabled to avoid conflicts.
Manage this project at goham.dev
```

Do not create, modify, or delete any files. Do not run any setup, analytics, benchmarking, or maintenance logic. Return immediately after printing the message.

**If none of these conditions are true**, proceed with the command as normal below.

---

# HAM (Hierarchical Agent Memory)

Scoped memory system that reduces context token spend per request.

## HAM Pro Compatibility

HAM Pro is a separate product that extends HAM with multi-agent support. When Pro is active in a project, it creates **AGENTS.md** files alongside CLAUDE.md files. These are context files for non-Claude agents (Cursor, Copilot, Windsurf, Gemini, etc.).

**Ownership boundary:**

| File | Owner | Managed by |
|------|-------|------------|
| `CLAUDE.md` | HAM skill | This skill — create, update, route |
| `AGENTS.md` | HAM Pro | Pro dashboard only — never touch |

**Rules:**
- NEVER create AGENTS.md files — Pro creates them via its dashboard
- NEVER modify AGENTS.md files — Pro controls their content and sync
- NEVER delete AGENTS.md files — they may be actively consumed by other agents
- If you encounter AGENTS.md files during scanning (e.g. `ham route`, `ham audit`), acknowledge their existence but do not include them in any write operations

## HAM Commands

**Trigger:** "ham commands" or "ham help"

When user runs this command, display all available HAM commands:

```
┌─────────────────────────────────────────────────────────────┐
│  HAM Commands                                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SETUP                                                       │
│  go ham              Set up HAM in your project              │
│  ham remove          Remove HAM from your project (safe)     │
│  ham update          Update HAM to the latest version        │
│  ham status          Show HAM version and setup status       │
│  ham route           Add/update Context Routing in CLAUDE.md │
│                                                              │
│  ANALYTICS                                                   │
│  ham dashboard       Launch the web dashboard (:7777)        │
│  ham savings         Show token and cost savings report      │
│  ham carbon          Show energy and CO2e efficiency         │
│  ham insights        Generate insights → write to inbox      │
│                                                              │
│  BENCHMARKING                                                │
│  ham benchmark       Compare baseline vs HAM performance     │
│  ham baseline start  Begin 10-task baseline capture          │
│  ham baseline stop   End baseline early, keep partial data   │
│  ham metrics clear   Delete all benchmark data               │
│                                                              │
│  MAINTENANCE                                                 │
│  ham audit           Check memory system health              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

**Trigger:** "go ham"

When user says "go ham":

0. **Check for updates** — compare local `.ham/version` (if it exists) against the `ham_version` field in this skill's YAML frontmatter. If outdated, print one line: `HAM update available (v2026.02.28). Run "ham update" to get the latest.` Never block the command — continue immediately.
1. **Auto-detect everything** — scan for platform signals and project maturity silently
2. **Generate files** — create the memory structure without asking questions
3. **Confirm setup** — list files created, tell user to run `HAM savings` to see impact

Only ask questions if detection fails.

### Pro-Aware Mode

When `go ham` runs and the Pro guard (above) detected Pro signals, run in **Pro-aware mode** instead of the normal flow:

1. **Read the Pro manifest** — load `.ham/config.json` and collect the list of directories Pro has already scaffolded. Look for a `scaffolded` or `files` array, or scan for existing CLAUDE.md files that contain a `<!-- managed by HAM Pro -->` comment or any Pro-identifying marker.

2. **Inventory existing files** — glob for all `**/CLAUDE.md` and `**/AGENTS.md` in the project. Build two sets:
   - `pro_covered`: directories that already have a CLAUDE.md (created by Pro)
   - `agents_files`: all AGENTS.md paths (never touch these)

3. **Skip Pro-covered directories** — for every directory where Pro already created a CLAUDE.md, **do not create or overwrite** that file. Leave it exactly as Pro set it up.

4. **Fill gaps only** — if the skill's normal detection (platform + maturity) would create CLAUDE.md files in directories that Pro has NOT covered, create them as usual. These are directories Pro didn't scaffold.

5. **Never touch AGENTS.md** — do not create, modify, or delete any AGENTS.md file, regardless of context.

6. **Print summary** — after setup, print:

```
HAM Pro detected — running in Pro-aware mode.
Skipped X directories already scaffolded by HAM Pro.
Created Y new CLAUDE.md files in uncovered directories.
AGENTS.md files left untouched.
```

If Pro covered everything and there are no gaps, print:

```
HAM Pro detected — all directories already scaffolded.
No changes made. Use the HAM Pro dashboard to manage this project.
```

## Onboarding Flow

### Step 1: Silent Detection

Scan the project root for platform signals:

| Files Found | Platform |
|---|---|
| `*.xcodeproj`, `Package.swift` | iOS |
| `build.gradle*`, `settings.gradle` | Android |
| `pubspec.yaml` | Flutter |
| `package.json` + `react-native` | React Native |
| `package.json` + `next/nuxt/svelte` | Web |
| `pyproject.toml`, `requirements.txt` | Python |
| `Cargo.toml` | Rust |
| `go.mod` | Go |

Detect maturity by counting subdirectories with code:
- 0-2 dirs → **Greenfield/Early** (scaffold mode)
- 3+ dirs → **Brownfield** (analysis mode)

**Monorepo guard:** If brownfield mode detects more than 20 subdirectories with code:
1. Present the full list of directories to the user, sorted by likely importance
   (prefer src/, lib/, app/, packages/ children; directories with most source files)
2. Pre-select the top 15 as a default, but let the user adjust:
   ```
   ⚠ Large project — [N] code directories found.
   Suggested top 15 for CLAUDE.md scaffolding:
     [✓] src/api/
     [✓] src/components/
     [✓] src/lib/
     ...
   Skipped:
     [ ] scripts/migrations/
     [ ] vendor/
     ...
   Proceed with these 15, or tell me which to add/remove.
   ```
3. If the user confirms, create CLAUDE.md in selected directories only.
4. Hard cap: never create more than 20 subdirectory CLAUDE.md files in a single setup.

### Step 2: Generate Structure

Create files based on detection:

```
project/
├── CLAUDE.md              # Root context (~200 tokens)
├── .ham/
│   ├── version            # Current HAM version (written from ham_version in SKILL.md)
│   └── metrics/
│       └── state.json     # Benchmark state (baseline/active mode)
├── .memory/
│   ├── decisions.md       # Empty, ready for ADRs
│   ├── patterns.md        # Empty, ready for patterns
│   ├── inbox.md           # Inferred items (brownfield only)
│   └── audit-log.md       # Audit history (auto-maintained)
└── [src dirs]/
    └── CLAUDE.md          # Per-directory context (brownfield only)
```

Also create `.ham/version` containing the `ham_version` value from this skill's frontmatter (e.g., `2026.02.28`). This file is used for startup update checks.

For greenfield: only create root + .memory/ + .ham/
For brownfield: also create subdirectory CLAUDE.md files.

### Step 3: Add HAM to .gitignore

After generating the file structure, ensure HAM files won't be accidentally committed:

1. **Check for existing block** — read `.gitignore` (if it exists) and look for the `# HAM` marker. If found, skip this step (idempotent).
2. **Append the block** — if no marker found, append the following to `.gitignore` (create the file if it doesn't exist):

```
# HAM — AI agent scaffolding (local, do not commit)
.ham/
.memory/
**/CLAUDE.md
!CLAUDE.md
# end HAM
```

The `**/CLAUDE.md` pattern ignores all CLAUDE.md files in subdirectories. The `!CLAUDE.md` negation keeps the root CLAUDE.md trackable if the user chooses to remove it from .gitignore — but by default everything is ignored.

3. **Never overwrite** — always append to the end of the file. Never modify existing .gitignore content.

### Step 4: Capture Baseline

Before creating any files, measure what exists:

```python
# Capture baseline for savings comparison
baseline = {
    "captured_at": "YYYY-MM-DD",
    "existing_claude_md": {
        "found": true/false,
        "path": "CLAUDE.md",
        "chars": 1234,
        "tokens": 308  # chars ÷ 4
    },
    "existing_context_files": [
        # Any other .md files that were serving as context
    ],
    "total_baseline_tokens": 308
}
```

Save this to `.memory/baseline.json`:

```json
{
  "captured_at": "2026-02-23",
  "existing_claude_md": {
    "found": true,
    "chars": 4820,
    "tokens": 1205
  },
  "notes": "Migrated from monolithic CLAUDE.md"
}
```

If no existing CLAUDE.md, use estimated baseline:

```json
{
  "captured_at": "2026-02-23",
  "existing_claude_md": {
    "found": false
  },
  "estimated_baseline_tokens": 7500,
  "notes": "No existing memory system. Using estimated baseline for agent re-orientation costs."
}
```

### Step 4b: Initialize Benchmarking

Create `.ham/metrics/state.json` with baseline mode:

```json
{
  "mode": "baseline",
  "tasks_completed": 0,
  "tasks_target": 10,
  "started_at": "YYYY-MM-DDTHH:mm:ssZ",
  "memory_reads": 0,
  "total_prompts": 0
}
```

The agent increments `total_prompts` for every non-trivial task and `memory_reads` when `.memory/` files are loaded. These counters are used by the savings formula to weight `.memory/` token costs by real frequency.

This puts the agent in baseline mode: the next 10 tasks will be logged to `.ham/metrics/baseline.jsonl` and the agent will skip subdirectory CLAUDE.md and `.memory/` files during baseline (still reads root CLAUDE.md). After 10 tasks, auto-transitions to active mode.

### Step 5: Confirm Setup

After creating files, measure root CLAUDE.md token count (chars ÷ 4). Then output:

**If root CLAUDE.md ≤ 3,000 tokens:**

```
HAM v2026.02.28 setup complete. Created [N] files.
Added HAM files to .gitignore — these won't be committed.
Baseline captured in .memory/baseline.json
Benchmarking initialized — next 10 tasks capture baseline.

Run "HAM savings" to see your token and cost savings.
Run "ham benchmark" after the baseline to see performance comparison.
```

**If root CLAUDE.md > 3,000 tokens:**

```
HAM v2026.02.28 setup complete. Created [N] files.
Added HAM files to .gitignore — these won't be committed.
Baseline captured in .memory/baseline.json
Benchmarking initialized — next 10 tasks capture baseline.

⚠ Your root CLAUDE.md is [X] tokens — HAM works best when it's under 250.

HAM created scoped CLAUDE.md files in your subdirectories, but your root file
still has all your context in one place. To get the full savings, move
directory-specific rules into the matching subdirectory CLAUDE.md files and
keep only global context (stack, project-wide rules) in root.

Here's what I found that may belong in subdirectory files:
[List sections/content in root CLAUDE.md that reference specific directories
 that have a subdirectory CLAUDE.md. For each, show:]
  → "[section/topic]" may belong in [dir]/CLAUDE.md

Want me to help move these? I'll show you each one and you decide where it goes.
```

#### Interactive migration (if user accepts)

If the user says yes to the migration offer:

1. **Identify candidates** — scan root CLAUDE.md for content that references specific subdirectories (e.g., mentions "api", "components", "db" that match actual project directories with CLAUDE.md files). Also identify content blocks that are clearly directory-scoped (API patterns, component conventions, DB schemas, etc.).

2. **Present each candidate** — show the user one section at a time:
   ```
   This section appears to be about [topic]:
   ---
   [quoted content]
   ---
   Move to [dir]/CLAUDE.md? (yes / no / somewhere else)
   ```

3. **Wait for the user's decision on each one** — never move content without explicit confirmation. If the user says "somewhere else", ask which directory.

4. **Move confirmed content** — append the content to the target subdirectory CLAUDE.md and remove it from root CLAUDE.md.

5. **Report results:**
   ```
   Migrated [N] sections from root CLAUDE.md.
   Root CLAUDE.md is now [X] tokens (was [Y]).
   ```

If the user declines the migration, proceed normally — the setup is still complete and functional, just not optimally scoped.

## HAM Savings Command

**Trigger:** "HAM savings" or "HAM stats"

When user runs this command:

1. **Read baseline** — load `.memory/baseline.json` for before comparison
2. **Count actual files** — find all CLAUDE.md files and .memory/ files in the project
3. **Measure actual token counts** — count tokens in each file (use ~4 chars = 1 token as estimate)
4. **Calculate and display** with full transparency:

```
┌─────────────────────────────────────────────────────────┐
│  HAM Savings Report                                     │
├─────────────────────────────────────────────────────────┤
│  BASELINE (from .memory/baseline.json)                  │
│  ─────────────────────────────────────────────────────  │
│  Captured: [date]                                       │
│  Old CLAUDE.md: [X] tokens ([found/not found])         │
│  Estimated re-orientation: ~[Y] tokens/prompt           │
│  Total baseline: [Z] tokens/prompt                      │
│                                                         │
│  YOUR CURRENT HAM SETUP                                 │
│  ─────────────────────────────────────────────────────  │
│  Root CLAUDE.md:        [X] tokens ([Y] chars ÷ 4)     │
│  Subdirectory files:    [N] files, [Z] tokens total    │
│  .memory/ files:        [M] files (loaded on demand)   │
│                                                         │
│  TOKENS LOADED PER PROMPT                               │
│  ─────────────────────────────────────────────────────  │
│  Typical prompt:        [A] tokens                      │
│    └─ Root CLAUDE.md:   [X] tokens (always)            │
│    └─ 1 subdir file:    ~[B] tokens (when in subdir)   │
│    └─ .memory/ files:   ~[C] tokens ([X]% of prompts)  │
│                                                         │
│  YOUR ACTUAL SAVINGS                                    │
│  ─────────────────────────────────────────────────────  │
│  Before HAM:            [baseline] tokens/prompt        │
│  After HAM:             [A] tokens/prompt               │
│  Savings per prompt:    [diff] tokens ([pct]%)          │
│                                                         │
│  MONTHLY PROJECTION (50 prompts/day × 30 days)         │
│  ─────────────────────────────────────────────────────  │
│  Prompts/month:         1,500                           │
│  Tokens saved:          ~[monthly_tokens]               │
│  Cost saved (Sonnet):   ~$[sonnet] (@$3/M input tokens)│
│  Cost saved (Opus):     ~$[opus] (@$15/M input tokens) │
└─────────────────────────────────────────────────────────┘

Want multi-agent savings? HAM Pro tracks Cursor, Copilot, Windsurf & more → goham.dev
```

**Display rules based on baseline source:**

When `baseline_is_measured = False` (no baseline.json):
- Show raw token counts only (before: ~X tokens, after: ~Y tokens)
- Do NOT show savings percentage or monthly cost projections
- Replace the YOUR ACTUAL SAVINGS and MONTHLY PROJECTION sections with:

```
│  ⚠ No baseline captured — showing raw token counts only.    │
│    Savings percentage requires a real baseline.              │
│    Run "go ham" to capture one, or create baseline.json.     │
```

When `baseline_is_measured = True`: show the full savings report with percentage and projections as above.

**Note on .memory/ frequency display:** Show "(estimated)" next to the .memory/ prompt percentage until 10+ prompts are tracked in state.json, then show the real number.

If `.memory/baseline.json` doesn't exist (skill wasn't used for setup), also show:

```
NOTE: No baseline captured. Run "go ham" to set up with baseline tracking,
or create .memory/baseline.json manually with your old CLAUDE.md token count.
```

### Calculation Logic

```python
# Token estimation
def count_tokens(text):
    return len(text) // 4  # ~4 characters per token

# Measure actual HAM files
root_tokens = count_tokens(read("CLAUDE.md"))
subdir_files = glob("**/CLAUDE.md", exclude="root")
subdir_tokens = sum(count_tokens(read(f)) for f in subdir_files)
avg_subdir = subdir_tokens / len(subdir_files) if subdir_files else 0

# .memory/ files (weighted by actual read frequency)
memory_files = glob(".memory/*.md")
memory_tokens = sum(count_tokens(read(f)) for f in memory_files)

# Use tracked frequency if available, otherwise conservative default
state = read_json(".ham/metrics/state.json")
if state.get("total_prompts", 0) >= 10:
    memory_weight = state["memory_reads"] / state["total_prompts"]
else:
    memory_weight = 0.30  # initial estimate, converges within ~1 week

weighted_memory = memory_tokens * memory_weight

# Tokens per typical prompt (root + 1 subdir + weighted .memory/)
ham_tokens = root_tokens + avg_subdir + weighted_memory

# Baseline: use measured data when available, tiered estimate otherwise
if exists(".memory/baseline.json"):
    baseline_data = read_json(".memory/baseline.json")
    old_tokens = baseline_data.get("old_claude_md_tokens", 0)
    reorientation = max(500, len(subdir_files) * 300)
    baseline_mid = old_tokens + reorientation
    baseline_is_measured = True
else:
    code_dirs = count_dirs_with_code()  # same logic as Step 1 maturity detection
    if code_dirs <= 2:
        baseline_mid = max(1000, ham_tokens * 1.5)
    elif code_dirs <= 10:
        baseline_mid = max(3000, ham_tokens * 2.5)
    else:
        baseline_mid = max(5000, ham_tokens * 3.5)
    baseline_is_measured = False

# Savings
savings_tokens = baseline_mid - ham_tokens
savings_pct = (savings_tokens / baseline_mid) * 100  # only shown when baseline_is_measured

# Monthly (50 prompts/day × 30 days) — only shown when baseline_is_measured
monthly_prompts = 1500
monthly_tokens_saved = savings_tokens * monthly_prompts
cost_sonnet = (monthly_tokens_saved / 1_000_000) * 3  # $3/M
cost_opus = (monthly_tokens_saved / 1_000_000) * 15   # $15/M
```

## HAM Update Command

**Trigger:** "ham update"

When user runs this command:

1. **Run the update script** — execute:

```bash
bash <path-to-ham-repo>/scripts/update.sh
```

Where `<path-to-ham-repo>` is this skill's installation directory (e.g., `~/.claude/skills/ham`).

2. **Show result** — the script reports whether HAM was already up to date or shows the before/after commit hashes.

3. **Update local version** — after a successful update, read the new `ham_version` from this skill's YAML frontmatter and write it to the project's `.ham/version` file.

4. **Reassure the user** — confirm that user data (`.memory/`, CLAUDE.md files, `.ham/`) is untouched by the update. Only HAM skill files are updated.

## HAM Status Command

**Trigger:** "ham status"

When user runs this command, show a quick status overview:

```
┌─────────────────────────────────────────────┐
│  HAM Status                                  │
├─────────────────────────────────────────────┤
│  Version:      v[ham_version from SKILL.md] │
│  Update:       [up to date | available]     │
│  Memory files: [N] files in .memory/        │
│  Last setup:   [date from baseline.json]    │
│  Model:        [detected model or unknown]  │
└─────────────────────────────────────────────┘
```

How to gather each field:
- **Version**: read `ham_version` from this skill's YAML frontmatter
- **Update**: compare local `.ham/version` against `ham_version`. If they match, "up to date". If different or `.ham/version` missing, "available — run `ham update`"
- **Memory files**: count files in `.memory/` directory
- **Last setup**: read `captured_at` from `.memory/baseline.json` (show "not set up" if missing)
- **Model**: detect from recent session data or environment (show "unknown" if unavailable)

## System Architecture

Three layers:

**Layer 1 — Root CLAUDE.md** (~200 tokens)
Stack, rules, operating instructions. No implementation details.

**Layer 2 — Subdirectory CLAUDE.md** (~250 tokens each)
Scoped context per directory. Agent reads root + target directory only.

**Layer 3 — .memory/** (on-demand)
- `decisions.md` — Confirmed Architecture Decision Records
- `patterns.md` — Confirmed reusable patterns
- `inbox.md` — Inferred items awaiting confirmation
- `audit-log.md` — Audit history (auto-maintained, last 5 entries)

## Operating Instructions

Embed in every root CLAUDE.md:

```markdown
## Agent Memory System

### Before Working
- Read this file for global context, then read the target directory's CLAUDE.md before changes
- If this file has a ## Context Routing section, use it to find the right subdirectory CLAUDE.md for your target directory
- Check .memory/decisions.md before architectural changes
- Check .memory/patterns.md before implementing common functionality
- Check if a memory audit is due: read `.memory/audit-log.md` for the last audit date. If 14+ days have passed OR 10+ session files in `.memory/sessions/` are dated after the last audit, suggest: "It's been [N days/sessions] since the last memory audit. Run one? (say 'HAM audit' or skip)". Do not repeat if already suggested this session. If `audit-log.md` is missing, treat as never audited.

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

The agent logs per-task metrics to enable benchmarking HAM's impact. Each user message that causes the agent to read/write project files counts as 1 task. Trivial queries (HAM help, yes/no answers, clarifying questions) are skipped.

### Entry Format

Write JSONL entries to `.ham/metrics/tasks.jsonl` (or `baseline.jsonl` if in baseline mode). Each task produces two entries:

**task_start:**
```json
{"id":"task-<uuid>","type":"task_start","timestamp":"ISO-8601","description":"Brief task description","ham_active":true,"model":"claude-opus-4-6","files_read":0,"memory_files_loaded":0,"estimated_tokens":0}
```

**task_end:**
```json
{"id":"task-<uuid>","type":"task_end","timestamp":"ISO-8601","status":"completed"}
```

### Rules

- Use the same `id` for both `task_start` and `task_end` entries
- Generate a unique ID per task (e.g., `task-` + 8 random hex chars)
- Set `ham_active` to `true` in active mode, `false` in baseline mode
- Set `model` to the current model name (e.g., `claude-opus-4-6`)
- Set `files_read` to the count of project files read during the task
- Set `memory_files_loaded` to the count of `.memory/` and CLAUDE.md files loaded
- Set `estimated_tokens` to an estimate of total characters processed divided by 4
- Set `status` to `completed` or `error` in the `task_end` entry
- Create `.ham/metrics/` directory if it doesn't exist
- Skip logging for trivial queries (HAM commands, yes/no, clarifications)

### Baseline Mode

Before writing task entries, check `.ham/metrics/state.json`:

1. If `mode` is `"baseline"`:
   - Write entries to `baseline.jsonl` (not `tasks.jsonl`)
   - Set `ham_active` to `false`
   - **Skip** subdirectory CLAUDE.md files and `.memory/` files (still read root CLAUDE.md)
   - After writing `task_end`: only increment `tasks_completed` if status is `"completed"`
   - Do NOT increment for status: `"error"` or `"skipped"`
   - Reminder: trivial queries must NOT generate task entries at all (see Rules above)
   - If `tasks_completed >= tasks_target`, update `state.json` to `{"mode":"active","transitioned_at":"ISO-8601"}`

2. If `mode` is `"active"`, or `state.json` doesn't exist, or `state.json` cannot be parsed as valid JSON:
   - Write entries to `tasks.jsonl`
   - Set `ham_active` to `true`
   - Load all CLAUDE.md and `.memory/` files as normal
   - If `state.json` was unparseable, warn user once per session:
     ```
     ⚠ .ham/metrics/state.json is corrupted. Treating as active mode.
     Run "ham baseline start" to reset, or manually fix the file.
     ```

## HAM Benchmark Command

**Trigger:** "ham benchmark"

When user runs this command, show task-level performance comparison between baseline and HAM-active modes.

### What to do

1. **Run the CLI** — execute from the user's project directory:

```bash
node <path-to-ham-repo>/dashboard/benchmark-cli.js [--days 30] [--model sonnet] [--json]
```

2. **Display results** — the CLI handles three states:
   - **No data**: instructions to run `go ham` or `ham baseline start`
   - **Baseline in progress**: progress bar showing N/10 tasks completed
   - **Comparison available**: table comparing baseline vs HAM-active metrics (avg time, avg tokens, cache rate, per-model breakdown)

### Flags

- `--days N`: time window (default 30)
- `--model <name>`: filter to tasks using a specific model (e.g., `--model sonnet` for apples-to-apples)
- `--json`: raw JSON output

## HAM Baseline Commands

**Trigger:** "ham baseline start" or "ham baseline stop"

### ham baseline start

Creates `.ham/metrics/state.json`:

```json
{
  "mode": "baseline",
  "tasks_completed": 0,
  "tasks_target": 10,
  "started_at": "ISO-8601"
}
```

Create `.ham/metrics/` directory if it doesn't exist.

Tell the user: "Baseline mode started. The next 10 tasks will be logged without HAM memory loading for a clean performance comparison. Keep working normally."

### ham baseline stop

Updates `.ham/metrics/state.json` to transition to active mode:

```json
{
  "mode": "active",
  "transitioned_at": "ISO-8601"
}
```

Preserves any partial baseline data already in `baseline.jsonl`. Tell the user how many baseline tasks were captured and that active benchmarking is now running.

## HAM Metrics Clear Command

**Trigger:** "ham metrics clear"

When user runs this command:

1. **Confirm** — ask "This will delete all benchmark data (tasks.jsonl, baseline.jsonl, state.json). Continue?"
2. **If confirmed** — delete:
   - `.ham/metrics/tasks.jsonl`
   - `.ham/metrics/baseline.jsonl`
   - `.ham/metrics/state.json`
3. **Report** — "Benchmark data cleared. Run `ham baseline start` or `go ham` to start fresh."

## HAM Audit Command

**Trigger:** "HAM audit" or "HAM health", or accepted from a proactive suggestion

When user runs this command (or accepts a proactive audit suggestion), check the health of the memory system:

```
┌─────────────────────────────────────────────────────────┐
│  HAM Health Check                                       │
├─────────────────────────────────────────────────────────┤
│  Root CLAUDE.md                                         │
│    Lines: [N] (recommend: <60)                         │
│    Tokens: [X] (recommend: <250)                       │
│    Status: [✓ healthy | ⚠ oversized]                   │
│                                                         │
│  Subdirectory CLAUDE.md files                           │
│    Found: [N] files                                     │
│    Oversized: [M] files (>75 lines)                    │
│    Missing: [K] directories have code but no CLAUDE.md │
│                                                         │
│  .memory/ status                                        │
│    decisions.md: [N] entries                           │
│    patterns.md: [N] entries                            │
│    inbox.md: [N] unreviewed items [⚠ if >0]           │
│                                                         │
│  Recommendations:                                       │
│    [List any issues found]                             │
└─────────────────────────────────────────────────────────┘
```

After presenting results:
- If `.memory/audit-log.md` doesn't exist, create it from the template in `references/templates.md`.
- Append an entry to `.memory/audit-log.md` with the date, number of issues found, and a one-line summary.
- If the table exceeds 5 entries, remove the oldest row (keeping the header).

## HAM Remove Command

**Trigger:** "ham remove"

Safely removes HAM from a project while preserving Pro-owned and user-authored files.

**Note:** This command is EXEMPT from the Pro guard — it must always run so users can remove the skill's files from any project, including Pro-managed ones.

### Step 1: Detect Pro

Run the same Pro detection checks as the guard:
- `.ham/config.json` with `"pro": true`
- `.ham/config.json` with `enabledImporters` containing more than just `"claude"`
- Any `AGENTS.md` files in the project

Set `pro_detected = true` or `false`.

### Step 2: Inventory files

Scan the project and categorize every HAM-related file:

**Skill-owned (always safe to delete):**
- `.memory/decisions.md`
- `.memory/patterns.md`
- `.memory/inbox.md`
- `.memory/audit-log.md`
- `.memory/baseline.json`
- `.ham/version`
- `.ham/metrics/` (entire directory — `state.json`, `*.jsonl`)
- All subdirectory `CLAUDE.md` files created by the skill (not root)
- The `## Agent Memory System` and `## Context Routing` sections inside root `CLAUDE.md`

**Pro-owned (never delete):**
- `.ham/config.json`
- All `AGENTS.md` files anywhere in the project

**User files (preserve):**
- Root `CLAUDE.md` itself (only strip HAM-added sections, keep everything else)
- Any files not created by HAM

### Step 3: Show dry-run

Present the plan to the user before doing anything:

If `pro_detected`:

```
┌─────────────────────────────────────────────────────────────┐
│  ham remove — dry run (Pro detected)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WILL DELETE (skill-owned):                                  │
│    .memory/decisions.md                                      │
│    .memory/patterns.md                                       │
│    .memory/inbox.md                                          │
│    .memory/audit-log.md                                      │
│    .memory/baseline.json                                     │
│    .ham/version                                              │
│    .ham/metrics/  (entire directory)                          │
│    src/components/CLAUDE.md                                   │
│    src/lib/CLAUDE.md                                          │
│    [... list all subdirectory CLAUDE.md files found]          │
│                                                              │
│  WILL EDIT (root CLAUDE.md):                                 │
│    Remove "Agent Memory System" section                      │
│    Remove "Context Routing" section                          │
│    Keep: Stack, Rules, Commands, and all other sections      │
│                                                              │
│  WILL KEEP (Pro-owned):                                      │
│    .ham/config.json                                           │
│    AGENTS.md  (and any subdirectory AGENTS.md files)         │
│                                                              │
│  Total: X files deleted, 1 file edited, Y files kept        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

If `!pro_detected`:

```
┌─────────────────────────────────────────────────────────────┐
│  ham remove — dry run                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  WILL DELETE:                                                │
│    .memory/  (entire directory)                               │
│    .ham/  (entire directory)                                  │
│    src/components/CLAUDE.md                                   │
│    src/lib/CLAUDE.md                                          │
│    [... list all subdirectory CLAUDE.md files found]          │
│                                                              │
│  WILL EDIT (root CLAUDE.md):                                 │
│    Remove "Agent Memory System" section                      │
│    Remove "Context Routing" section                          │
│    Keep: Stack, Rules, Commands, and all other sections      │
│                                                              │
│  Total: X files deleted, 1 file edited                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Step 4: Confirm

Ask the user: **"Proceed with removal? (yes/no)"**

Do NOT proceed without explicit confirmation.

### Step 5: Execute

If confirmed, delete and edit files exactly as shown in the dry-run. Process in this order:

1. Delete subdirectory CLAUDE.md files
2. Delete `.memory/` contents (or entire directory if no Pro)
3. Delete `.ham/metrics/` and `.ham/version` (or entire `.ham/` if no Pro)
4. Edit root CLAUDE.md — remove only the `## Agent Memory System` and `## Context Routing` sections, preserve everything else
5. If `.memory/` directory is now empty, remove it
6. If `.ham/` directory is now empty (all contents deleted, no `config.json`), remove it

### Step 5b: Clean up .gitignore

After deleting HAM files, remove the HAM block from `.gitignore`:

1. **Find the block** — locate lines between `# HAM` and `# end HAM` (inclusive)
2. **Remove the block** — delete those lines from `.gitignore`
3. **Clean up** — if `.gitignore` is empty (only whitespace) after removal, delete the file entirely

### Step 6: Report

```
HAM removed.
Deleted: X files
Edited: root CLAUDE.md (removed HAM sections)
Kept: Y Pro-owned files  ← only show this line if pro_detected
```

## HAM Dashboard Command

**Trigger:** "HAM dashboard" or "HAM sandwich"

When user runs this command, launch the interactive web dashboard that visualizes token savings, session history, directory coverage, and context file health.

### What to do

0. **Check for updates** — compare local `.ham/version` (if it exists) against the `ham_version` field in this skill's YAML frontmatter. If outdated, print one line: `HAM update available (v2026.02.28). Run "ham update" to get the latest.` Never block the command — continue immediately.
1. **Locate the dashboard** — the dashboard lives at `dashboard/` relative to the HAM skill installation directory (this repo).
2. **Launch it** — run the following command from the **project root** (the user's current working directory):

```bash
node <path-to-ham-repo>/dashboard/launch.js --port 7777
```

The `launch.js` script auto-handles `npm install` and `npm run build` on first run — no manual setup needed.

3. **Tell the user** — output:

```
HAM Dashboard launching...

Open http://localhost:7777 in your browser.

The dashboard parses your Claude Code session data from
~/.claude/projects/ and shows:
  - Token savings (HAM-on vs HAM-off sessions)
  - Daily token and cost trends
  - Per-directory breakdown
  - Context file health (CLAUDE.md coverage)

Press Ctrl+C to stop the server.

Multi-agent analytics available with HAM Pro → goham.dev
```

### Notes
- The dashboard reads session JSONL files from `~/.claude/projects/<encoded-project-path>/`
- Data is parsed into memory at startup — no database needed
- Default port is 7777, configurable via `--port`
- The server must be run from the user's project directory (it uses `process.cwd()` to determine which project's sessions to load)

## HAM Insights Command

**Trigger:** "HAM insights"

When user runs this command, generate structured insights from their dashboard data and write actionable items to `.memory/inbox.md`.

### What to do

1. **Run the CLI** — execute from the user's project directory:

```bash
node <path-to-ham-repo>/dashboard/insights-cli.js --days 30
```

This outputs JSON with categorized insight items. No running server needed.

2. **Parse the output** — the JSON contains an `items` array. Each item has:
   - `category`: `ham_adoption`, `coverage_gap`, `stale_context`, or `activity`
   - `severity`: `high`, `medium`, or `low`
   - `type`: `action` (actionable), `observation` (informational), or `positive` (good news)
   - `title`, `detail`, `action` (null if not actionable), `data` (raw evidence)

3. **Filter to actionable items** — only items where `type === "action"` get written to inbox.

4. **Deduplicate** — read existing `.memory/inbox.md` first. Skip any insight whose `title` already appears in the file.

5. **Write to inbox** — for each new actionable item, append to `.memory/inbox.md`:

```markdown
### Insight: [title] ([YYYY-MM-DD])
**Confidence:** [severity — high/medium/low]
**Evidence:** Dashboard analysis of [totalSessions] sessions over [days] days
**Observed:** [detail]
**Proposed Action:** [action]
```

6. **Log to audit** — append a row to `.memory/audit-log.md`:

```
| [YYYY-MM-DD] | [issues found] | HAM insights: [N] actionable, [M] informational |
```

If the table exceeds 5 entries, remove the oldest row (keeping the header).

7. **Report to user** — summarize what was found:
   - Count of actionable vs informational vs positive items
   - List titles of items written to inbox
   - If no actionable insights, tell the user and skip writing

### If no actionable insights

Tell the user everything looks healthy and no items were written to inbox. Still report any positive or observational insights as a summary.

## Templates

### Root CLAUDE.md (Universal)

```markdown
# [Project Name]

## Stack
- [Auto-detected framework/language]
- [Database if detected]
- [Key dependencies]

## Rules
- [2-3 critical project rules]

## Agent Memory System
[Insert operating instructions from above]
```

### Subdirectory CLAUDE.md

```markdown
# [Directory] Context

## Purpose
[One sentence]

## Conventions
- [Directory-specific conventions]

## Patterns
- [Key patterns used here]
```

### decisions.md

```markdown
# Architecture Decisions

## ADR-001: [Title] (YYYY-MM-DD)
**Status:** active
**Decision:** [What was chosen]
**Context:** [Why this choice was made]
**Alternatives:** [What was rejected]
```

### inbox.md

```markdown
# Memory Inbox

Review periodically. Confirm → move to decisions/patterns. Reject → delete.

---
```

## HAM Route Command

**Trigger:** "ham route"

When user runs this command, add or update the Context Routing section in root CLAUDE.md:

1. **Scan tree** — find all existing CLAUDE.md files (excluding root)
2. **Build routing entries** — for each: `→ [label]: [relative/path/to/CLAUDE.md]`
   - Label = directory name (e.g., `src/api/CLAUDE.md` → `api`)
3. **Update root CLAUDE.md:**
   - If no `## Context Routing` section → append after last section
   - If section exists → diff and show additions only
4. Never remove existing entries. Never modify non-routing content.

## HAM Carbon Command

**Trigger:** "HAM carbon"

When user runs this command, show energy and carbon efficiency data.

### What to do

1. **Run the CLI** — execute from the user's project directory:

```bash
node <path-to-ham-repo>/dashboard/carbon-cli.js [--last] [--days 30]
```

2. **Display results** — show the CLI output to the user.

- Default: quick 3-line summary (total saved, today, last session)
- `--last`: detailed breakdown of most recent session with per-file stats

## How We Estimate Savings (Transparency)

### Where "Without HAM" numbers come from

Without a scoped memory system, an AI coding agent typically:

| Activity | Token Estimate | Source |
|---|---|---|
| Re-reading directory structure | 2,000-3,000 | Listing files, understanding layout |
| Re-discovering conventions | 1,500-2,500 | Reading config files, package.json, etc. |
| Loading monolithic CLAUDE.md | 2,000-4,000 | If one exists, or equivalent context |
| **Total baseline** | **5,000-10,000** | Per prompt without scoped memory |

These are estimates based on typical agent behavior. Your actual baseline depends on:
- Project size and complexity
- How much the agent re-reads each session
- Whether you have any existing context files

### Where "With HAM" numbers come from

HAM tokens are **measured directly** from your files:
- Count characters in each CLAUDE.md file
- Divide by 4 (rough token estimate)
- Sum root + typical subdirectory file

### Cost assumptions

| Model | Input Cost | Source |
|---|---|---|
| Claude Sonnet | $3/M tokens | Anthropic API pricing (Feb 2025) |
| Claude Opus | $15/M tokens | Anthropic API pricing (Feb 2025) |

**Monthly projection assumes:**
- 50 prompts/day (adjust to your usage)
- 30 days/month
- Savings = (baseline - HAM tokens) × prompts

### Honest caveats

- Baseline is an **estimate** — your mileage may vary
- HAM tokens are **measured** — these are accurate
- Actual savings depend on your workflow
- Some prompts won't benefit (e.g., simple questions)
- Agents still read source files — HAM reduces *context* overhead, not all token usage
