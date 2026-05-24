---
name: janitor-discover
description: "Find new skills on GitHub or check a specific skill before installing. Use when the user wants to search for skills, evaluate a skill URL, check overlap with existing skills before installing, or compare a local skill against alternatives."
metadata:
  version: 1.3.0
---

# Skill Discovery & Pre-Install Check

Combined entry point for finding skills on GitHub and for evaluating a specific skill (URL or local path) before installing it.

Replaces the v1.2 split between `/janitor-search` and `/janitor-precheck`. The dispatcher picks the right mode from the argument shape:

| Argument | Mode | What runs |
|---|---|---|
| Keyword(s) like `seo` or `n8n workflows` | Discovery | `search.sh` — find matching skills on GitHub |
| `--compare <skill-name>` | Comparison | `search.sh --compare` — find alternatives to a local skill |
| Full URL: `https://github.com/user/skill` | Pre-install check | `precheck.sh` — analyze before installing |
| Short repo: `user/skill` | Pre-install check | `precheck.sh` (auto-expanded to URL) |
| Local path: `~/path/to/skill` | Pre-install check | `precheck.sh` (local folder) |

## How to Run

```bash
bash ~/.claude/skills/skills-janitor/scripts/discover.sh <query-or-url> [options]
```

Examples:
- `discover.sh seo` — search for SEO-related skills
- `discover.sh n8n --limit 20` — top 20 n8n skills
- `discover.sh --compare marketing-seo-audit` — alternatives to a local skill
- `discover.sh https://github.com/user/my-skill` — check before installing
- `discover.sh user/my-skill` — same, short form

## Output

**Discovery mode** — ranked list of GitHub repos with skill name, description, stars, last updated, and a one-line verdict.

**Pre-install mode** — overlap analysis: which of the user's existing skills (including plugin skills now scanned by v1.3) overlap with the candidate by description, and a recommendation to install / skip / replace.

## Related Skills

- `/janitor-report` — health check of currently installed skills
- `/janitor-value` — are existing skills earning their context cost
- `/janitor-fix` — fix issues with installed skills
