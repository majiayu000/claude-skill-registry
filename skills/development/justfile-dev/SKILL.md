---
name: justfile-dev
description: >-
  Justfile authoring, reviewing, and planning for the just command runner.
  Use when creating new justfiles, adding recipes, reviewing existing justfiles
  for quality, planning recipe sets for new projects, or upgrading justfiles
  as projects mature. Covers syntax patterns, module system, recipe groups,
  language-specific templates, and maturity assessment.
---

# Justfile Development

Workflows for authoring, reviewing, planning, and updating justfiles with the `just` command runner.

## When to Use

- Creating a new justfile for a project
- Adding or modifying recipes
- Reviewing a justfile for quality issues
- Planning which recipes a project needs
- Upgrading a justfile as a project matures
- Converting a Makefile to a justfile
- Setting up monorepo module structure

## Workflows

### Author

When creating a new justfile or adding recipes.

**New Justfile Scaffold:**

```just
set shell := ["bash", "-cu"]

default:
    @just --list

# =============================================================================
# Development
# =============================================================================

# Build the project
[group('dev')]
build:
    <build-command>

# =============================================================================
# Testing
# =============================================================================

# Run test suite
[group('test')]
test:
    <test-command>

# =============================================================================
# Code Quality
# =============================================================================

# Format code
[group('lint')]
fmt:
    <fmt-command>

# Run linter
[group('lint')]
lint:
    <lint-command>

# =============================================================================
# Utilities
# =============================================================================

# Remove build artifacts
[group('util')]
[confirm('Remove all build artifacts?')]
clean:
    <clean-command>
```

**Recipe Writing Rules:**

| Rule | Example |
|------|---------|
| Always add `[group('name')]` | `[group('dev')]` |
| Doc comment above every recipe | `# Build the project` |
| Private helpers start with `_` | `_ensure-tool name:` |
| `[confirm]` on destructive ops | `[confirm('Delete all?')]` |
| Prefer parameters over env vars | `recipe name='default':` |
| Single responsibility | Compose with dependencies |
| No `&&` chaining | Use separate lines or deps |
| No `cd` | Use `[working-directory]` |

**Adding Recipes to Existing Justfiles:**

1. Identify the correct group (see Standard Groups below)
2. Place recipe near related recipes in the same section
3. Add doc comment
4. Add `[group]` attribute
5. If destructive, add `[confirm]`

### Review

Use this checklist when reviewing justfiles.

```markdown
## Justfile Review

- [ ] `set shell` declared at top
- [ ] All recipes grouped with `[group('name')]`
- [ ] Every recipe has a doc comment
- [ ] No ungrouped recipes (except `default`)
- [ ] Private helpers prefixed with `_`
- [ ] Destructive recipes use `[confirm]`
- [ ] No `cd` usage (use `[working-directory]`)
- [ ] No `&&` chaining (use dependencies or separate lines)
- [ ] No secrets in justfile (env vars or `op://`)
- [ ] `default` recipe shows `just --list`
- [ ] Section separators between groups
- [ ] Recipe names are kebab-case
- [ ] No monolithic recipes (compose from focused ones)
- [ ] Parameters preferred over env vars for inputs
```

**Common Issues:**

| Issue | Fix |
|-------|-----|
| Missing `set shell` | Add `set shell := ["bash", "-cu"]` at top |
| Ungrouped recipes | Add `[group('name')]` attribute |
| Missing doc comments | Add `# Description` above recipe |
| `cd` in recipe body | Use `[working-directory('path')]` |
| `&&` chaining | Split into separate lines or deps |
| Hardcoded secrets | Replace with `env('VAR')` or `op://` |
| God recipe doing everything | Split into focused recipes, compose with deps |

### Plan

Use when deciding what recipes a project needs.

**3-Question Assessment:**

| Question | Yes | No |
|----------|-----|----|
| Has CI? | Add quality gates (coverage, check-all) | Skip quality recipes |
| Deploys to prod? | Add security + deploy recipes | Skip deploy/security |
| Multiple languages? | Add module structure | Keep single justfile |

**Recipe Sets by Project Type:**

| Project Type | Baseline | Quality | Deploy | Modules |
|-------------|----------|---------|--------|---------|
| Rust CLI | build, test, lint, fmt, clean | coverage, bench, release | docker | — |
| Rust lib | build, test, lint, fmt, docs | coverage, bench | release | — |
| Web app | build, test, lint, fmt, dev | coverage | docker, deploy | if polyglot |
| Monorepo | orchestrate, default | per-package | per-service | yes |
| MCP server | build, test, lint, fmt | coverage | docker, release | — |

**Decision: Single File vs Modules:**

| Criteria | Single `justfile` | Modules |
|----------|-------------------|---------|
| Recipe count | < 20 | > 20 |
| Languages | 1 | 2+ |
| Repo structure | flat | monorepo/workspace |
| Shared recipes | none | CDN imports needed |

### Convert

When migrating from a Makefile to a justfile.

**Steps:**

