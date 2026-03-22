---
name: product-verification
description: >
  Test, validate, and verify that code changes produce correct product behavior.
  Use when the user says 'verify this works', 'test the feature', 'check the output',
  'does this actually work', 'validate the behavior', 'smoke test', 'QA this',
  'acceptance test', or 'make sure it works end to end'. Also triggers on
  'product verification', 'behavior validation', 'functional check',
  'integration verification', 'sanity check', or after completing a feature implementation.
version: 1.0.0
---

# Product Verification

Code that compiles is not code that works. This skill closes the gap between "it builds" and "it does what users expect." Verification validates user-visible outcomes, not implementation details. A green build badge means nothing if the login button sends users to a 404.

## When to Activate

- **After implementing a feature** — before opening a PR, verify the feature does what it claims.
- **After a bug fix** — confirm the fix resolves the reported behavior, not just the symptom.
- **After refactoring** — regression-check that existing behavior is preserved.
- **On explicit request** — user says "verify", "test this", "QA", "smoke test", "does this work", "sanity check".
- **Before deployment** — final gate before code reaches users.

## Verification Hierarchy

Ordered by signal value. Start at Level 1 and climb until confidence is sufficient.

### Level 1: Structural

Does it compile and build without errors?

- Run `tsc --noEmit` for TypeScript projects
- Run the project's build command (`npm run build`, `cargo build`, etc.)
- Check for lint errors that indicate logic problems
- This is the minimum bar. Passing Level 1 means almost nothing about correctness.

### Level 2: Unit Behavior

Do individual functions produce expected outputs for known inputs?

- Call functions with representative inputs and assert outputs
- Test boundary values (zero, empty string, null, max values)
- Verify error cases throw or return expected errors
- Focus on functions that contain the changed logic

### Level 3: Integration

Do components work together correctly?

- API endpoints return expected response shapes and status codes
- Database operations persist and retrieve data correctly
- Service-to-service calls pass correct payloads
- Authentication and authorization gates behave as expected
- Queue/event producers and consumers agree on message format

### Level 4: Product Behavior

Does the user-visible flow work end-to-end?

- Walk through the user journey from entry point to completion
- Browser automation for UI flows (Playwright)
- Full API flow testing: create -> read -> update -> delete
- Verify side effects: emails sent, notifications triggered, logs written
- Check that the UI reflects the backend state accurately

### Level 5: Edge Cases

What happens when things go wrong?

- Bad input: malformed data, missing fields, oversized payloads
- Network failures: timeouts, connection refused, partial responses
- Concurrent access: two users editing the same resource
- Permission boundaries: accessing resources you should not own
- State transitions: what happens if a step is skipped or repeated

## Verification Workflow

### Step 1: Define Acceptance Criteria

Before touching any test runner, write down what must be true for this change to be considered working. Be specific and observable.

Bad: "The search feature works."
Good: "Searching for 'widget' returns products containing 'widget' in the name, sorted by relevance, with a maximum of 20 results per page."

Extract criteria from:
- The issue or ticket description
- The PR description or commit messages
- Conversation with the user
- The code diff itself (what changed implies what should be verified)

### Step 2: Choose Verification Level

Not everything needs E2E browser automation. Match effort to risk.

| Change Type | Recommended Level |
|---|---|
| Utility function change | Level 2 (Unit) |
| API endpoint change | Level 3 (Integration) |
| UI feature | Level 4 (Product Behavior) |
| Bug fix | Level that reproduces the bug |
| Refactoring | Level of the highest-risk change |
| Security fix | Level 3 + Level 5 |

### Step 3: Execute Verification

Run the appropriate checks. Capture evidence for every criterion.

- **Run existing tests first** — `npm test`, `pytest`, `cargo test`. If they pass, that is baseline confidence.
- **Write targeted checks** for gaps the existing suite does not cover.
- **Call real endpoints** when integration verification is needed. Use `curl`, `fetch`, or the project's HTTP client.
- **Automate browser flows** with Playwright when UI behavior is in scope.
- **Inspect state directly** — query the database, check file output, read logs.

