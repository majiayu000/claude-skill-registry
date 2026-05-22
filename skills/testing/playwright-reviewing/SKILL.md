---
name: playwright-reviewing
description: Review Playwright E2E tests for best practices violations. Detects mocked app data, explicit timeouts, CSS selectors, skipped tests, and assertion anti-patterns. Use when reviewing Playwright PRs or auditing test quality.
version: 1.0.0
---

# Playwright Code Review

## Purpose
Audit Playwright E2E tests for violations of best practices. Detects anti-patterns that cause flaky tests, hide bugs, or reduce maintainability.

## When NOT to Use
- Writing new tests (use `playwright-writing` skill instead)
- Unit test reviews (different patterns)
- API-only test reviews
- Non-Playwright E2E frameworks (Cypress, etc.)

---

## Review Workflow

### Step 1: Identify Playwright Test Files

```bash
# Find all Playwright test files
find . -name "*.spec.ts" -o -name "*.test.ts" | grep -v node_modules

# Or check specific directory
ls -la tests/e2e/ playwright/
```

### Step 2: Run Automated Violation Checks

Execute these checks in parallel for efficiency:

```bash
# === CRITICAL VIOLATIONS ===

# Find mocked application APIs (FORBIDDEN)
grep -rn "page.route('/api\|page.route(\"/api" --include="*.spec.ts" --include="*.test.ts"

# Find skipped tests (FORBIDDEN)
grep -rn "test.skip\|\.skip(\|test\.fixme" --include="*.spec.ts" --include="*.test.ts"

# Find commented-out tests
grep -rn "// test(\|// it(\|/\* test" --include="*.spec.ts" --include="*.test.ts"

# === HIGH PRIORITY VIOLATIONS ===

# Find waitForTimeout (FORBIDDEN)
grep -rn "waitForTimeout\|waitForTime" --include="*.spec.ts" --include="*.test.ts"

# Find CSS class selectors (FORBIDDEN)
grep -rn "\.locator('\.\|\.locator(\"\." --include="*.spec.ts" --include="*.test.ts"

# Find manual assertions without web-first (FORBIDDEN)
grep -rn "\.isVisible()).toBe\|\.isHidden()).toBe\|\.textContent()).toBe\|\.innerText()).toBe" --include="*.spec.ts" --include="*.test.ts"

# Find expect(await pattern (usually wrong)
grep -rn "expect(await.*\.isVisible\|expect(await.*\.isEnabled\|expect(await.*\.isChecked" --include="*.spec.ts" --include="*.test.ts"

# === MEDIUM PRIORITY CHECKS ===

# Find selectOption (may not work with Mantine)
grep -rn "\.selectOption(" --include="*.spec.ts" --include="*.test.ts"

# Find potential setTimeout/delay patterns
grep -rn "setTimeout\|new Promise.*resolve.*setTimeout" --include="*.spec.ts" --include="*.test.ts"
```

### Step 3: Manual Review

For each file, check:

1. **Locator Quality**
   - Are `getByRole`, `getByText`, `getByLabel` used?
   - Are CSS selectors avoided?
   - Is `data-testid` only used when necessary?

2. **Assertion Quality**
   - Are all assertions web-first (`await expect(locator).toBeVisible()`)?
   - No manual `isVisible()` / `textContent()` checks?

3. **Test Structure**
   - Is `beforeEach` used for common setup?
   - Are tests independent (no shared state)?
   - Is navigation handled properly?

4. **Mantine Components**
   - Are Mantine Selects handled with click pattern?
   - No `selectOption()` on Mantine components?

### Step 4: Report Findings

Use the output template below to report issues.

---

## Severity Classification

### CRITICAL (Must Fix Before Merge)

| Violation | Why It's Critical | Detection |
|-----------|-------------------|-----------|
| Mocked application API | Tests don't verify real behavior | `page.route('/api` |
| Skipped tests | Hides bugs, false confidence | `test.skip`, `.skip()` |
| Commented-out tests | Dead code, hidden failures | `// test(` |

### HIGH (Should Fix Before Merge)

| Violation | Why It's High Priority | Detection |
|-----------|------------------------|-----------|
| `waitForTimeout()` | Arbitrary delays cause flakiness | `waitForTimeout` |
| CSS class selectors | Fragile, break on styling changes | `.locator('.'` |
| Manual assertions | Race conditions, false positives | `isVisible()).toBe(true)` |
| `expect(await` pattern | Not web-first, misses auto-retry | `expect(await.*isVisible` |

### MEDIUM (Should Fix)

| Violation | Why It's Medium Priority | Detection |
|-----------|--------------------------|-----------|
| `selectOption` with Mantine | Won't work, test fails | Context review |
| Missing test isolation | Tests affect each other | No `beforeEach` |
| Poor locator choice | Less resilient to changes | `locator('#id')` |

### LOW (Suggestions)

| Suggestion | Benefit |
|------------|---------|
| Use `getByRole` over `getByTestId` | Better accessibility coverage |
| Add descriptive test names | Easier debugging |
| Group related tests in `describe` | Better organization |

