---
name: install-playwright-mcp
description: Install Playwright MCP server for browser automation in Claude Code
argument-hint: "[--scope <scope>] [--headless]"
---

# Install Playwright MCP Server

Install the Playwright MCP server to enable browser automation capabilities.

## What This Does

The Playwright MCP server provides:
- **Browser automation** - Navigate, click, fill forms, take screenshots
- **Accessibility snapshots** - LLM-friendly structured data, no vision models needed
- **Fast and lightweight** - Uses Playwright's accessibility tree

## Installation Command

Run this command to install:

```bash
claude mcp add playwright -- npx @playwright/mcp@latest
```

## Scope Options

- `--scope local` (default): Available only in current project
- `--scope project`: Shared with team via `.mcp.json`
- `--scope user`: Available across all your projects

```bash
# Install for user (all projects)
claude mcp add playwright --scope user -- npx @playwright/mcp@latest

# Install for project (team shared)
claude mcp add playwright --scope project -- npx @playwright/mcp@latest
```

## Headless Mode

For headless operation (no visible browser):

```bash
claude mcp add playwright -- npx @playwright/mcp@latest --headless
```

## Common Configurations

### With specific browser
```bash
claude mcp add playwright -- npx @playwright/mcp@latest --browser firefox
```

### With custom viewport
```bash
claude mcp add playwright -- npx @playwright/mcp@latest --viewport-size 1920x1080
```

### With isolated sessions (no persistence)
```bash
claude mcp add playwright -- npx @playwright/mcp@latest --isolated
```

## Verify Installation

After installation:
1. Restart Claude Code
2. Run `/mcp` to see the playwright server
3. Test with: "Navigate to google.com and take a snapshot"

## Available Tools After Installation

- `browser_navigate` - Go to URL
- `browser_click` - Click elements
- `browser_type` - Type text
- `browser_snapshot` - Get page accessibility tree
- `browser_take_screenshot` - Capture screenshot
- `browser_fill_form` - Fill multiple form fields
- And many more...

## Execution Instructions

When the user runs this command:

1. **Determine scope** from arguments or ask:
   - Default to `local` if not specified

2. **Run installation**:
   ```bash
   claude mcp add playwright [--scope <scope>] -- npx @playwright/mcp@latest [options]
   ```

3. **Verify success** by checking output

4. **Inform user** to restart Claude Code to use the new MCP server
