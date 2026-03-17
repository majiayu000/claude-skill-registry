# YAML Configuration Skill

## Purpose

Master YAML syntax for GitHub Actions workflows, avoiding common pitfalls and special character issues.

## YAML Syntax Rules

### Special Characters That Cause Errors

**Reserved Characters**: `<`, `>`, `&`, `|`, `:`, `{`, `}`, `[`, `]`, `!`, `%`, `@`, `` ` ``, `*`, `?`

**Fix**: Quote strings containing these characters

```yaml
# ❌ WRONG - Causes syntax error
- name: Check size (<200 lines)
- name: Email: test@example.com
- name: 100% coverage

# ✅ CORRECT - Quoted
- name: "Check size (<200 lines)"
- name: "Email: test@example.com"
- name: "100% coverage"

# ✅ ALSO CORRECT - Reworded (no special chars)
- name: Check size (under 200 lines)
- name: Contact test at example.com
- name: Full coverage
```

### String Quoting Rules

```yaml
# Simple strings (no special chars)
name: Simple workflow
description: This is fine

# Strings with colons
title: "Bug: Fix login error"  # MUST quote

# Strings with special chars
message: "Size <200 lines is ideal"  # MUST quote
email: "user@example.com"  # MUST quote

# Numbers as strings
version: "1.0"  # Quote to prevent interpretation as number
node-version: '18'  # Quote for consistency
```

### Multi-Line Strings

```yaml
# Literal block (| preserves newlines and formatting)
script: |
  echo "Line 1"
  echo "Line 2"
  npm test

# Folded block (> folds into single line)
description: >
  This is a long description
  that will be folded into
  a single line.

# Result: "This is a long description that will be folded into a single line."
```

### Lists

```yaml
# Block style (preferred)
branches:
  - main
  - develop
  - staging

# Flow style (inline)
branches: [main, develop, staging]

# Mixed (avoid - inconsistent)
branches:
  - main
  - [develop, staging]  # Don't do this
```

### Objects

```yaml
# Block style
env:
  NODE_VERSION: '18'
  CI: true
  API_URL: https://api.example.com

# Flow style (inline)
env: {NODE_VERSION: '18', CI: true}

# Nested objects
config:
  database:
    host: localhost
    port: 5432
  cache:
    enabled: true
```

## Common YAML Errors

### Error 1: Unquoted Colon
```yaml
# ❌ ERROR
- name: Note: This is important

# ✅ FIX
- name: "Note: This is important"
```

### Error 2: Unquoted Angle Brackets
```yaml
# ❌ ERROR
- name: Check if value <200

# ✅ FIX
- name: "Check if value <200"
- name: Check if value under 200
```

### Error 3: Unquoted @ Symbol
```yaml
# ❌ ERROR
email: test@example.com

# ✅ FIX
email: "test@example.com"
```

### Error 4: Incorrect Indentation
```yaml
# ❌ ERROR - jobs should be at root level
name: Test
  jobs:
    test:
      runs-on: ubuntu-latest

# ✅ CORRECT
name: Test
jobs:
  test:
    runs-on: ubuntu-latest
```

### Error 5: Mixing Tabs and Spaces
```yaml
# ❌ ERROR - YAML requires spaces, not tabs
jobs:
	test:  # Tab used here
	  runs-on: ubuntu-latest

# ✅ CORRECT - Use spaces only
jobs:
  test:  # 2 spaces
    runs-on: ubuntu-latest  # 4 spaces
```

## Validation Tools

```bash
# Validate YAML syntax
yamllint .github/workflows/workflow.yml

# GitHub CLI validation
gh workflow view workflow.yml

# Online validators
# - https://www.yamllint.com/
# - https://yaml-online-parser.appspot.com/

# Test workflow locally (requires act)
act -n  # Dry run
act push  # Simulate push event
```

## Best Practices

### ✅ Do
- Quote strings with special characters
- Use 2-space indentation consistently
- Validate YAML before committing
- Use meaningful names for jobs and steps
- Comment complex workflow logic
- Use literal blocks (`|`) for multi-line scripts

### ❌ Don't
- Use tabs for indentation
- Mix quoting styles inconsistently
- Leave unquoted special characters
- Use overly complex nested structures
- Forget to validate syntax

## Project-Specific Patterns

### Music-App Workflow Example
```yaml
name: Music-App CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js 18
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests with coverage
        run: npm test -- --coverage --watchAll=false
        env:
          CI: true

      - name: Build production bundle
        run: npm run build
```

## Common Issues

**Issue**: "Invalid workflow file" on line X
**Solution**: Check for unquoted special characters, incorrect indentation, missing quotes

**Issue**: "Unexpected value" error
**Solution**: Check for typos in keys (`on` not `in`, `runs-on` not `run-on`)

**Issue**: Workflow runs but fails
**Solution**: Not a YAML issue - debug the actual command or script

## Resources

- **YAML Specification**: https://yaml.org/spec/
- **GitHub Actions Syntax**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- **YAML Lint**: https://www.yamllint.com/
