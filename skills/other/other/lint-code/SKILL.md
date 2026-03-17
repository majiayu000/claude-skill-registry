---
name: lint-code
description: "Check code for style and quality issues. Use when validating code before commits."
mcp_fallback: none
category: analysis
tier: 1
user-invocable: false
---

# Lint Code

Run linting tools to identify style issues, potential bugs, and code quality problems in source files.

## When to Use

- Pre-commit code validation
- Finding simple mistakes (unused variables, typos)
- Enforcing style consistency
- Quick code review before merging

## Quick Reference

```bash
# Python linting
pylint module.py
flake8 .
black --check .  # Format checker

# Mojo formatting (enforced by pre-commit)
pixi run mojo format file.mojo

# All linters via pixi
pixi run quality-run-linters
```

## Workflow

1. **Select linters**: Choose appropriate tools (pylint, flake8, black, etc.)
2. **Run checks**: Execute linters on code
3. **Review issues**: Analyze warnings and errors
4. **Fix problems**: Address high-priority issues
5. **Verify fixes**: Re-run linters to confirm

## Output Format

Lint report:

- File path and line number
- Issue type (style, convention, error, warning)
- Issue description
- Suggested fix or reference
- Severity level

## References

- See CLAUDE.md > Pre-commit Hooks for automated checking
- See `quality-run-linters` skill for comprehensive linting
- See quality standards in CLAUDE.md for project guidelines
