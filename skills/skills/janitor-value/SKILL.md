---
name: janitor-value
description: "Show whether each skill is earning its context-window cost — combined tokens-used view sorted by waste. Use when the user asks 'are my skills worth it', 'what's my context budget', 'which skills are dead weight', or anything about skill value, token cost, or usage."
metadata:
  version: 1.3.0
---

# Skill Value Report

Show whether each installed skill is earning the context-window tokens it costs. Combines token cost and usage tracking into a single view, sorted with the heaviest unused skills at the top.

Replaces the v1.2 split between `/janitor-tokens` (cost only) and `/janitor-usage` (usage only).

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/value.sh [--weeks N] [--budget N] [--json]
```

- `--weeks N` — usage lookback window (default: 4)
- `--budget N` — context window size for % calculations (default: 200000)
- `--json` — emit raw JSON

## Output

A table of every installed skill with:
- **Tokens** — approximate token count of the skill's SKILL.md
- **Budget** — % of the configured context window
- **Used?** — `yes` if invoked in the lookback window, else `NO`
- **Last Used** — date of most recent invocation

Followed by a summary:
- Total tokens loaded into context
- Active vs. unused split
- Top wasters: heavy skills with zero usage

Plugin-namespaced skills appear with their full invocation name (e.g., `marketing-skills:image`, `figma:figma-use`).

## When to Suggest Action

If "unused skill cost" exceeds 20% of the budget, recommend the user run `/janitor-report` for a full health check or (in v1.4+) `/janitor-swipe` to triage interactively.

## Related Skills

- `/janitor-report` — full health check including duplicates and broken skills
- `/janitor-fix --prune` — remove broken symlinks and empty skill dirs
- `/janitor-discover` — find new skills or check one before installing
