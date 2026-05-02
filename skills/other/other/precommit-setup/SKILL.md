---
name: precommit-setup
description: "Configure pre-commit hooks for linting, type checking, formatting, and testing to enforce quality gates on every commit."
version: 1.9.3
globs: "**/.pre-commit-config.yaml"
alwaysApply: false
# Custom metadata (not used by Claude for matching):
model: claude-sonnet-4
tools:
- Read
- Write
- Bash
category: infrastructure
tags:
- pre-commit
- quality-gates
- linting
- type-checking
- testing
complexity: intermediate
model_hint: standard
estimated_tokens: 1800
progressive_loading: true
modules:
- modules/standard-hooks.md
- modules/component-level-hooks.md
- modules/validation-hooks.md
- modules/ci-integration.md
- modules/troubleshooting.md
---

# Pre-commit Setup Skill

Configure a three-layer pre-commit quality system that
enforces linting, type checking, and testing before every
commit.

## When To Use

- Setting up a new project with code-quality enforcement
- Adding pre-commit hooks to an existing project
- Upgrading from basic linting to a full quality system
- Setting up monorepo or plugin architecture with
  per-component quality checks
- Updating pre-commit hook versions

## When NOT To Use

- Pre-commit hooks already configured and working optimally
- Project does not use git version control
- Team explicitly avoids pre-commit hooks for workflow reasons

## Philosophy: Three-Layer Defense

The system is organised in three layers, each with a
different cost / coverage tradeoff:

- **Layer 1 -- Standard hooks**: fast global checks
  (50-200ms total). Lints and type-checks every staged file.
- **Layer 2 -- Component-specific checks**: per-component
  lint, typecheck, and test (10-30s total). Only the
  components touched by the staged files are run.
- **Layer 3 -- Validation hooks**: project-specific
  structure and pattern checks (varies). Catches violations
  that generic linters miss.

This layering keeps the fast feedback loop fast while still
catching the slow / project-specific bugs before they land.

## Module Loading

The detailed configuration patterns live in modules; load
only the ones you need:

- `modules/standard-hooks.md` -- Layer 1 patterns for
  Python, Rust, and TypeScript (load when configuring base
  linters).
- `modules/component-level-hooks.md` -- Layer 2 monorepo
  scripts and pre-commit wiring (load when project has
  multiple components / plugins).
- `modules/validation-hooks.md` -- Layer 3 custom hooks
  and SKIP patterns (load when enforcing project conventions
  beyond linting).
- `modules/ci-integration.md` -- GitHub Actions workflow
  plus a complete `.pre-commit-config.yaml` example (load
  when wiring CI to mirror local checks).
- `modules/troubleshooting.md` -- timing tables, cache
  clearing, hook-failure recovery (load when hooks are slow
  or failing).

## Workflow

### 1. Create Configuration Files

\`\`\`bash
# Create .pre-commit-config.yaml
python3 plugins/attune/scripts/attune_init.py \\
  --lang python \\
  --name my-project \\
  --path .

# Create quality check scripts (for monorepos)
mkdir -p scripts
chmod +x scripts/run-component-*.sh
\`\`\`

### 2. Configure Python Type Checking

Create `pyproject.toml` with strict type checking:

\`\`\`toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
strict = true

# Per-component configuration
[[tool.mypy.overrides]]
module = "plugins.*"
strict = true
\`\`\`

### 3. Configure Testing

\`\`\`toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = [
    "-v",                    # Verbose output
    "--strict-markers",      # Strict marker enforcement
    "--cov=src",             # Coverage for src/
    "--cov-report=term",     # Terminal coverage report
]

markers = [
    "slow: marks tests as slow (deselect with '-m \\"not slow\\"')",
    "integration: marks tests as integration tests",
]
\`\`\`

### 4. Install and Test Hooks

\`\`\`bash
# Install pre-commit tool
uv sync --extra dev

# Install git hooks
uv run pre-commit install

# Test on all files (first time)
uv run pre-commit run --all-files

# Normal usage - test on staged files
git add .
git commit -m "feat: add feature"
# Hooks run automatically
\`\`\`

### 5. Create Manual Quality Scripts

For full quality checks (CI/CD, monthly audits):

\`\`\`bash
#!/bin/bash
# scripts/check-all-quality.sh -- full quality check for all components

set -e

echo "=== Running Full Quality Checks ==="

./scripts/run-component-lint.sh --all
./scripts/run-component-typecheck.sh --all
./scripts/run-component-tests.sh --all

echo "=== All Quality Checks Passed ==="
\`\`\`

## Hook Execution Order

Pre-commit hooks run in this fixed order; all must pass for
the commit to succeed:

1. File validation (whitespace, EOF, YAML/TOML/JSON syntax)
2. Security scanning (bandit)
3. Global linting (ruff, all files)
4. Global type checking (mypy, all files)
5. Component linting (changed components only)
6. Component type checking (changed components only)
7. Component tests (changed components only)
8. Custom validation (structure, patterns, etc.)

## Best Practices

### For New Projects

Start with strict settings from the beginning -- they are
easier to maintain over time. Configure type checking with
`strict = true` in `pyproject.toml`, set up testing early
(include pytest in pre-commit), and document the reason
whenever you must skip a hook.

### For Existing Projects

Use a gradual adoption strategy. Start with global checks
(Layer 1), then add component-specific checks (Layer 2)
once legacy issues are resolved. Use `--no-verify` only for
true emergencies and document why.

### For Monorepos and Plugin Architectures

Standardize per-component Makefiles for `lint`, `typecheck`,
and `test` targets. Centralize common settings in a root
`pyproject.toml` while allowing per-component overrides.
Automate change detection so commits stay fast, and use
progressive disclosure (summary first, detail on failure).

## Related Skills

- `Skill(attune:project-init)` -- Full project initialization
- `Skill(attune:workflow-setup)` -- GitHub Actions setup
- `Skill(attune:makefile-generation)` -- Generate component
  Makefiles
- `Skill(pensive:shell-review)` -- Audit shell scripts for
  exit-code and safety issues

## See Also

- **Quality Gates** -- three-layer validation: pre-commit
  hooks (formatting, linting), CI checks (tests, coverage),
  and PR review gates (code quality, security).
