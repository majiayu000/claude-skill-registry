---
name: community-pulse
description: Monitor community feedback on Claude Code via Exa search. Gathers sentiment, real-world usage patterns, bug reports, and feature requests from blogs, forums, and social media.
argument-hint: "[--deep] [topic]"
user-invocable: true
---

# Community Pulse Skill

## Overview

Gathers and analyzes community feedback about Claude Code using Exa search tools.

## Modes

- **Quick** (default): Exa web_search for recent mentions
- **Deep** (--deep): Exa deep_researcher for comprehensive analysis

## Search Categories

| Category | Exa Query | Priority |
|----------|-----------|----------|
| Updates | `"Claude Code" release OR update 2026` | HIGH |
| Bugs | `"Claude Code" bug OR issue OR broken` | HIGH |
| Plugins | `"Claude Code" plugin OR hooks experience` | MEDIUM |
| Comparison | `"Claude Code" vs Cursor OR Windsurf` | LOW |
| Tips | `"Claude Code" tips OR workflow OR best practices` | MEDIUM |

## Workflow

1. **Search** using category-specific Exa queries
2. **Filter** for recent results (last 30 days)
3. **Analyze** sentiment (positive/neutral/negative)
4. **Extract** actionable insights
5. **Report** with sources and recommendations

## Sentiment Classification

| Signal | Classification |
|--------|---------------|
| "love", "amazing", "game changer" | Positive |
| "update", "released", "changed" | Neutral |
| "broken", "bug", "regression", "worse" | Negative |

## References

- [Exa Queries Reference](references/exa-queries.md)
- [Pulse Report Template](references/templates/pulse-report.md)
