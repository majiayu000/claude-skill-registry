---
description: Use for visual UI verification with Playwright MCP. Test user flows, verify UI states, and catch visual regressions.
---

# Visual Testing with Playwright

> "If you didn't see it with your own eyes, how do you know it works?"

## When to Apply

- **Always:** UI features, user flows, state changes, form interactions
- **Especially:** Features with visual feedback (loading states, toasts, modals)
- **Skip:** Pure backend changes, API-only features, CLI tools

## Available Tools

Playwright MCP provides browser control via these tools:

| Tool | Purpose |
|------|---------|
| `mcp__playwright__browser_navigate` | Go to a URL |
| `mcp__playwright__browser_click` | Click an element |
| `mcp__playwright__browser_type` | Type into an input |
| `mcp__playwright__browser_select_option` | Select from dropdown |
| `mcp__playwright__browser_hover` | Hover over element |
| `mcp__playwright__browser_screenshot` | Capture screenshot |
| `mcp__playwright__browser_evaluate` | Run JavaScript |
| `mcp__playwright__browser_close` | Close browser |

## The Workflow

### 1. Start Dev Server

Ensure the app is running before visual testing:

```bash
# Check if already running
curl -s http://localhost:3000 > /dev/null && echo "Server running" || pnpm dev &
```

### 2. Navigate to Feature

```
mcp__playwright__browser_navigate({ url: "http://localhost:3000/documents/test-doc" })
```

### 3. Interact with UI

Test the actual user flow, not just static rendering:

```
# Click the edit button
mcp__playwright__browser_click({ selector: "button[aria-label='Edit']" })

# Type in the editor
mcp__playwright__browser_type({ selector: ".ProseMirror", text: "Hello world" })

# Wait for auto-save indicator
mcp__playwright__browser_screenshot({ filename: "after-edit.png" })
```

### 4. Capture Key States

Screenshot the important UI states:

- **Initial load** - Does the page render correctly?
- **After interaction** - Did the state change visually?
- **Success/error states** - Is feedback visible?
- **Edge cases** - Empty states, loading states

### 5. Verify with Vision

Claude can analyze screenshots to verify:

- Element visibility and positioning
- Text content and formatting
- Color and styling
- Layout and responsiveness
- Error messages and feedback

## Selectors

Use stable selectors in this priority order:

1. **Role/Label** (best): `button[aria-label='Save']`, `input[name='email']`
2. **Test ID**: `[data-testid='submit-btn']`
3. **Semantic HTML**: `button`, `input[type='email']`
4. **Class** (avoid): `.btn-primary` (brittle)

## Common Flows

### Document Editing

```
1. Navigate to /documents/{id}
2. Click in editor
3. Type content
4. Screenshot → verify "Saving..." appears
5. Wait 1 second
6. Screenshot → verify "Saved" appears
7. Navigate away and back
8. Screenshot → verify content persisted
```

### Form Submission

```
1. Navigate to form page
2. Fill required fields with browser_type
3. Screenshot → verify form state
4. Click submit
5. Screenshot → verify success/error state
6. If error, verify message is helpful
```

### Navigation Flow

```
1. Navigate to starting page
2. Screenshot initial state
3. Click navigation element
4. Screenshot → verify correct page loaded
5. Click back
6. Screenshot → verify return to original
```

## Authentication for Protected Pages

Most Brief pages require authentication. Playwright tests use `@clerk/testing` to handle this.

### Environment Variables

Set these in your `.env` or shell:

```bash
PLAYWRIGHT_TEST_USER_EMAIL=test@example.com
PLAYWRIGHT_TEST_USER_PASSWORD=your-test-password
```

### How It Works

1. **Auth Setup** (`e2e/auth.setup.ts`):
   - Uses `setupClerkTestingToken()` to bypass bot detection
   - Signs in with test credentials
   - Saves auth state to `playwright/.clerk/user.json`

2. **Test Projects** (`playwright.config.ts`):
   - `chromium`: Authenticated tests (loads saved auth state)
   - `chromium-no-auth`: Unauthenticated tests (for sign-in flow testing)

