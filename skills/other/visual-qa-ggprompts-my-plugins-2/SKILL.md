---
name: visual-qa
description: "Visual QA checkpoint for conductor gates. Uses tabz MCP tools to check browser console errors, take screenshots, and identify obvious UI issues. Returns structured result with pass/fail status and captured screenshots."
user-invocable: true
---

# Visual QA Checkpoint

Visual quality assurance checkpoint that uses browser automation to verify the UI.

## What This Skill Does

1. Checks browser console for errors
2. Takes screenshot of current page
3. Analyzes for obvious visual issues
4. Writes result to checkpoint file

## Prerequisites

- TabzChrome extension running
- Application loaded in browser tab
- `tabz` MCP server connected

## Workflow

### Step 1: Check Console Errors

```bash
# Get console logs filtered for errors
mcp-cli info tabz/tabz_get_console_logs
mcp-cli call tabz/tabz_get_console_logs '{"level": "error"}'
```

**Important:** Console errors don't automatically fail - evaluate if they're blocking:
- JS runtime errors that prevent functionality = FAIL
- 404s for optional resources = WARNING
- Deprecation warnings = INFO

### Step 2: Take Screenshot

```bash
# Capture current page state
mcp-cli info tabz/tabz_screenshot
mcp-cli call tabz/tabz_screenshot '{}'
```

The screenshot file path is returned. Read it to visually inspect the page.

### Step 3: Check Page State

```bash
# Verify page loaded correctly
mcp-cli info tabz/tabz_get_page_info
mcp-cli call tabz/tabz_get_page_info '{}'
```

Verify:
- Page title is not error page
- URL matches expected
- Page is not stuck loading

### Step 4: Optional - Check Network Errors

If functionality seems broken:

```bash
# Enable capture first (if not already)
mcp-cli call tabz/tabz_enable_network_capture '{}'

# Trigger the problematic action, then:
mcp-cli call tabz/tabz_get_network_requests '{"statusMin": 400}'
```

### Step 5: Parse and Write Result

Create structured result:

```json
{
  "checkpoint": "visual-qa",
  "timestamp": "2026-01-19T12:00:00Z",
  "passed": true,
  "issues": [],
  "screenshots": ["/path/to/screenshot.png"],
  "console_errors": 0,
  "summary": "Page loads correctly, no visual issues detected"
}
```

**Result Fields:**
- `passed`: true if no blocking visual/console issues
- `issues`: array of `{severity: "error"|"warning"|"info", message: string, type: "console"|"visual"|"network"}`
- `screenshots`: array of screenshot file paths
- `console_errors`: count of console errors found
- `summary`: brief human-readable summary

### Step 6: Write Checkpoint File

```bash
mkdir -p .checkpoints
cat > .checkpoints/visual-qa.json << 'EOF'
{
  "checkpoint": "visual-qa",
  "timestamp": "...",
  "passed": true,
  "issues": [],
  "screenshots": [...],
  "console_errors": 0,
  "summary": "..."
}
EOF
```

## Decision Criteria

**Pass if:**
- Page loads without critical console errors
- No obvious visual breakage (blank page, missing components)
- Key functionality appears present

**Fail if:**
- JS errors prevent page from rendering
- Page shows error state or blank
- Critical UI elements missing
- API calls failing (5xx errors)

**Warning (pass with notes) if:**
- Non-critical console warnings
- Minor styling issues
- Slow load times

## Visual Inspection Guidelines

When viewing the screenshot, check for:

1. **Layout integrity** - Is content properly positioned?
2. **Text readability** - Is text visible, correct font/size?
3. **Interactive elements** - Are buttons/links visible?
4. **Error states** - Any error messages displayed?
5. **Responsive fit** - Does content fit the viewport?

## Example Usage

When invoked as `/visual-qa`:

```
Running Visual QA checkpoint...

Checking console for errors...
Found 0 errors, 2 warnings.

Taking screenshot...
Screenshot saved to /tmp/tabz-screenshot-123.png
[Viewing screenshot...]

Page appears to load correctly. Navigation visible, content renders.

Checking page info...
Title: "My App - Dashboard"
URL: http://localhost:3000/dashboard
Status: Complete

Result:
{
  "passed": true,
  "issues": [
    {"severity": "warning", "message": "React DevTools warning", "type": "console"}
  ],
  "screenshots": ["/tmp/tabz-screenshot-123.png"],
  "console_errors": 0,
  "summary": "Page loads correctly. Minor console warnings only."
}

Checkpoint result written to .checkpoints/visual-qa.json
```

## Troubleshooting

**No MCP connection:**
```bash
mcp-cli tools tabz  # Should list tabz_* tools
```

**Screenshot fails:**
- Ensure Chrome tab is focused
- Check TabzChrome extension is active
- Verify localhost:8129 backend is running
