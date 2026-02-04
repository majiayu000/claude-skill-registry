---
name: init
description: Initialize a project with bluera-base conventions
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# Init

Set up a project with bluera-base conventions. Orchestrates existing commands.

## Context

!`ls package.json pyproject.toml Cargo.toml go.mod pom.xml build.gradle Gemfile composer.json mix.exs 2>/dev/null | head -3 || echo "No project files detected"`

## Current State Detection

Check what's already set up:

```bash
# Config
[ -f .bluera/bluera-base/config.json ] && echo "config: YES" || echo "config: NO"

# Rules
ls .claude/rules/*.md 2>/dev/null | wc -l | xargs -I{} echo "rules: {} files"

# CLAUDE.md
[ -f CLAUDE.md ] && (grep -q "@bluera-base" CLAUDE.md && echo "CLAUDE.md: YES (has @include)" || echo "CLAUDE.md: YES (no @include)") || echo "CLAUDE.md: NO"
```

Show status table:

| Component | Status |
|-----------|--------|
| Config (.bluera/bluera-base/) | ✓ / ✗ |
| Rules (.claude/rules/) | ✓ / ✗ (N files) |
| CLAUDE.md | ✓ / ✗ / needs @include |

## Workflow

### If `--quick` argument

Skip interview, apply quick setup:

1. Config init (if missing)
2. Install rules (if missing)
3. CLAUDE.md with @include (if missing or needs update)

### If `--full` argument

Skip interview, apply full setup:

1. All of quick setup
2. Delegate to `/bluera-base:harden-repo`
3. Ask about feature enablement

### Otherwise: Interview

Use AskUserQuestion:

```yaml
question: "What would you like to set up?"
header: "Init"
options:
  - label: "Quick setup (Recommended)"
    description: "Config + rules + CLAUDE.md"
  - label: "Full setup"
    description: "Quick setup + harden repo (linting, formatting, hooks)"
  - label: "Customize"
    description: "Choose individual components"
multiSelect: false
```

If "Customize" selected:

```yaml
question: "Select components to set up"
header: "Components"
options:
  - label: "Initialize config"
    description: "Create .bluera/bluera-base/ config structure"
  - label: "Install rules"
    description: "Copy rule templates to .claude/rules/"
  - label: "CLAUDE.md"
    description: "Create/update with @bluera-base include"
  - label: "Harden repo"
    description: "Linting, formatting, hooks, coverage"
multiSelect: true
```

### Execute Selected Components

For each selected component:

#### 1. Config Init

If config not initialized:

1. Create `.bluera/bluera-base/` directory
2. Write default `config.json`
3. Update `.gitignore` with bluera patterns

See `/bluera-base:config init` for full workflow.

#### 2. Install Rules

If rules not installed:

1. Create `.claude/rules/` directory
2. Copy core rules: `00-base.md`, `anti-patterns.md`, `git.md`
3. Ask about optional rules

See `/bluera-base:install-rules` for full workflow.

#### 3. CLAUDE.md

If CLAUDE.md missing or needs @include:

1. If missing: create with @include header
2. If exists without @include: add @include at top
3. Audit structure

See `/bluera-base:claude-code-md` for full workflow.

#### 4. Harden Repo (if selected)

Delegate entirely to `/bluera-base:harden-repo` which has its own interview for:

- Language detection
- Linter/formatter selection
- Hook setup
- Coverage configuration

### Feature Enablement

After setup, offer to enable features using 3 grouped questions.

**Source of truth:** See `<repo root>/skills/config/SKILL.md` for the canonical feature list, descriptions, config paths, and dependencies.

**Feature groups:**

| Group | Features |
|-------|----------|
| Learning | `auto-learn`, `deep-learn` |
| Workflow | `auto-commit`, `auto-push`, `notifications` |
| Quality | `dry-check`, `dry-auto`, `strict-typing`, `standards-review` |

For each group, use AskUserQuestion with multiSelect=true. Pull feature labels and descriptions from the config skill's feature table.

**Dependency handling:** When enabling dependent features, auto-enable parent:

- `auto-push` → also enable `auto-commit`
- `dry-auto` → also enable `dry-check`

For each selected feature, update config using the config path from `<repo root>/skills/config/SKILL.md`.

### Report

Show summary:

```text
## Setup Complete

| Component | Status |
|-----------|--------|
| Config | ✓ Created |
| Rules | ✓ 3 files installed |
| CLAUDE.md | ✓ Updated with @include |
| Harden repo | ✓ ESLint, Prettier, husky |
| Features | ✓ strict-typing enabled |

Next steps:
- Review .claude/rules/ and customize if needed
- Run /bluera-base:config show to see all settings
- Run /bluera-base:help for available commands
```

## Constraints

- **Idempotent**: Running init multiple times should be safe
- **Non-destructive**: Never overwrite existing files without asking
- **Delegate**: Use existing command workflows, don't reimplement
- **Skip existing**: Don't re-run setup for components already configured
