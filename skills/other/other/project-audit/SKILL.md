---
name: project-audit
description: "Security scan, dead code detection, and code quality audit for any project"
version: 1.0.0
category: quality
tags: [security, dead-code, audit, sast, quality]
---

# Project Audit

Automated security + quality scan for any codebase. Generates a report, then optionally auto-fixes safe issues.

## Usage

```bash
# Scan current directory
vibeco audit

# Scan specific path
vibeco audit /path/to/project

# Auto-fix safe issues (console.log removal)
vibeco audit --fix

# JSON output for CI integration
vibeco audit --json
```

## What It Scans

### Security (SAST)
- **CRITICAL**: eval(), exec(), execSync(), os.system(), subprocess, SQL injection patterns
- **HIGH**: innerHTML, dangerouslySetInnerHTML, document.write(), pickle.load(), hardcoded secrets
- **MEDIUM**: Sensitive data in console.log, MD5/SHA1 weak crypto

### Code Quality
- Large files (>500 lines)
- TODO/FIXME/HACK/XXX count
- Excessive console.log (>3 per file)

### Test Coverage
- Source file to test file ratio
- Test file detection (.test.ts, .spec.js, etc.)

### Dependencies
- Lock file presence check
- Node engine version check

## Output

### Terminal Report
Color-coded report with grade (A+ to F):
- A+: Zero issues
- A-: Only MEDIUM issues
- B: Some MEDIUM issues
- C: HIGH issues present
- D: Many HIGH issues
- F: CRITICAL issues present

### JSON Report
Saved to `.vibeco-audit.json` in project root. Contains all findings for programmatic processing.

## Auto-Fix (--fix)

Currently auto-fixes:
- Removes console.log statements from files with >3 occurrences

Does NOT auto-fix (manual review required):
- Security issues (too risky for automation)
- Large file refactoring
- TODO/FIXME resolution

## Workflow

```
1. vibeco audit          -> Scan, generate report
2. Review report         -> Understand issues
3. vibeco audit --fix    -> Auto-fix safe issues
4. Manual fixes          -> Address security findings
5. vibeco audit          -> Re-scan to verify
```

## Ignored Directories

node_modules, dist, .git, vendor, __pycache__, .next, build, coverage

## Ignored in Security Scan

Test files (*.test.ts, *.spec.js, __tests__/, __mocks__/) are excluded from security scanning to avoid false positives.
