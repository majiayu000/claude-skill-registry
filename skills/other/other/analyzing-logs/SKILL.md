---
name: analyzing-logs
description: |
  Analyzes Robot Framework test logs to identify failures, group them by type,
  and suggest fixes. Use when a QA engineer wants to analyze logs, check test
  logs, understand why tests failed, or investigate Robot Framework output files.
tools: []
---

# analyzing-logs

Analyzes Robot Framework test logs to identify failures, group them by failure type, and suggest fixes.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Identify log format (XML output, HTML log, or directory)
- [ ] Step 2: Extract test results (names, PASS/FAIL, failure messages)
- [ ] Step 3: Group failures by type, suggest root cause and fix per group
- [ ] Step 4: Rewrite cryptic messages in plain English (if needed)
- [ ] Step 5: Output structured report
```

## Steps

### Step 1: Identify Log Format

Determine the input format:
- `.xml` file (e.g., `output.xml`) → XML output format
- `.html` file (e.g., `log.html`) → HTML log format
- Directory → scan for `output.xml` or `log.html` files

### Step 2: Extract Test Results

Run `/robot-log-analyzer` to extract test results from log files.

From the log file(s), extract for each test case:
- Test name
- Pass/Fail status
- Failure message (if failed)
- Test suite grouping

For large files, use Grep to search for patterns and Read with offset/limit to examine specific sections.

### Step 3: Group Failures

Group failing tests by failure pattern:
- Connection failures (timeouts, refused connections)
- Assertion failures (expected vs actual mismatches)
- Setup failures (missing dependencies, configuration issues)
- Element not found (UI locator issues)

For each group, identify:
- Root cause
- Suggested fix
- Number of affected tests

### Step 4: Rewrite Cryptic Messages (if needed)

If failure messages contain stack traces, exception class names, or framework jargon, run `/rewrite-text` to rewrite them in plain English.

### Step 5: Output Structured Report

```markdown
# Robot Framework Log Analysis Report

## Overview
- Total Tests: N
- Passed: N (XX%)
- Failed: N (XX%)

## Test Results
[Table of all tests with status]

## Failure Analysis
[Groups with root cause and suggested fix]

## Suggested Actions
[Prioritized list of fixes]
```

## Expected Input

Path to Robot Framework log file or directory:
- `output.xml`
- `log.html`
- `/path/to/results/` directory
