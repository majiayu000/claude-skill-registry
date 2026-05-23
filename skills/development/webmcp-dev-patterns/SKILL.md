---
name: webmcp-dev-patterns
description: Apply WebMCP cross-cutting development patterns — SPA routing, error handling, performance optimization, multi-site agents, accessibility, SEO, and production deployment. Use when architecting WebMCP-enabled sites or solving cross-cutting concerns.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Development Patterns

## Before writing code

**Fetch live docs**:
1. Fetch `https://developer.chrome.com/blog/webmcp` for the latest developer guidance and patterns
2. Web-search `webmcp development best practices patterns` for community patterns
3. Web-search `webmcp SPA single page application routing` for SPA-specific patterns
4. Web-search `webmcp SEO agent discovery` for discoverability patterns

## Conceptual Architecture

### SPA Tool Lifecycle

In single-page applications, tools must be managed across route changes:

```js
// React example: register/unregister tools on route change
useEffect(() => {
  const tools = getToolsForRoute(currentRoute);
  tools.forEach(tool => navigator.modelContext.registerTool(tool));

  return () => {
    // Cleanup on route change
    tools.forEach(tool => navigator.modelContext.unregisterTool(tool.name));
  };
}, [currentRoute]);
```

**Key principles:**
- Clear context on navigation (`clearContext()` or selective `unregisterTool`)
- Register tools relevant to the current view only
- Handle async data loading — don't register tools until data is available
- Consider preregistering common tools (search) that are always relevant

### Error Handling

Tools should handle errors at multiple levels:

**Network errors:**
```js
async execute(input) {
  try {
    const res = await fetch(`/api/products?q=${input.query}`);
    if (!res.ok) {
      return { status: "error", code: res.status, message: "Server error" };
    }
    return await res.json();
  } catch (err) {
    return { status: "error", code: "network_error", message: "Unable to reach server" };
  }
}
```

**Business logic errors:**
```js
async execute(input) {
  const product = await fetchProduct(input.productId);
  if (!product) {
    return { status: "error", code: "not_found", message: "Product not found" };
  }
  if (!product.inStock) {
    return { status: "error", code: "out_of_stock", message: "Product is out of stock" };
  }
  // proceed...
}
```

**Consistent error format:**
```js
{ status: "error", code: "error_code", message: "Human-readable message" }
```

### Performance Optimization

WebMCP tools are inherently faster than UI scraping, but optimize further:

- **Avoid redundant fetches** — Cache API responses within a tool session
- **Batch operations** — Combine related API calls in a single tool
- **Lightweight responses** — Return only what the agent needs, not entire page data
- **Async registration** — Register tools after the critical rendering path
- **Lazy tool loading** — Load tool execute logic only when the tool is invoked

### Multi-Site Agent Patterns

Agents may navigate across multiple sites, each with WebMCP:

```
Agent Journey:
1. Open site-a.com → discovers tools [searchA, addToCartA, checkoutA]
2. Call searchA("wireless headphones") → get results
3. Open site-b.com → discovers tools [searchB, addToCartB, checkoutB]
4. Call searchB("wireless headphones") → get results
5. Agent compares results and recommends best option to user
6. User picks site-a → agent calls addToCartA and checkoutA
```

**Design implications:**
- Tool names should be descriptive enough to distinguish across sites
- Return standardized response formats (product name, price, currency, availability)
- Include site identity in tool descriptions ("Search products on ExampleStore")

### Accessibility

WebMCP tools should support accessible interactions:
- User interaction prompts (confirmations) must be keyboard-navigable
- Screen readers should announce agent actions and confirmation dialogs
- ARIA labels on confirmation UI elements
- Focus management — return focus appropriately after user interaction
- High-contrast support for confirmation dialogs

### SEO and AI Discovery

WebMCP enhances AI discoverability:
- Agents prefer sites with structured tools over sites requiring scraping
- Tool names and descriptions are effectively "agent SEO" — write them clearly
- Consider how AI search engines (Google AI Mode) discover and rank your tools
- Declarative form annotations make your site instantly agent-ready for crawlers
- WebMCP may become a ranking factor — early adoption is a competitive advantage

### Versioning

As tools evolve:
- Version tool schemas when making breaking changes
- Consider tool name versioning (`searchProductsV2`) for backward compatibility
- Document tool changes in a changelog
- Deprecate old tools gracefully before removing them

### Production Deployment Checklist

- [ ] All tools tested with at least one AI agent
- [ ] Schemas validated with a JSON Schema validator
- [ ] Annotations (`destructiveHint`, etc.) set on all tools
- [ ] User interaction flows tested for sensitive actions
- [ ] Error handling covers network failures, auth expiration, and business logic
- [ ] Server-side rate limiting on all APIs called by tools
- [ ] Audit logging for tool invocations
- [ ] Feature detection with polyfill fallback
- [ ] Performance tested under concurrent agent load
- [ ] Accessibility verified for confirmation dialogs
- [ ] CSRF protection on all state-changing endpoints
- [ ] Monitoring/alerting for tool invocation errors

### Monitoring and Observability

Track agent interactions in production:
- **Tool invocation count** — Which tools are used most?
- **Tool success/failure rate** — Which tools fail frequently?
- **Agent conversion rate** — Do agent-assisted sessions convert better?
- **Latency percentiles** — How fast are tool responses?
- **User interaction outcomes** — How often do users approve vs decline?

### Commerce Platform Integration

Commerce platforms will likely add built-in WebMCP support:
- **Shopify** — May add `toolname` attributes to Liquid templates
- **Magento** — Custom modules for tool registration
- **WooCommerce** — WordPress plugins for WebMCP
- **Headless CMS** — API-first platforms can provide tool definitions

Monitor your platform's announcements for native WebMCP support.

### Best Practices Summary

- Treat tool descriptions as a first-class UX concern — they are the agent's interface
- Start with read-only tools, add transactional tools incrementally
- Test every tool with a real AI agent before shipping
- Monitor tool usage in production and iterate on descriptions/schemas
- Keep tools focused — one action per tool, not multi-step wizards
- Document your tool surface for other developers and future agents

Fetch the latest community patterns, Chrome DevTools features, and platform integration announcements before architecting.
