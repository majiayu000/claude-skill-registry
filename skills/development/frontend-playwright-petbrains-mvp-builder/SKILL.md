---
name: frontend-playwright
description: 'Visual QA gate for frontend code. ALWAYS use before delivering any UI
  changes - navigate, screenshot, verify console is error-free. Use for: responsive
  testing across viewports, form/interaction testi'
---

---
name: frontend-playwright
description: Visual QA gate for frontend code. ALWAYS use before delivering any UI changes - navigate, screenshot, verify console is error-free. Use for: responsive testing across viewports, form/interaction testing, debugging hydration and render issues. Catches visual bugs before users see them.
allowed-tools: Bash (*), mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_click, mcp__playwright__browser_type, mcp__playwright__browser_console_messages, mcp__playwright__browser_network_requests, mcp__playwright__browser_resize, mcp__playwright__browser_evaluate, mcp__playwright__browser_wait_for, mcp__playwright__browser_hover, mcp__playwright__browser_close
---

# Playwright MCP

Browser automation for visual verification. **Self-check UI before delivering.**

## When to Use

- After creating/modifying components → verify render
- Before delivering code → **final QA check**
- Debugging UI issues → see actual browser state
- Responsive testing → check mobile/tablet/desktop

## Process

**NAVIGATE → VERIFY → FIX → DELIVER**

```yaml
1. Start dev server: npm run dev
2. browser_navigate → open page
3. browser_take_screenshot → visual check
4. browser_console_messages { onlyErrors: true } → MUST BE EMPTY
5. Fix issues if any → repeat
6. Deliver when clean
```

## Tools Quick Reference

```yaml
Navigation:
  browser_navigate:      { url: "http://localhost:3000" }
  browser_resize:        { width: 375, height: 812 }
  browser_wait_for:      { time: 2 } | { text: "Success" }
  browser_close:         {}

Inspection:
  browser_snapshot:           # Get element refs for interactions
  browser_take_screenshot:    { filename: "check.png", fullPage: true }
  browser_console_messages:   { onlyErrors: true }  # CRITICAL
  browser_network_requests:   {}
  browser_evaluate:           { function: "() => ..." }

Interaction:
  browser_click:   { element: "Submit button", ref: "e5" }
  browser_type:    { element: "Email input", ref: "e3", text: "user@example.com" }
  browser_hover:   { element: "Menu item", ref: "e8" }
```

## Pre-Delivery Checklist

```yaml
MUST PASS before delivery:
  ✓ browser_take_screenshot → looks correct
  ✓ browser_console_messages { onlyErrors: true } → EMPTY
  ✓ browser_network_requests → no 4xx/5xx
  ✓ Mobile viewport (375px) works
```

## Common Workflows

### Quick Verification
```yaml
browser_navigate → browser_take_screenshot → browser_console_messages { onlyErrors: true }
```

### Responsive Test
```yaml
browser_resize { width: 375, height: 812 }  → screenshot
browser_resize { width: 768, height: 1024 } → screenshot
browser_resize { width: 1440, height: 900 } → screenshot
```

### Form Test
```yaml
browser_snapshot              # get refs
browser_type { ref, text }    # fill fields
browser_click { ref }         # submit
browser_wait_for { text }     # wait for result
browser_console_messages      # check errors
```

## Common Console Errors

```yaml
"Hydration mismatch":
  → Server/client render different
  → Fix: 'use client', useEffect for browser-only code

"Cannot read property of undefined":
  → Data not loaded
  → Fix: optional chaining, loading states

"Failed to fetch":
  → API error
  → Check: browser_network_requests for details
```

## Viewport Sizes

```yaml
Mobile:     { width: 375, height: 812 }   # iPhone
Tablet:     { width: 768, height: 1024 }  # iPad
Laptop:     { width: 1366, height: 768 }
Desktop:    { width: 1440, height: 900 }
Full HD:    { width: 1920, height: 1080 }
```

## References

- **[tools.md](references/tools.md)** — Full MCP tools documentation with all parameters
- **[workflows.md](references/workflows.md)** — Ready-to-use verification scenarios