1. Map targets to recipes (all recipes are phony — no `.PHONY` needed)
2. Add `set shell := ["bash", "-cu"]` at top
3. Add `default` recipe with `@just --list`
4. Group recipes with `[group('name')]` and add section separators
5. Add doc comments above each recipe
6. Fix anti-patterns (see translations below)
7. Add `[confirm]` to destructive recipes
8. Validate: `just --list` shows grouped, documented recipes

**Makefile → just Translations:**

| Makefile | just |
|----------|------|
| `.PHONY: target` | Not needed (all recipes are phony) |
| `target: dep1 dep2` | `recipe: dep1 dep2` (same syntax) |
| `cd dir && cmd` | `[working-directory('dir')]` attribute |
| `cmd1 && cmd2` | Separate lines in recipe body |
| `$(VAR)` | `{{VAR}}` |
| `@echo "msg"` | `@echo "msg"` (same) |
| `export VAR=val` | `export VAR := "val"` at top |
| `include file.mk` | `import "file.just"` |

### Update

When upgrading an existing justfile.

**Maturity Progression:**

| Level | When | Add |
|-------|------|-----|
| 0: Baseline | Every project | default, build, test, lint, fmt, clean |
| 1: Quality | CI/CD added | coverage, test-watch, check-all, bench |
| 2: Security | Deploying | audit, sbom, doctor |
| 3: Production | Prod systems | deploy, migrate, logs, status |
| 4: Polyglot | Multi-language | modules, orchestration |

**YAGNI**: Only add levels you currently need. Reassess when project scope changes.

**Module Migration:**

When a justfile exceeds ~20 recipes, consider splitting:

1. Create `just/` directory
2. Move related recipes to `just/<group>.just`
3. Add `import? "just/<group>.just"` to root justfile
4. Or use CDN: `mod name "https://just.arusty.dev/modules/<name>.just"`

## Quick Reference

### Standard Groups

| Group | Purpose | Typical Recipes |
|-------|---------|-----------------|
| `dev` | Development | build, setup, install, watch, dev |
| `test` | Testing | test, coverage, bench, test-watch |
| `lint` | Code quality | fmt, lint, clippy, check |
| `docs` | Documentation | docs-build, docs-serve |
| `docker` | Containers | docker-build, docker-run, docker-push |
| `release` | Publishing | release, version-bump, changelog |
| `util` | Maintenance | clean, update, doctor |

### Essential Syntax

| Feature | Syntax |
|---------|--------|
| Settings | `set shell := ["bash", "-cu"]` |
| Groups | `[group('dev')]` |
| Confirm | `[confirm('message')]` |
| Working dir | `[working-directory('path')]` |
| Private | `_recipe-name:` |
| Parameters | `recipe name:` |
| Default params | `recipe name='value':` |
| Variadic | `recipe *args:` |
| Dependencies | `recipe: dep1 dep2` |
| Param deps | `recipe: (dep1 "arg")` |
| Conditional | `if os() == "macos" { ... }` |
| Shebang | `#!/usr/bin/env python3` |
| Script attr | `[script('python3')]` |
| Optional import | `import? "just/mod.just"` |
| CDN module | `mod name "https://url"` |

### Common Functions

| Function | Returns |
|----------|---------|
| `os()` | `"linux"`, `"macos"`, `"windows"` |
| `arch()` | `"x86_64"`, `"aarch64"` |
| `env('VAR')` | Environment variable value |
| `env('VAR', 'default')` | With fallback |
| `justfile_directory()` | Dir containing justfile |
| `invocation_directory()` | Dir where `just` was called |

## aRustyDev Conventions

- Shell: always `set shell := ["bash", "-cu"]`
- CDN modules from `just.arusty.dev`
- Local modules in `just/` with `import?`
- Gist templates via `just apply-gist` (see `gist-templates` rule)
- KuzuDB recipes follow `graph-data-pattern` rule

## Language Patterns

Quick lookup — see `references/recipe-patterns.md` for full details.

| Recipe | Rust | Go | TypeScript | Python |
|--------|------|----|------------|--------|
| `fmt` | `cargo fmt` | `gofmt -w .` | `prettier --write .` | `ruff format .` |
| `lint` | `cargo clippy` | `golangci-lint run` | `eslint .` | `ruff check .` |
| `test` | `cargo test` | `go test ./...` | `vitest` | `pytest` |
| `build` | `cargo build` | `go build ./...` | `tsc` | `python -m build` |
| `coverage` | `cargo tarpaulin` | `go test -cover` | `vitest --coverage` | `pytest --cov` |

## See Also

- `references/syntax-quick-ref.md` — full syntax reference
- `references/recipe-patterns.md` — recipe patterns by category and language
- `references/module-system.md` — module system deep dive
- `references/maturity-model.md` — maturity assessment details
- `examples/rust-project.just` — complete Rust CLI/lib justfile
- `examples/monorepo-root.just` — monorepo router pattern
- `examples/arustydev.just` — aRustyDev conventions with gist templates
- `tables/standard-groups.md` — group definitions and ordering
- `tables/language-recipes.md` — Rust/Go/TS/Python recipe matrix
