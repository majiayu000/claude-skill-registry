---
name: janitor-search
description: "Search GitHub for new skills to install. Also use with --compare to analyze a local skill against GitHub alternatives and marketplace competition."
metadata:
  version: 1.1.0
---

# Skill Discovery & Comparison

Search GitHub for Claude Code skills by keyword, or compare a local skill against alternatives.

## How to Run

```bash
# Search for skills
bash ~/.claude/skills/skills-janitor/scripts/search.sh <keyword> [--limit N] [--json]

# Compare your skill against GitHub alternatives
bash ~/.claude/skills/skills-janitor/scripts/search.sh --compare <skill-name> [--json]
```

## Search Mode

- `<keyword>` - required search term (e.g., "marketing", "deployment", "testing")
- `--limit N` - max results (default: 10)
- `--json` - raw JSON output

### How It Works

1. Searches GitHub repos matching `{keyword} claude skill` in name/description/README
2. Also searches by topic tag `claude-code`
3. Cross-references results against your installed skills and plugins
4. Marks each result as `INSTALLED` or `AVAILABLE`

## Compare Mode (`--compare`)

Analyzes a local skill against alternatives found on GitHub:
- Composite scoring: 40% keyword overlap, 30% popularity, 15% recency, 15% activity
- Shows marketplace install counts when available
- Reports market position (unique niche vs. crowded space)

```bash
search.sh --compare my-marketing-skill
```

## Rate Limits

- Unauthenticated: 60 requests/hour
- Set `GITHUB_TOKEN` env var for 5,000 requests/hour
- Results cached for 24 hours

## Related Skills

- For checking which skills you actually use: `/janitor-usage`
- For token cost analysis: `/janitor-tokens`
- For pre-install overlap check: `/janitor-precheck`
