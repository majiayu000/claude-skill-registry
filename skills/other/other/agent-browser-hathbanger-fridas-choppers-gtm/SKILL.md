---
name: agent-browser
description: Headless browser automation for AI agents - auto-installs if needed
---

# Agent Browser

Headless browser automation CLI for AI agents. [GitHub](https://github.com/vercel-labs/agent-browser)

## On Skill Invoke

**Step 1: Check if installed**

```bash
which agent-browser
```

**Step 2: If NOT installed, offer to install**

```
agent-browser not installed.

This tool lets me browse the web, fill forms, take screenshots, and scrape dynamic content.

Install it?

  npm install -g agent-browser
  agent-browser install

[Yes] [No]
```

If user says yes, run:
```bash
npm install -g agent-browser && agent-browser install
```

On Linux, if install fails with dependency errors:
```bash
agent-browser install --with-deps
```

After install, confirm:
```
Done. agent-browser ready.

Try: agent-browser navigate https://example.com
```

**Step 3: If already installed, show status**

```
agent-browser is installed.

Quick commands:
  agent-browser navigate <url>    # Go to URL
  agent-browser snapshot          # Get page structure (for AI)
  agent-browser click <ref>       # Click element
  agent-browser type <ref> <text> # Type into input
  agent-browser screenshot        # Capture page
  agent-browser pdf               # Generate PDF

Need help with something specific?
```

## What It Does

Agent-browser gives Claude the ability to:
- Navigate and interact with web pages
- Click, type, scroll
- Take screenshots and generate PDFs
- Extract accessibility trees (semantic page understanding)
- Monitor network requests
- Manage cookies and storage

## Common Commands

| Command | What It Does |
|---------|--------------|
| `agent-browser navigate <url>` | Go to a URL |
| `agent-browser snapshot` | Get accessibility tree (for AI understanding) |
| `agent-browser click <ref>` | Click an element by reference |
| `agent-browser type <ref> <text>` | Type into an input |
| `agent-browser screenshot` | Capture the page |
| `agent-browser pdf` | Generate PDF |

## When to Use

Use agent-browser when you need to:
- Scrape dynamic content (SPAs, JS-rendered pages)
- Fill out forms programmatically
- Test user flows
- Capture screenshots for docs/previews
- Extract data from authenticated pages

## Typical Workflow

1. `agent-browser navigate <url>` - load the page
2. `agent-browser snapshot` - understand page structure
3. `agent-browser click <ref>` / `agent-browser type <ref> <text>` - interact
4. `agent-browser screenshot` or extract data

## Troubleshooting

### "chromium not found"
```bash
agent-browser install
```

### Permission errors on Linux
```bash
agent-browser install --with-deps
```

### Page not loading
Some sites block headless browsers. The tool handles most cases, but very aggressive bot detection may block it.
