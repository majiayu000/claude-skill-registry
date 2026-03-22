---
name: webmcp-register-tool
description: Implement the WebMCP Imperative API — register tools via navigator.modelContext.registerTool() with proper schemas, execute callbacks, and lifecycle management. Use when building dynamic tool registration in JavaScript.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Tool Registration (Imperative API)

## Before writing code

**Fetch live docs**:
1. Fetch `https://webmachinelearning.github.io/webmcp/` for the latest `registerTool` method signature and parameters
2. Web-search `webmcp navigator.modelContext registerTool specification` for the full API reference
3. Web-search `site:developer.chrome.com webmcp registerTool` for Chrome-specific guidance
4. Web-search `site:github.com mcp-b registerTool` for polyfill-compatible registration patterns

## Conceptual Architecture

### What registerTool Does

`navigator.modelContext.registerTool()` is the core imperative method for exposing a tool to AI agents. Each registered tool becomes discoverable and invocable by any agent integrated with the browser.

### Tool Definition Object

A tool object passed to `registerTool()` has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique tool identifier (e.g., `"addToCart"`) |
| `description` | string | Yes | Natural-language description for the agent |
| `inputSchema` | object | Yes | JSON Schema defining accepted parameters |
| `execute` | async function | Yes | Callback `(input, client) => Promise<result>` |
| `annotations` | object | No | Safety hints (`readOnlyHint`, `destructiveHint`, `idempotentHint`) |

### Execute Callback

The `execute(input, client)` callback:
- **input** — Validated against the `inputSchema`, already parsed as a JavaScript object
- **client** — A `ModelContextClient` object providing `requestUserInteraction()` for human-in-the-loop flows
- **Returns** — A Promise resolving to a JSON-serializable result object

### Tool Lifecycle

1. **Register** — `navigator.modelContext.registerTool(tool)` makes the tool discoverable
2. **Discovery** — Agent queries available tools and reads names/descriptions/schemas
3. **Invocation** — Agent calls a tool; browser validates input against schema and calls `execute`
4. **Execution** — Tool logic runs in the page's context (can use fetch, DOM APIs, session cookies)
5. **Result** — Tool returns JSON result to the agent
6. **Unregister** — `navigator.modelContext.unregisterTool(name)` removes the tool

### Registration Patterns

**Simple read-only tool:**
```js
navigator.modelContext.registerTool({
  name: "getProductInfo",
  description: "Get details about a product by ID",
  inputSchema: {
    type: "object",
    properties: { productId: { type: "string" } },
    required: ["productId"]
  },
  annotations: { readOnlyHint: true },
  async execute(input) {
    const res = await fetch(`/api/products/${input.productId}`);
    return await res.json();
  }
});
```

**Transactional tool with user confirmation:**
```js
navigator.modelContext.registerTool({
  name: "placeOrder",
  description: "Place the current order and charge the saved payment method",
  inputSchema: { type: "object", properties: {}, required: [] },
  annotations: { destructiveHint: true },
  async execute(input, client) {
    const confirmed = await client.requestUserInteraction((resolve) => {
      showConfirmDialog("Confirm order?", resolve);
    });
    if (!confirmed) return { status: "canceled" };
    const res = await fetch("/api/orders", { method: "POST" });
    return await res.json();
  }
});
```

### Naming Best Practices

- Use camelCase for tool names (`searchProducts`, not `search-products`)
- Be specific and descriptive (`addToCart` not `add`)
- Group by domain: `cart.add`, `cart.remove` or `addToCart`, `removeFromCart`
- Avoid generic names that could conflict across sites

### Description Best Practices

- Write descriptions for the AI agent, not the end user
- Be precise about what the tool does, its side effects, and what it returns
- Mention constraints: "Requires the user to be logged in" or "Only available for items in stock"
- Avoid jargon the agent may not understand

### Error Handling

Tools should handle errors gracefully:
- Return structured error objects rather than throwing exceptions
- Include error codes and human-readable messages
- Distinguish between user errors (bad input) and system errors (server failure)

### Dynamic Registration

Tools can be registered and unregistered dynamically based on page state:
- Register cart tools only when the cart page is active
- Register checkout tools only when the user is authenticated
- Unregister tools when navigating away from relevant pages
- Use `clearContext()` on page transitions in SPAs

Fetch the specification for exact method signatures, return types, and any new fields before implementing.
