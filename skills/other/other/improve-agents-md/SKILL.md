---
name: improve-agents-md
description: "Generate and update AGENTS.md (CLAUDE.md) for projects using a single template with dynamic per-type tooling injection. Auto-detects project type and renders the appropriate Environment & Tooling section. Triggers on keywords: improve agents, generate agents.md, update agents.md, setup claude.md, bootstrap agents"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# improve-agents-md

Generate and manage AGENTS.md (rendered as CLAUDE.md) using a single base
template with dynamic tooling values from `tooling.yml`.

## Architecture

```
assets/
  AGENTS.md.template     # Single base template with {{VAR}} placeholders
  tooling.yml            # Per-type tooling values (package_manager, linter, etc.)
  extras/pep723.md       # Optional section injected for Python types
  templates/shared/      # Shared templates (.gitignore)
tools/
  bootstrap.py           # Entrypoint: setup, update, validate
  template_engine.py     # Reads tooling.yml, renders template, injects extras
  project_type.py        # Auto-detect project type from file indicators
  preserve_custom.py     # Backup + CLAUDE.md migration detection
```

## Modes

### setup

Generate AGENTS.md for a project:
1. Detect project type (or accept `--type` override)
2. Back up existing files if `--force`
3. Load tooling values from `tooling.yml` for detected type
4. Render `AGENTS.md.template` with tooling substitution
5. Inject extras (e.g., PEP 723 section for Python types)
6. Write rendered AGENTS.md to project root
7. Create CLAUDE.md and GEMINI.md as symlinks to AGENTS.md

### update

Re-render AGENTS.md with latest template:
1. Re-detect project type (or accept `--type` override)
2. Preserve customizations if `--force`
3. Re-render AGENTS.md with current tooling values

### validate

Check AGENTS.md content:
1. Verify AGENTS.md exists
2. Check for unresolved `{{VAR}}` placeholders
3. Verify required sections present
4. Check CLAUDE.md is a symlink to AGENTS.md
5. Warn if legacy PROJECT_AGENTS.md is present
6. Check template assets exist

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | false | Print actions without executing |
| `--force` | false | Force overwrite (backup + re-render) |
| `--type` | auto | Override project type detection |

## Dynamic Rendering

Template variables resolved from `tooling.yml`:

| Variable | Description |
|----------|-------------|
| `{{PACKAGE_MANAGER}}` | Package manager command (uv, pnpm, cargo, etc.) |
| `{{TYPE_CHECKER}}` | Type checking command |
| `{{LINTER}}` | Linter command |
| `{{AFTER_EDIT}}` | Post-edit validation command chain |
| `{{STYLE}}` | Language-specific style conventions |

Null values in tooling.yml become `(customizable)` in output.

## Extras Injection

Types with `extras: [pep723]` in tooling.yml get the PEP 723 section
injected after `## Style & Conventions`.

## Questionnaire

Questions only asked when `tooling.yml` has null values for a type:

- **python-pip**: Type checker (pyright/mypy/skip) + Linter (ruff/flake8/pylint)
- **generic**: Project type selection (maps to known type or stays customizable)
- **Ambiguous detection**: Primary project type confirmation

## Supported Project Types

| Type ID | Detection |
|---------|-----------|
| typescript | package.json with typescript/@types |
| ts-bun | bun.lockb present |
| python-uv | uv.lock or [tool.uv] in pyproject.toml |
| python-poetry | [tool.poetry] in pyproject.toml |
| python-pip | requirements.txt or setup.py |
| rust | Cargo.toml |
| generic | fallback |

## Customization Preservation

- If CLAUDE.md exists as a regular file, its content is backed up before migration
- AGENTS.md is the primary file; CLAUDE.md and GEMINI.md are symlinks
- Timestamped backup created before any destructive operation
- Legacy PROJECT_AGENTS.md is no longer created; validate warns if present
