---
name: instinct-status
description: Display learned instincts with confidence bars grouped by domain. Shows personal and inherited instincts, observation count, and auto-applied threshold status.
---

# Instinct Status

Display the status of all learned instincts from the Continuous Learning system.

## When to Use

- To see what patterns Claude has learned from your sessions
- To check confidence levels of instincts before they auto-apply
- To verify instinct import/export operations worked
- To monitor the learning pipeline health

## Usage

Run this skill via `/instinct-status` or when asked "show my instincts" or "what has Claude learned".

## Behavior

1. Run the instinct CLI to get status:

```bash
node "$CLAUDE_PROJECT_DIR/.claude/scripts/instinct-cli.js" status
```

2. Display the output to the user, which includes:
   - Total instinct count
   - Personal vs inherited breakdown
   - Instincts grouped by domain (git, workflow, testing, etc.)
   - Confidence bars (█░) showing strength of each instinct
   - Trigger conditions and actions
   - Observation count and file location

## Output Format

```text
============================================================
  INSTINCT STATUS - 5 total
============================================================

  Personal:  3
  Inherited: 2

## GIT (2)

  ███████░░░  70%  prefer-rebase-over-merge
            trigger: when merging branches
            action: Use rebase for cleaner history

  █████░░░░░  50%  commit-message-style
            trigger: when writing commit messages
            action: Use conventional commit format

## WORKFLOW (3)
...

─────────────────────────────────────────────────────────
  Observations: 142 events logged
  File: .claude/learned/observations.jsonl

============================================================
```

## Confidence Thresholds

- **≥ 70%** (███████░░░): Auto-applied — Claude uses this instinct automatically
- **50-69%** (█████░░░░░): Suggested — Claude may suggest but won't auto-apply
- **< 50%** (███░░░░░░░): Tentative — Still gathering evidence

## Related Skills

- `/evolve` — Cluster high-confidence instincts into discoverable skills
- Import/export via `instinct-cli.js import` and `instinct-cli.js export`
