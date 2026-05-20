---
name: browser-use
description: Browser automation for UI testing, screenshots, and workflow verification. Routes to optimal tool based on context.
allowed-tools: all
---

# Browser Use Skill

Browser automation for UI testing, visual verification, and workflow testing. This skill routes to the optimal browser tool based on your specific needs.

## Available Browser Tools

| Tool | Type | Best For |
|------|------|----------|
| **Claude in Chrome** | MCP (`mcp__claude-in-chrome__*`) | Authenticated flows, GIF recording, live debugging, network monitoring |
| **Browser MCP** | MCP (`mcp__browsermcp__*`) | Interactive isolated testing, simple interactions, accessibility snapshots |
| **Playwright Test** | CLI (`npx playwright test`) | Structured test suites, assertions, CI/CD, regression testing |

## Quick Decision

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHICH BROWSER TOOL?                          │
│                                                                 │
│  Running structured test suite with assertions?                 │
│      YES ──► Playwright Test (npx playwright test)              │
│      NO  ──► Continue below                                     │
│                                                                 │
│  Need user's logged-in session?                                 │
│      YES ──► Claude in Chrome                                   │
│      NO  ──► Either MCP tool works                              │
│                                                                 │
│  Creating a GIF/recording?                                      │
│      YES ──► Claude in Chrome (has gif_creator)                 │
│      NO  ──► Either MCP tool works                              │
│                                                                 │
│  Monitoring network requests?                                   │
│      YES ──► Claude in Chrome (read_network_requests)           │
│      NO  ──► Either MCP tool works                              │
│                                                                 │
│  Need clean/isolated test state?                                │
│      YES ──► Browser MCP                                        │
│      NO  ──► Either MCP tool works                              │
│                                                                 │
│  Quick smoke test, simple interaction?                          │
│      YES ──► Browser MCP (simpler API)                          │
│      NO  ──► Claude in Chrome (more features)                   │
│                                                                 │
│  DEFAULT for interactive: Claude in Chrome (most capabilities)  │
│  DEFAULT for test suites: Playwright Test (assertions/reports)  │
└─────────────────────────────────────────────────────────────────┘
```

## Decision Matrix

| Scenario | Recommended | Why |
|----------|-------------|-----|
| **Test suites with assertions** | Playwright Test | Built for structured testing |
| **CI/CD integration** | Playwright Test | Reports, parallelization, retries |
| **Regression test suite** | Playwright Test | Repeatable, deterministic |
| Test authenticated flow | Claude in Chrome | Uses user's logged-in session |
| Create demo/documentation GIF | Claude in Chrome | Has gif_creator tool |
| Debug live issue with user | Claude in Chrome | See exactly what user sees |
| Monitor API/network calls | Claude in Chrome | read_network_requests |
| Execute JavaScript in page | Claude in Chrome | javascript_tool |
| Multi-tab workflow | Claude in Chrome | Tab management |
| Quick isolated smoke test | Browser MCP | Clean state, simpler API |
| Accessibility tree inspection | Browser MCP | browser_snapshot |
| Simple form fill + submit | Either MCP | Both capable |
| Console error checking | Either MCP | Both have console access |

## Claude in Chrome

**Use when you need:**
- User's authenticated session (already logged in)
- GIF recording for documentation
- Network request monitoring
- JavaScript execution in page context
- Multi-tab coordination
- Real-time user observation

**Setup:** Call `tabs_context_mcp` first to get available tabs.

**Key tools:**
```
mcp__claude-in-chrome__tabs_context_mcp    # Get tab context (call FIRST)
mcp__claude-in-chrome__tabs_create_mcp     # Create new tab
mcp__claude-in-chrome__navigate            # Go to URL
mcp__claude-in-chrome__computer            # Click, type, screenshot, scroll
mcp__claude-in-chrome__read_page           # Get accessibility tree
mcp__claude-in-chrome__find                # Natural language element search
mcp__claude-in-chrome__form_input          # Fill form fields
mcp__claude-in-chrome__javascript_tool     # Execute JS in page
mcp__claude-in-chrome__read_network_requests  # Monitor API calls
mcp__claude-in-chrome__read_console_messages  # Get console output
mcp__claude-in-chrome__gif_creator         # Record GIF
```

See `reference/claude-in-chrome.md` for complete documentation.

## Browser MCP

**Use when you need:**
- Clean/isolated test environment
- Simple navigation and interaction
- Accessibility snapshots
- When Claude in Chrome isn't available

**Key tools:**
```
mcp__browsermcp__browser_navigate          # Go to URL
mcp__browsermcp__browser_snapshot          # Get accessibility tree
mcp__browsermcp__browser_screenshot        # Capture page
mcp__browsermcp__browser_click             # Click element
mcp__browsermcp__browser_type              # Type text
mcp__browsermcp__browser_hover             # Hover element
mcp__browsermcp__browser_select_option     # Select dropdown
mcp__browsermcp__browser_press_key         # Press key
mcp__browsermcp__browser_wait              # Wait
mcp__browsermcp__browser_get_console_logs  # Get console
```

See `reference/browser-mcp.md` for complete documentation.

## Playwright Test

**Use when you need:**
- Structured test suites with assertions
- CI/CD integration with reports
- Regression testing (repeatable, deterministic)
- Parallel test execution
- Test retries and flaky test handling

**Key commands:**
```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/auth.spec.ts

