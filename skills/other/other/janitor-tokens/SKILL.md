---
name: janitor-tokens
description: "Show how many context window tokens each skill consumes. Use when the user asks about token cost, context budget, skill size, or wants to know which skills waste the most context space."
metadata:
  version: 1.2.0
---

# Context Window Token Cost

Show how many tokens each skill's system prompt consumes and identify unused skills wasting context budget.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/tokencost.sh [--budget N] [--weeks N] [--json]
```

## Options

- `--budget N` - Context window size in tokens (default: 200,000)
- `--weeks N` - Usage lookback period for cross-referencing (default: 4)
- `--json` - Output as JSON

## Output

```
=== Skills Janitor - Context Window Cost ===
Budget: 200,000 tokens

  Skill                               Tokens  Budget  Used?  Last Used
  ─────────────────────────────────── ─────── ─────── ────── ──────────
  marketing-copywriting                 2,340   1.2%    yes  2026-04-10
  n8n-workflows                         1,890   0.9%    yes  2026-04-12
  marketing-seo-audit                   1,560   0.8%     NO  never
  marketing-page-cro                    1,230   0.6%     NO  never
  ...

──────────────────────────────────────────────────────────────────────────
  TOTAL                                18,720   9.4%

--- Summary ---
  Skills loaded: 35 (4 active, 31 unused)
  Total token cost: 18,720 (9.4% of 200,000 budget)
  Unused skill cost: 14,300 (7.2% of budget wasted)

--- Top Unused Token Wasters ---
  1,560 tokens (0.8%)  marketing-seo-audit
  1,230 tokens (0.6%)  marketing-page-cro
  ...
```

## How Token Estimation Works

- Counts words in each SKILL.md file
- Applies 1.3x multiplier (average English markdown token ratio)
- Cross-references with usage history to flag unused + expensive skills

## After Reviewing

- Remove unused skills with the highest token cost first
- Skills you actively use are worth keeping regardless of size
- Use `/janitor-report` to find other issues before cleaning up

## Related Skills

- For usage tracking: `/janitor-usage`
- For removing broken skills: `/janitor-fix --prune`
- For full health report: `/janitor-report`
