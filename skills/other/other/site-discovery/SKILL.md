---
name: site-discovery
description: Systematic website exploration and mapping. Use when exploring a new website, mapping site structure, identifying pages to test, or understanding site architecture. Triggers on "explore", "discover", "map the site", "what pages exist", "site structure".
---

# Site Discovery

Systematically explore and map websites to understand what needs testing.

## CRITICAL: Playwright Session Behavior

**⚠️ EACH MCP CALL CREATES A NEW BROWSER SESSION. THE BROWSER CLOSES AFTER EACH CALL.**

### What This Means for Discovery

```
❌ WRONG:
Call 1: browser_navigate to homepage
Call 2: browser_click on category → FAILS (new blank browser!)

✅ CORRECT:
Call 1: browser_run_code with navigate + accept cookies + capture snapshot
Call 2: browser_run_code with navigate + accept cookies + click category + capture snapshot
       (must repeat ALL setup steps because session is gone)
```

### The Rule

For any multi-step exploration, use `browser_run_code` with ALL steps in one script.

If you need to explore a different page or interaction, you MUST start fresh:
1. Navigate to the URL
2. Accept cookies again
3. Perform the interaction
4. Capture snapshot

**There is no way to "continue" from a previous session.**

---

## Discovery Process

### Phase 1: Homepage Analysis

Use a single `browser_run_code` call to get everything:

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com\");

    // Handle cookies
    const acceptBtn = page.getByRole(\"button\", { name: /accept|agree|cookie/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(1000);
    }

    // Get all navigation links
    const navLinks = await page.locator(\"nav a, header a\").evaluateAll(els =>
      els.map(e => ({ text: e.textContent?.trim(), href: e.href }))
    );

    // Get footer links
    const footerLinks = await page.locator(\"footer a\").evaluateAll(els =>
      els.map(e => ({ text: e.textContent?.trim(), href: e.href }))
    );

    // Get all links for full mapping
    const allLinks = await page.getByRole(\"link\").evaluateAll(els =>
      els.slice(0, 50).map(e => ({
        text: e.textContent?.trim()?.substring(0, 50),
        href: e.href
      }))
    );

    // Get forms (login, search, etc.)
    const forms = await page.locator(\"form\").evaluateAll(els =>
      els.map(e => ({
        action: e.action,
        inputs: Array.from(e.querySelectorAll(\"input\")).map(i => ({
          type: i.type,
          name: i.name,
          placeholder: i.placeholder
        }))
      }))
    );

    // Get accessibility snapshot
    const snapshot = await page.accessibility.snapshot();

    return JSON.stringify({
      url: page.url(),
      title: await page.title(),
      navLinks,
      footerLinks,
      allLinks,
      forms,
      snapshot
    }, null, 2);
  "
}'
```

### Phase 2: Explore Subpages

For EACH subpage, run a NEW `browser_run_code` (previous session is closed!):

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com/login\");

    // Handle cookies AGAIN (new session!)
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    // Analyze this page
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
        type: e.type,
        testid: e.dataset.testid
      }))
    );

    const snapshot = await page.accessibility.snapshot();

    return JSON.stringify({
      url: page.url(),
      pageType: \"authentication\",
      inputs,
      buttons,
      snapshot
    }, null, 2);
  "
}'
```

### Phase 3: Explore Interactive Elements

