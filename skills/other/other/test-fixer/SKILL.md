---
name: test-fixer
description: |
  Automatically debug and fix failing Playwright tests by navigating to the failed step using browser automation.
  Use when: (1) A Playwright test fails after creation or execution, (2) Test selectors are broken or outdated,
  (3) Page structure has changed and tests need updating, (4) Need to visually inspect what the test sees vs expects.
  Triggers on: "test failed", "fix the test", "selector not found", "element not visible", "timeout", test errors.
---

# Test Fixer

Debug and fix failing Playwright tests by visually inspecting the actual page state.

> **⚠️ CRITICAL: Browser Session Behavior**
>
> Each MCP call = new browser session. Browser CLOSES after each call.
> You CANNOT navigate in one call and interact in another.
> Use `browser_run_code` for ALL test debugging.
> If you need to return to a specific state (e.g., after login), you MUST redo ALL steps from scratch.

## Workflow

1. **Parse the error** - Extract failing test file, line number, selector, and error type
2. **Capture page state** - Use `browser_run_code` to navigate AND interact in one session
3. **Analyze the issue** - Compare expected vs actual selectors/state
4. **Fix the code** - Update page object and/or test spec
5. **Verify** - Re-run the single failing test

## Step 1: Parse Error

Extract from test output:
- **File path**: e.g., `tests/olx-landing.spec.ts:45`
- **Error type**: timeout, strict mode violation, element not found, assertion failed
- **Failing selector**: the locator that failed
- **Expected vs received**: for assertion errors

## Step 2: Capture Page State

### CRITICAL: Browser Session Behavior

**Each MCP call creates a NEW browser session. For multi-step operations, use `browser_run_code`!**

### Option A: Single `browser_run_code` Call (Recommended)

