---
name: webmcp-setup
description: Set up a WebMCP project — enable Chrome flags, install MCP-B polyfill, scaffold tool registration, and configure development environment. Use when starting a new WebMCP-enabled website from scratch.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Project Setup

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.chrome.com/blog/webmcp` for the latest Chrome WebMCP announcement and API overview
2. Web-search `site:github.com mcp-b polyfill README` for the MCP-B polyfill installation and quickstart
3. Web-search `webmcp chrome canary flag enable` for current browser flag names and version requirements
4. Fetch the MCP-B npm page for the latest package version numbers
5. Web-search `site:chromestatus.com webmcp` for feature status and milestones

## Conceptual Architecture

### What Setup Involves

WebMCP project setup prepares a website to expose tools to AI agents:
1. **Enable browser support** — Chrome 146+ Canary with the `WebMCP for Testing` flag, or install the MCP-B polyfill
2. **Install polyfill (if needed)** — `mcp-b` packages for vanilla JS or React
3. **Scaffold tool registration** — create the entry point where tools are registered via `navigator.modelContext.registerTool()`
4. **Configure development environment** — set up testing with AI agents

### Project Structure (Vanilla JS)

```
my-webmcp-site/
├── src/
│   ├── webmcp/
│   │   ├── tools.js              # Tool definitions and registration
│   │   ├── schemas.js            # JSON Schemas for tool inputs
│   │   └── interactions.js       # User interaction handlers
│   ├── index.html                # Page with optional declarative form attributes
│   └── app.js                    # Main application entry
├── package.json
└── tests/
    └── webmcp.test.js
```

### Project Structure (React + MCP-B)

```
my-webmcp-react-app/
├── src/
│   ├── webmcp/
│   │   ├── tools.ts              # Tool definitions
│   │   ├── schemas.ts            # JSON Schemas
│   │   ├── McpProvider.tsx        # MCP-B React provider/hooks wrapper
│   │   └── interactions.ts       # User interaction logic
│   ├── App.tsx
│   └── index.tsx
├── package.json
├── tsconfig.json
└── tests/
    └── webmcp.test.tsx
```

### Setup Decision Checklist

- **Browser target** — Native Chrome 146+ (flag-gated) or polyfill for broader support?
- **Framework** — Vanilla JS, React, Vue, or server-rendered HTML?
- **API approach** — Imperative (JS `registerTool`), Declarative (HTML attributes), or both?
- **Tool scope** — Which user journeys will be exposed as tools?
- **Authentication** — What user role is required before registering sensitive tools?
- **Testing strategy** — Which AI agents to test with (Gemini, Claude, etc.)?

### Chrome Flag Setup

To enable native WebMCP in Chrome Canary:
1. Install Chrome 146+ Canary
2. Navigate to `chrome://flags`
3. Search for the WebMCP flag (name may change — search for it live)
4. Enable the flag and restart Chrome

### MCP-B Polyfill Setup

For browsers without native WebMCP, the MCP-B polyfill provides the same API surface. Fetch the README for exact installation commands, as packages and APIs may have changed.

### Best Practices

- Start with one or two simple read-only tools before adding transactional ones
- Use the polyfill for development even if targeting native Chrome — it works everywhere
- Register tools after the page has loaded and the user is authenticated
- Group related tools logically (all cart tools together, all search tools together)
- Test tool discovery with at least one AI agent before going to production

Fetch the latest Chrome blog post and MCP-B README for exact commands, package names, and API patterns before scaffolding.
