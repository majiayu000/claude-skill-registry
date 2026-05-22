---
name: beautiful-code
description: Multi-language code quality standards for TypeScript, Python, Go, and Rust. Enforces type safety, security, performance, and maintainability with progressive enforcement. Use when writing, reviewing, or refactoring code across any of these languages.
---

# Beautiful Code Standards

Enforce production-grade code quality across TypeScript, Python, Go, and Rust.

## When to Use

- Writing or reviewing code in TS/Python/Go/Rust
- Setting up linting/CI for a project
- Code quality audit or refactoring
- User requests code review or style check

## Quick Reference

| Language | Type Safety | Linter | Complexity |
|----------|-------------|--------|------------|
| TypeScript | `strict`, no `any` | ESLint + tsx-eslint | max 10 |
| Python | mypy `strict`, PEP 484 | Ruff + mypy | max 10 |
| Go | staticcheck | golangci-lint | max 10 |
| Rust | clippy pedantic | clippy + cargo-audit | - |

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Security vulnerabilities | Block merge |
| **Error** | Bugs, type violations, `any` | Block merge |
| **Warning** | Code smells, complexity | Must address |
| **Style** | Formatting, naming | Auto-fix |

## Core Rules (All Languages)

### Type Safety
- No implicit any / untyped functions
- No type assertions without guards
- Explicit return types on public APIs

### Security
- No hardcoded secrets (use gitleaks)
- No eval/pickle/unsafe deserialization
- Parameterized queries only
- SCA scanning (npm audit/pip-audit/govulncheck/cargo-audit)

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

### Python
See: `references/python.md` (extends `pep8` skill)

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

## Cross-Language Standards

### Structured Logging
See: `references/logging.md`

```typescript
// TypeScript (pino)
logger.info({ userId, action: 'login' }, 'User logged in');

// Python (structlog)
logger.info("user_login", user_id=user_id)

// Go (zerolog)
log.Info().Str("user_id", userID).Msg("user logged in")
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

- Use proper HTTP status codes (200, 201, 204, 400, 401, 403, 404, 422, 429, 500)
- RFC 7807 error format (type, title, status, detail, errors)
- Plural nouns for resources: `/users/{id}/orders`
- Validate at API boundary, not deep in services

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

### Emergency Bypass

```bash
EMERGENCY_BYPASS=true git commit -m "HOTFIX: [ticket] description"
```

## Tooling

### Pre-commit
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    hooks: [gitleaks]
  # Language-specific hooks...
```

### CI Jobs
- secrets-scan (gitleaks)
- lint (per-language matrix)
- coverage (80% threshold)
- go-race (if Go files changed)

## Config Files

Available in `configs/`:
- `typescript/` - ESLint, tsconfig, Prettier
- `python/` - pyproject.toml, pre-commit
- `go/` - golangci.yaml
- `rust/` - clippy.toml

## Scripts

Available in `scripts/`:
- `check_changed.sh` - Monorepo-aware incremental linting
- `check_all.sh` - Full repository check

## AI-Friendly Patterns

1. **Explicit Types**: Always declare types explicitly
2. **Single Responsibility**: One function = one purpose
3. **Small Functions**: < 30 lines ideal
4. **Flat is Better**: Max nesting depth 3
5. **Guard Clauses**: Early returns for edge cases
6. **No Magic**: Named constants only
7. **Obvious Flow**: Linear, predictable execution

## Naming Conventions

| Element | TypeScript | Python | Go | Rust |
|---------|------------|--------|-----|------|
| Variables | camelCase | snake_case | camelCase | snake_case |
| Functions | camelCase | snake_case | camelCase | snake_case |
| Constants | SCREAMING_SNAKE | SCREAMING_SNAKE | MixedCaps | SCREAMING_SNAKE |
| Types | PascalCase | PascalCase | PascalCase | PascalCase |
| Files | kebab-case | snake_case | lowercase | snake_case |
