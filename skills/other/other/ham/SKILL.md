---
name: ham
description: Set up Hierarchical Agent Memory (HAM) — scoped CLAUDE.md files per directory that reduce token spend. Trigger on "go ham", "set up HAM", "HAM savings", or "HAM stats".
---

# HAM (Hierarchical Agent Memory)

Scoped memory system that reduces context token spend per request.

## Quick Start

**Trigger:** "go ham"

When user says "go ham":

1. **Auto-detect everything** — scan for platform signals and project maturity silently
2. **Generate files** — create the memory structure without asking questions
3. **Confirm setup** — list files created, tell user to run `HAM savings` to see impact

Only ask questions if detection fails.

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

### Step 2: Generate Structure

Create files based on detection:

```
project/
├── CLAUDE.md              # Root context (~200 tokens)
├── .memory/
│   ├── decisions.md       # Empty, ready for ADRs
│   ├── patterns.md        # Empty, ready for patterns
│   ├── inbox.md           # Inferred items (brownfield only)
│   └── audit-log.md       # Audit history (auto-maintained)
└── [src dirs]/
    └── CLAUDE.md          # Per-directory context (brownfield only)
```

For greenfield: only create root + .memory/
For brownfield: also create subdirectory CLAUDE.md files

### Step 3: Capture Baseline

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

### Step 4: Confirm Setup

After creating files, output:

```
HAM setup complete. Created [N] files.
Baseline captured in .memory/baseline.json

Run "HAM savings" to see your token and cost savings.
```

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
```

If `.memory/baseline.json` doesn't exist (skill wasn't used for setup), show:

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

# Tokens per typical prompt (root + 1 subdir)
ham_tokens = root_tokens + avg_subdir

# Baseline estimate (without any memory system)
# Conservative: agent re-orients each prompt
baseline_low = 5000
baseline_high = 10000
baseline_mid = 7500

# Savings
savings_tokens = baseline_mid - ham_tokens
savings_pct = (savings_tokens / baseline_mid) * 100

# Monthly (50 prompts/day × 30 days)
monthly_prompts = 1500
monthly_tokens_saved = savings_tokens * monthly_prompts
cost_sonnet = (monthly_tokens_saved / 1_000_000) * 3  # $3/M
cost_opus = (monthly_tokens_saved / 1_000_000) * 15   # $15/M
```

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
- Read this file for global context
- Read target directory's CLAUDE.md before changes
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