# Run tests with UI mode (interactive debugging)
npx playwright test --ui

# Run tests in headed mode (see the browser)
npx playwright test --headed

# Generate test report
npx playwright show-report
```

**Test file structure:**
```typescript
// tests/e2e/example.spec.ts
import { test, expect } from '@playwright/test';

test('user can log in', async ({ page }) => {
  await page.goto('http://localhost:3001/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

See `reference/playwright-test.md` for complete documentation.

## Common Patterns

### Verify UI Change (Quick)
```
1. Browser MCP: browser_navigate to localhost:3001/[page]
2. Browser MCP: browser_screenshot
3. Browser MCP: browser_get_console_logs
```

### Verify UI Change (Authenticated)
```
1. Claude in Chrome: tabs_context_mcp (get tab context)
2. Claude in Chrome: navigate to page
3. Claude in Chrome: computer action=screenshot
4. Claude in Chrome: read_console_messages
```

### Test Form Submission
```
1. Navigate to form page
2. Get element refs (snapshot or read_page)
3. Fill fields (type or form_input)
4. Submit
5. Check console for errors
6. Screenshot result
```

### Create Demo GIF
```
1. Claude in Chrome: tabs_context_mcp
2. Claude in Chrome: gif_creator action=start_recording
3. Claude in Chrome: computer action=screenshot (initial frame)
4. Perform demo steps (navigate, click, etc.)
5. Claude in Chrome: computer action=screenshot (final frame)
6. Claude in Chrome: gif_creator action=stop_recording
7. Claude in Chrome: gif_creator action=export download=true
```

### Monitor Network Requests
```
1. Claude in Chrome: tabs_context_mcp
2. Claude in Chrome: navigate to page
3. Perform actions that trigger API calls
4. Claude in Chrome: read_network_requests urlPattern="/api/"
```

## Best Practices

1. **Start with context**: Claude in Chrome requires `tabs_context_mcp` first
2. **Get refs before interacting**: Use snapshot/read_page to get element references
3. **Check console after actions**: Both tools support console access
4. **Screenshot for evidence**: Capture visual state at key points
5. **Use patterns for filtering**: Console and network tools support pattern filtering

## Troubleshooting

### Claude in Chrome not responding
- Check extension is installed and enabled
- Try `tabs_context_mcp` to reset state
- User may need to dismiss browser dialogs manually

### Element not found
- Take fresh snapshot/read_page
- Wait for page to load (`browser_wait` or `computer action=wait`)
- Check if element is in different tab or iframe

### Authentication needed
- Use Claude in Chrome to leverage user's logged-in session
- Or manually log in via Browser MCP before testing

## Integration

This skill is used by:
- **Test Agent** for comprehensive testing
- **Any agent** for quick visual verification
- **test-from-docs** Phase 4 (Browser Verification)
