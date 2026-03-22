---
name: browser-automation
description: Built-in browser automation skill for AgentForge agents. Navigate web pages, interact with elements, extract content, and take screenshots using Playwright.
version: 1.0.0
tags:
  - web
  - browser
  - automation
  - scraping
---

# Browser Automation

**Built-in AgentForge Skill** — Automate web browsers to navigate, interact, extract data, and capture screenshots.

## Overview

The Browser Automation skill gives agents the ability to interact with web pages programmatically using Playwright. This is essential for:

1. **Web scraping** — Extract text, data, and structured content from any website
2. **Form filling** — Automate login flows, form submissions, and multi-step workflows
3. **Visual verification** — Take screenshots for visual QA or documentation
4. **Research** — Navigate and read web pages to gather information
5. **Testing** — Verify web application behavior

## Supported Actions

| Action | Description | Key Parameters |
|--------|-------------|----------------|
| `navigate` | Go to a URL | `url` (required) |
| `click` | Click an element | `selector` (CSS selector) |
| `type` | Type text into an input | `selector`, `text` |
| `screenshot` | Capture the page | `fullPage` (optional) |
| `snapshot` | Get accessibility tree | — |
| `extractText` | Extract page text | `selector` (optional) |
| `evaluate` | Run JavaScript | `js` (code string) |
| `wait` | Wait for element/time | `selector` or `timeMs` |
| `scroll` | Scroll the page | `direction`, `amount` |
| `select` | Select dropdown option | `selector`, `value` |
| `hover` | Hover over element | `selector` |
| `goBack` | Navigate back | — |
| `goForward` | Navigate forward | — |
| `reload` | Reload the page | — |
| `close` | Close the session | — |

## How to Use

### Setup

```typescript
import { createBrowserTool, MCPServer } from '@agentforge-ai/core';

// Create browser tool with default config
const { tool, shutdown } = createBrowserTool({ headless: true });

// Register with MCP server
const server = new MCPServer({ name: 'my-tools' });
server.registerTool(tool);

// Or use the convenience function
import { registerBrowserTool } from '@agentforge-ai/core';
const { shutdown: cleanup } = registerBrowserTool(server, { headless: true });
```

### Docker Sandbox Mode

For secure, isolated browser execution (recommended for production):

```typescript
const { tool, shutdown } = createBrowserTool({
  sandboxMode: true,
  headless: true,
});
```

This launches the browser inside a Docker container with:
- Isolated network and filesystem
- 2GB shared memory for stability
- Automatic cleanup on shutdown

### Direct Import

```typescript
import { createBrowserTool } from '@agentforge-ai/core/browser';
```

## Agent Instructions

When a user asks you to interact with a web page:

1. **Navigate** to the target URL first
2. **Wait** for key elements to load before interacting
3. Use **snapshot** to understand the page structure (accessibility tree)
4. Use **extractText** to get readable content from the page
5. Use **click** and **type** to interact with forms and buttons
6. Use **screenshot** to capture visual state when needed
7. Always **close** sessions when done to free resources

### Tips for Reliable Automation

- Prefer `#id` selectors over class-based selectors
- Use `waitForSelector` before clicking or typing
- For SPAs, wait after navigation for content to render
- Use `extractText` with a selector to get specific section content
- Take screenshots before and after critical actions for verification

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `headless` | boolean | `true` | Run browser without UI |
| `defaultTimeout` | number | `30000` | Navigation timeout (ms) |
| `browserType` | string | `'chromium'` | Browser engine |
| `viewportWidth` | number | `1280` | Viewport width |
| `viewportHeight` | number | `720` | Viewport height |
| `userAgent` | string | — | Custom user agent |
| `persistState` | boolean | `false` | Save cookies/state |
| `statePath` | string | — | Path for state file |
| `sandboxMode` | boolean | `false` | Docker isolation |
| `maxSessions` | number | `5` | Max concurrent sessions |

## Session Management

Each session gets its own isolated browser context with separate cookies, storage, and state. Use `sessionId` to manage multiple concurrent browsing sessions:

```typescript
// Session A: logged into site X
await tool.handler({ action: { kind: 'navigate', url: 'https://site-x.com' }, sessionId: 'session-a' });

// Session B: logged into site Y (completely isolated)
await tool.handler({ action: { kind: 'navigate', url: 'https://site-y.com' }, sessionId: 'session-b' });
```

## Prerequisites

- **Playwright**: `npm install playwright && npx playwright install chromium`
- **Docker** (optional): Required only for `sandboxMode`
