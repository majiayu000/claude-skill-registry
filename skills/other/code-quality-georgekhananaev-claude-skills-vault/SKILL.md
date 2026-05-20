---
name: code-quality
description: Multi-language code quality standards and review for TypeScript, Python, Go, and Rust. Enforces type safety, security, performance, and maintainability. Use when writing, reviewing, or refactoring code. Includes review process, checklist, and Python PEP 8 deep-dive.
author: George Khananaev
replaces: [beautiful-code, code-reviewer, pep8]
---

# Code Quality

Production-grade code standards and review for TypeScript, Python, Go, and Rust.

## When to Use

- Writing or reviewing code in TS/Python/Go/Rust
- Code review or pull request analysis
- Security or performance audit
- Setting up linting/CI for a project
- Python-specific style check (PEP 8)

## Quick-Start Modes

| Intent | Sections to Use |
|--------|----------------|
| **Write code** | Core Rules + Language Standards + AI-Friendly Patterns |
| **Review PR** | Review Process + `references/checklist.md` + Severity Levels |
| **Setup CI** | Config Files + Scripts + Enforcement Strategy |
| **Python style** | `references/python.md` (full PEP 8 deep-dive) |

**Context loading:** For deep reviews, read the relevant `references/` file for the language under review.

## Quick Reference

| Language | Type Safety | Linter | Complexity |
|----------|-------------|--------|------------|
| TypeScript | `strict`, no `any` | ESLint + typescript-eslint | max 10 |
| Python | mypy `strict`, PEP 484 | Ruff + mypy | max 10 |
| Go | staticcheck | golangci-lint | max 10 |
| Rust | clippy pedantic | clippy + cargo-audit | - |

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Security vulnerabilities, data loss | Block merge |
| **Error** | Bugs, type violations, `any` | Block merge |
| **Warning** | Code smells, complexity | Must address |
| **Style** | Formatting, naming | Auto-fix |

---

## Core Rules (All Languages)

### Type Safety
- No implicit any / untyped functions
- No type assertions without guards
- Explicit return types on public APIs

### Security
- No hardcoded secrets (use gitleaks)
- No eval/pickle/unsafe deserialization
- Parameterized queries only
- SCA scanning (npm audit / pip-audit / govulncheck / cargo-audit)

### Complexity
- Max cyclomatic complexity: 10
- Max function lines: 50
- Max nesting depth: 3
- Max parameters: 5

### Error Handling
- No ignored errors (Go: no `_` for err)
- No bare except (Python)
- No unwrap in prod (Rust)
- Wrap errors with context

---

## Language-Specific Standards

### TypeScript
See: `references/typescript.md`

```typescript
// CRITICAL: Never use any
const bad: any = data;           // Error
const good: unknown = data;      // OK

// ERROR: No type assertions
const bad = data as User;        // Error
const good = isUser(data) ? data : null;  // OK

// ERROR: Non-null assertions
const bad = user!.name;          // Error
const good = user?.name ?? '';   // OK
```

### Python (PEP 8 / 3.11+)
See: `references/python.md`

```python
# CRITICAL: All functions must be typed
def bad(data):                   # Error
    return data

def good(data: dict[str, Any]) -> list[str]:  # OK
    return list(data.keys())

# Use modern syntax
value: str | None = None         # OK (not Optional)
items: list[str] = []            # OK (not List)
```

### Go
See: `references/go.md`

```go
// CRITICAL: Never ignore errors
result, _ := doSomething()       // Error
result, err := doSomething()     // OK
if err != nil {
    return fmt.Errorf("doing something: %w", err)
}
```

### Rust
See: `references/rust.md`

```rust
// CRITICAL: No unwrap in production
let value = data.unwrap();        // Error
let value = data?;                // OK
let value = data.unwrap_or_default(); // OK
```

---

## Cross-Language Standards

### Structured Logging
See: `references/logging.md`

```typescript
logger.info({ userId, action: 'login' }, 'User logged in');   // TS (pino)
```
```python
logger.info("user_login", user_id=user_id)                    # Python (structlog)
```
```go
log.Info().Str("user_id", userID).Msg("user logged in")       // Go (zerolog)
```

### Test Coverage
See: `references/testing.md`

| Metric | Threshold |
|--------|-----------|
| Line coverage | 80% min |
| Branch coverage | 70% min |
| New code | 90% min |

### Security Scanning
See: `references/security.md`

