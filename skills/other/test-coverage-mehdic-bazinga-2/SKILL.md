---
name: test-coverage
description: "Generate comprehensive test coverage reports when reviewing code. Identifies untested code paths and low-coverage areas. Supports Python (pytest-cov), JavaScript (jest), Go (go test -cover), Java (JaCoCo). Use when reviewing tests or before approving code changes."
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Test Coverage Analysis Skill

You are the test-coverage skill. When invoked, you run appropriate coverage tools based on project language and generate structured coverage reports.

## When to Invoke This Skill

**Invoke this skill when:**
- Tech Lead is reviewing test files
- Before approving code changes or pull requests
- Developer claims "added tests"
- Before merging to main branch
- Checking if coverage meets project standards

**Do NOT invoke when:**
- No tests exist in the project
- Just viewing code (not reviewing for approval)
- Emergency hotfix (skip coverage check)
- Documentation-only changes

---

## Your Task

When invoked:
1. Execute the test coverage script
2. Read the generated coverage report
3. Return a summary to the calling agent

---

## Step 1: Execute Coverage Script

Use the **Bash** tool to run the pre-built coverage script.

**On Unix/macOS:**
```bash
bash .claude/skills/test-coverage/scripts/coverage.sh
```

**On Windows (PowerShell):**
```powershell
pwsh .claude/skills/test-coverage/scripts/coverage.ps1
```

> **Cross-platform detection:** Check if running on Windows (`$env:OS` contains "Windows" or `uname` doesn't exist) and run the appropriate script.

This script will:
- Detect project language (Python, JavaScript, Go, Java)
- Auto-install required tools (pytest-cov, jest, etc.) if needed
- Run coverage analysis
- Parse results
- Generate `bazinga/artifacts/{SESSION_ID}/skills/coverage_report.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read:

```bash
bazinga/artifacts/{SESSION_ID}/skills/coverage_report.json
```

Extract key information:
- `overall_coverage` - Total line coverage percentage
- `files_below_threshold` - Files with coverage < 80%
- `critical_uncovered_paths` - Important code without tests

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
Test Coverage Report:
- Overall coverage: {percentage}%
- Files below 80% threshold: {count} files
- Critical areas with low coverage:
  - {file1}: {percentage}% coverage
  - {file2}: {percentage}% coverage

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/coverage_report.json
```

---

## Example Invocation

**Scenario: Reviewing PR with New Authentication Tests**

Input: Tech Lead reviewing PR #123 with new auth module tests

Expected output:
```
Test Coverage Report:
- Overall coverage: 78%
- Files below 80% threshold: 2 files
- Critical areas with low coverage:
  - auth.py: 68% coverage (uncovered lines: 45-52, 89-103)
  - payment.py: 52% coverage (uncovered lines: 23, 45-78)

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/coverage_report.json
```

**Scenario: Full Coverage Achieved**

Input: Tech Lead final review before merge

Expected output:
```
Test Coverage Report:
- Overall coverage: 94%
- Files below 80% threshold: 0 files
- All critical code paths covered

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/coverage_report.json
```

---

## Error Handling

**If coverage tool not installed:**
- Script attempts auto-installation
- Falls back gracefully if installation fails
- Returns partial report with error note

**If no tests found:**
- Return: "No tests found in project. Cannot generate coverage report."

**If tests fail:**
- Return: "Tests failed. Coverage report not generated. Fix failing tests first."

---

## Notes

- The script (260+ lines) handles all language detection and tool execution
- Supports both bash (Linux/Mac) and PowerShell (Windows)
- Graceful degradation when tools unavailable
- Focuses on line coverage as primary metric
- Excludes test files, generated code, and config from coverage analysis
