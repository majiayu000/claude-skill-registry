---
name: detect-code-smells
description: "Identify code quality issues and anti-patterns. Use when reviewing code for maintainability problems."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Detect Code Smells

Identify code quality issues, anti-patterns, and maintainability problems that suggest need for refactoring.

## When to Use

- Code review before merging
- Identifying refactoring priorities
- Mentoring and code quality improvement
- Planning technical debt reduction

## Quick Reference

```bash
# Python code smell detection
pip install pylint radon
pylint --disable=all --enable=convention,refactor module.py
radon cc -a module.py  # Cyclomatic complexity
radon mi -s module.py  # Maintainability index
```

## Workflow

1. **Scan for patterns**: Identify common code smell patterns (long functions, duplication, magic numbers)
2. **Check complexity**: Measure cyclomatic and cognitive complexity
3. **Evaluate naming**: Check for unclear variable/function names
4. **Review structure**: Identify violations of SOLID principles
5. **Document findings**: List smells with severity and recommendations

## Output Format

Code quality report:

- Code smell type (duplication, long method, magic number, etc.)
- Location (file:line)
- Severity (critical/high/medium/low)
- Explanation of the issue
- Suggested fix or refactoring approach

## References

- See CLAUDE.md > SOLID principles for design guidance
- See CLAUDE.md > DRY and KISS principles for quality standards
- See `refactor-code` skill for applying fixes
