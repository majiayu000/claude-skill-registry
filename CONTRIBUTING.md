# Contributing to Claude Skills Registry

Thanks for your interest in contributing!

## How to Submit a New Skill

### Option 1: Open an Issue (Recommended)

Open an [issue](https://github.com/majiayu000/claude-skill-registry-core/issues/new) with the following info:

- **Name**: Skill name (kebab-case)
- **Repository**: GitHub URL of your skill repo
- **Description**: One-line description
- **Category**: e.g. `development`, `devops`, `productivity`, `data`, `design`, `testing`
- **Tags**: Relevant keywords

We'll review and add it to the registry.

### Option 2: Pull Request to This Core Repo

This repository (`claude-skill-registry-core`) is the **authoritative pipeline repo**. The separate main repository (`claude-skill-registry`) is a generated publish artifact and will be overwritten on the next publish cycle.

To submit a PR directly, open it against **this repo** and edit `sources/community.json`:

```json
{
  "name": "your-skill-name",
  "repo": "owner/repo",
  "path": "",
  "description": "One-line description of your skill.",
  "category": "development",
  "tags": ["tag1", "tag2"],
  "stars": 0
}
```

## Requirements

- Your repo must contain a valid `SKILL.md` file (root or subdirectory)
- Must have an open-source license (MIT, Apache-2.0, etc.)
- No malicious code or credential harvesting

## Architecture

```
Core (source of truth) ──► Data (skills archive) ──► Main (publish artifact)
```

- **Core**: `majiayu000/claude-skill-registry-core` — scripts, sources, CI/CD
- **Data**: `majiayu000/claude-skill-registry-data` — archived `SKILL.md` tree
- **Main**: `majiayu000/claude-skill-registry` — merged artifact published from pinned core + data refs
