---
name: mojo-format
description: "Format Mojo code using mojo format command. Use when preparing code for commit or when formatting checks fail."
mcp_fallback: none
category: mojo
agent: test-engineer
user-invocable: false
---

# Mojo Format Skill

Format Mojo code files to ensure consistent style.

## When to Use

- Preparing code for commit
- Pre-commit hook reports formatting issues
- Code review requests formatting fixes
- Verifying formatting compliance

## Quick Reference

```bash
# Format single file
pixi run mojo format path/to/file.mojo

# Format directory
pixi run mojo format `find src/ -name "*.mojo"`

# Check without modifying
pixi run mojo format --check path/to/file.mojo
```

## Workflow

1. **Identify files** - Single file or directory
2. **Run formatter** - `pixi run mojo format <path>`
3. **Verify changes** - Review formatted output
4. **Commit** - Stage and commit formatted code

## Mojo-Specific Notes

- Formats indentation (4 spaces), line length, spacing around operators
- Does NOT change logic, variable names, or comment content
- Preserves all comments, only adjusts spacing
- Safe to run multiple times (idempotent)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Syntax error` | Invalid Mojo syntax | Fix syntax before formatting |
| `File not found` | Wrong path | Verify file exists |
| `Permission denied` | File permissions | Check `chmod` settings |
| `Mojo not installed` | Missing Mojo | Install via `pixi` or Magic |

## References

- `.claude/shared/mojo-guidelines.md` - Mojo syntax standards
- `.pre-commit-config.yaml` - Pre-commit hook configuration