Run all exploration steps in one session:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    // Navigate to page
    await page.goto(\"https://www.olx.ro\");

    // Handle cookies
    const acceptBtn = page.getByRole(\"button\", { name: \"Accept\" });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    // Replicate test steps up to failure
    const categoryLink = page.getByRole(\"link\", { name: /Auto, moto/i }).first();
    await categoryLink.click();
    await page.waitForTimeout(1500);

    // Capture state at failure point
    const snapshot = await page.accessibility.snapshot();
    return JSON.stringify({
      url: page.url(),
      didNavigate: page.url().includes(\"auto\"),
      snapshot: snapshot
    }, null, 2);
  "
}'
```

### Option B: Simple Navigate (When No Interactions Needed)

`browser_navigate` returns both page AND snapshot in one call:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'
```

### Option C: Run Test in Debug Mode

For complex scenarios requiring visual debugging:

```bash
# Run the specific failing test with headed browser and pause on failure
npx playwright test "tests/example.spec.ts:45" --headed --debug
```

### Option D: Use Test Artifacts

Check the test-results folder for screenshots and traces:

```bash
# View trace from failed test
npx playwright show-trace test-results/*/trace.zip
```

## Step 3: Analyze Issue

| Error Type | Analysis | Typical Fix |
|------------|----------|-------------|
| `strict mode violation` | Multiple elements match | Add `.first()`, use more specific selector |
| `element not visible` | Element exists but hidden | Wait for visibility, check cookie banners |
| `timeout waiting for selector` | Selector outdated | Update to match actual DOM |
| `toHaveURL failed` | Navigation didn't happen | Add waitForURL, check click target |
| `toContainText failed` | **Wrong assumed text** | Discover actual error message text |
| `click opens submenu, not page` | Multi-step interaction needed | Add click on "View all" or final nav link |

### Common Issue: Wrong Assumed Text

If assertion fails on `toContainText` or `toHaveText`, the test probably assumed the wrong error message.

**Fix:** Discover the actual text:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com/login\");

    // Cookies
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
    }

    // Trigger the error condition
    await page.fill(\"input[type=email]\", \"wrong@test.com\");
    await page.fill(\"input[type=password]\", \"wrongpass\");
    await page.click(\"button[type=submit]\");
    await page.waitForTimeout(3000);

    // Capture ACTUAL error text
    const errors = await page.locator(\"[class*=error], [role=alert]\").evaluateAll(els =>
      els.filter(e => e.offsetParent !== null).map(e => ({
        text: e.textContent?.trim(),
        selector: e.className ? \".\" + e.className.split(\" \")[0] : \"[role=alert]\"
      }))
    );

    return JSON.stringify({ errors }, null, 2);
  "
}'
```

Then update test with actual text:
```typescript
// Before (assumed)
await expect(page.locator('.error')).toContainText('Invalid credentials');

// After (discovered)
await expect(page.getByRole('alert')).toContainText('Email sau parolă incorectă');
```

### Selector Priority (best to worst)

1. `getByRole()` - Accessible, stable
2. `getByTestId()` - Stable if devs maintain it
3. `getByText()` - Readable, somewhat stable
4. `locator('[href="..."]')` - For links
5. CSS selectors - Last resort

### Understanding Element Behavior

Use `browser_run_code` to test what clicking does:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://www.olx.ro\");

    // Dismiss cookies
    const acceptBtn = page.getByRole(\"button\", { name: \"Accept\" });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
    }

    // Record initial state
    const initialUrl = page.url();

    // Click the element that failed
    const element = page.getByRole(\"link\", { name: /Auto, moto/i }).first();
    await element.click();
    await page.waitForTimeout(1500);

    // Analyze what happened
    const finalUrl = page.url();
    const didNavigate = finalUrl !== initialUrl;

    // Look for submenus or dropdowns
    const submenuVisible = await page.locator(\"[class*=submenu], [class*=dropdown], [class*=menu]\").first().isVisible().catch(() => false);

    // Get visible links that might be \"View all\" type
    const navLinks = await page.getByRole(\"link\").filter({ hasText: /vezi|view|all|toate/i }).allTextContents();

    const snapshot = await page.accessibility.snapshot();

    return JSON.stringify({
      initialUrl,
      finalUrl,
      didNavigate,
      submenuVisible,
      navLinks,
      snapshot
    }, null, 2);
  "
}'
```

## Step 4: Fix the Code

### Page Object Updates

When selectors break, update the page object locator:

```typescript
// Before (broken)
this.searchButton = page.getByRole('button', { name: 'Search' });

// After (from snapshot showing actual name)
this.searchButton = page.getByRole('button', { name: /Căutare/i });
```

### Test Updates

When assertions fail, update test logic:

```typescript
// Before (navigation not waiting)
await categoryLink.click();
await expect(page).toHaveURL(/category/);

// After (proper navigation wait)
await Promise.all([
  page.waitForURL(/category/),
  categoryLink.click()
]);
```

### Multi-Step Navigation Fixes

When click opens submenu instead of navigating:

```typescript
// Before (assumes direct navigation)
async navigateToCategory(categoryName: string) {
  await this.page.getByRole('link', { name: categoryName }).click();
}

// After (handles submenu)
async navigateToCategory(categoryName: string) {
  // Click category to open submenu
  const categoryLink = this.page.getByRole('link', { name: categoryName }).first();
  await categoryLink.click();

  // Click "View all" to actually navigate
  const viewAllLink = this.page.getByRole('link', { name: /Vezi toate anunturile/i });
  await viewAllLink.click();
}
```

## Common Fixes Reference

### Cookie Banner Blocking

```typescript
// Add to page object
async acceptCookies() {
  const banner = this.page.getByRole('dialog').filter({ hasText: /cookie|privacy/i });
  if (await banner.isVisible({ timeout: 2000 }).catch(() => false)) {
    await this.page.getByRole('button', { name: /accept|agree/i }).click();
  }
}
```

### Multiple Elements Match

```typescript
// Use .first() for first match
await page.getByRole('link', { name: 'Category' }).first().click();

// Or use more specific parent context
await page.locator('nav').getByRole('link', { name: 'Category' }).click();

// Or use getByTestId if available
await page.getByTestId('login-submit-button').click();
```

### Element Not Ready

```typescript
// Wait for element to be actionable
await expect(element).toBeVisible();
await element.click();

// Or wait for network idle
await page.waitForLoadState('networkidle');
```

### Navigation Not Completing

```typescript
// Wait for URL change explicitly
await Promise.all([
  page.waitForURL(/expected-path/),
  triggerElement.click()
]);
```

## Step 5: Verify

Re-run only the failing test:

```bash
npx playwright test "tests/olx-landing.spec.ts" -g "Category links navigate correctly"
```

Or run by line number:

```bash
npx playwright test tests/olx-landing.spec.ts:45
```

## Checklist Before Fixing

- [ ] Read the failing test file
- [ ] Navigate to the URL the test uses (with `browser_run_code`)
- [ ] Accept cookies/dismiss popups if present
- [ ] **Replicate test steps up to failure**
- [ ] Capture fresh DOM snapshot
- [ ] **Understand actual UI behavior** (dropdowns, submenus, multi-step flows)
- [ ] Find the actual element in snapshot
- [ ] Update selector AND flow to match reality
- [ ] Re-run the single failing test to verify

## Common Misunderstandings

| Assumption | Reality | Fix |
|------------|---------|-----|
| Click navigates directly | Opens submenu first | Add step to click "View all" or similar |
| Element is immediately visible | Requires scroll or hover | Add `scrollIntoViewIfNeeded()` or hover action |
| Form submits on button click | Requires Enter key or specific trigger | Use correct submission method |
| Modal closes on outside click | Requires explicit close button | Click the close/X button |
| Page loads immediately | Redirect to different domain | Add `waitForURL` with correct domain pattern |

## References

See **[references/error-patterns.md](references/error-patterns.md)** for detailed diagnosis and fixes for:
- Timeout errors (selector, URL)
- Strict mode violations
- Assertion failures (text, URL)
- Element state errors (not visible, disabled)
- Navigation issues

## Quick Debug Script

For complex debugging, use this exploration script:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    // ====== CUSTOMIZE THIS SECTION ======
    const URL = \"https://www.olx.ro/cont/\";
    const WAIT_FOR_REDIRECT = /login\\.olx\\.ro/;
    // =====================================

    await page.goto(URL);

    // Handle cookies
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    // Wait for redirect if specified
    if (WAIT_FOR_REDIRECT) {
      await page.waitForURL(WAIT_FOR_REDIRECT, { timeout: 10000 });
    }

    // Get comprehensive element info
    const inputs = await page.locator(\"input\").evaluateAll(els =>
      els.map(e => ({
        type: e.type,
        name: e.name,
        placeholder: e.placeholder,
        testid: e.dataset.testid
      }))
    );

    const buttons = await page.locator(\"button\").evaluateAll(els =>
      els.map(e => ({
        text: e.textContent?.trim(),
        testid: e.dataset.testid,
        type: e.type
      }))
    );

    const links = await page.getByRole(\"link\").evaluateAll(els =>
      els.slice(0, 20).map(e => ({
        text: e.textContent?.trim()?.substring(0, 50),
        href: e.href
      }))
    );

    const snapshot = await page.accessibility.snapshot();

    return JSON.stringify({
      url: page.url(),
      inputs,
      buttons,
      links,
      snapshot
    }, null, 2);
  "
}'
```
