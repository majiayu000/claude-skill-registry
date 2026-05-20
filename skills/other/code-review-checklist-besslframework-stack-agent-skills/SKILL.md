---
name: code-review-checklist
description: |
  Reads a git diff (staged or between branches) and generates a checklist of things
  to verify before merging. Not a code review itself, but the list of what a reviewer
  should look at. Each item references specific files and lines, with priority levels.
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Write
---

# Code Review Checklist

Generate the list of things to check, not the review itself.

---

## Why This Exists

Code reviews catch more bugs when reviewers know what to look for. A diff with 40 changed files across 6 directories is hard to review without a map. This skill reads the diff, identifies the risky parts, and produces a prioritized checklist so the reviewer spends time where it matters.

---

## Commands

### `/code-review-checklist`

Generate a checklist from staged changes (`git diff --cached`).

### `/code-review-checklist [branch]`

Generate a checklist from the diff between `[branch]` and the current branch. Defaults to comparing against `main`.

```
/code-review-checklist feature/add-payments
/code-review-checklist main..HEAD
```

---

## How It Works

### Step 1: Get the diff

Run `git diff --cached --stat` (for staged) or `git diff [branch]...HEAD --stat` (for branch comparison) to get the list of changed files.

Then run `git diff --cached` or `git diff [branch]...HEAD` for the full diff content.

If no staged changes exist and no branch is specified, fall back to `git diff HEAD~1` and tell the user.

### Step 2: Categorize changed files

Group files by type:

| Category | File patterns |
|---|---|
| Database/Schema | `*.sql`, `*migration*`, `*schema*`, `prisma/schema.prisma` |
| API/Backend | `**/api/**`, `**/server/**`, `**/actions/**`, `*.resolver.*` |
| UI/Frontend | `*.tsx`, `*.jsx`, `*.vue`, `*.svelte` (in component dirs) |
| Config | `*.config.*`, `*.env*`, `package.json`, `tsconfig.*` |
| Tests | `*.test.*`, `*.spec.*`, `__tests__/**` |
| Types | `*.d.ts`, `types.*`, `**/types/**` |
| Styles | `*.css`, `*.scss`, `*.module.*` |

### Step 3: Analyze each category for risks

Run through the checklist generators below. Only include items that are actually relevant to the diff. Do not generate generic checklists.

### Step 4: Assign priorities

- P0 (blocks merge): Security holes, data loss risk, broken builds, missing auth checks
- P1 (should fix): Performance issues, missing error handling, test gaps, naming problems
- P2 (nice to have): Style nits, minor refactoring opportunities, documentation gaps

### Step 5: Output the checklist

Write to stdout. If the user wants a file, they can ask.

---

## Checklist Categories

### Logic Errors

Look for in the diff:

- Conditional logic that doesn't cover all cases (missing `else`, incomplete `switch`)
- Off-by-one errors in loops or array access
- Null/undefined access without guards
- Async operations without `await`
- State mutations where immutability is expected
- Race conditions in concurrent code
- Wrong comparison operators (`==` vs `===`, `>` vs `>=`)

Grep patterns to run:
```
# Missing await on async calls
grep -n "\.then\(" in changed files
# Loose equality
grep -n "[^!=]=[^=]" is unreliable, so check manually for == vs ===
```

### Security

Look for:

- SQL concatenation instead of parameterized queries
- `dangerouslySetInnerHTML` or equivalent
- User input passed directly to `eval`, `exec`, `child_process`, or shell commands
- Missing authentication middleware on new endpoints
- Missing authorization checks (user A accessing user B's data)
- Secrets or API keys in code (not env vars)
- CORS configuration changes
- New dependencies with network access

Grep patterns:
```bash
grep -rn "dangerouslySetInnerHTML" [changed tsx files]
grep -rn "eval(" [changed files]
grep -rn "exec(" [changed files]
grep -rn "password\|secret\|api_key\|apiKey" [changed files] --ignore-case
```

### Performance

Look for:

- N+1 query patterns (database call inside a loop)
- Missing indexes on new database columns used in WHERE clauses
- Large objects in React state causing unnecessary re-renders
- Missing `useMemo` / `useCallback` where dependency arrays matter
- Unbounded list rendering without virtualization
- Missing pagination on database queries
- Synchronous file I/O in request handlers
- Bundle size impact from new imports

### Naming and Style

Look for:

- Functions or variables whose names don't describe what they do
- Inconsistent naming conventions within the diff
- Abbreviations that aren't obvious (`usr`, `mgr`, `btn` in business logic)
- Boolean variables not phrased as questions (`isActive`, `hasPermission`)
- Magic numbers without named constants

### Test Coverage

Look for:

- New functions or endpoints with no corresponding test file changes
- Changed logic where existing tests weren't updated
- Test files that only test the happy path
- Mocked dependencies that hide real behavior
- Snapshot tests updated without reviewing the snapshot diff

Detection approach:
```bash
# List changed source files
git diff --cached --name-only | grep -v test | grep -v spec > /tmp/src_changes
# List changed test files
git diff --cached --name-only | grep -E "test|spec" > /tmp/test_changes
# Source files without matching test changes = potential gap
```

### Error Handling

Look for:

- `try/catch` blocks with empty catch or generic swallowing
- API calls without error responses defined
- `fetch` or HTTP calls without timeout or retry logic
- Promise chains without `.catch()`
- User-facing operations that fail silently
- Missing loading/error states in UI components

---

## Output Format

```markdown
# Review Checklist: [branch or "staged changes"]

**Files changed**: [N]
**Generated**: [date]

---

## P0 - Blocks Merge

- [ ] `src/api/payments.ts:42-58` - New endpoint missing auth middleware.
      All routes in this directory use `withAuth()` wrapper except this one.
- [ ] `prisma/migrations/003_add_balance.sql` - Column `balance` has no default value.
      Existing rows will fail on migration.

## P1 - Should Fix

- [ ] `src/components/UserList.tsx:15-30` - Database query inside `.map()` loop.
      Will execute N+1 queries. Consider fetching all users in one query.
- [ ] `src/api/payments.ts:60-62` - Catch block logs error but returns 200.
      Should return 500 or appropriate error status.
- [ ] `src/services/billing.ts` - New service with 4 public methods, no test file added.

## P2 - Nice to Have

- [ ] `src/utils/helpers.ts:12` - Variable `d` could be more descriptive.
      Maybe `daysSinceLastPayment`?
- [ ] `src/components/Dashboard.tsx:88` - Magic number `86400000`.
      Extract to `MS_PER_DAY` constant.

---

## Coverage Gaps

| Source File Changed | Has Test Changes |
|---|---|
| `src/services/billing.ts` (new) | No |
| `src/api/payments.ts` (modified) | No |
| `src/components/UserList.tsx` (modified) | Yes |

---

## Files by Risk

| File | Lines Changed | Risk Areas |
|---|---|---|
| `src/api/payments.ts` | +45 -2 | Auth, error handling |
| `prisma/migrations/003_add_balance.sql` | +12 | Data integrity |
| `src/services/billing.ts` | +89 | Untested, new logic |
| `src/components/UserList.tsx` | +15 -8 | Performance |
```

---

## Important Constraints

- Only flag things actually present in the diff. Do not generate a generic checklist.
- Every checklist item must reference a specific file and line range.
- Read the surrounding code (not just the diff) to understand context. A function added in the diff might be covered by a test file that wasn't changed.
- When a checklist item needs explanation, keep it to one sentence. The reviewer is not looking for an essay.
- If the diff is small (under 20 lines), the checklist might only have 2 items. That is fine.
- If there are zero issues found, say so. Do not invent problems.
