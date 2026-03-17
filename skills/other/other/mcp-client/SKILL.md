---
name: mcp-client
description: Universal MCP client for connecting to any MCP server with progressive disclosure. Wraps MCP servers as skills to avoid context window bloat from tool definitions. Use when interacting with external MCP servers (Playwright, GitHub, filesystem, etc.), listing available tools, or executing MCP tool calls. Triggers on "connect to MCP", "list MCP tools", "call MCP", "use Playwright", "browser navigate", "browser snapshot".
---

# Universal MCP Client

Connect to any MCP server without bloating context with tool definitions.

> **⚠️ PLAYWRIGHT USERS: READ "CRITICAL: Playwright Browser Session Behavior" SECTION BELOW!**
>
> Each MCP call = new browser session. Browser CLOSES after each call.
> You CANNOT navigate in one call and click in another.
> Use `browser_run_code` for ANY multi-step operation.
> If you need to return to a state (e.g., logged in), you MUST redo ALL steps from scratch.

## How It Works

Instead of loading all MCP tool schemas into context, this client:
1. Lists available servers from config
2. Queries tool schemas on-demand
3. Executes tools with JSON arguments

## Configuration

Config location priority:
1. `MCP_CONFIG_PATH` environment variable
2. `.claude/skills/mcp-client/references/mcp-config.json`
3. `.mcp.json` in current directory
4. `~/.claude.json`

## Commands

```bash
# List configured servers
python scripts/mcp_client.py servers

# List tools from a specific server
python scripts/mcp_client.py tools playwright

# Call a tool
python scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'
```

---

# CRITICAL: Playwright Browser Session Behavior

## ⚠️ The Session Problem

**Each MCP call creates a NEW browser session. The browser CLOSES after each call.**

This means:
```bash
# ❌ WRONG - These run in SEPARATE browser sessions!
python scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'
python scripts/mcp_client.py call playwright browser_click '{"element": "Accept cookies"}'
python scripts/mcp_client.py call playwright browser_snapshot '{}'
# ^ The snapshot captures a FRESH page, not the page after clicking!
```

## ✅ The Solution: `browser_run_code`

Use `browser_run_code` to run **multiple Playwright steps in ONE browser session**:

```bash
python scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com\");

    // Wait for and click cookie banner
    const acceptBtn = page.getByRole(\"button\", { name: /accept/i });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(1000);
    }

    // Wait for page to stabilize
    await page.waitForLoadState(\"networkidle\");

    // Return snapshot data for analysis
    const snapshot = await page.accessibility.snapshot();
    return JSON.stringify(snapshot, null, 2);
  "
}'
```

## When to Use Each Approach

| Scenario | Tool | Why |
|----------|------|-----|
| Simple page load + snapshot | `browser_navigate` | Returns snapshot automatically |
| Multi-step interaction | `browser_run_code` | Keeps session alive |
| Click then observe result | `browser_run_code` | Session persists |
| Fill form and submit | `browser_run_code` | Session persists |
| Hover to reveal menu | `browser_run_code` | Session persists |

---

# Playwright Workflows for Test Discovery

## 1. Basic Page Exploration (Single Step)

`browser_navigate` returns **both** navigation result AND accessibility snapshot:

```bash
python scripts/mcp_client.py call playwright browser_navigate '{"url": "https://example.com"}'
```

Output includes:
- Page URL and title
- Full accessibility tree (all visible elements with roles, names, states)
- Element references for further interaction

**Use this when:** Simple page load without interactions

## 2. Page with Cookie Banner (Multi-Step)

```bash
python scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://www.olx.ro\");

    // Handle cookie consent
    try {
      const cookieBtn = page.getByRole(\"button\", { name: \"Accept\" });
      await cookieBtn.click({ timeout: 5000 });
      await page.waitForTimeout(1000);
    } catch (e) {
      // No cookie banner
    }

    // Get accessibility snapshot
    const snapshot = await page.accessibility.snapshot({ interestingOnly: false });
    return JSON.stringify(snapshot, null, 2);
  "
}'
```

## 3. Navigate to Subpage (Multi-Step)

```bash
python scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://www.olx.ro\");

    // Dismiss cookies
    const acceptBtn = page.getByRole(\"button\", { name: \"Accept\" });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
      await page.waitForTimeout(500);
    }

    // Navigate to login
    await page.goto(\"https://www.olx.ro/cont/\");

    // Wait for redirect to login domain
    await page.waitForURL(/login\\.olx\\.ro/, { timeout: 10000 });

    // Get form structure
    const snapshot = await page.accessibility.snapshot();
    return JSON.stringify({ url: page.url(), snapshot }, null, 2);
  "
}'
```

## 4. Explore Element Interactions (Multi-Step)

Use this to understand how menus/dropdowns behave:

```bash
python scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://www.olx.ro\");

    // Dismiss cookies
    const acceptBtn = page.getByRole(\"button\", { name: \"Accept\" });
    if (await acceptBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
      await acceptBtn.click();
    }

    // Click on category to see what happens
    const categoryLink = page.getByRole(\"link\", { name: /Auto, moto/i }).first();
    await categoryLink.click();

    // Wait to see result
    await page.waitForTimeout(1500);

    // Capture state after click
    const snapshot = await page.accessibility.snapshot();
    return JSON.stringify({
      url: page.url(),
      didNavigate: page.url().includes(\"auto\"),
      snapshot: snapshot
    }, null, 2);
  "
}'
```

