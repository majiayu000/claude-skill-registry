---
name: playwright-mcp
description:
  Browser testing, web scraping, and UI validation using Playwright MCP. Use this skill when you
  need to test Streamlit apps, validate web interfaces, test responsive design, check accessibility,
  or automate browser interactions through MCP tools.
---

# Playwright MCP Testing

Automate browser testing, web scraping, and UI validation using Playwright MCP server for
comprehensive browser automation.

## Quick Start

**Core Testing Workflow:**

1. Navigate to application
2. Take snapshot (accessibility tree)
3. Interact with elements
4. Verify expected behavior
5. Take screenshots for documentation

## Key Tools

### Navigation & Waiting

- `browser_navigate` - Load URL
- `browser_wait_for` - Wait for time, text, or element

### Interaction

- `browser_click` - Click buttons and elements
- `browser_fill_form` - Batch fill multiple form fields
- `browser_type` - Type into inputs
- `browser_select_option` - Select dropdown options

### Validation

- `browser_snapshot` - Accessibility tree (for AI analysis)
- `browser_take_screenshot` - Visual capture
- `browser_console_messages` - Check for JavaScript errors

## Testing Patterns

### Page Load Verification

```sql
Navigate to http://localhost:8501
Wait 5 seconds
Take snapshot
Verify expected elements present
```

### Form Testing

```sql
Fill form fields (use browser_fill_form for speed)
Click Submit button
Wait for "Success" text to appear
Take screenshot
```

### Responsive Design

```sql
Resize to 375x667 (mobile)
Take screenshot
Resize to 1920x1080 (desktop)
Take screenshot
```

### Multi-Page Navigation

```sql
Navigate to homepage
Click navigation link
Verify URL changed
Verify new page content
```

## Best Practices

✅ **DO:**

- Use `browser_snapshot` for AI analysis
- Wait for content (3-5 seconds)
- Batch form fields with `browser_fill_form`
- Use element refs from snapshots for reliable clicks
- Check console for errors

❌ **AVOID:**

- Using screenshots when you need to interact
- Typing each field individually
- Skipping waits for dynamic content
- Ignoring console errors

## Common Workflows

### Pre-Deployment Testing

- Test all pages load without errors
- Verify navigation works
- Test forms submit successfully
- Check data displays correctly
- Validate responsive design (375, 768, 1920px)
- Check console for JavaScript errors

### Accessibility Validation

- Take snapshot of each page
- Verify interactive elements have labels
- Check heading hierarchy
- Verify form labels associated

### Visual Regression

- Take full-page screenshots
- Compare with baseline
- Document changes

## Quick Reference

### Common Test Flow

```sql
Navigate to http://localhost:8501
Wait 5 seconds
Take snapshot
Click element with ref from snapshot
Wait for "Success" text
Take screenshot
```

### Responsive Testing

```sql
Resize to 375x667  # Mobile
Take screenshot
Resize to 768x1024  # Tablet
Take screenshot
Resize to 1920x1080  # Desktop
Take screenshot
```

### Form Submission

```sql
Fill form fields (batch)
Click Submit
Wait for success message
Verify in snapshot
```

### Error Checking

```sql
Get console messages (onlyErrors=true)
Get network requests
Verify no 404s or 500s
```

---

## Troubleshooting

| Issue                      | Solution                                                               |
| -------------------------- | ---------------------------------------------------------------------- |
| Browsers not installed     | Run `npx @playwright/mcp browser install`                              |
| Element not found          | Take snapshot first to get current page state and exact ref            |
| Tests too slow             | Use `browser_fill_form` instead of multiple `browser_type`             |
| MCP not starting           | Restart IDE, verify `mcp.json` is valid JSON                           |
| Timeout errors             | Increase wait times or use `browser_wait_for` with specific conditions |
| Screenshots blank          | Ensure page is fully loaded before taking screenshot                   |
| Console errors not showing | Use `browser_console_messages` with `onlyErrors=true` parameter        |

---

## Resources

- `TESTING_PATTERNS.md` - Common test scenarios (coming soon)
- `STREAMLIT_TESTING.md` - Streamlit-specific patterns (coming soon)
- `ACCESSIBILITY.md` - Accessibility testing workflows (coming soon)
- `mcp-config.json` - MCP server configuration
