---
name: janitor-compare
description: "Compare your skill with similar ones on GitHub"
metadata:
  version: 1.0.0
---

# Market Comparison

Compare a local skill against alternatives found on GitHub, with composite scoring and marketplace install counts.

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/compare.sh <skill-name> [--json]
```

- `<skill-name>` - the local skill folder name to analyze
- `--json` - raw JSON output

## Scoring

Each alternative gets a composite relevance score (0-100):
- **40%** keyword overlap with your skill's description
- **30%** popularity (log-scaled GitHub stars)
- **15%** recency (days since last update)
- **15%** activity (forks/stars ratio)

## Data Sources

- GitHub repository search (keyword-based)
- `~/.claude/plugins/install-counts-cache.json` - official marketplace install counts (150+ plugins, maintained by Claude Code itself)

## Example Output

```
=== Skills Janitor - Market Analysis ===
Analyzing: skills-janitor

--- Alternatives Found ---
  #  Repository                Score  Stars  Overlap  Updated
  1  obra/superpowers           72.3  106k     45%    2026-03-22
  2  user/skill-manager         58.1  2.1k     62%    2026-03-18

--- Related Marketplace Plugins (install counts) ---
   169,670  code-review (shared: code)
    77,603  skill-creator (shared: skills)

  Your skill is not in the official marketplace.
```

## Related Skills

- For finding skills by keyword: `/janitor-search`
- For checking your usage: `/janitor-usage`
- For full inventory: `/janitor-audit`
