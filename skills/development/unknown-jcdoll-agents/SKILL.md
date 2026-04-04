---
name: code-review
description: Reviews code for quality, security, and maintainability. Use after implementing features, completing significant work, or when user asks for code review.
targets: ["*"]
claudecode:
  allowed-tools: ["Read", "Grep", "Glob", "Bash"]
codexcli:
  allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Code Review

## Instructions

1. Run `git diff` to identify changed files
2. Read modified files to understand the intent of changes
3. Review against the checklist below
4. Provide structured feedback organized by priority

## Review Checklist

### Security
- No exposed credentials, API keys, or secrets
- Input validation implemented where needed
- File paths are sanitized (no path traversal)
- External commands are safely constructed (no injection)

### Code Quality
- Variables and functions are clearly named
- Functions have single responsibility
- No code duplication (DRY principle)
- Complex logic has explanatory comments
- Error handling is comprehensive
- No unused imports or variables
- Clean separation of concerns

### Parameters
- Use enums rather than bare strings for parameters
- Do not spread "magic strings" throughout the code, use a single source of truth for parameter defaults (config.py)
- Do not use the "if (check config) then (value = from config) else (value = default)" pattern - this breaks the single source of truth rule

### Python Specific
- Type hints used appropriately
- Exceptions are specific (not bare `except:`)
- Context managers used for resources
- f-strings preferred over `.format()` or `%`

### Testing
- New functionality has test coverage
- Edge cases are tested
- Error conditions are tested
- Tests are readable and maintainable

### Project Standards
- Code passes `ruff` linting
- No legacy wrappers or thin compatibility layers
- No "last updated" dates or copyright headers

## Output Format

Organize feedback by severity:

### Critical (must fix)
- Security issues
- Bugs that will cause failures
- Include specific line numbers and suggested fixes

### Warnings (should fix)
- Code quality issues
- Missing error handling
- Potential edge cases
- Include rationale and improvement suggestions

### Suggestions (consider)
- Style improvements
- Minor optimizations
- Include brief explanation of benefit