## 5. Fill Form and Capture State

```bash
python scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://login.olx.ro\");

    // Fill login form
    await page.locator(\"input[type=email]\").fill(\"test@example.com\");
    await page.locator(\"input[type=password]\").fill(\"test123\");

    // Click login button
    await page.getByTestId(\"login-submit-button\").click();

    // Wait for response
    await page.waitForTimeout(3000);

    // Capture any error messages
    const errors = await page.locator(\"[class*=error], [role=alert]\").allTextContents();
    const snapshot = await page.accessibility.snapshot();

    return JSON.stringify({
      url: page.url(),
      errors: errors,
      snapshot: snapshot
    }, null, 2);
  "
}'
```

---

# Gathering Selectors for Page Objects

## Best Practices

### 1. Use Accessibility Tree First

The snapshot from `browser_navigate` or `browser_run_code` provides:
- **Role**: button, link, textbox, combobox, etc.
- **Name**: accessible name (from label, aria-label, text content)
- **State**: disabled, checked, expanded, etc.

Map these to Playwright locators:
```typescript
// From snapshot: { role: "button", name: "Căutare" }
page.getByRole('button', { name: /Căutare/i })

// From snapshot: { role: "textbox", name: "Ce anume cauți?" }
page.getByRole('textbox', { name: /Ce anume cauți/i })

// From snapshot: { role: "link", name: "Auto, moto și ambarcațiuni" }
page.getByRole('link', { name: /Auto, moto/i })
```

### 2. Selector Priority

| Priority | Method | Use When |
|----------|--------|----------|
| 1 | `getByRole()` | Element has semantic role + accessible name |
| 2 | `getByTestId()` | Element has `data-testid` attribute |
| 3 | `getByText()` | Unique text content |
| 4 | `getByPlaceholder()` | Input with placeholder |
| 5 | `locator('[attr="value"]')` | CSS attribute selector |
| 6 | `locator('.class')` | CSS class (fragile, avoid) |

### 3. Handling Multiple Matches

```typescript
// Use .first() when multiple match
page.getByRole('link', { name: 'Category' }).first()

// Use parent context
page.locator('nav').getByRole('link', { name: 'Category' })

// Use filter
page.getByRole('button').filter({ hasText: /submit/i })
```

### 4. Get Full DOM for Complex Cases

When accessibility tree isn't enough, get raw HTML:

```bash
python scripts/mcp_client.py call playwright browser_run_code '{
  "code": "
    await page.goto(\"https://example.com\");

    // Get specific element HTML
    const formHtml = await page.locator(\"form\").first().innerHTML();

    // Or get all buttons with their attributes
    const buttons = await page.locator(\"button\").evaluateAll(btns =>
      btns.map(b => ({
        text: b.textContent,
        testid: b.dataset.testid,
        class: b.className,
        type: b.type
      }))
    );

    return JSON.stringify({ formHtml, buttons }, null, 2);
  "
}'
```

---

# Quick Reference: Playwright MCP Tools

| Tool | Session Behavior | Use Case |
|------|-----------------|----------|
| `browser_navigate` | New session, returns snapshot | Simple page load |
| `browser_run_code` | **Single session, custom script** | Multi-step operations |
| `browser_click` | New session | Single click (usually not useful alone) |
| `browser_type` | New session | Single type (usually not useful alone) |
| `browser_snapshot` | Reuses if session exists | Get current page state |
| `browser_screenshot` | Reuses if session exists | Visual capture |

## Tool Arguments

### browser_navigate
```json
{"url": "https://example.com"}
```

### browser_run_code
```json
{
  "code": "await page.goto('https://example.com'); return await page.title();"
}
```

The `code` must be valid JavaScript that:
- Uses `page` object (Playwright Page)
- Uses `await` for async operations
- Returns the data you want (use `JSON.stringify` for objects)

### browser_click
```json
{"element": "Submit button", "ref": "optional-element-ref"}
```

### browser_type
```json
{"element": "Email input", "text": "user@example.com"}
```

---

# Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "No MCP config found" | Missing config file | Create mcp-config.json |
| "Server not found" | Server not in config | Add server to config |
| "Connection failed" | Server not running | Start the MCP server |
| "Invalid JSON" | Bad tool arguments | Check argument format |
| "Timeout" | Page too slow | Increase timeout in code |
| "Element not found" | Wrong selector | Check snapshot for actual names |

---

# Setup

1. Copy the example config:
   ```bash
   cp .claude/skills/mcp-client/references/mcp-config.example.json \
      .claude/skills/mcp-client/references/mcp-config.json
   ```

2. The config should contain:
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }
   ```

3. Install dependencies:
   ```bash
   pip install mcp fastmcp
   ```

## Config Example

See [references/mcp-config.example.json](references/mcp-config.example.json)

## Available Servers

See [references/mcp-servers.md](references/mcp-servers.md) for:
- Playwright (browser automation)
- GitHub (repository operations)
- Filesystem (file access)
- Sequential Thinking (reasoning)
- And more...

## Dependencies

```bash
pip install mcp fastmcp
```
