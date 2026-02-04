# Scheme 2: Core + Data Repo (Git-browsable archive)

Goal: keep the **full `skills/**` archive browsable on GitHub**, while making this repo fast to `clone/pull` by moving the huge working tree into a separate **data repo**.

## Repos

### 1) `registry-core` (this repo)

Contains:
- Crawlers + build scripts (`scripts/`, `crawler/`)
- Source lists (`sources/`)
- Schemas (`schema/`)
- Published metadata (`registry.json`)
- GitHub Pages site sources (`docs/` static assets)

Does **not** contain:
- The expanded skill archive `skills/**` (moved to the data repo)

### 2) `registry-data` (new repo)

Contains:
- archived skill contents (category folders like `data/`, `development/`, etc.)

This is the repo you’ll browse on GitHub to view a skill.

## How sync works

This repo’s GitHub Actions workflow checks out the data repo into `./skills/` (as a separate checkout). That keeps paths stable (e.g. `./skills/data/<skill>/SKILL.md`) while the core repo stays small.

You’ll need:
- A GitHub repository variable: `REGISTRY_DATA_REPO` (e.g. `yourname/claude-skill-registry-data`)
- A secret: `DATA_REPO_TOKEN` (PAT with `repo` scope for private, or `public_repo` for public)

## One-time migration (local)

1) Create a new GitHub repo for the archive, e.g. `claude-skill-registry-data`
2) From a clone that still has `skills/` on disk, run:

```bash
bash scripts/migrate_to_data_repo.sh ../claude-skill-registry-data
```

3) Push `../claude-skill-registry-data` to GitHub
4) Set `REGISTRY_DATA_REPO` + `DATA_REPO_TOKEN` in this repo
