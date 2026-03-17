---
name: dev-test-playwright
description: "Playwright MCP browser testing. Headless E2E, cross-browser, CI/CD automation."
---

**Announce:** "I'm using dev-test-playwright for headless browser automation."

<EXTREMELY-IMPORTANT>
## Gate Reminder

Before taking screenshots or running E2E tests, you MUST complete all 6 gates from dev-tdd:

```
GATE 1: BUILD
GATE 2: LAUNCH (with file-based logging)
GATE 3: WAIT
GATE 4: CHECK PROCESS
GATE 5: READ LOGS ← MANDATORY, CANNOT SKIP
GATE 6: VERIFY LOGS
THEN: E2E tests/screenshots
```

**You loaded dev-tdd earlier. Follow the gates now.**
</EXTREMELY-IMPORTANT>

## Contents

- [Tool Availability Gate](#tool-availability-gate)
- [When to Use Playwright MCP](#when-to-use-playwright-mcp)
- [MCP Tools Overview](#mcp-tools-overview)
- [Navigation](#navigation)
- [Element Interaction](#element-interaction)
- [Verification](#verification)
- [Form Handling](#form-handling)
- [Advanced Patterns](#advanced-patterns)
- [Complete E2E Examples](#complete-e2e-examples)

# Playwright MCP Browser Automation

<EXTREMELY-IMPORTANT>
## Tool Availability Gate

**Verify Playwright MCP tools are available before proceeding.**

Check for these MCP functions:
- `mcp__playwright__browser_navigate`
- `mcp__playwright__browser_snapshot`
- `mcp__playwright__browser_click`

**If MCP tools are not available:**
```
STOP: Cannot proceed with Playwright automation.

Missing: Playwright MCP server

The Playwright MCP server must be configured and running.
Check your Claude Code MCP configuration.

Reply when configured and I'll continue testing.
```

**This gate is non-negotiable. Missing tools = full stop.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## When to Use Playwright MCP

**USE Playwright MCP when you need:**
- Headless browser automation (CI/CD)
- Cross-browser testing (Chromium, Firefox, WebKit)
- Test isolation (fresh browser state per test)
- Standard E2E test suite automation
- Network mocking/interception
- Parallel test execution

**DO NOT use Playwright MCP when:**
- Debugging console messages (use Chrome MCP)
- Inspecting network requests/responses (use Chrome MCP)
- Executing custom JavaScript in page (use Chrome MCP)
- Recording GIFs of interactions (use Chrome MCP)
- Interactive debugging with real browser (use Chrome MCP)

**For debugging, use:** `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-test-chrome/SKILL.md")`

### Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "Playwright can do everything" | NO. It cannot read console or network requests. |
| "I don't need console debugging" | You will. Start with Chrome MCP if unsure. |
| "I'll add console checks later" | You can't with Playwright. Choose the right tool now. |
| "Headless mode doesn't matter" | YES IT DOES for CI/CD. |
| "Chrome MCP works for CI" | NO. It requires visible browser. |

### Capability Comparison

| Capability | Playwright MCP | Chrome MCP |
|------------|---------------|------------|
| Navigate/click/type | ✅ | ✅ |
| Accessibility tree | ✅ `browser_snapshot` | ✅ `read_page` |
| Screenshots | ✅ | ✅ |
| **Headless mode** | ✅ | ❌ |
| **Cross-browser** | ✅ | ❌ |
| Console messages | ❌ | ✅ |
| Network requests | ❌ | ✅ |
| JavaScript execution | ❌ | ✅ |
| GIF recording | ❌ | ✅ |
</EXTREMELY-IMPORTANT>

## MCP Tools Overview

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Navigate to URL |
| `browser_snapshot` | Get accessibility tree (page state) |
| `browser_click` | Click elements |
| `browser_type` | Type into inputs |
| `browser_select_option` | Select dropdown options |
| `browser_hover` | Hover over elements |
| `browser_wait_for` | Wait for conditions |
| `browser_take_screenshot` | Visual capture |
| `browser_press` | Press keys |

## Navigation

### Basic Navigation

```
mcp__playwright__browser_navigate(url="https://example.com")
```

### Wait for Page Load

```
mcp__playwright__browser_navigate(url="https://example.com")
mcp__playwright__browser_wait_for(state="networkidle")
```

### Get Current State

```
mcp__playwright__browser_snapshot()
```

The snapshot returns the **accessibility tree** - a structured representation of all interactive elements on the page.

## Element Interaction

### Clicking Elements

```
# By visible text
mcp__playwright__browser_click(element="Submit button")

# By ref (from snapshot)
mcp__playwright__browser_click(ref="button[type=submit]")

# By role and name
mcp__playwright__browser_click(element="Login", role="button")
```

### Typing Text

```
# Into focused element
mcp__playwright__browser_type(text="hello world")

# Into specific element
mcp__playwright__browser_click(element="Email input")
mcp__playwright__browser_type(text="user@example.com")

# Clear and type
mcp__playwright__browser_click(element="Search box")
mcp__playwright__browser_type(text="new search", clear=true)
```

### Keyboard Shortcuts

```
# Press Enter
mcp__playwright__browser_press(key="Enter")

# Keyboard shortcuts
mcp__playwright__browser_press(key="Control+a")
mcp__playwright__browser_press(key="Control+c")
```

## Verification

<EXTREMELY-IMPORTANT>
### The Iron Law of Verification

**EVERY action must be VERIFIED. Taking action is not enough.**

After clicking, typing, or navigating, you MUST:
1. Wait for the expected result
2. Take a snapshot to verify state
3. Document the verification in LEARNINGS.md

| Action | Verification |
|--------|--------------|
| Click submit | `wait_for(text="Success")` + snapshot |
| Navigate | `wait_for(state="networkidle")` + snapshot |
| Fill form | Snapshot shows filled values |
| Login | Snapshot shows dashboard/logged-in state |

**"I clicked it" is not verification. Prove the click worked.**
</EXTREMELY-IMPORTANT>

### Snapshot Verification

```
# 1. Perform action
mcp__playwright__browser_click(element="Submit")

# 2. Wait for result
mcp__playwright__browser_wait_for(text="Success")

# 3. Take snapshot to verify
mcp__playwright__browser_snapshot()
# Check snapshot contains expected elements
```

### Wait Conditions

```
# Wait for text to appear
mcp__playwright__browser_wait_for(text="Welcome back")

# Wait for element
mcp__playwright__browser_wait_for(selector="#success-message")

# Wait for network idle
mcp__playwright__browser_wait_for(state="networkidle")

# Wait for navigation
mcp__playwright__browser_wait_for(state="load")
```

### Screenshots

```
# Full page
mcp__playwright__browser_take_screenshot(path="/tmp/screenshot.png", fullPage=true)

# Viewport only
mcp__playwright__browser_take_screenshot(path="/tmp/viewport.png")

# Specific element
mcp__playwright__browser_take_screenshot(
    path="/tmp/element.png",
    selector="#main-content"
)
```

## Form Handling

### Text Inputs

```
mcp__playwright__browser_click(element="Username")
mcp__playwright__browser_type(text="john_doe")

mcp__playwright__browser_click(element="Password")
mcp__playwright__browser_type(text="secret123")
```

### Dropdowns

```
mcp__playwright__browser_select_option(
    element="Country dropdown",
    value="US"
)

# Or by label
mcp__playwright__browser_select_option(
    element="Country",
    label="United States"
)
```

### Checkboxes and Radio Buttons

```
# Check checkbox
mcp__playwright__browser_click(element="Accept terms checkbox")

# Verify checked state (via snapshot)
mcp__playwright__browser_snapshot()
# Look for checked="true" in accessibility tree
```

### File Upload

```
mcp__playwright__browser_set_input_files(
    selector="input[type=file]",
    files=["/path/to/file.pdf"]
)
```

## Advanced Patterns

### Multi-Step Form

```
# Step 1
mcp__playwright__browser_click(element="Name input")
mcp__playwright__browser_type(text="John Doe")
mcp__playwright__browser_click(element="Next button")
mcp__playwright__browser_wait_for(text="Step 2")

# Step 2
mcp__playwright__browser_click(element="Email input")
mcp__playwright__browser_type(text="john@example.com")
mcp__playwright__browser_click(element="Next button")
mcp__playwright__browser_wait_for(text="Step 3")

# Step 3 - Submit
mcp__playwright__browser_click(element="Submit button")
mcp__playwright__browser_wait_for(text="Success")
```

### Handling Modals

```
# Click to open modal
mcp__playwright__browser_click(element="Open Dialog")
mcp__playwright__browser_wait_for(text="Dialog Title")

# Interact with modal
mcp__playwright__browser_click(element="Confirm button")
mcp__playwright__browser_wait_for(state="hidden", selector=".modal")
```

### Iframes

```
# Switch to iframe
mcp__playwright__browser_frame(name="payment-iframe")

# Interact within iframe
mcp__playwright__browser_click(element="Card number")
mcp__playwright__browser_type(text="4111111111111111")

# Switch back to main
mcp__playwright__browser_main_frame()
```

### Hover and Tooltips

```
mcp__playwright__browser_hover(element="Help icon")
mcp__playwright__browser_wait_for(text="This is the tooltip text")
mcp__playwright__browser_snapshot()
```

## Complete E2E Examples

### Login Flow

```
# 1. Navigate to login page
mcp__playwright__browser_navigate(url="https://app.example.com/login")
mcp__playwright__browser_wait_for(state="networkidle")

# 2. Take initial snapshot
mcp__playwright__browser_snapshot()
# Verify: Login form is visible

# 3. Fill credentials
mcp__playwright__browser_click(element="Email")
mcp__playwright__browser_type(text="user@example.com")

mcp__playwright__browser_click(element="Password")
mcp__playwright__browser_type(text="password123")

# 4. Submit
mcp__playwright__browser_click(element="Sign In")
mcp__playwright__browser_wait_for(text="Dashboard")

# 5. Verify success
mcp__playwright__browser_snapshot()
# Verify: Dashboard is visible, user name shown

# 6. Screenshot for evidence
mcp__playwright__browser_take_screenshot(path="/tmp/login_success.png")
```

### E-Commerce Checkout

```
# 1. Navigate to product
mcp__playwright__browser_navigate(url="https://shop.example.com/product/123")
mcp__playwright__browser_wait_for(state="networkidle")

# 2. Add to cart
mcp__playwright__browser_click(element="Add to Cart")
mcp__playwright__browser_wait_for(text="Added to cart")

# 3. Go to cart
mcp__playwright__browser_click(element="Cart icon")
mcp__playwright__browser_wait_for(text="Your Cart")

# 4. Verify cart
mcp__playwright__browser_snapshot()
# Verify: Product in cart, correct price

# 5. Proceed to checkout
mcp__playwright__browser_click(element="Checkout")
mcp__playwright__browser_wait_for(text="Shipping Address")

# 6. Fill shipping
mcp__playwright__browser_click(element="Address")
mcp__playwright__browser_type(text="123 Main St")

mcp__playwright__browser_click(element="City")
mcp__playwright__browser_type(text="New York")

mcp__playwright__browser_select_option(element="State", value="NY")

mcp__playwright__browser_click(element="Zip")
mcp__playwright__browser_type(text="10001")

# 7. Continue to payment
mcp__playwright__browser_click(element="Continue to Payment")
mcp__playwright__browser_wait_for(text="Payment Method")

# 8. Verify order summary
mcp__playwright__browser_snapshot()
# Verify: Correct items, shipping address, total

mcp__playwright__browser_take_screenshot(path="/tmp/checkout_complete.png")
```

### Search and Filter

```
# 1. Navigate
mcp__playwright__browser_navigate(url="https://search.example.com")

# 2. Search
mcp__playwright__browser_click(element="Search box")
mcp__playwright__browser_type(text="laptop")
mcp__playwright__browser_press(key="Enter")
mcp__playwright__browser_wait_for(text="results")

# 3. Apply filter
mcp__playwright__browser_click(element="Price filter")
mcp__playwright__browser_click(element="Under $1000")
mcp__playwright__browser_wait_for(state="networkidle")

# 4. Verify filtered results
mcp__playwright__browser_snapshot()
# Verify: Results shown, filter applied

# 5. Click first result
mcp__playwright__browser_click(element="First product link")
mcp__playwright__browser_wait_for(text="Product Details")

mcp__playwright__browser_take_screenshot(path="/tmp/search_result.png")
```

## Error Handling

### Retry Pattern

```
# Attempt action with retry
for attempt in range(3):
    try:
        mcp__playwright__browser_click(element="Flaky Button")
        mcp__playwright__browser_wait_for(text="Success", timeout=5000)
        break  # Success
    except:
        if attempt == 2:
            raise  # Give up after 3 attempts
        time.sleep(1)  # Wait before retry
```

### Timeout Handling

```
# Set explicit timeout
mcp__playwright__browser_wait_for(
    text="Slow loading content",
    timeout=30000  # 30 seconds
)
```

## Limitations

<EXTREMELY-IMPORTANT>
### What Playwright MCP Cannot Do

| Need | Why Playwright Fails | Use Instead |
|------|---------------------|-------------|
| Read console.log | No console access | Chrome MCP `read_console_messages` |
| Inspect API responses | No network access | Chrome MCP `read_network_requests` |
| Execute page JavaScript | No JS execution | Chrome MCP `javascript_tool` |
| Record GIF | No recording capability | Chrome MCP `gif_creator` |

**If you need debugging capabilities, switch to Chrome MCP.**
</EXTREMELY-IMPORTANT>

## Integration

This skill is referenced by `dev-test` for Playwright browser automation.

**For debugging (console/network), use:** `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-test-chrome/SKILL.md")`

For TDD protocol, see: `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-tdd/SKILL.md")`
