---
name: python-scaffold
description: Add Python VS Code workspace config to a project. Composable — works standalone or merges into existing .vscode/ from a prior kit scaffold.
argument-hint: ""
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Configure VS Code for Python development by creating or merging `.vscode/settings.json` and `.vscode/extensions.json`. Designed to compose with `/mern-scaffold`, `/nean-scaffold`, or `/ios-scaffold` — or run standalone for Python-only projects.

## Template-first rule
Use files from `templates/` as the source of truth for Python VS Code config.

Templates provide:
- VS Code workspace settings (interpreter path, pytest, Ruff, Black formatter)
- VS Code extension recommendations (Python, Pylance, Ruff, Black, mypy, coverage gutters)

## What gets created or merged

```
<project>/
└── .vscode/
    ├── settings.json      # Python workspace settings (merged if exists)
    └── extensions.json    # Python extension recommendations (merged if exists)
```

## Scaffold steps

### 1. Detect virtual environment location
- Check if `.venv/` directory exists in the project root
- If not, check if `venv/` directory exists
- Use whichever exists; default to `.venv/` if neither exists yet
- Update the `python.defaultInterpreterPath` value in settings template accordingly

### 2. Handle `.vscode/extensions.json`

**If `.vscode/extensions.json` already exists** (from a prior kit scaffold):
- Read the existing file
- Parse the `recommendations` array
- Append Python recommendations from the template (deduplicate — skip any already present)
- Write back the merged file

**If `.vscode/extensions.json` does not exist:**
- Copy `templates/.vscode/extensions.json` directly

### 3. Handle `.vscode/settings.json`

**If `.vscode/settings.json` already exists** (from a prior kit scaffold):
- Read the existing file
- Merge Python-specific keys from the template into the existing object:
  - `python.defaultInterpreterPath`
  - `python.testing.pytestEnabled`
  - `python.testing.pytestArgs`
  - `ruff.enable`
  - `[python]` formatter and code actions block
- Do NOT overwrite existing keys from the prior scaffold
- Write back the merged file

**If `.vscode/settings.json` does not exist:**
- Copy `templates/.vscode/settings.json` directly (with venv path adjusted per step 1)

## Output
Summarize: what was created vs merged, venv path used, and list the recommended extensions.
