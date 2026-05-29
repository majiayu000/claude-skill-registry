---
name: browser-content-capture
description: Capture content from JavaScript-rendered pages, login-protected sites, and multi-page documentation using agent-browser CLI. Use when capturing browser content, extracting web data, saving page content.
context: fork
agent: data-pipeline-engineer
version: 2.0.0
author: SkillForge AI Agent Hub
tags: [browser, agent-browser, scraping, spa, authentication, 2026]
user-invocable: false
allowed-tools: Bash(agent-browser:*)
---

# Browser Content Capture

**Capture web content that traditional scrapers cannot access using agent-browser CLI.**

## Overview

This skill enables content extraction from sources that require browser-level access:
- **JavaScript-rendered SPAs** (React, Vue, Angular apps)
- **Login-protected documentation** (private wikis, gated content)
- **Dynamic content** (infinite scroll, lazy loading, client-side routing)
- **Multi-page site crawls** (documentation trees, tutorial series)

## Overview

**Use when:**
- `WebFetch` returns empty or partial content
- Page requires JavaScript execution to render
- Content is behind authentication
- Need to navigate multi-page structures
- Extracting from client-side routed apps

**Do NOT use when:**
- Static HTML pages (use `WebFetch` - faster)
- Public API endpoints (use direct HTTP calls)
- Simple RSS/Atom feeds

---

## Quick Start

### Basic Capture Pattern

```bash
# 1. Navigate to URL
agent-browser open https://docs.example.com

# 2. Wait for content to render
agent-browser wait --load networkidle

# 3. Get interactive snapshot
agent-browser snapshot -i

# 4. Extract text content
agent-browser get text body

# 5. Take screenshot
agent-browser screenshot /tmp/capture.png

# 6. Close when done
agent-browser close
```

---

## agent-browser Commands Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `open <url>` | Go to URL | First step of any capture |
| `snapshot -i` | Get interactive element tree | Understanding page structure |
| `eval "<script>"` | Run custom JS | Extract specific content |
| `click @e#` | Click elements | Navigate menus, pagination |
| `fill @e# "value"` | Fill inputs | Authentication flows |
| `wait @e#` | Wait for element | Dynamic content loading |
| `screenshot <path>` | Capture image | Visual verification |
| `console` | Read JS console | Debug extraction issues |
| `network requests` | Monitor XHR/fetch | Find API endpoints |

**Full reference:** See [references/agent-browser-commands.md](references/agent-browser-commands.md)

---

## Capture Patterns

### Pattern 1: SPA Content Extraction

For React/Vue/Angular apps where content renders client-side:

```bash
# Navigate and wait for hydration
agent-browser open https://react-docs.example.com
agent-browser wait --load networkidle

# Get snapshot to identify content element
agent-browser snapshot -i

# Extract after framework mounts (use ref from snapshot)
agent-browser get text @e5  # Main content area

# Or use eval for custom extraction
agent-browser eval "document.querySelector('article').innerText"
```

**Details:** See [references/spa-extraction.md](references/spa-extraction.md)

### Pattern 2: Authentication Flow

For login-protected content:

```bash
# Navigate to login
agent-browser open https://docs.example.com/login
agent-browser snapshot -i

# Fill credentials (refs from snapshot)
agent-browser fill @e1 "user@example.com"  # Email field
agent-browser fill @e2 "password123"        # Password field

# Click submit and wait for redirect
agent-browser click @e3
agent-browser wait --url "**/dashboard"

# Save authenticated state for reuse
agent-browser state save /tmp/auth-state.json

# Now navigate to protected content
agent-browser open https://docs.example.com/private-docs
```

**Details:** See [references/auth-handling.md](references/auth-handling.md)

### Pattern 3: Multi-Page Crawl

For documentation with navigation trees:

```bash
# Get all page links from sidebar
agent-browser open https://docs.example.com
agent-browser snapshot -i

# Extract links via eval
LINKS=$(agent-browser eval "JSON.stringify(Array.from(document.querySelectorAll('nav a')).map(a => a.href))")

# Iterate and capture each page
for link in $(echo "$LINKS" | jq -r '.[]'); do
    agent-browser open "$link"
    agent-browser wait --load networkidle
    agent-browser get text body > "/tmp/content-$(basename $link).txt"
done
```

**Details:** See [references/multi-page-crawl.md](references/multi-page-crawl.md)

---

## Session Management

### Save and Reuse Authentication

```bash
# Login once and save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "$USERNAME"
agent-browser fill @e2 "$PASSWORD"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save /tmp/app-auth.json

# Later: restore state
agent-browser state load /tmp/app-auth.json
agent-browser open https://app.example.com/protected-content
```

### Parallel Sessions

```bash
# Run isolated sessions for different tasks
agent-browser --session scrape1 open https://site1.com
agent-browser --session scrape2 open https://site2.com

# Extract from each
agent-browser --session scrape1 get text body > site1.txt
agent-browser --session scrape2 get text body > site2.txt
```

---

## Fallback Strategy

Use this decision tree for content capture:

```
User requests content from URL
         │
         ▼
    ┌─────────────┐
    │ Try WebFetch│ ← Fast, no browser needed
    └─────────────┘
         │
    Content OK? ──Yes──► Done
         │
         No (empty/partial)
         │
         ▼
    ┌──────────────────┐
    │ Use agent-browser│
    └──────────────────┘
         │
    ├─ Known SPA (react, vue, angular) ──► wait --load networkidle
    ├─ Requires login ──► Authentication flow with state save
    └─ Dynamic content ──► wait @element or wait --text
```

---

## Best Practices

### 1. Minimize Browser Usage
- Always try `WebFetch` first (10x faster, no browser overhead)
- Cache extracted content to avoid re-scraping
- Use `get text @e#` to extract only needed content

### 2. Handle Dynamic Content
- Always use `wait` after navigation
- Use `wait --load networkidle` for heavy SPAs
- Use `wait --text "Expected"` for specific content

### 3. Respect Rate Limits
- Add delays between page navigations
- Don't crawl faster than a human would browse
- Honor robots.txt and terms of service

### 4. Clean Extracted Content
- Use targeted refs from snapshot to extract main content
- Use `eval` to remove noise elements before extraction
- Convert to clean markdown for downstream processing

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty content | Add `wait --load networkidle` after navigation |
| Partial render | Use `wait --text "Expected content"` |
| Login required | Use authentication flow with `state save/load` |
| CAPTCHA blocking | Manual intervention required |
| Content in iframe | Use `frame @e#` then extract |

---

## Related Skills

- `agent-browser` - Full agent-browser command reference
- `webapp-testing` - Playwright test automation patterns
- `streaming-api-patterns` - Handle SSE progress updates

---

**Version:** 2.0.0 (January 2026)
**Browser Tool:** agent-browser CLI (replaces Playwright MCP)

## Capability Details

### spa-extraction
**Keywords:** react, vue, angular, spa, javascript, client-side, hydration, ssr
**Solves:**
- WebFetch returns empty content
- Page requires JavaScript to render
- React/Vue app content extraction

### auth-handling
**Keywords:** login, authentication, session, cookie, protected, private, gated
**Solves:**
- Content behind login wall
- Need to authenticate first
- Private documentation access

### multi-page-crawl
**Keywords:** crawl, sitemap, navigation, multiple pages, documentation, tutorial series
**Solves:**
- Capture entire documentation site
- Extract multiple pages
- Follow navigation links

### agent-browser-commands
**Keywords:** agent-browser, open, snapshot, click, fill, eval, get text
**Solves:**
- Which command to use
- Browser automation reference
- agent-browser CLI guide
