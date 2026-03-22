---
name: webmcp-polyfill
description: Set up and use the MCP-B polyfill — vanilla JS and React packages that implement navigator.modelContext for browsers without native WebMCP. Use when developing for browsers that don't yet support WebMCP natively.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MCP-B Polyfill for WebMCP

## Before writing code

**Fetch live docs**:
1. Web-search `site:github.com mcp-b README` for the polyfill repository, packages, and API documentation
2. Web-search `site:npmjs.com mcp-b` for the latest package names and versions
3. Fetch the MCP-B GitHub README for installation, usage, and React hooks API
4. Web-search `mcp-b polyfill react hooks useMcpServer` for React integration patterns
5. Web-search `mcp-b vanilla javascript navigator.modelContext` for vanilla JS usage

## Conceptual Architecture

### What MCP-B Is

MCP-B (Model Context Protocol for Browser) is an open-source polyfill that implements the `navigator.modelContext` API for browsers without native WebMCP support. It allows developers to build and test WebMCP tools today, regardless of native browser support.

### Why Use the Polyfill

- **Chrome Canary only** — Native WebMCP is behind a flag in Chrome 146+ Canary; most users don't have it
- **Cross-browser** — The polyfill works in any modern browser (Chrome, Firefox, Safari, Edge)
- **Development** — Build and test tools before native support rolls out
- **Production** — Ship WebMCP tools to all users, with graceful enhancement when native support arrives

### Package Structure

MCP-B provides multiple packages (fetch the README for exact names, as they may change):
- **Vanilla JS package** — Direct `navigator.modelContext` polyfill
- **React package** — React hooks (`useMcpServer` and related) for declarative tool registration

### Feature Detection

Check for native WebMCP support and fall back to the polyfill:

```js
if (!navigator.modelContext) {
  // Load MCP-B polyfill
  await import("mcp-b"); // or whatever the current package name is
}

// Now navigator.modelContext is available (native or polyfill)
navigator.modelContext.registerTool({ /* ... */ });
```

### Vanilla JS Usage Pattern

```js
// 1. Import polyfill (if needed)
import "mcp-b";

// 2. Register tools using the standard API
navigator.modelContext.registerTool({
  name: "searchProducts",
  description: "Search the catalog",
  inputSchema: { /* ... */ },
  async execute(input) { /* ... */ }
});
```

### React Hooks Usage Pattern

```jsx
import { useMcpServer } from "mcp-b/react"; // verify package name

function ProductPage() {
  useMcpServer({
    tools: [
      {
        name: "viewProduct",
        description: "View product details",
        inputSchema: { /* ... */ },
        execute: async (input) => { /* ... */ }
      }
    ]
  });

  return <div>Product Page</div>;
}
```

### MCP-B Backend Translation

MCP-B can also translate between client-side WebMCP tools and backend MCP servers:
- Register backend MCP tools as browser-accessible WebMCP tools
- Forward WebMCP tool calls to a backend MCP server
- Handle the protocol translation transparently

### Polyfill vs Native

| Aspect | Native WebMCP | MCP-B Polyfill |
|--------|--------------|----------------|
| **Browser support** | Chrome 146+ Canary (flagged) | Any modern browser |
| **Performance** | Native speed | Slight JS overhead |
| **Permission prompts** | Browser-native UI | Custom/simulated |
| **API surface** | Full spec | May lag behind spec updates |
| **Production readiness** | Not yet (still in preview) | Usable today |

### Progressive Enhancement Strategy

1. Ship the polyfill for broad browser support
2. Detect native WebMCP support at runtime
3. Use native when available, polyfill as fallback
4. Remove polyfill dependency once native support is widespread

### Best Practices

- Always check the MCP-B repo for the latest package names and APIs before installing
- Use feature detection, not browser sniffing, to decide polyfill loading
- Test with both the polyfill and native Chrome to catch behavior differences
- Keep the polyfill updated — APIs may change as the spec evolves
- Consider code-splitting — only load the polyfill for browsers that need it

Fetch the MCP-B README for exact installation commands, import paths, hook names, and API patterns before implementing.