3. **State Persistence**:
   - Auth state is saved after first sign-in
   - Subsequent runs reuse the saved session
   - State files are gitignored

### Running Authenticated Tests

```bash
# Run all tests (will authenticate first)
pnpm test:e2e

# Run only authenticated tests
pnpm test:e2e --project=chromium

# Run only unauthenticated tests
pnpm test:e2e --project=chromium-no-auth
```

### For MCP Visual Testing

The Playwright MCP browser is a **separate instance** from the Playwright test runner, so it doesn't automatically load saved auth state. The MCP browser persists cookies within a Claude Code session, so you only need to sign in once per session.

> **⚠️ CRITICAL: Clerk uses MULTI-STEP sign-in!**
> 1. Page 1: Enter EMAIL only → click Continue
> 2. Page 2 (`/sign-in/factor-one`): Enter PASSWORD → click Continue
>
> Do NOT try to fill password on the email page - it doesn't exist there!

**Test credentials** (from `.env.local`):
- Email: `PLAYWRIGHT_TEST_USER_EMAIL` (test@briefhq.ai)
- Password: `PLAYWRIGHT_TEST_USER_PASSWORD`

#### Sign-in Flow via MCP

1. **Navigate to sign-in:**
   ```text
   mcp__playwright__browser_navigate({ url: "http://localhost:3000/sign-in" })
   ```

2. **Take a snapshot to get element refs:**
   ```text
   mcp__playwright__browser_snapshot()
   ```

3. **Fill email and continue:**
   ```text
   mcp__playwright__browser_type({ ref: "[identifier-input-ref]", text: "test@briefhq.ai", element: "Email input" })
   mcp__playwright__browser_click({ ref: "[continue-button-ref]", element: "Continue button" })
   ```

4. **Wait for password step, take snapshot, then fill password:**
   ```text
   mcp__playwright__browser_wait_for({ text: "Password" })
   mcp__playwright__browser_snapshot()
   mcp__playwright__browser_type({ ref: "[password-input-ref]", text: "<password>", element: "Password input" })
   mcp__playwright__browser_click({ ref: "[continue-button-ref]", element: "Continue button" })
   ```

5. **Wait for redirect away from sign-in, then continue testing**

**Important Notes:**
- Use `browser_snapshot` to get element refs - refs change between page loads
- Clerk uses multi-step sign-in: email first, then redirects to `/sign-in/factor-one` for password
- The MCP browser persists cookies, so subsequent navigations stay authenticated
- Close browser with `browser_close` when done to free resources

#### Quick Check: Already Authenticated?

Navigate to a protected page and check the URL:
```text
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
```

If you see the home page (not `/sign-in`), you're already authenticated from a previous interaction.

### Creating Test Users

Create a dedicated test user in your Clerk dev instance:
1. Go to Clerk Dashboard > Users
2. Create user with known email/password
3. Store credentials in env vars (never commit!)

## Integration with Ralph

When `--visual-check` is enabled, Ralph will:

1. Add Playwright tools to allowed tools
2. Include visual verification instructions in prompts
3. Expect visual verification results in activity.md

### Example Activity Log Entry

```markdown
## Visual Verification

Tested SaveStatus component after implementation:

1. Navigated to http://localhost:3000/documents/test-doc
2. Made edit in editor
3. Screenshot: SaveStatus showing "Saving..." ✅
4. Waited for debounce
5. Screenshot: SaveStatus showing "Saved" with green text ✅
6. Navigated away and back
7. Screenshot: Content persisted correctly ✅

All visual checks passed.
```

## Red Flags

- Testing only happy path (test errors too!)
- Not waiting for async operations before screenshot
- Using unstable selectors (indexes, generated classes)
- Skipping visual verification for "simple" UI changes
- Not testing on different viewport sizes

## Best Practices

1. **Wait for stability** before screenshots (animations, loading)
2. **Test real user flows** not just individual components
3. **Verify error states** not just success
4. **Document findings** in activity.md with screenshot filenames
5. **Close browser** when done to free resources

## References

- `brief-design` skill for design system tokens and patterns
- `testing-strategy` skill for coverage requirements
- Playwright docs: https://playwright.dev/docs/api/class-page