- Secrets: gitleaks (pre-commit + CI)
- Dependencies: npm audit / pip-audit / govulncheck / cargo-audit
- Accessibility: jsx-a11y (TypeScript)
- Race detection: go test -race (Go)

### API Design
See: `references/api-design.md`

- Proper HTTP status codes (200, 201, 204, 400, 401, 403, 404, 422, 429, 500)
- RFC 7807 error format
- Plural nouns for resources: `/users/{id}/orders`
- Validate at API boundary

### Database Patterns
See: `references/database.md`

- Transactions for multi-write operations
- N+1 prevention: eager load or batch
- Safe migrations (expand-contract pattern)
- Always paginate list queries

### Async & Concurrency
See: `references/async-concurrency.md`

- Always clean up resources (try/finally, defer, Drop)
- Set timeouts on all async operations
- Use semaphores for rate limiting
- Avoid blocking in async contexts

---

## Review Process

### Step 1: Understand Context
1. Identify the language/framework
2. Understand the purpose of the code
3. Check for existing patterns in the codebase
4. Review any related tests

### Step 2: Systematic Review
Use the checklist at `references/checklist.md` for thorough reviews covering:
- Code quality (structure, naming, type safety, dead code)
- Security (injection, auth, secrets, input validation)
- Performance (N+1, memory leaks, caching, re-renders)
- Error handling (edge cases, recovery, cleanup)
- Testing (coverage, quality, assertions)
- Best practices (SOLID, patterns, maintainability)

### Step 3: Categorize & Report

```markdown
**[SEVERITY] Issue Title**
- File: `path/to/file.ts:line`
- Problem: Clear description
- Impact: What could go wrong
- Fix: Specific code suggestion
```

### Git Integration

```bash
# Review staged changes
git --no-pager diff --cached

# Review specific commit
git --no-pager show <commit>

# Review PR diff
gh pr diff <number>
```

## Review Output Format

Use severity levels from the table above (Critical / Error / Warning / Style).

```markdown
# Code Review Summary

## Overview
- Files reviewed: X
- Issues found: Y (X Critical, Y Error, Z Warning)
- Recommendation: [Approve / Request Changes / Needs Discussion]

## Critical Issues
[Security vulnerabilities, data loss - must fix]

## Error Issues
[Bugs, type violations - must fix]

## Warnings
[Code smells, complexity - should address]

## Style
[Formatting, naming - auto-fixable]

## Positive Observations
[Good practices found]
```

---

## Naming Conventions

| Element | TypeScript | Python | Go | Rust |
|---------|------------|--------|-----|------|
| Variables | camelCase | snake_case | camelCase | snake_case |
| Functions | camelCase | snake_case | camelCase | snake_case |
| Constants | SCREAMING_SNAKE | SCREAMING_SNAKE | MixedCaps | SCREAMING_SNAKE |
| Types | PascalCase | PascalCase | PascalCase | PascalCase |
| Files | kebab-case | snake_case | lowercase | snake_case |

## AI-Friendly Patterns

1. Explicit types always
2. Single responsibility per function
3. Small functions (< 30 lines ideal)
4. Max nesting depth 3
5. Guard clauses for early returns
6. Named constants, no magic values
7. Linear, predictable execution flow

## Enforcement Strategy

### Progressive (Ratchet-Based)
```
Phase 1: Errors block, Warnings tracked
Phase 2: Strict on NEW files only
Phase 3: Strict on TOUCHED files
Phase 4: Full enforcement
```

### WIP vs Merge Mode

| Mode | Trigger | Behavior |
|------|---------|----------|
| WIP | Local commit | Warnings only |
| Push | git push | Errors block |
| PR | PR to main | Full strict |

## Config Files

Available in `configs/`:
- `typescript/` - ESLint, tsconfig, Prettier
- `python/` - pyproject.toml, pre-commit
- `go/` - golangci.yaml
- `rust/` - clippy.toml
- `.pre-commit-config.yaml`
- `.gitleaks.toml`

## Scripts

Available in `scripts/`:
- `check_changed.sh` - Monorepo-aware incremental linting
- `check_all.sh` - Full repository check
- `check_style.py` - Python full check (ruff + pycodestyle + mypy)
- `check_pep8.sh` - Quick PEP 8 only
- `check_types.sh` - Python type hints only
- `fix_style.sh` - Python auto-fix issues
