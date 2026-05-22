---
name: code-review
description: Review code changes for quality, security, and adherence to project standards
user-invocable: true
---

You are helping the user review code for quality and adherence to Jocko Fuel coding standards.

Follow these steps:

### Step 1: Identify What to Review

Ask the user what to review:
- **Staged changes** — review `git diff --staged`
- **Branch diff** — review changes on current branch vs main
- **Specific files** — review named files
- **Pull request** — review a PR by number

### Step 2: Read the Code

Read the files or diffs identified in Step 1. For each file, check against the project's coding standards from `CLAUDE.md` and `.claude/rules/`:

**Code Quality**
- ABOUTME headers on all source files
- No temporal naming (NEW_, V2_, UPDATED_)
- Smallest reasonable changes
- No unnecessary complexity or over-engineering
- Proper error handling at system boundaries

**Security**
- No hardcoded credentials, API keys, or secrets
- No command injection, XSS, or SQL injection vectors
- Input validation at system boundaries
- No sensitive data in URL parameters or logs

**Style**
- Matches surrounding code style
- Names describe purpose, not implementation
- Comments explain what/why, not how it changed

**Testing**
- New functionality has corresponding tests
- Tests validate real behavior, not mocked behavior
- Test output is clean

### Step 3: Present Findings

Organize findings by severity:

**Must Fix** — Blocking issues (security vulnerabilities, broken functionality, rule violations)

**Should Fix** — Quality issues (naming, missing tests, complexity)

**Nit** — Style suggestions (formatting, minor improvements)

For each finding, include the file path, line number, and a specific suggestion.

### Step 4: Summary

Provide an overall assessment: Approve, Request Changes, or Needs Discussion. Include a brief rationale.

### Error Handling

- If no changes are found, inform the user and suggest what to review
- If git commands fail (not in a repo), offer to review specific files instead
