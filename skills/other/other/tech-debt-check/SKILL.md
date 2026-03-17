---
name: tech-debt-check
description: Detect technical debt patterns in code including duplication, complexity, and maintainability issues. Use at phase checkpoints or on-demand to assess code quality.
---

# Technical Debt Check Skill

Analyze the codebase for technical debt patterns that commonly accumulate during AI-assisted development.

## Why This Matters

Research shows AI-generated code creates:
- 8x increase in code duplication (GitClear 2024)
- 1.64x more maintainability issues than human code
- Frequent DRY principle violations

This skill catches these issues before they compound.

## Workflow Overview

Copy this checklist and track progress:

```
Tech Debt Check Progress:
- [ ] Step 1: Detect project type
- [ ] Step 2: Run duplication analysis
- [ ] Step 3: Run complexity analysis
- [ ] Step 4: Run file size analysis
- [ ] Step 5: Check for AI code smells
- [ ] Step 6: Generate report
```

## Thresholds Reference

| Category | Metric | Good | Warning | Critical |
|----------|--------|------|---------|----------|
| **Duplication** | Duplicate % | <3% | 3-7% | >7% |
| | Duplicate blocks | <5 | 5-15 | >15 |
| | Lines per block | <10 | 10-20 | >20 |
| **Complexity** | Avg complexity | <5 | 5-10 | >10 |
| | Max complexity | <15 | 15-25 | >25 |
| | Functions >10 | 0 | 1-3 | >3 |
| **File Size** | Max file lines | <300 | 300-500 | >500 |
| | Avg file lines | <150 | 150-250 | >250 |
| | Files >300 lines | 0 | 1-3 | >3 |

## Step 1: Detect Project Type

Identify the project's primary language and available tooling:

| File | Language | Tools Available |
|------|----------|-----------------|
| `package.json` | JavaScript/TypeScript | jscpd, eslint |
| `requirements.txt` / `pyproject.toml` | Python | pylint, radon, flake8 |
| `Cargo.toml` | Rust | cargo clippy |
| `go.mod` | Go | staticcheck |

If no package manager found, fall back to file extension analysis.

## Step 2: Duplication Analysis

Check for duplicate code blocks (a primary AI coding failure mode).

### Using jscpd (JS/TS projects)

```bash
# Install if needed
npm list -g jscpd || npm install -g jscpd

# Run analysis
jscpd src/ --min-lines 5 --min-tokens 50 --reporters json --output .tech-debt-report/
```

Parse output for total duplicate lines, percentage, and specific blocks (file, start line, end line).

### Manual detection (fallback)

If jscpd unavailable, use grep-based pattern matching for repeated code blocks.

## Step 3: Complexity Analysis

### JavaScript/TypeScript

Use eslint with complexity rules:

```bash
npx eslint src/ --rule '{"complexity": ["error", 10]}' --format json
```

Or check manually for:
- Functions with >10 branches
- Nested callbacks >3 levels deep
- Files with >300 lines

### Python

Use radon for cyclomatic complexity:

```bash
radon cc src/ -a -s --json
```

Or use pylint:

```bash
pylint src/ --disable=all --enable=R0912,R0915 --output-format=json
```

## Step 4: File Size Analysis

Large files often indicate poor separation of concerns. Find files exceeding thresholds:

```bash
find src/ -name "*.ts" -o -name "*.js" -o -name "*.py" | xargs wc -l | sort -rn | head -20
```

## Step 5: AI Code Smell Detection

Check for patterns commonly produced by AI:

### 5.1 Excessive Error Handling

```bash
# Check try-catch density (ratio > 1:1 suggests over-defensive code)
echo "try blocks: $(grep -r 'try {' src/ | wc -l)"
echo "catch blocks: $(grep -r 'catch' src/ | wc -l)"
```

### 5.2 Unused Code

```bash
# TypeScript/JavaScript
npx eslint src/ --rule '{"no-unused-vars": "error"}' --format json

# Python
pylint src/ --disable=all --enable=W0611,W0612 --output-format=json
```

### 5.3 Inconsistent Patterns

Look for multiple implementations of the same concern (date formatting, HTTP clients, validation):

```bash
grep -r "new Date\|moment\|dayjs\|date-fns" src/ | cut -d: -f1 | sort | uniq -c
grep -r "fetch\|axios\|got\|request" src/ | cut -d: -f1 | sort | uniq -c
```

### 5.4 Comment Ratio

