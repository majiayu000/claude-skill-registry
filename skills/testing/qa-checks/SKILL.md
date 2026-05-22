---
name: qa-checks
description: Run comprehensive quality verification including build, types, lint, tests, and security scans.
---

# QA Checks Skill

Run comprehensive quality verification.

## When Used

| Agent       | Phase    |
| ----------- | -------- |
| code-agent  | VALIDATE |
| ui-agent    | VALIDATE |
| check-agent | All      |

## CLI Tools

All test operations use pnpm scripts (vitest CLI):

```bash
# List test files
find . -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" | head -20

# Run all tests
pnpm test:run

# Run specific tests
pnpm test:run src/lib/formatDate

# Run tests with coverage
pnpm test:coverage

# Run tests in watch mode
pnpm test
```

### Test Command Reference

| Operation         | Command                                         |
| ----------------- | ----------------------------------------------- |
| Run all tests     | `pnpm test:run`                                 |
| Run specific file | `pnpm test:run <path>`                          |
| Run with coverage | `pnpm test:coverage`                            |
| Watch mode        | `pnpm test`                                     |
| List test files   | `find . -name "*.test.ts" -o -name "*.spec.ts"` |

**Note:** The vitest MCP server has been replaced with CLI commands. TypeScript diagnostics still use cclsp MCP.

## Steps

### 1. Build Check

```bash
pnpm build 2>&1 | tail -30
```

**Pass criteria:** Exit code 0, no compilation errors.

**On failure:** STOP - fix build errors before continuing.

---

### 2. Type Check

```bash
pnpm typecheck 2>&1 | head -50
```

**Pass criteria:** Zero TypeScript errors.

**Common issues:**

| Error Type         | Fix                                |
| ------------------ | ---------------------------------- |
| Missing type       | Add explicit type annotation       |
| Type mismatch      | Fix the type or the value          |
| Cannot find module | Check import path, add declaration |

---

### 3. Lint Check

```bash
pnpm lint 2>&1 | head -50
```

**Pass criteria:** Zero ESLint errors (warnings OK).

**Auto-fix when possible:**

```bash
pnpm lint --fix
```

**Common issues:**

| Rule                   | Fix                              |
| ---------------------- | -------------------------------- |
| max-lines-per-function | Split into smaller functions     |
| complexity             | Simplify logic                   |
| no-unused-vars         | Remove or use the variable       |
| @typescript-eslint/... | Follow TypeScript best practices |

---

### 4. Test Suite

```bash
pnpm test:run --coverage 2>&1 | tail -50
```

**Pass criteria:**

- All tests pass
- Coverage ≥ 70% lines
- Coverage ≥ 60% branches

**On failure:**

1. Identify failing test(s)
2. Check if test or implementation is wrong
3. Fix the implementation (not the test) unless test is incorrect

---

### 5. Security Scan

```bash
# Check for hardcoded secrets
grep -rn "sk-" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
grep -rn "api_key\s*=" --include="*.ts" src/ 2>/dev/null | head -10
grep -rn "password\s*=" --include="*.ts" src/ 2>/dev/null | head -10

# Check for console.log (should use logger)
grep -rn "console\.log" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10

# Check for TODO/FIXME (should be tracked)
grep -rn "TODO\|FIXME" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
```

**Pass criteria:**

- No hardcoded secrets
- No console.log in production code
- TODOs tracked in issues

---

### 6. Diff Review (Optional)

```bash
git diff --stat
git diff HEAD~1 --name-only 2>/dev/null || git diff --staged --name-only
```

**Review each file for:**

- Unintended changes
- Missing error handling
- Edge cases
- Console.log statements

## Output Format

```markdown
## QA CHECK REPORT

| Check    | Status | Details                    |
| -------- | ------ | -------------------------- |
| Build    | PASS   | Compiled successfully      |
| Types    | PASS   | 0 errors                   |
| Lint     | PASS   | 0 errors, 2 warnings       |
| Tests    | PASS   | 45/45 passed, 82% coverage |
| Security | PASS   | No issues found            |

**Overall: PASS**

Ready for PR.
```

**On failure:**

```markdown
## QA CHECK REPORT

| Check    | Status | Details                |
| -------- | ------ | ---------------------- |
| Build    | PASS   | Compiled successfully  |
| Types    | FAIL   | 3 errors               |
| Lint     | PASS   | 0 errors               |
| Tests    | SKIP   | Blocked by type errors |
| Security | SKIP   | Blocked by type errors |

**Overall: FAIL**

### Issues to Fix

1. **Type Error** `src/lib/feature.ts:25`
   - Property 'name' does not exist on type 'unknown'
   - Fix: Add type assertion or narrow the type

2. **Type Error** `src/lib/feature.ts:30`
   - Argument of type 'string' is not assignable to parameter of type 'number'
   - Fix: Convert string to number or change parameter type

3. **Type Error** `src/components/Card.tsx:15`
   - Missing required prop 'title'
   - Fix: Add title prop to component call
```

## Error Handling

| Error           | How to Handle                          |
| --------------- | -------------------------------------- |
| Build fails     | Report error, suggest fix              |
| Type errors     | List all with file:line, suggest fixes |
| Lint errors     | Auto-fix if possible, list remaining   |
| Test failures   | Report failed tests with output        |
| Coverage low    | Report uncovered files/lines           |
| Security issues | Report with severity, require fix      |

## Phase-Specific Usage

Run individual phases when needed:

| Command           | Runs                |
| ----------------- | ------------------- |
| `/check`          | All phases          |
| `/check build`    | Build only          |
| `/check types`    | Type check only     |
| `/check lint`     | Lint only           |
| `/check tests`    | Tests with coverage |
| `/check security` | Security scan only  |

## Quality Gates

| Check    | Requirement              | Blocking |
| -------- | ------------------------ | -------- |
| Build    | Must pass                | Yes      |
| Types    | 0 errors                 | Yes      |
| Lint     | 0 errors (warnings OK)   | Yes      |
| Tests    | All pass, 70%+ coverage  | Yes      |
| Security | 0 secrets, 0 console.log | Yes      |