To understand what clicking does (e.g., does it open a submenu or navigate?):

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com\");

    // Handle cookies
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    const initialUrl = page.url();

    // Click on navigation element
    const navItem = page.getByRole(\"link\", { name: /products/i }).first();
    await navItem.click();
    await page.waitForTimeout(1500);

    const afterClickUrl = page.url();
    const didNavigate = afterClickUrl !== initialUrl;

    // Check if submenu appeared
    const submenuVisible = await page.locator(\"[class*=submenu], [class*=dropdown]\").isVisible().catch(() => false);

    // Look for \"View all\" type links
    const viewAllLinks = await page.getByRole(\"link\").filter({ hasText: /view all|see all|vezi toate/i }).allTextContents();

    const snapshot = await page.accessibility.snapshot();

    return JSON.stringify({
      initialUrl,
      afterClickUrl,
      didNavigate,
      submenuVisible,
      viewAllLinks,
      snapshot
    }, null, 2);
  "
}'
```

---

## Phase 4: Discover Behavioral Data (For Negative Tests)

**MANDATORY before writing negative tests!** You must discover actual error messages, validation text, and UI behavior.

### Why This Matters

You cannot assume:
- What error message appears on failed login
- How validation errors are displayed
- What text/class/role error elements have
- Whether errors appear inline, as toasts, or in alerts

### Discover Login Error Behavior

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com/login\");

    // Handle cookies
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    // Trigger login failure with invalid credentials
    await page.fill(\"input[type=email]\", \"fake_user_12345@nonexistent.com\");
    await page.fill(\"input[type=password]\", \"WrongPassword123!\");
    await page.click(\"button[type=submit]\");

    // Wait for error response
    await page.waitForTimeout(3000);

    // Capture ALL error-related elements
    const errors = await page.locator(\"[class*=error], [class*=Error], [role=alert], [data-testid*=error]\").evaluateAll(els =>
      els.map(e => ({
        text: e.textContent?.trim(),
        className: e.className,
        role: e.getAttribute(\"role\"),
        testid: e.dataset?.testid,
        tagName: e.tagName,
        isVisible: e.offsetParent !== null
      }))
    );

    // Check for toast/snackbar notifications
    const toasts = await page.locator(\"[class*=toast], [class*=notification], [class*=snackbar], [class*=alert]\").evaluateAll(els =>
      els.map(e => ({
        text: e.textContent?.trim(),
        className: e.className,
        isVisible: e.offsetParent !== null
      }))
    );

    return JSON.stringify({
      url: page.url(),
      errors: errors.filter(e => e.isVisible),
      toasts: toasts.filter(t => t.isVisible)
    }, null, 2);
  "
}'
```

### Discover Form Validation Behavior

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com/login\");

    // Handle cookies
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
    }

    // Test 1: Empty form submission
    await page.click(\"button[type=submit]\");
    await page.waitForTimeout(500);

    // Check HTML5 validation messages
    const emailInput = page.locator(\"input[type=email]\");
    const emailValidation = await emailInput.evaluate((el) => ({
      validationMessage: el.validationMessage,
      validity: {
        valueMissing: el.validity.valueMissing,
        typeMismatch: el.validity.typeMismatch
      }
    }));

    // Test 2: Invalid email format
    await page.fill(\"input[type=email]\", \"not-an-email\");
    await page.click(\"button[type=submit]\");
    await page.waitForTimeout(500);

    const emailFormatValidation = await emailInput.evaluate((el) => ({
      validationMessage: el.validationMessage,
      validity: {
        typeMismatch: el.validity.typeMismatch
      }
    }));

    // Check for custom validation messages near inputs
    const customErrors = await page.locator(\"input ~ [class*=error], input + [class*=error], [class*=field-error]\").evaluateAll(els =>
      els.map(e => ({
        text: e.textContent?.trim(),
        className: e.className
      }))
    );

    return JSON.stringify({
      emptyEmailValidation: emailValidation,
      invalidEmailValidation: emailFormatValidation,
      customErrors
    }, null, 2);
  "
}'
```

### Discover Success State Behavior

```bash
python .claude/skills/mcp-client/scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    // Example: Discover what happens on successful action
    await page.goto(\"https://example.com/search\");

    // Perform action
    await page.fill(\"input[type=search]\", \"test query\");
    await page.click(\"button[type=submit]\");

    // Wait for navigation or results
    await page.waitForLoadState(\"networkidle\");

    return JSON.stringify({
      finalUrl: page.url(),
      urlContainsQuery: page.url().includes(\"test\") || page.url().includes(\"q=\"),
      title: await page.title()
    }, null, 2);
  "
}'
```

### Document Discovered Behavior

Add to your site map:

```markdown
## Discovered UI Behaviors

### Login Errors
- **Invalid credentials**: "Email sau parolă incorectă" (role="alert")
- **Empty email**: HTML5 validation "Please fill out this field"
- **Invalid email format**: HTML5 validation "Please include an '@' in the email address"

### Form Validation
- Validation appears: inline below input
- Error class: `.error-message`
- Required fields show: HTML5 native validation

### Success States
- Login success: Redirects to /dashboard
- Search success: URL contains ?q={query}
```

---

## Page Classification

For each discovered page, classify as:

| Type | Indicators |
|------|------------|
| **Authentication** | /login, /register, password field |
| **Listing** | Multiple items, filters, pagination |
| **Detail** | Single item focus, add to cart |
| **Transaction** | Cart, checkout, payment |
| **Form** | Contact, application, feedback |
| **Content** | Blog, about, FAQ |
| **Dashboard** | Requires auth, user data |

See [references/page-classification.md](references/page-classification.md) for detailed indicators.

---

## Output Format

```markdown
# Site Map: [Website Name]

## Statistics
- Pages discovered: X
- Requires auth: Y
- Critical paths: Z

## Pages

### Authentication (P0)
| URL | Type | Auth Required |
|-----|------|---------------|
| /login | Login | No |
| /register | Registration | No |

### Core Features (P0)
| URL | Type | Auth Required |
|-----|------|---------------|
| / | Homepage | No |
| /products | Listing | No |
| /cart | Cart | No |

### User Area (P1)
| URL | Type | Auth Required |
|-----|------|---------------|
| /account | Dashboard | Yes |
| /orders | Order History | Yes |

## URL Patterns
- /products/:id - Product detail pages
- /category/:slug - Category pages

## Auth Barriers
- /account/* requires login
- /checkout requires login

## Navigation Behavior
- Category links open submenus (click "View all" to navigate)
- User menu requires hover to reveal
```

---

## Limits

| Scope | Max Pages | Max Depth |
|-------|-----------|-----------|
| Smoke | 20 | 2 |
| Regression | 100 | 4 |

## Edge Cases

**Login wall:** Map public pages first, note auth requirement
**Large site:** Focus on main nav, sample from large sections
**SPA:** Watch for URL hash changes, trigger nav via clicks
**Multi-step nav:** Some clicks open submenus, not pages - document the behavior

## Remember

**Every exploration requires a fresh `browser_run_code` call that includes:**
1. Navigation to URL
2. Cookie acceptance (session is new!)
3. Any interactions needed
4. Snapshot capture

**You cannot "continue" from a previous exploration. Start fresh each time.**
