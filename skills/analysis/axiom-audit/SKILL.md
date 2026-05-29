---
name: axiom-audit
description: Audit Axiom logs to identify and prioritize errors and warnings, research probable causes, and flag log smells. Use when user asks to check Axiom logs, analyze production errors, investigate log issues, or audit logging patterns.
allowed-tools: Bash, Read, Grep, Write
---

# Axiom Logs Audit Skill

Systematically audit Axiom logs to identify, prioritize, and research errors and warnings.

## Setup

**Install axiom-mcp:**
```bash
go install github.com/axiomhq/axiom-mcp@latest
```

**Install mcptools:**
```bash
# macOS
brew tap f/mcptools
brew install mcp

# Windows/Linux
go install github.com/f/mcptools/cmd/mcptools@latest
```

**Set credentials:**
```bash
export AXIOM_TOKEN="xaat-your-token"
export AXIOM_ORG_ID="your-org-id"  # Optional
```

Find credentials in repo:
```bash
grep -r "AXIOM" . --include="*.env*" --include="*.config.*"
```

## Usage

**List datasets:**
```bash
mcp call listDatasets --params '{"arguments":{}}' ~/go/bin/axiom-mcp
```

**Query APL:**
```bash
# Query errors
mcp call queryApl --params '{"arguments":{"dataset":"logs","apl":"['\''now-24h'\'':now] | where level == \"error\" | summarize count() by message"}}' ~/go/bin/axiom-mcp

# Query warnings
mcp call queryApl --params '{"arguments":{"dataset":"logs","apl":"['\''now-24h'\'':now] | where level == \"warn\" | summarize count() by message"}}' ~/go/bin/axiom-mcp
```

**Interactive shell (recommended for multiple queries):**
```bash
mcp shell ~/go/bin/axiom-mcp
```

## Audit Process

### 1. Identify Dataset
```bash
mcp call listDatasets --params '{"arguments":{}}' ~/go/bin/axiom-mcp
```

Or search codebase for dataset names:
```bash
grep -r "axiom.*dataset" . --include="*.ts" --include="*.js"
```

### 2. Query Errors & Warnings

**Errors:**
```apl
['now-24h':now]
| where level in ("error", "ERROR", "fatal", "FATAL")
| summarize count() by error_message=coalesce(_error, message, msg), error_type
| order by count_desc
```

**Warnings:**
```apl
['now-24h':now]
| where level in ("warn", "WARNING", "WARN")
| summarize count() by message
| order by count_desc
```

**Error trends:**
```apl
['now-7d':now]
| where level in ("error", "ERROR", "fatal", "FATAL")
| summarize count() by bin_auto(_time), error_type
```

### 3. Prioritize Errors

**Priority scoring:**
- **P0**: CRITICAL + High Frequency (>100/hour)
- **P1**: CRITICAL + Low Frequency OR HIGH + High Frequency
- **P2**: HIGH + Low Frequency OR MEDIUM + High Frequency
- **P3**: MEDIUM + Low Frequency
- **P4**: LOW

**Severity levels:**
- **CRITICAL**: Data loss, security issues, service down
- **HIGH**: Feature broken, user-facing errors
- **MEDIUM**: Degraded functionality, intermittent issues
- **LOW**: Minor warnings, non-critical issues

### 4. Research Each Error

For each unique error:
1. Find source in codebase using Grep
2. Read surrounding code to understand context
3. Identify probable cause (code bug, infrastructure, data, integration, config)
4. Collect evidence from code patterns and related errors
5. Flag log smells (see below)

### 5. Flag Log Smells

- **Excessive logging**: Same message flooding logs
- **Missing context**: No request ID, user ID, trace info
- **Poor error messages**: Vague or unhelpful
- **Logged but not handled**: Errors logged then ignored
- **Inconsistent logging**: Different levels for similar issues
- **Sensitive data exposure**: PII, secrets, tokens in logs
- **No stack traces**: Errors without stack traces
- **Generic catch-all handlers**: Hiding real issues

### 6. Generate Report

Create `.audits/axiom-audit-[timestamp].md` with:

```markdown
# Axiom Logs Audit Report
**Date**: [timestamp]
**Time Range**: [start] to [end]
**Total Errors**: X | **Total Warnings**: Y

## Executive Summary
- **P0 Issues**: X (immediate action required)
- **P1 Issues**: Y (urgent)
- **P2 Issues**: Z
- **P3+ Issues**: W

## Prioritized Error List

### P0: [Error Type]
**Occurrences**: X times | **Trend**: [↑/→/↓]
**First Seen**: [timestamp] | **Last Seen**: [timestamp]

**Error Message**:
```
[Actual error message]
```

**Source**: `path/to/file.ts:line`

**Probable Cause**: [Analysis]

**Evidence**:
- [Code patterns, related errors]

---

### P1: [Next Error]
[Same structure]

---

## Log Smells Detected

### Excessive Logging
- `[error pattern]` - X,000 times in Y minutes
- **Location**: `file.ts:line`

### Sensitive Data Exposure
- User emails logged in `auth.ts:42`
- **Impact**: Privacy/compliance risk

---

## Error Categories

**Infrastructure**: X% | **Code Bugs**: Y% | **Data Issues**: Z% | **External**: W%

---

## Trend Analysis

**New Errors**: [Errors that appeared recently]
**Increasing**: [Errors with rising frequency]
**Resolved**: [Errors that stopped]
```

### 7. Provide Summary

Brief summary for user highlighting:
- P0/P1 count and top issues
- Critical log smells
- Category breakdown
- Link to full report

## Critical Rules

- **NEVER EDIT FILES** - Audit only, no fixes
- **NEVER ASSUME** - Research each error in codebase
- **DO PRIORITIZE** - Use consistent priority scoring
- **DO IDENTIFY PATTERNS** - Group similar errors
- **DO FLAG LOG SMELLS** - Document logging anti-patterns
- **DO PROVIDE EVIDENCE** - Support analysis with code/data

## Success Criteria

✅ All errors/warnings extracted from Axiom
✅ Prioritized with severity + frequency scoring
✅ Root cause research for each error type
✅ Log smells identified
✅ Categorization and trend analysis complete
✅ Structured report generated