### Step 4: Report Results

Produce a structured verification report. Every criterion gets a verdict.

```
VERIFICATION REPORT
===================
Feature: [name]
Criteria: [N total]

[PASS] Criterion 1: [description] — [evidence]
[FAIL] Criterion 2: [description] — [what went wrong]
[SKIP] Criterion 3: [description] — [why skipped]

Result: [X/N passed] — [VERIFIED / NOT VERIFIED]
```

If any criterion fails:
1. Report the failure with evidence (error message, screenshot, wrong output).
2. Identify the root cause if possible.
3. Suggest a fix or next debugging step.
4. Do not mark the feature as verified.

## Verification Techniques

### API Testing

Use `curl` or the project's HTTP client to hit real endpoints.

```bash
# Verify a GET endpoint returns expected data
curl -s http://localhost:3000/api/products/1 | jq '.name'

# Verify a POST endpoint creates a resource
curl -s -X POST http://localhost:3000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "price": 9.99}' | jq '.id'

# Verify error handling
curl -s -w "\n%{http_code}" http://localhost:3000/api/products/nonexistent
```

### Browser Automation

Use Playwright for UI verification. See `references/browser-testing-patterns.md` for detailed patterns.

```typescript
const page = await browser.newPage()
await page.goto('http://localhost:3000/login')
await page.fill('[name="email"]', 'user@example.com')
await page.fill('[name="password"]', 'password')
await page.click('button[type="submit"]')
await page.waitForURL('**/dashboard')
// Verify the dashboard loaded with user data
await expect(page.locator('h1')).toContainText('Welcome')
```

### Database State Inspection

Verify that operations actually persisted correctly.

```bash
# Check a record was created
psql -c "SELECT name, price FROM products WHERE id = 1;"

# Verify a migration ran
psql -c "SELECT column_name FROM information_schema.columns WHERE table_name = 'products';"
```

### Log Output Analysis

Verify event sequences by inspecting logs.

```bash
# Check that a background job completed
grep "job:complete" logs/worker.log | tail -5

# Verify an email was queued
grep "email:send" logs/app.log | grep "user@example.com"
```

## Gotchas

### Verification Is Not Testing

Verification checks product behavior; testing checks code paths. A test suite with 95% coverage can miss that the checkout button does not actually charge the credit card. Verification asks: "Does the product do what the user expects?" Do not conflate coverage metrics with behavioral confidence.

### Environment Differences

A verification that passes locally may fail in staging or production. Common causes:
- Different environment variables or configuration
- Missing permissions or IAM roles
- Different data sets (empty DB vs. seeded DB)
- Network policies blocking service-to-service calls

Always note which environment verification was performed in.

### Race Conditions in UI Verification

Never use `sleep()` or fixed delays. UI timing is nondeterministic. Use explicit waits:
- `waitForSelector` — wait for an element to appear
- `waitForURL` — wait for navigation to complete
- `waitForResponse` — wait for a specific API call to return
- `waitForLoadState` — wait for the page to finish loading

### Scope Creep

Verify the change, not the entire product. Define acceptance criteria before starting and stick to them. If you discover unrelated issues during verification, note them separately but do not expand the scope of the current verification.

### False Positives

A 200 status code does not mean the response is correct. Always verify the response body, not just the status. A form submission that returns "success" but does not persist the data is a false positive. Check the actual outcome, not the acknowledgment.

### State Pollution

Previous test runs, manual testing, or seed data can make verification results unreliable. A test that passes because the expected data already exists from a previous run is not a real pass. When possible:
- Use a clean database or isolated test environment
- Create test data explicitly at the start of verification
- Clean up test data after verification completes
- Use unique identifiers to avoid collisions with existing data