---

## Critical Violation Details

### Mocked Application APIs

**FORBIDDEN:** Mocking YOUR application's API endpoints.

```typescript
// ❌ CRITICAL VIOLATION
await page.route('/api/users', route => route.fulfill({
  body: JSON.stringify([{ id: 1, name: 'Mock' }])
}));

// ❌ CRITICAL VIOLATION
await page.route('/api/products/**', route => route.fulfill({
  body: JSON.stringify({ price: 99.99 })
}));
```

**ALLOWED:** Mocking external third-party APIs only:
```typescript
// ✅ ACCEPTABLE - external service
await page.route('https://api.stripe.com/**', route => route.fulfill({ ... }));
```

**Review action:** Check if the mocked URL is YOUR API or an external service.

### Skipped Tests

**FORBIDDEN:** Using `.skip()` to hide failing tests.

```typescript
// ❌ CRITICAL VIOLATION
test.skip('checkout flow', async ({ page }) => { ... });

// ❌ CRITICAL VIOLATION
test('checkout flow', async ({ page }) => {
  test.skip(true, 'TODO: fix later');
});

// ❌ CRITICAL VIOLATION
test.fixme('broken test', async ({ page }) => { ... });
```

**Review action:** Require fix or removal. No exceptions without documented ticket.

---

## High Violation Details

### Explicit Timeouts

```typescript
// ❌ HIGH VIOLATION
await page.waitForTimeout(2000);
await page.waitForTimeout(500);

// ❌ HIGH VIOLATION
await new Promise(resolve => setTimeout(resolve, 1000));

// ✅ CORRECT - web-first assertion
await expect(page.getByText('Loaded')).toBeVisible();
```

### CSS Class Selectors

```typescript
// ❌ HIGH VIOLATION
page.locator('.btn-primary')
page.locator('.MuiButton-root')
page.locator('div.container > .item')

// ✅ CORRECT
page.getByRole('button', { name: 'Submit' })
page.getByTestId('submit-button')  // if disambiguation needed
```

### Manual Assertions

```typescript
// ❌ HIGH VIOLATION - no auto-wait/retry
expect(await page.locator('#status').isVisible()).toBe(true);
expect(await page.getByText('Hello').textContent()).toBe('Hello');

// ✅ CORRECT - web-first, auto-waits
await expect(page.getByTestId('status')).toBeVisible();
await expect(page.getByText('Hello')).toHaveText('Hello');
```

---

## Mantine Component Checks

### Select Components

```typescript
// ❌ HIGH VIOLATION - selectOption doesn't work with Mantine
await page.getByRole('combobox').selectOption('value');

// ✅ CORRECT pattern for Mantine Select
await page.locator('[data-testid="StatusSelect"]').click();
await page.locator('div[value="active"]').click();
```

**Review action:** If you see `selectOption`, check if it's a Mantine component.

---

## Review Output Template

```markdown
## Playwright Test Review: [File/PR Name]

### Summary
[1-2 sentence overview of findings]

### Critical Issues (Must Fix)
- [ ] **Mocked app API** - `tests/checkout.spec.ts:45` - Mocking `/api/cart`
- [ ] **Skipped test** - `tests/auth.spec.ts:23` - `test.skip('login flow')`

### High Priority (Should Fix)
- [ ] **waitForTimeout** - `tests/dashboard.spec.ts:67` - `waitForTimeout(2000)`
- [ ] **CSS selector** - `tests/form.spec.ts:34` - `.locator('.submit-btn')`
- [ ] **Manual assertion** - `tests/profile.spec.ts:89` - `isVisible()).toBe(true)`

### Medium Priority
- [ ] **selectOption on Mantine** - `tests/filters.spec.ts:56` - Review if Mantine component

### Passed Checks
- [x] No skipped tests
- [x] Web-first assertions used
- [x] User-facing locators preferred
- [x] Test isolation with beforeEach

### Recommendations
- [Optional improvements and suggestions]
```

---

## Quick Commands Reference

```bash
# Full audit - run all checks
grep -rn "waitForTimeout\|test\.skip\|\.skip(\|page\.route('/api\|\.locator('\.\|isVisible()).toBe" --include="*.spec.ts" --include="*.test.ts"

# Count violations by type
echo "=== waitForTimeout ===" && grep -c "waitForTimeout" **/*.spec.ts 2>/dev/null || echo "0"
echo "=== test.skip ===" && grep -c "test.skip\|\.skip(" **/*.spec.ts 2>/dev/null || echo "0"
echo "=== CSS selectors ===" && grep -c "\.locator('\." **/*.spec.ts 2>/dev/null || echo "0"
```

---

## Integration

**Related skills:**
- `playwright-writing` - Writing new tests (use for guidance)
- `run-tests` - Executing test suite
- `quality-check` - General code quality

**Cross-reference:** All rules in this review skill match those in `playwright-writing`.


---

## Related Agent

For comprehensive E2E testing guidance that coordinates this and other Playwright skills, use the **`playwright-e2e-expert`** agent.
