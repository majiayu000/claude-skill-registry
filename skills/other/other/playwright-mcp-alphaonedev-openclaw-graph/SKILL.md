---
name: playwright-mcp
cluster: community
description: "Playwright MCP server: browser automation via MCP protocol, page interaction, form filling"
tags: ["playwright","mcp","browser","automation"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "playwright mcp browser automation page interact form fill"
---

# playwright-mcp

## Purpose
This skill provides a Playwright-based MCP server for browser automation, enabling programmatic control of web pages via the MCP protocol. It focuses on tasks like navigating sites, interacting with elements, and filling forms, integrated with OpenClaw for AI-driven workflows.

## When to Use
Use this skill for automating browser interactions in scenarios like web scraping, UI testing, or dynamic form submissions. It's ideal when you need remote browser control, such as in CI/CD pipelines, data extraction from JavaScript-heavy sites, or simulating user actions across multiple pages.

## Key Capabilities
- Launch browsers (e.g., Chromium, Firefox) and manage sessions via MCP protocol.
- Interact with page elements: select, click, or type using methods like `page.click('button')`.
- Handle form filling and submissions: auto-populate fields and submit with `page.fill('input[name="username"]', 'user123')`.
- Support for asynchronous operations: wait for elements with `page.waitForSelector('selector')`.
- Error-resilient navigation: retry failed loads with built-in timeouts.
- Configurable via JSON files, e.g., {"browser": "chromium", "headless": true}.

## Usage Patterns
To use this skill, start the MCP server and send commands from OpenClaw. Always initialize with authentication via `$PLAYWRIGHT_MCP_API_KEY`. Pattern 1: Launch a browser session and perform actions in sequence. Pattern 2: Use in loops for repetitive tasks, like form testing. For integration, wrap calls in try-catch blocks. Example pattern: Set up server with CLI, then use API endpoints to execute scripts.

## Common Commands/API
- CLI: Run `playwright-mcp start --port 8080 --headless` to launch the server; add `--debug` for verbose logging.
- API: POST to `/mcp/execute` with JSON payload, e.g., {"action": "navigate", "url": "https://example.com"}.
- Code snippet for basic navigation:
  ```
  const response = fetch('http://localhost:8080/mcp/execute', {
    method: 'POST',
    headers: {'Authorization': `Bearer ${process.env.PLAYWRIGHT_MCP_API_KEY}`},
    body: JSON.stringify({action: 'goto', url: 'https://example.com'})
  });
  ```
- For element interaction: Use `/mcp/interact` endpoint, e.g., POST with {"selector": '#id', "action": "click"}.
- Config format: YAML or JSON, e.g., {"timeout": 30000, "retries": 3} in a file passed via `--config path/to/config.json`.
- Authentication: Always include `$PLAYWRIGHT_MCP_API_KEY` in headers; check for 401 errors if missing.

## Integration Notes
Integrate by running the server as a subprocess or via HTTP clients in OpenClaw. Set `$PLAYWRIGHT_MCP_API_KEY` as an environment variable for authentication. For example, in OpenClaw scripts, import as a module and call functions like `mcpClient.execute({action: 'fill', selector: 'input', value: 'data'}). Use WebSockets for real-time updates on `/mcp/ws`. Ensure compatibility with Node.js 14+; handle CORS by adding `--allow-origins *` to CLI. Test integrations with mock servers to simulate failures.

## Error Handling
Common errors include timeout exceptions (e.g., network delays) or selector failures; use `page.waitForTimeout(5000)` before actions. For API errors, check response codes: 404 for invalid endpoints, 500 for server issues. Handle with try-catch in code, e.g.:
  ```
  try {
    await page.click('nonexistent');
  } catch (error) {
    console.error('Element not found:', error.message);
    // Retry or fallback
  }
  ```
Prescribe logging all errors with `--debug` flag. For authentication failures, verify `$PLAYWRIGHT_MCP_API_KEY` and retry. Use exponential backoff for transient errors like 429 (rate limit).

## Concrete Usage Examples
1. Automate form filling: Start server with `playwright-mcp start --port 8080`, then send API call to fill and submit a login form: POST `/mcp/execute` with {"action": "fill", "selector": '#username', "value": "testuser", "then": "click('#submit')"}. This extracts data or verifies login success.
2. Web scraping task: Use in OpenClaw to navigate to a page and extract content: CLI command `playwright-mcp execute --url 'https://site.com' --script 'page.evaluate(() => document.querySelector("#data").textContent)'`, then process the output for analysis.

## Graph Relationships
- Related to: browser-automation (depends on for core functionality), web-scraping (extends for data extraction), mcp-protocol (implements as base).
- Clusters: community (part of), automation-tools (links to for broader ecosystem).
- Dependencies: playwright-core (requires for browser control), mcp-server (bases on for protocol handling).
