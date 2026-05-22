---
name: code-quality-standards
description: "Apply code quality standards for testing, coverage, CI/CD, and automation: Vitest, coverage philosophy, git hooks, GitHub Actions, quality gates. Use when setting up testing, configuring CI, discussing quality practices, or reviewing automation."
---

# Code Quality Standards

Standards and practices for maintaining high code quality through testing, automation, and continuous integration.

## Testing Framework: Vitest

**Default test runner for all projects.**

**Why Vitest:**
- Fast, modern test runner
- Jest-compatible API (easy migration from Jest)
- Great TypeScript support
- Watch mode, coverage, snapshots built-in
- Works seamlessly with Vite projects

**Setup:**
```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
```

**Basic test structure:**
```typescript
import { describe, it, expect } from 'vitest'

describe('Module Name', () => {
  it('should do something', () => {
    expect(result).toBe(expected)
  })
})
```

## Coverage Philosophy: Test Boundaries, Not Lines

**Don't chase arbitrary percentage targets.**

### The Wrong Approach

❌ "We need 80% coverage"
❌ "This file has low coverage, add more tests"
❌ Testing implementation details to hit coverage goals
❌ Writing tests just to make coverage numbers green

### The Right Approach

✅ **Test module boundaries (inputs → outputs)**
- Public API surface, not internal implementation
- Contract between modules
- What callers depend on

✅ **Test critical paths and edge cases**
- Happy path (most common use case)
- Error conditions (what happens when things fail)
- Edge cases (boundary conditions, empty inputs, etc.)

✅ **Skip testing implementation details**
- Private functions (test through public API)
- UI component internals (test behavior, not implementation)
- Framework code (already tested by framework)

✅ **Coverage as diagnostic, not goal**
- Use coverage to find untested code paths
- Don't use coverage as success metric
- 60% meaningful coverage > 95% meaningless coverage

## Differential Coverage (Patch Coverage)

**Focus on new code, not absolute project coverage.**

**GitHub Actions Setup** (zero external services):
```yaml
# .github/workflows/test.yml
- uses: davelosert/vitest-coverage-report-action@v2
  with:
    file-coverage-mode: changes  # Only show changed files
```

**Standards**:
- **Patch coverage**: 80%+ for new/changed code (enforced)
- **Overall coverage**: Track but don't block (diagnostic only)
- **Critical paths**: 90%+ (payment, auth, data integrity)

**PR Comments**: Automatic via GitHub Action, no Codecov needed

### Coverage Integration: GitHub Actions (Recommended)

**Why Codecov:**
- GitHub integration for PR coverage reports
- Track coverage trends over time
- Block PRs that significantly drop coverage (configurable)

**Configuration:**
```yaml
# .codecov.yml
coverage:
  status:
    project:
      default:
        target: auto  # Maintain current coverage
        threshold: 5% # Allow 5% decrease
```

## Testing Boundaries

### Unit Tests
**What to test:**
- Pure functions (deterministic, no side effects)
- Utilities and helpers
- Isolated components (with mocked dependencies)

**Example:**
```typescript
// ✅ Good unit test
it('should format currency correctly', () => {
  expect(formatCurrency(1234.56)).toBe('$1,234.56')
})
```

### Integration Tests
**What to test:**
- Feature flows (multiple components working together)
- API contracts (request/response shapes)
- Component interactions (parent-child, state sharing)

**Example:**
```typescript
// ✅ Good integration test
it('should submit form and show success message', async () => {
  render(<ContactForm />)
  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com')
  await userEvent.click(screen.getByRole('button', { name: 'Submit' }))
  expect(await screen.findByText('Success!')).toBeInTheDocument()
})
```

### E2E Tests (Playwright)
**What to test:**
- Critical user journeys end-to-end
- Happy path through entire application
- Critical error scenarios

**NOT every feature needs E2E.**

