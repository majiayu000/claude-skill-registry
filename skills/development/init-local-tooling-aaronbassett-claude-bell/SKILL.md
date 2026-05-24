---
name: init-local-tooling
description: Initialize and configure local development tooling for TypeScript, Rust, and Python projects including monorepos. Use when setting up linting (ESLint, Biome, clippy, ruff), formatting (Prettier, rustfmt, ruff), type checking (tsc, mypy), testing (Vitest, Jest, cargo test, pytest), Git hooks (lefthook for commit-msg, pre-commit, pre-push), GitHub Actions workflows, package publishing (npm, crates.io, PyPI), version management (Changesets), and automated releases. Covers both single-language projects and multi-language monorepos using Nx + pnpm workspaces.
---

# Local Tooling Initialization

Comprehensive setup for linting, formatting, type checking, testing, Git hooks, CI/CD, and publishing across TypeScript, Rust, and Python projects.

## When to Use This Skill

Use this skill when you need to:
- Initialize tooling for a new TypeScript/Rust/Python project
- Set up monorepo with Nx + pnpm workspaces
- Configure Git hooks with lefthook (conventional commits, pre-commit, pre-push)
- Add GitHub Actions for CI/CD
- Set up automated publishing to npm/crates.io/PyPI
- Configure version bumping and changelog generation with Changesets
- Migrate from Husky to lefthook
- Choose between ESLint+Prettier vs Biome for TypeScript

## Quick Start

### TypeScript Project

**Automated setup:**
```bash
./scripts/init_typescript.sh
```

**Choose tooling:**
- **Biome** (recommended) - Fast, all-in-one, modern
- **ESLint + Prettier** - Traditional, highly configurable

**What you get:**
- Linting and formatting
- TypeScript strict mode
- Vitest for testing
- Package.json scripts

→ **See:** [references/typescript.md](references/typescript.md)

### Rust Project

**Manual setup (opinionated configs in assets/):**
```bash
# Tools come with Rust
rustup component add rustfmt clippy

# Optional: Enhanced tooling
brew install cargo-nextest cargo-deny

# Copy configs from assets/configs/rust/
cp assets/configs/rust/rustfmt.toml .
cp assets/configs/rust/clippy.toml .
```

→ **See:** [references/rust.md](references/rust.md)

### Python Project

**Using uv (recommended):**
```bash
# Install uv
brew install uv

# Create project
uv init my-project
cd my-project

# Add dev dependencies
uv add --dev ruff mypy pytest

# Copy config from assets/
cp assets/configs/python/pyproject.toml .
```

→ **See:** [references/python.md](references/python.md)

### Monorepo Setup

**Create Nx + pnpm monorepo:**
```bash
./scripts/init_monorepo.sh
```

Or manually:
```bash
npx create-nx-workspace@latest my-monorepo
# Choose: pnpm + integrated monorepo
```

→ **See:** [references/monorepo.md](references/monorepo.md)

---

## Workflow Decision Tree

### 1. Choose Project Type

**Single Language Project**
→ Use language-specific init script or manual setup
→ See Quick Start above

**Monorepo (Multiple Packages)**
→ Set up Nx + pnpm workspaces
→ See [references/monorepo.md](references/monorepo.md)

### 2. Configure Git Hooks

**Automated setup:**
```bash
./scripts/setup_lefthook.sh
```

This configures:
- **commit-msg** - Conventional commits validation
- **pre-commit** - Format and lint staged files
- **pre-push** - Full validation (lint, type-check, test, build)

→ **See:** [references/git-hooks.md](references/git-hooks.md)

### 3. Set Up CI/CD

**Copy workflow templates:**
```bash
# Basic CI
cp assets/workflows/ci.yml .github/workflows/

# Language-specific workflows available in assets/
```

→ **See:** [references/ci-cd.md](references/ci-cd.md)

### 4. Configure Publishing (Optional)

**For npm packages:**
```bash
./scripts/setup_changesets.sh
```

Then copy publishing workflows from `assets/workflows/`.

→ **See:**
- [references/version-management.md](references/version-management.md)
- [references/publishing.md](references/publishing.md)

---

## Language-Specific Guides

### TypeScript/JavaScript

**Tooling options:**
- **Biome** - Fast, opinionated, all-in-one (recommended for new projects)
- **ESLint + Prettier** - Traditional, highly configurable (recommended for existing projects)

**Testing:**
- **Vitest** - Modern, fast, Vite-based (recommended)
- **Jest** - Established, widely used

**Key decisions:**
- Choose Biome for speed and simplicity
- Choose ESLint+Prettier for existing projects or specific plugins

