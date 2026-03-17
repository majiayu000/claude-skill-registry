---
name: sc-readme
description: Auto-update README.md by analyzing git diff against main branch with PAL consensus validation for significant changes. Use when synchronizing documentation with code changes.
---

# README Auto-Update Skill

Intelligent README maintenance based on git branch changes with multi-model consensus validation for critical updates.

## Quick Start

```bash
# Analyze and update README based on current branch changes
/sc:readme

# Preview changes without writing
/sc:readme --preview

# Force PAL consensus for all updates
/sc:readme --consensus

# Compare against different base branch
/sc:readme --base develop
```

## Behavioral Flow

1. **DISCOVER** - Run `git diff main...HEAD --name-status` to find changed files
2. **ANALYZE** - Read changed files, categorize by type (API, config, deps, features)
3. **PLAN** - Read current README, identify sections needing updates
4. **VALIDATE** - Use PAL consensus for API/breaking changes
5. **GENERATE** - Update README sections via Write tool
6. **VERIFY** - Review final README with PAL codereview

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--base` | string | `main` | Base branch to compare against |
| `--preview` | bool | false | Preview changes without writing |
| `--consensus` | bool | false | Force PAL consensus for all updates |

## Git Commands Used

```bash
# Get list of changed files
git diff main...HEAD --name-status

# Get actual diff content for analysis
git diff main...HEAD

# Check for new exports/functions in specific file
git diff main...HEAD -- path/to/file.py

# Get commit messages for context
git log main...HEAD --oneline
```

## Change Categories

| Category | File Patterns | README Sections |
|----------|---------------|-----------------|
| API | `*.py`, `*.ts`, `*.js` with new exports | API Reference, Usage |
| Dependencies | `package.json`, `requirements.txt`, `pyproject.toml` | Installation, Dependencies |
| Config | `.env*`, `*.config.*`, `settings.*` | Configuration |
| Features | New modules, significant additions | Features, Usage |

## MCP Integration

### PAL MCP

```bash
# Consensus for API changes
mcp__pal__consensus(
    models=[{"model": "gpt-5.2", "stance": "for"}, {"model": "gemini-3-pro", "stance": "against"}],
    step="Evaluate: Does this README update accurately reflect the code changes?",
    relevant_files=["/README.md", "/src/changed_file.py"]
)

# Review final README
mcp__pal__codereview(
    review_type="quick",
    step="Review README accuracy",
    relevant_files=["/README.md"]
)
```

## Tool Coordination

- **Bash** - Git commands (`git diff`, `git log`)
- **Read** - README.md, changed source files
- **Write** - Update README.md
- **Grep** - Find patterns in codebase

## Examples

### Basic Flow
```bash
/sc:readme
# 1. Bash: git diff main...HEAD --name-status
# 2. Read: README.md + changed files
# 3. Analyze: what sections need updates
# 4. PAL consensus if API changes detected
# 5. Write: updated README.md
```

### Preview Mode
```bash
/sc:readme --preview
# Same analysis, but output changes instead of writing
```

## Guardrails

1. **Back up README** before modifications
2. **Never remove sections** without user confirmation
3. **Require consensus** for breaking changes
4. **Preserve custom content** not related to code changes

## Related Skills

- `/sc:git` - Git operations
- `/sc:document` - General documentation
