---
name: quality-run-linters
description: Run all configured linters including mojo format, markdownlint, and pre-commit hooks. Use before committing code to ensure quality standards are met.
mcp_fallback: none
category: quality
agent: test-engineer
user-invocable: false
---

# Run Linters Skill

Run all configured linters to ensure code quality.

## When to Use

- Before committing code
- CI/CD quality checks
- Pre-PR validation
- Troubleshooting quality issues

## Quick Reference

```bash
# Run all linters
./scripts/run_all_linters.sh

# Check mode (no fixes)
./scripts/run_all_linters.sh --check

# Fix mode
./scripts/run_all_linters.sh --fix

# Specific linter
./scripts/run_linters.sh --mojo
```

## Configured Linters

| Linter | Purpose | Auto-Fix |
|--------|---------|----------|
| `mojo-format` | Format Mojo code | Yes |
| `markdownlint` | Lint markdown files | Partial |
| `pre-commit` | Multiple checks | Yes (most) |

### Pre-commit Hooks

- `trailing-whitespace` - Remove trailing spaces (Yes)
- `end-of-file-fixer` - Add final newline (Yes)
- `check-yaml` - Validate YAML syntax (No)
- `check-added-large-files` - Prevent large files (No)
- `mixed-line-ending` - Fix line endings (Yes)

## Workflow

```bash
# 1. Run all linters
./scripts/run_all_linters.sh

# 2. Review output
# Check which issues found

# 3. Fix issues
# Most auto-fixed, some need manual fixes

# 4. Stage changes
git add .

# 5. Commit
git commit -m "fix: address linting issues"
```

## Common Issues

| Error | Linter | Fix |
|-------|--------|-----|
| "MD040" | markdownlint | Add language to code block |
| "MD031" | markdownlint | Add blank lines around block |
| "Trailing whitespace" | pre-commit | Auto-fixed, re-commit |
| "YAML error" | check-yaml | Fix YAML syntax manually |

## Linter Details

### Mojo Format

Checks: indentation, spacing, line length, operators, blank lines

```bash
pixi run mojo format src/tensor.mojo        # Fix
pixi run mojo format --check src/tensor.mojo  # Check only
```

### Markdownlint

Checks: code block languages, blank lines, line length, heading style

```bash
npx markdownlint-cli2 "**/*.md"        # Check
npx markdownlint-cli2 --fix "**/*.md"  # Fix auto-fixable
```

### Pre-commit

Checks: trailing whitespace, file endings, YAML syntax, large files, line endings

```bash
just pre-commit-all        # Run all
pixi run pre-commit trailing-whitespace --all-files  # Specific
```

## CI Integration

Linters run automatically in GitHub Actions:

```yaml
- name: Run Linters
  run: |
    just pre-commit-all
```

## Workflow Integration

### Before Commit

```bash
./scripts/run_all_linters.sh
git add .
git commit -m "message"
```

### Pre-commit Hook (Automatic)

```bash
git commit -m "message"
# Hooks run, fix issues if needed
# If fixed, re-commit
git add .
git commit -m "message"
```

### Before PR

```bash
./scripts/run_all_linters.sh --check
git add .
git commit -m "fix: address linting issues"
gh pr create --issue 42
```

## Error Handling

| Error | Solution |
|-------|----------|
| "Linter not found" | Install tool or check PATH |
| "Syntax error" | Fix code before running linter |
| "False positive" | Check configuration files |
| "Permission denied" | Check file permissions |

## Configuration Files

- `.pre-commit-config.yaml` - Pre-commit hooks
- `.markdownlint.yaml` - Markdown rules
- Mojo built-in formatting (no config)

## Best Practices

1. **Run before commit** - Always check locally first
2. **Auto-fix when possible** - Use fix mode to save time
3. **Understand errors** - Don't blindly fix without understanding
4. **Keep updated** - Update linter versions regularly
5. **CI enforcement** - Ensure CI runs all linters

## References

- Configuration: `.pre-commit-config.yaml`, `.markdownlint.yaml`
- Related skill: `quality-fix-formatting` for manual fixes
- Related skill: `run-precommit` for pre-commit details