→ **Full guide:** [references/typescript.md](references/typescript.md)

### Rust

**Built-in tools:**
- `rustfmt` - Code formatting
- `clippy` - Linting
- `cargo test` - Testing

**Enhanced tools:**
- `cargo-nextest` - Faster test runner
- `cargo-deny` - Dependency security
- `cargo-make` - Task runner

→ **Full guide:** [references/rust.md](references/rust.md)

### Python

**Modern stack (recommended):**
- **uv** - Fast package manager
- **ruff** - Fast linting + formatting (replaces black, isort, flake8)
- **mypy** - Type checking
- **pytest** - Testing

→ **Full guide:** [references/python.md](references/python.md)

---

## Git Hooks with lefthook

### Why lefthook?

- **Language-agnostic** - Works across TS, Rust, Python
- **Fast** - Parallel execution, written in Go
- **Simple** - Single YAML config
- **Better than Husky** - Faster, works across languages

### Setup

**Automated:**
```bash
./scripts/setup_lefthook.sh
```

**Manual:**
```bash
brew install lefthook
lefthook install
```

### Configuration Example

**lefthook.yml:**
```yaml
commit-msg:
  commands:
    commitlint:
      run: npx commitlint --edit {1}

pre-commit:
  parallel: true
  commands:
    format:
      glob: "*.{ts,rs,py}"
      run: format-staged-files {staged_files}
      stage_fixed: true

pre-push:
  commands:
    validate:
      run: ./scripts/validate_all.sh
```

→ **Full guide:** [references/git-hooks.md](references/git-hooks.md)

---

## Monorepo Management

### Nx + pnpm Workspaces

**Key principle:** Nx builds on top of pnpm, doesn't replace it.

- **pnpm workspaces** - Dependency management
- **Nx** - Task orchestration, caching, affected commands

### Benefits

- Run tasks only for affected packages
- Intelligent caching
- Parallel execution
- Supports multiple languages

### Common Commands

```bash
# Run target for all packages
nx run-many --target=build --all

# Run only for affected
nx affected --target=test

# Visualize dependencies
nx graph
```

→ **Full guide:** [references/monorepo.md](references/monorepo.md)

---

## Version Management & Publishing

### Changesets Workflow

**Recommended for monorepos and npm packages.**

1. **Add changeset:**
```bash
pnpm changeset
# Select packages, type (major/minor/patch), write summary
```

2. **Version packages:**
```bash
pnpm changeset version
# Updates package.json, generates CHANGELOG.md
```

3. **Publish:**
```bash
pnpm changeset publish
git push --follow-tags
```

### Automated Publishing

Use GitHub Actions to automate releases:

**Copy workflow:**
```bash
cp assets/workflows/publish-changesets.yml .github/workflows/
```

This creates "Version Packages" PR on main when changesets exist.

→ **See:**
- [references/version-management.md](references/version-management.md)
- [references/publishing.md](references/publishing.md)

---

## CI/CD Setup

### Match Local Validation

**Best practice:** Run same checks in CI as local pre-push hook.

**GitHub Actions templates:**
- `ci.yml` - Basic linting, testing, building
- `publish-npm.yml` - Automated npm publishing
- `publish-crates.yml` - Automated crates.io publishing
- `publish-pypi.yml` - Automated PyPI publishing

### Matrix Testing

Test across multiple versions:

```yaml
strategy:
  matrix:
    node-version: [18, 20, 21]
    os: [ubuntu-latest, macos-latest]
```

### Nx Monorepo CI

Use affected commands to only test changed packages:

```bash
nx affected --target=test
nx affected --target=build
```

→ **Full guide:** [references/ci-cd.md](references/ci-cd.md)

---

## Common Tasks

### Initialize TypeScript Project

**Automated:**
```bash
./scripts/init_typescript.sh --biome
# or
./scripts/init_typescript.sh --eslint-prettier
```

**Creates:**
- tsconfig.json (strict mode)
- Linting config (biome.json or eslint.config.js)
- Formatting config (.prettierrc.json if ESLint)
- Testing config (vitest.config.ts)
- Package.json scripts

### Set Up Git Hooks

```bash
./scripts/setup_lefthook.sh
```

**Configures:**
- Conventional commits validation
- Pre-commit: lint/format staged files
- Pre-push: full validation

### Configure Changesets

```bash
./scripts/setup_changesets.sh
```

**Sets up:**
- .changeset/ directory
- Package.json scripts
- Public access configuration

### Full Validation

```bash
./scripts/validate_all.sh
```

**Runs:**
- Format checking
- Linting
- Type checking
- Tests
- Builds

---

## Bundled Resources

