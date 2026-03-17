---
name: run-precommit
description: Run pre-commit hooks locally or in CI to validate code quality before committing. Use to ensure commits meet quality standards and CI will pass.
mcp_fallback: none
category: ci
user-invocable: false
---

# Run Pre-commit Hooks Skill

Validate code quality with pre-commit hooks before committing.

## When to Use

- Before committing code
- Testing if CI will pass
- After making code changes
- Troubleshooting commit failures

## Quick Reference

```bash
# Install hooks (one-time)
pixi run pre-commit install

# Run on all files
just pre-commit-all

# Run on staged files
just precommit

# NEVER use --no-verify to bypass hooks
# Fix the code instead to pass hooks

# If a specific hook is broken (not your code):
SKIP=hook-name git commit -m "message"  # Document why in message
```

## Configured Hooks

| Hook | Purpose | Auto-Fix |
|------|---------|----------|
| `mojo-format` | Format Mojo code | Yes |
| `trailing-whitespace` | Remove trailing spaces | Yes |
| `end-of-file-fixer` | Add final newline | Yes |
| `check-yaml` | Validate YAML syntax | No |
| `check-added-large-files` | Prevent large files | No |
| `mixed-line-ending` | Fix line endings | Yes |

## Workflow

```bash
# 1. Make changes
# ... edit files ...

# 2. Run hooks on staged files
just precommit

# 3. If hooks auto-fixed files
git add .              # Stage fixed files
git commit -m "feat: feature name"

# 4. If hooks reported errors
# Fix issues manually, then re-commit
```

## Hook Behavior

### Auto-Fix Hooks

These hooks fix issues automatically:

```bash
git commit -m "message"
# Hooks run, fix files, abort commit
# Files are fixed but not staged

git add .              # Stage fixes
git commit -m "message"  # Commit again
```

### Check-Only Hooks

These hooks report but don't fix:

```bash
git commit -m "message"
# check-yaml fails - fix manually

# Fix YAML syntax
git add .
git commit -m "message"
```

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| "Trailing whitespace" | Spaces at line end | Run hooks again (auto-fixed) |
| "Check YAML failed" | Invalid YAML syntax | Fix YAML manually |
| "Large file rejected" | File > 1MB | Use Git LFS or remove file |
| "Mixed line ending" | Inconsistent line endings | Run hooks again (auto-fixed) |

## Setup

```bash
# Install pre-commit (first time)
pip install pre-commit

# Install hooks (first time)
pre-commit install

# Hooks now run automatically on commit
```

## CI Integration

Pre-commit runs in GitHub Actions:

```yaml
jobs:
  precommit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pre-commit
      - run: just pre-commit-all
```

## Advanced Usage

```bash
# Run specific hook only
pixi run pre-commit trailing-whitespace --all-files

# Run on specific file
pixi run pre-commit --files src/tensor.mojo

# Update hook versions
pixi run pre-commit autoupdate

# Skip a specific broken hook (document reason in commit message)
SKIP=hook-name git commit -m "fix: reason for skipping hook-name"

# NEVER use --no-verify to skip all hooks
```

## Error Handling

| Issue | Solution |
|-------|----------|
| Hooks not installed | Run `pre-commit install` |
| Hooks not running | Verify `.pre-commit-config.yaml` exists |
| All files modified after hook | Stage fixes and re-commit |
| Need to skip hook | Use `SKIP=hook-id git commit` |

## Hook Bypass Policy

**STRICT POLICY: `--no-verify` is PROHIBITED.**

**Why this matters:**

- Pre-commit hooks catch errors before they reach CI
- Bypassing hooks allows broken code into the repository
- CI will reject commits that bypass hooks anyway

**What to do when hooks fail:**

1. ✅ **Read the error** - Hook output explains what's wrong
2. ✅ **Fix your code** - Update to pass the check
3. ✅ **Re-run hooks** - Verify with `pre-commit run`
4. ✅ **Commit again** - Let hooks validate

**Exception for broken hooks:**

If the hook itself is broken (not your code), use `SKIP=hook-id`:

```bash
# Example: trailing-whitespace hook is broken
SKIP=trailing-whitespace git commit -m "fix: skip broken hook (see issue #123)"
```

**Never acceptable:**

- ❌ `git commit --no-verify`
- ❌ `git commit -n`
- ❌ Bypassing all hooks

## References

- [Git Commit Policy](../../shared/git-commit-policy.md) - Strict enforcement rules
- Configuration: `.pre-commit-config.yaml`
- Related skill: `quality-fix-formatting` for manual fixes
- Related skill: `quality-run-linters` for all linters
