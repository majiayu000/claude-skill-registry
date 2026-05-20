---
name: webmcp-mcp-bridge
description: Integrate WebMCP client-side tools with backend MCP servers and UCP endpoints — bridge browser-based agent interactions with server-to-server protocols. Use when connecting front-end WebMCP to existing backend API infrastructure.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP + Backend Protocol Bridge

## Before writing code

**Fetch live docs**:
1. Fetch `https://webmachinelearning.github.io/webmcp/` for WebMCP client-side specification
2. Web-search `webmcp backend MCP integration bridge` for bridge architecture patterns
3. Web-search `site:github.com mcp-b backend MCP bridge` for MCP-B polyfill's backend translation features
4. Web-search `webmcp UCP Universal Commerce Protocol integration` for UCP bridge patterns

## Conceptual Architecture

### Why Bridge WebMCP and Backend Protocols

WebMCP and backend protocols serve different scenarios:

| Scenario | Protocol |
|----------|----------|
| User in browser, agent assisting | **WebMCP** (client-side) |
| Headless agent, no UI | **MCP** (server-to-server) |
| Agent-to-agent delegation | **A2A** (agent-to-agent) |
| Structured product discovery | **UCP** (commerce-specific) |
| Payment authorization | **AP2** (cryptographic payments) |

A business often needs both: WebMCP for browser-present users and MCP/UCP for headless scenarios. The bridge ensures both paths use the same backend logic.

### Architecture Patterns

#### Pattern 1: WebMCP Tool → Existing REST API → Same Backend as MCP

```
Browser Agent                     Headless Agent
     |                                  |
  WebMCP Tool                     MCP Tool Call
     |                                  |
  fetch("/api/products")          JSON-RPC to MCP Server
     |                                  |
     +--------→ Same Backend API ←------+
```

Both WebMCP tools and MCP tools call the same backend services. WebMCP tools use the user's session; MCP tools use API credentials.

#### Pattern 2: WebMCP Tool → UCP Endpoint

```
Browser Agent
     |
  WebMCP searchProducts tool
     |
  fetch("https://merchant.com/.well-known/ucp/products")
     |
  UCP-formatted response → parsed → returned to agent
```

WebMCP tools can call UCP endpoints directly, translating between the browser tool interface and UCP's JSON/REST API.

#### Pattern 3: MCP-B Polyfill Translation

The MCP-B polyfill can translate between WebMCP client-side tools and backend MCP services:

```
Browser Agent ←→ MCP-B Polyfill ←→ Backend MCP Server
```

This enables a single tool definition to work in both browser and server contexts.

### Implementation: WebMCP Tool Calling REST API

```js
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Search the product catalog",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string" },
      maxPrice: { type: "number" }
    },
    required: ["query"]
  },
  annotations: { readOnlyHint: true },
  async execute(input) {
    // Call the same API that the MCP server would call
    const params = new URLSearchParams({
      q: input.query,
      ...(input.maxPrice && { max_price: input.maxPrice })
    });
    const res = await fetch(`/api/products/search?${params}`, {
      credentials: "same-origin" // Uses user's session cookies
    });
    return await res.json();
  }
});
```

### Implementation: WebMCP Tool Calling UCP

```js
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Search products via Universal Commerce Protocol",
  inputSchema: { /* ... */ },
  async execute(input) {
    // Call UCP product discovery endpoint
    const res = await fetch("/api/ucp/products", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: input.query,
        filters: input.filters
      }),
      credentials: "same-origin"
    });
    return await res.json();
  }
});
```

### Shared Tool Definition Strategy

Define tool schemas once, use in both WebMCP and MCP:

```js
// shared/tool-definitions.js
export const searchProductsTool = {
  name: "searchProducts",
  description: "Search the product catalog",
  inputSchema: { /* ... */ }
};

// webmcp/tools.js — browser-side
import { searchProductsTool } from "../shared/tool-definitions.js";
navigator.modelContext.registerTool({
  ...searchProductsTool,
  async execute(input) {
    return await fetch(`/api/search?q=${input.query}`).then(r => r.json());
  }
});

// mcp/server.js — server-side
import { searchProductsTool } from "../shared/tool-definitions.js";
mcpServer.registerTool({
  ...searchProductsTool,
  handler: async (input) => {
    return await productService.search(input.query);
  }
});
```

### Best Practices

- Share tool schemas between WebMCP and MCP to ensure consistency
- WebMCP tools use session cookies; MCP tools use API keys — same backend, different auth
- Test both paths (browser and headless) against the same backend
- Consider caching at the API layer to handle both WebMCP and MCP traffic
- Document which tools are available via WebMCP vs MCP vs both

Fetch the latest MCP-B bridge documentation and UCP integration patterns before implementing cross-protocol bridges.
