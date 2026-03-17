---
name: skill-finder
description: "Full-featured Agent Skills management: Search 35+ skills, install locally, star favorites, update from sources. Use when looking for skills, installing new skills, or managing your skill collection."
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Skill Finder

Full-featured Agent Skills management tool.

## When to Use

- **Find skill**, **search skill**, **install skill**, **スキル検索**
- Looking for skills for a specific task or domain
- Finding and installing skills locally
- Managing favorites with star feature

## Features

| Feature | Description                             |
| ------- | --------------------------------------- |
| Search  | Local index + GitHub API + Web fallback |
| Tags    | Filter by category (`#azure #bicep`)    |
| Install | Download to local directory             |
| Star    | Mark and manage favorites               |
| Update  | Sync all sources from GitHub            |

## Quick Start

```bash
# Search
python scripts/search_skills.py "pdf"
python scripts/search_skills.py "#azure #development"

# Management
python scripts/search_skills.py --info skill-name
python scripts/search_skills.py --install skill-name
python scripts/search_skills.py --star skill-name

# Index
python scripts/search_skills.py --update
python scripts/search_skills.py --add-source https://github.com/owner/repo
```

## Command Reference

| Command            | Description               |
| ------------------ | ------------------------- |
| `<query>`          | Search skills by keyword  |
| `#tag`             | Filter by category        |
| `--info SKILL`     | Show skill details        |
| `--install SKILL`  | Download skill locally    |
| `--star SKILL`     | Add to favorites          |
| `--list-starred`   | Show favorites            |
| `--similar SKILL`  | Find similar skills       |
| `--update`         | Update index from sources |
| `--add-source URL` | Add new source repository |
| `--stats`          | Show index statistics     |
| `--check`          | Verify dependencies       |

## Files

| File                             | Description               |
| -------------------------------- | ------------------------- |
| `scripts/search_skills.py`       | Python script             |
| `scripts/Search-Skills.ps1`      | PowerShell script         |
| `references/skill-index.json`    | Skill index (220+ skills) |
| `references/starred-skills.json` | Your starred skills       |

## Requirements

→ **[references/setup-guide.md](references/setup-guide.md)** for installation

| Tool                 | Required    |
| -------------------- | ----------- |
| GitHub CLI (`gh`)    | 2.0+        |
| curl                 | Any         |
| Python or PowerShell | One of them |

## Agent Instructions

→ **[references/agent-instructions.md](references/agent-instructions.md)** for complete guide

### Core Rules

- Use "Do it? Yes/No?" style proposals
- **NEVER** show commands to users - execute silently
- **ALWAYS** include proposal block after search results

### Search Response Format

```
{N} repos, {M} skills searched (last updated: {date})

| Skill | Description | Source | Trust |
| ----- | ----------- | ------ | ----- |
| ...   | ...         | ...    | ...   |

**Next?**
1. Install?
2. Details?
3. Update index? (last: {date})
4. Web search?
```

### Trust Levels

| Type           | Badge     | Description                |
| -------------- | --------- | -------------------------- |
| `official`     | Official  | Anthropic / GitHub 公式    |
| `awesome-list` | Curated   | キュレーションリスト       |
| `community`    | Community | コミュニティ製（自己責任） |

## Done Criteria

- [ ] Search query returns results
- [ ] Skill installed to local directory (if requested)
- [ ] Index updated successfully (if requested)
