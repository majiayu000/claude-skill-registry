---
name: code-review
description: Review and score code quality across 12 dimensions. Read-only analysis with numeric scoring. Use to diagnose issues before fixing.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob, Task
---

# Code Review

Comprehensive code quality review with numeric scoring. **Read-only** — this skill does not modify any files.

## How it works

This skill is **agent-implemented** — the agent reads the steps below and executes them autonomously. There is no standalone bash script.

```
/code-review
/code-review security
/code-review src/api/
```

## Input

- `$ARGUMENTS` = optional focus area (e.g., "security", "tests", "src/api/")
- If empty, reviews the entire project

## Phase 1: Context Gathering

Understand the project before reviewing:

```bash
# Project type and structure
ls -la
cat package.json 2>/dev/null || cat Cargo.toml 2>/dev/null || cat pyproject.toml 2>/dev/null || echo "unknown project type"

# Recent changes (what to focus on)
git diff --stat HEAD~5..HEAD 2>/dev/null || git diff --stat
git log --oneline -10

# Test infrastructure
ls -la test/ tests/ __tests__/ spec/ 2>/dev/null
```

## Phase 2: Run Automated Checks

Run every available automated check and capture results:

```bash
# Auto-detect and run checks
if [ -f "pnpm-lock.yaml" ]; then
  pnpm typecheck 2>&1 || true
  pnpm lint 2>&1 || true
  pnpm test 2>&1 || true
elif [ -f "yarn.lock" ]; then
  yarn typecheck 2>&1 || true
  yarn lint 2>&1 || true
  yarn test 2>&1 || true
elif [ -f "package-lock.json" ]; then
  npm run typecheck 2>&1 || true
  npm run lint 2>&1 || true
  npm test 2>&1 || true
elif [ -f "Cargo.toml" ]; then
  cargo clippy 2>&1 || true
  cargo test 2>&1 || true
elif [ -f "pyproject.toml" ]; then
  ruff check . 2>&1 || true
  pytest 2>&1 || true
fi
```

Capture pass/fail and any error output for each check.

## Phase 3: Manual Code Analysis

Review code across **12 quality dimensions**. For each dimension, read relevant files and assess:

### Dimensions and Weights

| # | Dimension | Weight | What to check |
|---|---|---|---|
| 1 | **Correctness** | 15% | Do tests pass? Does the build succeed? Logic errors? |
| 2 | **Completeness** | 10% | Are requirements met? Missing edge cases? TODO/FIXME items? |
| 3 | **Robustness** | 10% | Error handling, null checks, boundary conditions, input validation |
| 4 | **Readability** | 10% | Naming clarity, function size, code organization |
| 5 | **Maintainability** | 10% | Coupling, cohesion, single responsibility, DRY |
| 6 | **Complexity** | 8% | Cyclomatic complexity, nesting depth, function length |
| 7 | **Duplication** | 7% | Copy-paste code, repeated patterns that should be abstracted |
| 8 | **Test Coverage** | 10% | Line/branch coverage, critical paths tested |
| 9 | **Test Quality** | 5% | Meaningful assertions, edge cases, test isolation |
| 10 | **Security** | 8% | OWASP top 10, injection, XSS, hardcoded secrets, auth gaps |
| 11 | **Documentation** | 4% | Public API docs, complex logic explained, README accuracy |
| 12 | **Style** | 3% | Linting compliance, consistent formatting |

### Severity Classification

For each issue found, classify as:

- **P0 Critical** — Blocks deployment. Security vulnerabilities, data loss, crashes.
- **P1 High** — Must fix before merge. Bugs, missing error handling, failing tests.
- **P2 Medium** — Should fix soon. Code smells, moderate complexity, weak tests.
- **P3 Low** — Nice to have. Style issues, minor refactors, documentation gaps.

## Phase 4: Scoring

Calculate the weighted score (0-100):

For each dimension:
1. Assign a score from 0-100 based on the analysis
2. Multiply by the weight
3. Sum all weighted scores

```
TOTAL = sum(dimension_score * weight) for all 12 dimensions
```

### Score interpretation

| Score | Grade | Meaning |
|---|---|---|
| 95-100 | A+ | Excellent — production ready, exemplary code |
| 85-94 | A | Senior-level — solid, maintainable, well-tested |
| 70-84 | B | Good — some issues but functional and reasonable |
| 50-69 | C | Needs work — significant issues to address |
| 0-49 | D | Poor — critical problems, not ready for review |

## Output Format

Present the results in this exact format:

```
## Code Review Report

### Summary
- **Score: XX/100 (Grade X)**
- Files analyzed: N
- Issues found: N (P0: N, P1: N, P2: N, P3: N)

### Dimension Scores

| Dimension        | Score | Weight | Weighted | Notes |
|------------------|-------|--------|----------|-------|
| Correctness      | XX    | 15%    | XX.X     | ...   |
| Completeness     | XX    | 10%    | XX.X     | ...   |
| Robustness       | XX    | 10%    | XX.X     | ...   |
| Readability      | XX    | 10%    | XX.X     | ...   |
| Maintainability  | XX    | 10%    | XX.X     | ...   |
| Complexity       | XX    | 8%     | XX.X     | ...   |
| Duplication      | XX    | 7%     | XX.X     | ...   |
| Test Coverage    | XX    | 10%    | XX.X     | ...   |
| Test Quality     | XX    | 5%     | XX.X     | ...   |
| Security         | XX    | 8%     | XX.X     | ...   |
| Documentation    | XX    | 4%     | XX.X     | ...   |
| Style            | XX    | 3%     | XX.X     | ...   |
| **TOTAL**        |       | 100%   | **XX.X** |       |

### Issues (sorted by severity)

#### P0 Critical
- [file:line] Description of the issue

#### P1 High
- [file:line] Description of the issue

#### P2 Medium
- [file:line] Description of the issue

#### P3 Low
- [file:line] Description of the issue

### Recommendations
1. Top priority fix: ...
2. Second priority: ...
3. ...
```

## Important

- This skill is **read-only** — it NEVER modifies files
- Run `/code-fix` after this to apply fixes based on the findings
- Run `/coco-fix-iterate` to automatically review, fix, and iterate until the score target is met
- Be honest with scores — inflated scores defeat the purpose
- Focus analysis on recently changed files when a focus area is not specified
