---
name: self-check
description: Pre-commit self-validation for code quality and security
allowed-tools: Read, Grep, Glob, Bash(git:*)
---

# Pre-Commit Self-Check

Validate your changes before committing to ensure code quality and security standards are met.

## Purpose

This skill performs a comprehensive self-check on staged changes to catch issues before they are committed. It combines code quality checks with security validation.

## What It Checks

### 1. Code Quality
- Syntax errors in changed files
- Linting issues (if linter available)
- Type errors (if type checker available)
- Test coverage for new code

### 2. Security
- Hardcoded credentials
- Injection vulnerabilities
- Insecure dependencies
- Debug code and TODO comments

### 3. Git Hygiene
- Commit message format
- No large binary files
- No merge conflict markers
- No unresolved TODOs marked as blockers

## Usage

```
/self-check
```

Run this skill before `git commit` to validate your changes.

## Process

1. **Identify Changes**: Get list of staged files
2. **Syntax Check**: Ensure code parses correctly
3. **Security Scan**: Check for common vulnerabilities
4. **Quality Check**: Run available linters
5. **Report**: Summarize findings with actionable items

## Output Format

```
=== Self-Check Results ===

Staged Files: 5
  - src/handler.py
  - src/utils.py
  - tests/test_handler.py
  - package.json
  - README.md

[PASS] Syntax Check: All files parse correctly
[FAIL] Security Check: 2 issues found
  - src/handler.py:25 - Potential SQL injection
  - src/utils.py:10 - Hardcoded password

[PASS] Quality Check: No linting errors
[WARN] Coverage: New code in handler.py not covered by tests

Recommendation: Fix security issues before committing
```

## Exit Codes

- **0**: All checks passed
- **1**: Security issues found (blocking)
- **2**: Quality issues found (warning)

## Integration

This skill should be run:
1. Before every commit
2. As part of the remediation loop
3. When requested by the orchestrator