### Scripts (`scripts/`)

**Setup scripts:**
- `init_typescript.sh` - Initialize TypeScript project
- `setup_lefthook.sh` - Configure Git hooks
- `setup_changesets.sh` - Set up version management
- `validate_all.sh` - Run all checks (used by pre-push)

**Usage:**
```bash
./scripts/script_name.sh
```

All scripts check if tools are installed/up-to-date before proceeding.

### Config Templates (`assets/configs/`)

**TypeScript:**
- `tsconfig.strict.json` - Strict TypeScript config
- `biome.json` - Biome configuration
- `eslint.config.js` - ESLint flat config
- `.prettierrc.json` - Prettier configuration

**Rust:**
- `rustfmt.toml` - Rustfmt configuration
- `clippy.toml` - Clippy lints
- `deny.toml` - Cargo-deny configuration

**Python:**
- `pyproject.toml` - ruff, mypy, pytest config
- `ruff.toml` - Standalone ruff config

**Monorepo:**
- `nx.json` - Nx configuration
- `pnpm-workspace.yaml` - pnpm workspaces

**Git Hooks:**
- `lefthook.yml` - Complete lefthook config
- `commitlint.config.js` - Conventional commits

**GitHub Workflows:**
- `ci.yml` - Basic CI
- `publish-changesets.yml` - Automated releases
- `publish-npm.yml` - npm publishing
- `publish-crates.yml` - crates.io publishing
- `publish-pypi.yml` - PyPI publishing

### Reference Documentation (`references/`)

**Language guides:**
- `typescript.md` - ESLint+Prettier vs Biome, testing, monorepo
- `rust.md` - rustfmt, clippy, cargo-nextest, cargo-deny
- `python.md` - ruff, mypy, pytest, uv vs poetry

**Infrastructure:**
- `monorepo.md` - Nx + pnpm workspaces setup
- `git-hooks.md` - lefthook configuration
- `ci-cd.md` - GitHub Actions workflows
- `publishing.md` - npm, crates.io, PyPI publishing
- `version-management.md` - Changesets workflow

---

## Best Practices

1. **Use lefthook over Husky** - Faster, language-agnostic
2. **Match CI and local** - Same checks in pre-push and CI
3. **Choose Biome for new TS projects** - Faster, simpler
4. **Use Nx affected commands** - Only test changed packages
5. **Automate versioning** - Use Changesets for npm packages
6. **Conventional commits** - Enables automated changelogs
7. **Pre-commit: staged files** - Fast feedback
8. **Pre-push: full validation** - Catch issues before pushing
9. **Type-check everything** - TypeScript, mypy, clippy
10. **Test before publish** - Always run tests in pre-publish

---

## Troubleshooting

### Hooks Not Running

**Check installation:**
```bash
lefthook install
ls -la .git/hooks/
```

**Test manually:**
```bash
lefthook run pre-commit
```

### Format Conflicts

**ESLint + Prettier conflicts:**
- Ensure `eslint-config-prettier` is last in config
- Run Prettier separately from ESLint

**Biome + Prettier conflicts:**
- Don't use both - choose one
- Biome is drop-in Prettier replacement

### CI Failures

**Debugging:**
1. Run `./scripts/validate_all.sh` locally
2. Check CI runs same commands
3. Verify Node/Rust/Python versions match
4. Check caching is working

---

## Quick Reference

**Setup new TypeScript project:**
```bash
./scripts/init_typescript.sh
```

**Setup Git hooks:**
```bash
./scripts/setup_lefthook.sh
```

**Setup Changesets:**
```bash
./scripts/setup_changesets.sh
```

**Run full validation:**
```bash
./scripts/validate_all.sh
```

**Common commands:**
```bash
# TypeScript
npm run lint && npm run type-check && npm test

# Rust
cargo fmt -- --check && cargo clippy -- -D warnings && cargo test

# Python
ruff check . && mypy . && pytest

# Monorepo
nx affected --target=test
nx run-many --target=build --all

# Changesets
pnpm changeset
pnpm changeset version
pnpm changeset publish
```

---

## Getting Help

- **TypeScript:** See [references/typescript.md](references/typescript.md)
- **Rust:** See [references/rust.md](references/rust.md)
- **Python:** See [references/python.md](references/python.md)
- **Monorepo:** See [references/monorepo.md](references/monorepo.md)
- **Git Hooks:** See [references/git-hooks.md](references/git-hooks.md)
- **CI/CD:** See [references/ci-cd.md](references/ci-cd.md)
- **Publishing:** See [references/publishing.md](references/publishing.md) and [references/version-management.md](references/version-management.md)