Healthy ratio is 10-20%. AI tends to over-comment or under-comment.

## Step 6: Generate Report

```
TECHNICAL DEBT REPORT
=====================
Project: {name}
Analyzed: {timestamp}
Files scanned: {N}

SUMMARY
-------
Overall Health: GOOD | WARNING | CRITICAL
Tech Debt Score: {0-100} (lower is better)

DUPLICATION ({status})
----------------------
Duplicate code: {N} blocks, {X}% of codebase
Largest duplicates:
1. {file1}:{lines} ↔ {file2}:{lines} ({N} lines)
2. {file1}:{lines} ↔ {file2}:{lines} ({N} lines)

Action: Consider extracting to shared utility

COMPLEXITY ({status})
---------------------
Average complexity: {N}
High complexity functions:
1. {file}:{function} — complexity {N}
2. {file}:{function} — complexity {N}

Action: Refactor functions with complexity >15

FILE SIZE ({status})
--------------------
Large files (>300 lines):
1. {file} — {N} lines
2. {file} — {N} lines

Action: Split into smaller, focused modules

AI CODE SMELLS ({status})
-------------------------
- Excessive try-catch: {found/not found}
- Unused code: {N} instances
- Inconsistent patterns: {list}

Action: Review flagged patterns for consolidation

RECOMMENDATIONS
---------------
Priority fixes:
1. {specific action with file reference}
2. {specific action with file reference}
3. {specific action with file reference}

Deferred items:
- {lower priority items}
```

## Integration with Phase Checkpoint

When invoked from `/phase-checkpoint`:

1. Run full analysis
2. Return summary status: PASSED | PASSED WITH NOTES | FAILED
3. FAILED if any CRITICAL thresholds exceeded
4. PASSED WITH NOTES if WARNING thresholds exceeded
5. PASSED if all metrics GOOD

## Exit Criteria

| Result | Condition |
|--------|-----------|
| PASSED | All metrics in GOOD range |
| PASSED WITH NOTES | Some WARNING, no CRITICAL |
| FAILED | Any CRITICAL metric |

## Limitations

- Duplication detection requires jscpd or similar tool
- Complexity analysis requires language-specific linters
- Manual review still needed for semantic duplication
- Cannot detect architectural debt or design issues

## When Check Cannot Complete

**If multiple CRITICAL thresholds are exceeded:**
- Report all CRITICAL issues, not just the first
- Prioritize by impact: duplication first (compounds fastest), then complexity, then file size
- Ask user: "Fix issues incrementally or address all before proceeding?"
- If incremental: suggest tackling one category at a time

**If required tools are not installed:**
- Report which tools are missing and why they're needed
- Provide installation commands: `npm install -g jscpd`, `pip install radon`, etc.
- Fall back to manual pattern matching where possible
- Mark checks as SKIPPED (not FAILED) when tool unavailable

**If codebase is too large for analysis:**
- Report: "Codebase exceeds analysis threshold ({N} files)"
- Suggest: Focus on recently modified files: `git diff --name-only HEAD~10`
- Offer to run on specific directories instead
- Provide incremental analysis option

**If analysis reveals overwhelming debt:**
- Do NOT suggest fixing everything at once
- Prioritize: Top 3 highest-impact fixes only
- Suggest: Create tracking issue for remaining items
- Recommend: `/add-todo` for each deferred fix

## Example

Given a TypeScript project:

```
$ /tech-debt-check

TECHNICAL DEBT REPORT
=====================
Project: my-api
Analyzed: 2025-01-10 14:30:00
Files scanned: 45

SUMMARY
-------
Overall Health: WARNING
Tech Debt Score: 34/100

DUPLICATION (WARNING)
----------------------
Duplicate code: 8 blocks, 4.2% of codebase

Largest duplicates:
1. src/api/users.ts:45-60 ↔ src/api/posts.ts:32-47 (15 lines)
   → Both validate request body identically

Action: Extract to src/middleware/validateBody.ts

COMPLEXITY (GOOD)
-----------------
Average complexity: 4.2
No functions exceed threshold.

FILE SIZE (WARNING)
-------------------
Large files:
1. src/services/auth.ts — 342 lines

Action: Split token management into separate module

AI CODE SMELLS (GOOD)
---------------------
No significant issues detected.

RECOMMENDATIONS
---------------
Priority fixes:
1. Extract duplicate validation logic (saves 30 lines)
2. Split auth.ts into auth.ts + tokens.ts

Status: PASSED WITH NOTES
```
