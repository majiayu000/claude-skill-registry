---
name: test:playwright
description: Write and review Playwright demo tests for Kagenti - markStep segments, assertions, selectors, narration alignment
---

# Write Playwright Demo Tests

Write Playwright tests for recording narrated demo videos of the Kagenti platform.

## When to Use

- Creating a new demo walkthrough test
- Reviewing an existing demo test for quality
- Fixing a failing demo test (wrong selectors, missing assertions)
- Called by `playwright-demo` before recording

## Test Location

Source tests: `.worktrees/playwright-demos/local_experiments/e2e/<name>.spec.ts`

## Required Structure

Every Playwright demo test MUST have:

### 1. Timestamp tracking

```typescript
const stepTimestamps: { step: string; time: number }[] = [];
const demoStartTime = Date.now();
const markStep = (step: string) => {
  const elapsed = (Date.now() - demoStartTime) / 1000;
  stepTimestamps.push({ step, time: elapsed });
  console.log(`[demo-ts] ${elapsed.toFixed(1)}s - ${step}`);
};
```

### 2. Cursor injection

Copy `injectCursor`, `humanMove`, `demoClick` from existing tests. These
create a visible red cursor dot in the video (headless Playwright has no cursor).

### 3. markStep at every visual transition

```typescript
markStep('section_name');  // MUST be outside any if/catch block
```

Rules:
- ALWAYS outside conditionals (narration sync depends on every step firing)
- Each section should be 3-15 seconds
- Names must match `[section]` markers in narration file exactly

### 4. Section-level assertions

Tests MUST fail if content doesn't load. Never use silent `.catch(() => {})`:

```typescript
// REQUIRED after login
expect(page.url()).not.toContain('/realms/');

// REQUIRED after SPA navigation
await expect(page).toHaveURL(/\/agents/, { timeout: 10000 });

// REQUIRED before critical interaction
await expect(element).toBeVisible({ timeout: 5000 });

// REQUIRED after content load
expect(cardCount, 'Page should have cards').toBeGreaterThan(0);
```

Keep `.catch()` ONLY for truly optional elements:
- VERIFY_PROFILE form fields
- scrollIntoViewIfNeeded
- waitForLoadState('networkidle')

### 5. SPA navigation (Kagenti pages)

Use sidebar clicks, NOT `page.goto()` — full reload loses Keycloak tokens:

```typescript
// CORRECT - SPA client-side routing
const link = page.locator('nav a').filter({ hasText: /^Agents$/ });
await demoClick(link.first(), 'Agents sidebar');

// WRONG - loses auth tokens
await page.goto(`${UI_URL}/agents`);
```

Use `page.goto()` only for external apps (MLflow, Phoenix, Kiali).

### 6. Timestamps file

Write at test end:

```typescript
const fs = require('fs');
const path = require('path');
const scriptDir = process.env.PLAYWRIGHT_OUTPUT_DIR || path.join(__dirname, '..');
const tsFile = path.join(scriptDir, '..', '<name>-timestamps.json');
fs.writeFileSync(tsFile, JSON.stringify(stepTimestamps, null, 2));
```

## Selector Patterns

Read UI source (`kagenti/ui-v2/src/pages/`) to find correct selectors:

| UI Pattern | Playwright Selector |
|------------|-------------------|
| PatternFly Button | `page.getByRole('button', { name: /text/i })` |
| PatternFly Tab | `page.getByRole('tab', { name: /text/i })` |
| React Router Link | `page.locator('nav a').filter({ hasText: /text/ })` |
| Aria label | `page.locator('[aria-label="Select namespace"]')` |
| Button with onClick (not `<a>`) | `page.getByRole('button', { name: /View Agents/i })` |
| PatternFly Card | `page.locator('.pf-v5-c-card')` |

### Multiple selector strategies

Try multiple selectors with `.or()` for resilience:

```typescript
const chatTab = page.getByRole('tab', { name: /Chat/i })
  .or(page.locator('button:has-text("Chat")'))
  .or(page.locator('.pf-v5-c-tabs__link:has-text("Chat")'));
```

## Narration File

Each test needs a matching narration file with one `[section]` per `markStep()`:

```
[intro]
Welcome to the Kay-jentee platform...

[login]
We authenticate through Keycloak...

[section_name]
Description of what's visible on screen.
```

Pronunciation: Kay-jentee, A-to-A, M-C-P, mutual TLS, O-I-D-C.

## Review Checklist

Before recording, verify:

- [ ] All `markStep()` calls outside conditionals
- [ ] Every section has `expect()` assertion (not silent `.catch()`)
- [ ] markStep names match narration `[section]` markers 1:1
- [ ] SPA navigation for Kagenti pages (not `page.goto()`)
- [ ] `demoClick()` used for cursor visibility (not `.click()`)
- [ ] Timestamps written to `<name>-timestamps.json`
- [ ] 10-second final pause
- [ ] Test passes without narration: `--no-narration`

## After Writing

1. Run test without narration to verify it passes
2. Fix any selector issues using `playwright-demo:debug`
3. Proceed to `playwright-demo` for recording with voiceover

## Related Skills

- `playwright-demo` -- Record videos (uses this skill's tests)
- `playwright-demo:debug` -- Fix failing selectors and auth
- `playwright-research` -- Analyze UI code for selectors
- `test:review` -- General test quality review patterns
