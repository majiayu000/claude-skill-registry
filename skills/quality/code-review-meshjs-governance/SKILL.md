---
name: code-review
updated: 2026-02-20
description: Security and quality review of uncommitted changes. Checks for vulnerabilities, code smells, and best practice violations. Use before committing.
argument-hint: [--staged|--all] (default: --all uncommitted)
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
---

# Code Review

Systematic security and quality review of uncommitted changes. Groups findings by severity.

## Instructions

### Step 1: Get Changed Files

```bash
git diff --name-only HEAD
git diff --name-only --cached
```

Combine staged and unstaged changes. Filter to source files. If `--staged` argument, only review staged files.

### Step 2: Get Diffs

For each changed file, get the full diff:

```bash
git diff HEAD -- <file>
```

Read the diff carefully. Focus on ADDED and MODIFIED lines (lines starting with `+`).

### Step 3: Check Each File

Review each changed file against three severity tiers.

#### CRITICAL (Security) — Blocks commit

| Check | Pattern | Why |
|-------|---------|-----|
| Hardcoded secrets | API keys, passwords, tokens in source | Credential exposure |
| SQL injection | String concatenation in SQL queries | Data breach |
| XSS vulnerability | Unescaped user input rendered as HTML | Script injection |
| Missing input validation | API handlers without validation | Injection attacks |
| Path traversal | User input in file paths without sanitization | File system access |
| Exposed server secrets | Server-only env vars in client code | Key leakage |
| Command injection | User input in shell commands without sanitization | Remote code execution |

#### HIGH (Quality) — Should fix before commit

| Check | Pattern | Why |
|-------|---------|-----|
| Functions > 80 lines | Count lines in new/modified functions | Maintainability |
| Nesting > 4 levels | Deeply nested if/for/try blocks | Readability |
| Missing error handling | Async calls without try-catch or error handling | Runtime crashes |
| Debug statements | `console.log`, `print()`, `dbg!()` in production code | Debug noise |
| TODO/FIXME/HACK comments | Temporary markers being committed | Technical debt |
| Unused imports | Imports not referenced in changed code | Dead code |
| Any/unknown type usage | `as any`, `: any`, `# type: ignore` | Type safety loss |
| Hardcoded URLs/ports | `http://localhost:3000` or similar | Environment coupling |

#### MEDIUM (Best Practice) — Nice to fix

| Check | Pattern | Why |
|-------|---------|-----|
| Direct state mutation | Mutating objects/arrays instead of copies | Bugs in reactive frameworks |
| Missing loading states | Async data fetching without loading/error UI | UX |
| Missing accessibility | Interactive elements without aria labels | a11y |
| Magic numbers | Unexplained numeric constants | Readability |
| Missing types | Implicit `any` from missing type annotations | Type safety |
| Large file additions | New files > 300 lines | Consider splitting |

### Step 4: Report

```
CODE REVIEW: <file count> files reviewed
═══════════════════════════════════════

CRITICAL (X issues) — Must fix before commit
  [C1] src/api/foo.ts:42 — Hardcoded API key in source
  [C2] src/components/Bar.tsx:18 — Unescaped user input in HTML

HIGH (X issues) — Should fix
  [H1] src/store/slice.ts:100-180 — Function exceeds 80 lines (80 lines)
  [H2] src/api/bar.ts:25 — Missing try-catch on async operation

MEDIUM (X issues) — Nice to fix
  [M1] src/components/Baz.tsx:55 — Hardcoded string (consider i18n)
  [M2] src/utils/calc.ts:12 — Magic number 86400 (add named constant)

═══════════════════════════════════════
VERDICT: [COMMIT OK / FIX REQUIRED]
```

### Step 5: Verdict

- **Any CRITICAL** → `FIX REQUIRED`, do not commit
- **3+ HIGH** → `FIX REQUIRED`
- **Only MEDIUM** → `COMMIT OK` with suggestions
- **Clean** → `COMMIT OK`
