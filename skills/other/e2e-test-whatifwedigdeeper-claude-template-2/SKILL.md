---
skill: e2e-test
description: Create Playwright e2e tests for features in isolated worktree
location: project
---

# E2E Tests: $ARGUMENTS

Creates comprehensive Playwright end-to-end tests in an isolated git worktree.

## Arguments

- **Specific feature**: `login-form`, `dashboard`, `settings`
- **Glob pattern**: `user-*`, `*-modal`
- **All features**: `.` or `all`

## Process

### 1. Create Isolated Worktree

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
WORKTREE_PATH="../e2e-test-worktree-$TIMESTAMP"
git worktree add "$WORKTREE_PATH" -b "e2e-test-$TIMESTAMP"
```

### 2. Setup Playwright

If not installed:
```bash
npm install -D @playwright/test
npx playwright install --with-deps
```

Create `playwright.config.ts` if missing with standard configuration.

Add npm scripts if missing:
```json
{
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui",
  "test:e2e:debug": "playwright test --debug"
}
```

### 3. Identify Features

- For specific feature: Create single test file
- For glob: Search components/app directories, create tests for matches
- For `all`: List all components/routes, use Task tool with parallel subagents if >3 features

### 4. Generate Tests

Create `tests/e2e/[feature-name].spec.ts` with:
- Happy path scenarios
- Edge cases and error states
- Input validation
- Accessibility checks

**Selector strategy**: Use `data-testid` attributes. Add them to components if missing.

### 5. Run and Fix

```bash
npm run test:e2e
```

**Application fixes** (MUST be general, not test-specific):
- Add missing `data-testid` attributes
- Fix broken functionality
- Add proper loading states

**Test fixes**:
- Update selectors
- Fix assertions
- Add proper waits

### 6. Validate Full Suite

```bash
npm run build
npm run lint
npm test
npm run test:e2e
```

### 7. Report and Prompt

**On success**: Prompt to merge or keep for review
**On failure**: Categorize errors, offer debug or cleanup options

## Test Standards

- Use Page Object Model for complex features
- Test coverage: happy path, edge cases, errors, accessibility
- Prefer `data-testid` over CSS selectors
- Use `toBeVisible()` not arbitrary timeouts
- Tests must be deterministic and independent

## Parallel Execution

When >3 features to test:
- Split into groups of 1-2 features per agent
- Launch Task tool with general-purpose subagents
- Collect results and continue with validation
