---
name: lint-service
description: Unified linting scripts for all services in the monorepo. Use when the user wants to lint code, check formatting, or run type checks.
---

# Lint Service Skill

Unified linting scripts for all services in the Saturn's Oracle monorepo.

## Services

### TypeScript (2 services)
- apollos-ui
- polling-service

### Python (3 services)
- mercury-clustering
- terra-local-gpu
- apollo-video-distillation

### Rust (3 services)
- flora-clustering-rust
- hercules-local-algo
- vulcan-gpu-sdk (also has Python)

## Usage

### From Anywhere in the Repo

```bash
# TypeScript
.claude/skills/lint-service/lint-typescript.sh apollos-ui
.claude/skills/lint-service/lint-typescript.sh apollos-ui --staged-only

# Python
.claude/skills/lint-service/lint-python.sh mercury-clustering
.claude/skills/lint-service/lint-python.sh terra-local-gpu --staged-only

# Rust
.claude/skills/lint-service/lint-rust.sh flora-clustering-rust
.claude/skills/lint-service/lint-rust.sh hercules-local-algo --staged-only
```

### What Each Script Does

**lint-typescript.sh:**
- ESLint with --max-warnings=-1 (errors only)
- TypeScript type checking (tsc --noEmit)
- Staged-only: Lints only staged .ts/.tsx files

**lint-python.sh:**
- Ruff check (linting)
- Ruff format --check (formatting)
- mypy (type checking, full mode only)
- Staged-only: Lints only staged .py files

**lint-rust.sh:**
- cargo clippy (linting)
- cargo fmt --check (formatting)
- cargo test (only in CI, not precommit)
- Staged-only: Skips if no .rs files staged

## Exit Codes

- 0: Success
- 1: Linting failed (blocking)

## Integration

These scripts are called by:
1. **Precommit hook** (.husky/pre-commit) with --staged-only
2. **GitHub Actions** (without --staged-only, full service)
3. **Manual invocation** by developers or Claude

## Examples

### Lint all Python services
```bash
for service in mercury-clustering terra-local-gpu apollo-video-distillation; do
  .claude/skills/lint-service/lint-python.sh $service
done
```

### Lint only staged files in current service
```bash
# If working in apollos-ui
.claude/skills/lint-service/lint-typescript.sh apollos-ui --staged-only
```

### Check if linting will pass before committing
```bash
# TypeScript
.claude/skills/lint-service/lint-typescript.sh apollos-ui --staged-only

# Python
.claude/skills/lint-service/lint-python.sh mercury-clustering --staged-only

# Rust
.claude/skills/lint-service/lint-rust.sh flora-clustering-rust --staged-only
```

## Linting Config Location

All services extend root configs:
- **Python**: `/pyproject.toml` (ruff + mypy)
- **Rust**: `/rustfmt.toml` + `/.clippy.toml`
- **TypeScript**: `/.eslintrc.monorepo.js`

Services can override with local configs if needed.

## Auto-fix Commands

If linting fails, use these commands to auto-fix:

**TypeScript:**
```bash
cd apollos-ui
pnpm lint:fix
```

**Python:**
```bash
cd mercury-clustering
uv run ruff check --fix .
uv run ruff format .
```

**Rust:**
```bash
cd flora-clustering-rust
cargo fmt --all
cargo clippy --all-targets --all-features --fix
```
