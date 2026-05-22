---
name: bugfix-and-debug
description: |
  Diagnose errors and failing tests in Laravel + React + Python applications. Use when encountering bugs, exceptions,
  stack traces, 500 errors, TypeErrors, failing tests, or unexpected behavior. EXCLUSIVE to debugger agent.
allowed-tools: Read, Edit, Bash, Grep, Glob, mcp_context7
---
# Bugfix and Debug

**Exclusive to:** `debugger` agent

## 📚 Context7 (Memory) — Up-to-Date Docs

Lookup error patterns and fixes in official docs:
```
mcp_context7_resolve-library-id(libraryName="[library]", query="[error type]")
mcp_context7_query-docs(libraryId="/[resolved-id]", query="[specific error message]")
```

## Validation Loop (MANDATORY)

Before completing any fix, run this verification sequence:
```bash
composer test            # All PHP tests pass
npm run types           # No TypeScript errors
npm run lint            # No linting errors
```

If any command fails, investigate and fix before reporting completion.

## Instructions

### Phase 1: Evidence Collection
1. Capture exact error message and stack trace
2. Identify reproduction steps (command + inputs)
3. Note when it started (recent changes?)
4. Check logs: `storage/logs/laravel.log`

### Phase 2: Hypothesis Formation
Form 1-3 ranked hypotheses based on:
- Error message keywords
- Stack trace file paths
- Recent git changes
- Similar past issues

### Phase 3: Verification
```bash
# Search for error patterns
grep -r "error text" --include="*.php" --include="*.tsx" app/ resources/

# Check recent changes
git log --oneline -10
git diff HEAD~3

# Run isolated test
php artisan test --filter=TestName
```

### Phase 4: Minimal Fix
- Fix **root cause**, not symptoms
- Make **smallest** change possible
- Consider related edge cases

### Phase 5: Regression Prevention
- Add/update test covering the fixed case
- Verify test fails without fix, passes with fix

## Common Laravel Error Patterns

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `ModelNotFoundException` | Wrong ID, missing record | Check route model binding |
| `ValidationException` | Invalid input | Review FormRequest rules |
| `AuthorizationException` | Policy failure | Check policy methods |
| `QueryException` | SQL error | Check migration/schema |
| `TokenMismatchException` | CSRF issue | Add @csrf directive |
| `Class not found` | Autoload issue | Run `composer dump-autoload` |

## Common React/TypeScript Errors

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `Cannot read property of undefined` | Null access | Add optional chaining `?.` |
| `Type 'X' is not assignable` | Type mismatch | Fix interface/props |
| `Hook call violation` | Hook in wrong place | Move to component |
| `Hydration mismatch` | SSR/client diff | Use `useEffect` |

## Debugging Commands

```bash
# Laravel
php artisan tinker                    # Interactive REPL
tail -f storage/logs/laravel.log     # Watch logs
php artisan route:list               # Check routes
php artisan migrate:status           # Check migrations

# Frontend
npm run types                        # TypeScript errors
npm run lint                         # ESLint issues
```

## Output Template

```markdown
## 🐛 Bug
[One sentence description]

## 🔍 Root Cause
[What was wrong and why]

## 🔧 Fix
| File | Change |
|------|--------|
| `path/file` | Description |

## 🧪 Regression Test
[Test name and coverage]

## ✅ Verification
$ [command]
[output]
```

## Examples
- "Fix this failing Pest test"
- "Users can't log in; find why and patch it safely"
- "Debug why form submission fails with 500 error"
