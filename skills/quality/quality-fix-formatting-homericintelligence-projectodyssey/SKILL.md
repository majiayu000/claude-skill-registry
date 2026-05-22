---
name: quality-fix-formatting
description: Automatically fix code formatting issues using mojo format, markdownlint, and pre-commit hooks. Use when formatting checks fail or before committing code.
mcp_fallback: none
category: quality
agent: test-engineer
user-invocable: false
---

# Fix Formatting Skill

Automatically fix code formatting issues across file types.

## When to Use

- Pre-commit checks fail due to formatting
- Before committing code
- After writing new code
- CI formatting checks fail

## Quick Reference

```bash
# Fix everything
./scripts/fix_all_formatting.sh

# Fix specific types
pixi run mojo format src/**/*.mojo
npx markdownlint-cli2 --fix "**/*.md"
just pre-commit-all
```

## Auto-Fix Capabilities

| Tool | Coverage | Manual Fixes |
|------|----------|--------------|
| pixi run mojo format | 100% | None |
| markdownlint | 70% | Language tags, line length |
| pre-commit | 100% | None |

## Formatting Tools

### Mojo Code (100% auto-fix)

```bash
# Format all Mojo files
pixi run mojo format src/**/*.mojo

# Format single file
pixi run mojo format src/tensor.mojo

# Check without fixing
pixi run mojo format --check src/**/*.mojo
```

Fixes: indentation, spacing, line wrapping, blank lines

### Markdown (Partial auto-fix)

```bash
# Fix markdown issues
npx markdownlint-cli2 --fix "**/*.md"

# Check only
npx markdownlint-cli2 "**/*.md"
```

Auto-fixes: blank lines, spacing
Manual fixes: language tags, line length

### Pre-commit Hooks (100% auto-fix)

```bash
# Run hooks on changed files
just pre-commit

# Run hooks on all files
just pre-commit-all
```

Auto-fixes: trailing whitespace, missing newlines, line endings, YAML

## Workflow

```bash
# 1. Fix all formatting
./scripts/fix_all_formatting.sh

# 2. Review changes
git diff

# 3. Stage changes
git add .

# 4. Commit
git commit -m "fix: apply code formatting"
```

## Common Fixes

### Before/After: Mojo

```mojo
# Before
fn add(x:Int,y:Int)->Int:
    return x+y

# After
fn add(x: Int, y: Int) -> Int:
    return x + y
```

### Before/After: Markdown

**Before**: Code block immediately follows text without blank line.

**After**: Add blank line before opening fence and after closing fence.

### Before/After: Whitespace

**Before** (trailing spaces):

```text
line with trailing spaces
another line
```

**After** (no trailing spaces):

```text
line with trailing spaces
another line
```

## Manual Fixes Required

Some issues need manual intervention:

### Markdown Language Tags

**Before** (no language tag):

````text
```
code here
```
````

**After** (with language tag):

````text
```python
code here
```
````

### Line Length

```markdown
# Too long (break manually at 120 chars)
This is a very long line that exceeds 120 characters and should be
manually broken into multiple lines for readability.
```

## Scripts Available

- `scripts/fix_all_formatting.sh` - Fix everything
- `scripts/fix_formatting.sh --mojo` - Mojo only
- `scripts/fix_formatting.sh --markdown` - Markdown only
- `scripts/fix_formatting.sh --precommit` - Pre-commit only

## CI Integration

CI checks formatting but doesn't fix:

```yaml
- name: Check Formatting
  run: |
    pixi run mojo format --check src/**/*.mojo
    npx markdownlint-cli2 "**/*.md"
```

Fix locally and push if CI fails.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "Syntax error" | Invalid Mojo code | Fix syntax before formatting |
| "Permission denied" | File permissions | Check file ownership |
| "Merge conflict" | Merge markers present | Resolve conflicts first |

## Best Practices

1. **Fix before commit** - Always format before committing
2. **Use pre-commit hooks** - Let hooks auto-fix
3. **Review changes** - Check what was formatted
4. **Separate commits** - Format in separate commit if large changes
5. **NEVER bypass hooks** - Using `--no-verify` is strictly prohibited. If formatting fails, fix the code instead of
   bypassing the check.

## References

- [Git Commit Policy](../../shared/git-commit-policy.md) - Hook bypass prohibition
- Configuration: `.pre-commit-config.yaml`, `.markdownlint.yaml`
- Related skill: `run-precommit` for pre-commit hooks
- Related skill: `quality-run-linters` for complete linting