**Example:**
```typescript
// ✅ Good E2E test
test('user can sign up and create first project', async ({ page }) => {
  await page.goto('/signup')
  await page.fill('input[name="email"]', 'user@example.com')
  await page.click('button:has-text("Sign Up")')
  await page.waitForURL('/projects')
  await page.click('button:has-text("New Project")')
  await expect(page.locator('h1')).toContainText('New Project')
})
```

## Git Hooks

**Purpose: Fast feedback before committing/pushing code.**

### Pre-Commit Hook
**Run on every commit (fast checks only):**

```json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm lint-staged"
  }
}
```

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{ts,tsx}": "tsc-files --noEmit"
  }
}
```

**What it does:**
- Lint staged files only (ESLint --fix)
- Format with Prettier
- Type-check staged files (tsc --noEmit)

**Why staged files only:**
- Fast feedback (seconds, not minutes)
- Only checks what you're committing
- Doesn't block on existing issues

### Pre-Push Hook
**Run before pushing (comprehensive checks):**

```json
{
  "simple-git-hooks": {
    "pre-push": "pnpm test:ci"
  }
}
```

```json
{
  "scripts": {
    "test:ci": "vitest run --coverage"
  }
}
```

**What it does:**
- Run full test suite
- Generate coverage report
- Ensures all tests pass before pushing

**Why pre-push:**
- Prevents breaking main/master
- Comprehensive validation before sharing code
- Can be skipped in emergencies (`git push --no-verify`)

### Hook Tooling

**Option 1: simple-git-hooks**
- Minimal, fast, no dependencies
- Just a script runner

**Option 2: Husky**
- More features, wider adoption
- Git hooks as npm scripts

**Either is fine — consistency matters more than choice.**

## CI/CD: GitHub Actions

### Required Checks

**Every PR must pass these checks:**

```yaml
# .github/workflows/ci.yml
name: CI
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm type-check
      - run: pnpm test:ci
      - run: pnpm build

      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

**Checks:**
1. **Lint** (ESLint) — No linting errors
2. **Type-check** (tsc --noEmit) — No TypeScript errors
3. **Tests** (Vitest with coverage) — All tests pass
4. **Build** — Production build succeeds
5. **Coverage** (Codecov) — Coverage maintained

### Optional But Recommended

- **E2E tests** (Playwright) on critical paths
- **Security scanning** (npm audit, Snyk)
- **Dependency updates** (Renovate, Dependabot)

## Quality Gates for PR Merge

**PR can only merge when:**

✅ All CI checks pass
✅ Coverage not significantly decreased (Codecov check)
✅ No new TypeScript errors introduced
✅ At least 1 approval (for team projects)
✅ No merge conflicts

**Enforce via GitHub branch protection rules:**
- Require status checks to pass
- Require pull request reviews (1+ approvals)
- Require branches to be up to date before merging

## Quick Setup Guide

### 1. Install Testing Dependencies

```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
pnpm add -D @vitest/coverage-v8  # For coverage
```

### 2. Configure Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './test/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
})
```

### 3. Setup Git Hooks

```bash
pnpm add -D simple-git-hooks lint-staged
```

```json
// package.json
{
  "simple-git-hooks": {
    "pre-commit": "pnpm lint-staged",
    "pre-push": "pnpm test:ci"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write", "tsc-files --noEmit"]
  }
}
```

```bash
# Initialize hooks
pnpm simple-git-hooks
```

### 4. Add npm Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ci": "vitest run --coverage",
    "lint": "eslint .",
    "type-check": "tsc --noEmit"
  }
}
```

### 5. Setup GitHub Actions

Create `.github/workflows/ci.yml` with required checks (see above).

### 6. Configure Codecov

Create `.codecov.yml` with coverage thresholds (see above).

## Philosophy

**Quality is not a checklist — it's a habit.**

Automation ensures baseline quality, but doesn't replace:
- Thoughtful design
- Code review
- Refactoring
- User feedback

**Tests verify the code does what you intended. They don't verify you intended the right thing.**

Use these tools to catch regressions and maintain standards. Use your judgment to build the right thing.
