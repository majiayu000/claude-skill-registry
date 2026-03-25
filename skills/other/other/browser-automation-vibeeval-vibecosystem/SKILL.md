---
name: browser-automation
description: AI browser automation - navigate, interact, extract, verify via browser-use MCP
allowed-tools: [Bash, Read, Write, WebFetch]
keywords: [browser, automation, scrape, navigate, click, form, screenshot, deploy-verify, e2e]
mcp_servers: [browser-use]
---

# Browser Automation

AI-powered browser automation via `browser-use` MCP server. Navigate web pages, fill forms, extract content, take screenshots, and verify deployments.

## Setup

Add to `~/.mcp.json`:

```json
{
  "mcpServers": {
    "browser-use": {
      "command": "uvx",
      "args": ["browser-use", "--mcp"]
    }
  }
}
```

Restart Claude Code after adding.

## Usage

### Navigate & Extract

```
/browser-automation navigate https://docs.example.com
/browser-automation extract https://docs.example.com --format markdown
```

### Form Interaction

```
/browser-automation fill https://app.example.com/login
  email: test@example.com
  password: [from env TEST_PASSWORD]
  submit: button[type=submit]
```

### Deploy Verification

```
/browser-automation verify https://myapp.com
  - Check: homepage loads (< 3s)
  - Check: /api/health returns 200
  - Check: login page renders
  - Screenshot: homepage, login, dashboard
```

### Screenshot

```
/browser-automation screenshot https://myapp.com --full-page
/browser-automation screenshot https://myapp.com --element "#hero-section"
```

## Integration Points

| Trigger | How It Helps |
|---------|-------------|
| `shipper` deploys | Auto-verify live URL, take screenshots |
| `e2e-runner` needs browser | Natural language browser tests |
| `oracle` needs deep docs | Navigate multi-page documentation |
| `designer` needs references | Capture UI patterns from live sites |
| `qa-engineer` tests forms | Fill and submit forms, verify results |
| `growth` analyzes competitors | Extract features, pricing, UX patterns |

## MCP Tools Available

| Tool | Description |
|------|-------------|
| `browser_navigate` | Go to a URL |
| `browser_click` | Click element by selector or text |
| `browser_type` | Type into input field |
| `browser_screenshot` | Capture page/element screenshot |
| `browser_extract` | Extract page content as text/markdown |
| `browser_wait` | Wait for element or condition |
| `browser_evaluate` | Execute JavaScript in page context |
| `browser_scroll` | Scroll page or element |

## Rules

- Max 1 request/second to same domain
- Respect robots.txt
- Never store credentials in output
- Timeout: 30 seconds per page
- Retry once on failure, then report error
- Blur sensitive data in screenshots
