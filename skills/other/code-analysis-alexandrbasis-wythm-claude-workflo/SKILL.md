---
name: code-analysis
description: "Deep code analysis with metrics, patterns, and recommendations. Use for architecture review, tech debt assessment, codebase exploration, or when asked 'analyze this code/project'."
context: fork
agent: Explore
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(wc *)
  - Bash(cloc *)
  - Bash(find *)
  - Bash(git log *)
  - Bash(git shortlog *)
---

# Deep Code Analysis

## Overview

Perform comprehensive code analysis returning structured findings. Since this runs in a forked context, explore extensively - only the final report returns to the main conversation.

## Analysis Process

### 1. Scope Discovery
```bash
# Understand project structure
find . -type f -name "*.ts" | head -50
cloc . --exclude-dir=node_modules,dist,coverage --json 2>/dev/null || wc -l **/*.ts
```

### 2. Architecture Analysis
- Identify layers and boundaries (DDD patterns for Wythm)
- Map module dependencies
- Find circular dependencies or violations
- Check adherence to project patterns (`backend/docs/project-structure.md`)

### 3. Code Quality Metrics
- File sizes and complexity hotspots
- Test coverage gaps
- Code duplication patterns
- Naming consistency

### 4. Tech Debt Assessment
- TODO/FIXME comments
- Deprecated patterns
- Missing error handling
- Incomplete implementations

### 5. Git History Insights
```bash
# Most changed files (churn)
git log --format=format: --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -20

# Recent contributors
git shortlog -sn --since="3 months ago"
```

## Output Format

Return a structured report:

```markdown
# Code Analysis Report

**Scope**: [what was analyzed]
**Date**: [ISO date]

## Executive Summary
[2-3 sentence overview]

## Metrics
| Metric | Value |
|--------|-------|
| Total Files | X |
| Lines of Code | X |
| Test Coverage | X% |
| Tech Debt Items | X |

## Architecture Findings
### Strengths
- [finding]

### Concerns
- [finding with severity: HIGH/MEDIUM/LOW]

## Recommendations
1. [actionable recommendation]
2. [actionable recommendation]

## Detailed Findings
[expandable sections for each area]
```

## Wythm-Specific Checks

For this project, also verify:
- DDD layer separation (domain → application → infrastructure)
- Prisma schema consistency
- NestJS module boundaries
- Service injection patterns
- Error handling with domain exceptions
