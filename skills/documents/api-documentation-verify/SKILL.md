---
name: api-documentation-verify
description: Verifies API documentation against source code to eliminate fabricated claims, ensure accuracy, and validate examples. Zero tolerance for unverified claims, marketing language, or non-runnable code examples. Use before committing API docs or during documentation reviews.
version: 1.0.0
---

# API Documentation Verification Skill

## Purpose

Verify API documentation accuracy against source code. This skill eliminates fabricated API methods, unverified performance claims, non-runnable code examples, and marketing language. Every documented feature must exist in the codebase.

## Quick Start

Use this skill to verify:

- **API methods** exist with correct signatures
- **Code examples** are runnable and accurate
- **Performance claims** have benchmark support
- **Configuration options** match source code
- **Error documentation** matches thrown errors
- **Marketing language** is removed
- **Dependencies** match package.json

## Verification Categories (Summary)

### CRITICAL (Must Fix Before Commit)

- **API Method Existence**: Every documented method must exist in source with exact signature
- **Parameter/Return Types**: Types must exactly match implementation (no guessing)
- **Code Examples**: All examples must be runnable with proper imports and error handling
- **Performance Claims**: ZERO tolerance for unverified claims - require benchmarks

### HIGH (Should Fix Soon)

- **Configuration**: Documented options must exist with correct field names
- **Error Documentation**: All thrown errors must be documented

### MEDIUM (Nice to Have)

- **Marketing Language**: Remove buzzwords (blazing-fast, revolutionary, enterprise-grade)
- **Dependency Versions**: Match package.json exactly

**For detailed checks with examples and verification patterns:**

```
Read `~/.claude/skills/api-documentation-verify/references/VERIFICATION-CHECKS.md`
```

Use when: Need specific verification patterns, examples of good/bad documentation, or detailed check descriptions

---

## Execution Process (Summary)

### Core Steps

1. **Identify Documentation**: Find all .md files, README, DOCS, API files
2. **Extract Claims**: Methods, examples, config, performance claims
3. **Verify Against Source**: Compare documented vs actual (read source files)
4. **Check Marketing Language**: Scan for banned words/phrases
5. **Generate Report**: CRITICAL/HIGH/MEDIUM issues with line numbers
6. **Provide Corrections**: Show correct versions for critical issues
7. **Summary Statistics**: Count issues, verified items

**For detailed execution steps with bash commands and report formats:**

```
Read `~/.claude/skills/api-documentation-verify/references/EXECUTION-STEPS.md`
```

Use when: Performing verification, need bash commands, or want detailed report format templates

---

## LEGACY CONTENT TO REMOVE

## Integration Points

This skill can be invoked:

- **Manually** when reviewing documentation
- **Before commits** that modify documentation
- **In CI/CD** as documentation linting step
- **Before releases** to ensure doc accuracy

## Exit Criteria

- All API methods verified against source code
- All code examples validated for runnability
- All performance claims checked for benchmark support
- All configuration options verified
- All errors documented
- Marketing language flagged
- Report generated with specific line numbers
- CRITICAL issues should block documentation commits

## Example Usage

```bash
# Manual invocation
/skill api-documentation-verify

# Verify specific doc file
/skill api-documentation-verify README.md

# Verify all docs in directory
/skill api-documentation-verify docs/
```

## Automation Opportunities

This skill can be automated in CI/CD:

```yaml
# .github/workflows/docs-verify.yml
name: Verify Documentation

on:
  pull_request:
    paths:
      - "**.md"
      - "docs/**"

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Verify API Documentation
        run: |
          # Run skill via Claude Code API
          claude-code skill api-documentation-verify
```

## References

- Diátaxis Framework: https://diataxis.fr/
- Technical Documentation Expert Agent
- Good Docs Project: https://thegooddocsproject.dev/
- API Documentation Best Practices: https://swagger.io/resources/articles/best-practices-in-api-documentation/

---

## Related Agent

For comprehensive documentation guidance that coordinates this and other documentation skills, use the **`documentation-coordinator`** agent.
