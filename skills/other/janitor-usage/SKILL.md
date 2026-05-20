---
name: janitor-usage
description: "Show which skills you use and which you never use"
metadata:
  version: 1.0.0
---

# Usage Tracking

Parse your Claude Code conversation history to see which skills you actually invoke and which are dead weight.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/usage.sh [--weeks N] [--json]
```

- `--weeks N` - how many weeks to analyze (default: 4)
- `--json` - output raw JSON instead of formatted table

## What It Detects

### Explicit Invocations
Slash commands starting with `/skill-name` (e.g., `/n8n-workflows`, `/janitor-audit`). Most reliable signal.

### Estimated Invocations
Natural language matching against skill description keywords. Higher threshold (50%) to avoid false positives. Labeled as "estimated" in output.

## Example Output

```
=== Skills Janitor - Usage Report ===
Period: 2026-02-24 to 2026-03-24 (4 weeks)

--- Most Used ---
  Skill                    Explicit  Estimated  Total
  n8n-workflows                   2          0      2
  23studio-social-post            1          0      1

--- Never Used (32 skills) ---
  marketing-ab-test        (user)
  marketing-analytics      (user)
  ... and 30 more

=== Summary ===
  Active skills: 4 / 36 (11%)
  Unused skills: 32 (89%)
```

## Persistent Data

Results are saved to `data/usage-history.json`, keeping the last 12 weeks for trend tracking across runs.

## Related Skills

- For finding better alternatives: `/janitor-search`
- For comparing against the market: `/janitor-compare`
- For removing unused skills: `/janitor-cleanup`
