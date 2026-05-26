---
name: agent-ops-git-story
description: "Generate narrative summaries from git history for onboarding, retrospectives, changelogs, and exploration. LLM-enhanced when available, works without LLM too."
category: analysis
invokes: []
invoked_by: [agent-ops-docs, agent-ops-versioning]
state_files:
  read: [constitution.md, focus.md]
  write: []
---

# Git Story Skill

Generate human-readable narratives from git commit history. Useful for:
- **Onboarding** — Help new team members understand project evolution
- **Retrospectives** — Create sprint/milestone summaries
- **Changelogs** — Generate release notes from commits
- **Exploration** — Understand "what happened here?" for any period

## Requirements

- **Git**: Must be installed locally and available on PATH
- **LLM**: Optional — enhanced narratives when available, templated output without

## Data Extraction

**Works with or without `aoc` CLI installed.** Story generation uses raw `git log` commands by default.

### Git Commands (Default)

| Operation | Command |
|---------|---------|
| Recent commits | `git log --oneline -N` |
| Date range | `git log --since="YYYY-MM-DD" --until="YYYY-MM-DD"` |
| By author | `git log --author="name"` |
| Detailed | `git log --stat --since="YYYY-MM-DD"` |
| JSON-like | `git log --format="%H|%an|%ad|%s" --date=short` |

### CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, enhanced commands are available:

| Command | Description |
|---------|-------------|
| `aoc git story` | Generate narrative from commits |
| `aoc git stats` | Quick repository statistics |
| `aoc git info` | Basic repository information |

### Story Command Options (CLI)

```bash
aoc git story [OPTIONS]

Options:
  --since DATE         Include commits after this date (YYYY-MM-DD)
  --until DATE         Include commits before this date (YYYY-MM-DD)
  --last N             Last N commits only
  --author NAME        Filter by author name or email
  --group [date|author|type]  Grouping strategy (default: date)
  --format [narrative|changelog|bullets|json]  Output format
  --output FILE        Write to file (default: stdout)
  --merges             Include merge commits
  --repo PATH          Repository path (default: current directory)
  --title TEXT         Custom story title
```

### Examples

```bash
# Last 30 days of activity
aoc git story --since 2026-01-01

# Generate changelog format
aoc git story --last 50 --format changelog

# Filter by author, group by type
aoc git story --author "John Doe" --group type

# Export to file
aoc git story --last 100 --output story.md

# Quick stats
aoc git stats
```

## Agent Workflow

When user requests a git story or narrative:

### 1. Gather Requirements

```
What kind of git story do you need?

A) **Recent activity** — Last N days or commits
B) **Release notes** — Changelog format for a version
C) **Sprint retrospective** — Specific date range
D) **Author focus** — Contributions by a specific person
E) **Full history** — Complete project evolution
```

### 2. Extract Data

Run appropriate `aoc git` command based on requirements:

```bash
# For recent activity
aoc git story --last 30 --format json

# For date range (sprint)
aoc git story --since 2026-01-01 --until 2026-01-15 --format json

# For changelog
aoc git story --since <last-release> --format changelog
```

### 3. Enhance with LLM (Optional)

When LLM is available, transform raw data into rich narrative:

**Input (from CLI JSON output):**
```json
{
  "title": "Git Story",
  "period": "January 1-15, 2026",
  "total_commits": 45,
  "groups": [...]
}
```

**LLM Prompt:**
```
Transform this git commit data into a human-readable narrative.

Context: {purpose - onboarding/retrospective/changelog}
Audience: {who will read this}
Tone: {technical/casual/formal}

Data:
{json_output}

Create a narrative that:
1. Opens with an overview of the period
2. Highlights major themes/features
3. Groups related changes logically
4. Notes significant contributors
5. Ends with a summary

Format: Markdown with headers, bullets, and emphasis.
```

**Output (LLM-enhanced):**
```markdown
# Development Update: January 1-15, 2026

## Overview
The first two weeks of January saw intense development activity with 45 commits 
from 5 contributors. The focus was on authentication improvements and API stability.

## Major Themes

### 🔐 Authentication Overhaul
John and Sarah led a comprehensive rework of the auth system:
- Implemented OAuth2 with Google and GitHub providers
- Added session management with automatic refresh
- Fixed critical security vulnerability in token validation

### 🚀 API Performance
The API team delivered significant improvements:
- Reduced average response time by 40%
- Added pagination to all list endpoints
- Implemented request rate limiting

## Contributors
- **John Doe** (18 commits) — Auth system, security fixes
- **Sarah Smith** (12 commits) — OAuth integration, tests
- **Mike Chen** (10 commits) — API optimization
- 2 others with 5 commits total

## What's Next
The groundwork for v2.0 is complete. Next sprint focuses on the dashboard UI.
```

### 4. Without LLM

When LLM is not available, use templated output from CLI:

```bash
# Narrative format (human-readable)
aoc git story --format narrative

# Changelog format (conventional)
aoc git story --format changelog

# Bullets (simple list)
aoc git story --format bullets
```

## Output Formats

### Narrative (default)
Rich markdown with sections for contributors, grouped commits, and context.
Best for: Onboarding docs, retrospectives

### Changelog
Conventional changelog format grouped by commit type (feat, fix, etc.).
Best for: Release notes, CHANGELOG.md updates

### Bullets
Simple bullet list of commits.
Best for: Quick summaries, PR descriptions

### JSON
Structured data for further processing.
Best for: Feeding to LLM, programmatic use

## Integration Points

### With agent-ops-versioning
```
When generating release notes:
1. Determine version range (last tag to HEAD)
2. Run: aoc git story --since <last-tag> --format changelog
3. Insert into CHANGELOG.md
```

### With agent-ops-docs
```
When updating project documentation:
1. Generate story for significant period
2. Add to docs/history/ or similar
3. Link from main README if appropriate
```

### With Obsidian (FEAT-0196)
```bash
# Export git story to Obsidian vault
aoc git story --last 50 --output story.md
aoc obsidian export-report git-story --last 30 --vault ~/notes
```

## Best Practices

1. **Be specific about time range** — "Last 30 days" is better than "recent"
2. **Exclude merge commits** — Default behavior, cleaner output
3. **Use appropriate format** — Changelog for releases, narrative for humans
4. **Filter by author** when highlighting individual contributions
5. **Group by type** for release notes, by date for retrospectives

## Example Session

**User:** Generate a summary of what happened in the codebase this month.

**Agent:**
```
I'll generate a git story for January 2026.

Running: aoc git story --since 2026-01-01 --format narrative

[Output displayed]

Key highlights:
- 127 commits from 8 contributors
- Major features: OAuth integration, API pagination, Dashboard redesign
- Notable fixes: Security vulnerability patched, performance improvements

Would you like me to:
1. Generate a more detailed breakdown by feature?
2. Create a changelog format for release notes?
3. Focus on a specific contributor's work?
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "git is not available" | Install git and ensure it's on PATH |
| No commits found | Check date range, verify you're in a git repo |
| Merge commits cluttering output | Default excludes merges; add `--merges` if needed |
| Large output | Use `--last N` to limit, or filter by date |
