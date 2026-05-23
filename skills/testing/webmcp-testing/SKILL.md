---
name: webmcp-testing
description: Test WebMCP tools with AI agents — Chrome DevTools integration, agent testing workflows, tool discovery verification, and end-to-end commerce flow testing. Use when validating that tools work correctly with real AI agents.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Testing

## Before writing code

**Fetch live docs**:
1. Web-search `webmcp testing tools agents Chrome DevTools` for testing tooling and guidance
2. Web-search `site:developer.chrome.com webmcp testing early preview` for Chrome EPP testing instructions
3. Web-search `webmcp tool discovery verification testing` for testing patterns
4. Web-search `site:github.com mcp-b testing` for polyfill-specific testing utilities

## Conceptual Architecture

### Testing Dimensions

WebMCP tools need testing across multiple dimensions:

1. **Unit testing** — Does the tool logic work correctly in isolation?
2. **Schema testing** — Does the JSON Schema validate correctly?
3. **Integration testing** — Does the tool interact correctly with backend APIs?
4. **Agent testing** — Do real AI agents discover and invoke tools correctly?
5. **Permission testing** — Do annotations and user interactions work as expected?
6. **End-to-end testing** — Does the full agent-to-checkout flow succeed?

### Unit Testing Tool Logic

Test the `execute` callback independently:

```js
// Extract execute logic into a testable function
async function searchProductsLogic(input) {
  const res = await fetch(`/api/products?q=${input.query}`);
  return await res.json();
}

// Unit test
describe("searchProducts tool", () => {
  it("returns products matching query", async () => {
    mockFetch("/api/products?q=headphones", { products: [...] });
    const result = await searchProductsLogic({ query: "headphones" });
    expect(result.products).toHaveLength(3);
  });

  it("handles empty results", async () => {
    mockFetch("/api/products?q=nonexistent", { products: [] });
    const result = await searchProductsLogic({ query: "nonexistent" });
    expect(result.products).toHaveLength(0);
  });
});
```

### Schema Validation Testing

Verify that schemas accept valid input and reject invalid input:

```js
import Ajv from "ajv";

const ajv = new Ajv();
const validate = ajv.compile(searchProductsSchema);

test("accepts valid input", () => {
  expect(validate({ query: "headphones", maxPrice: 100 })).toBe(true);
});

test("rejects missing required field", () => {
  expect(validate({ maxPrice: 100 })).toBe(false);
});

test("rejects invalid type", () => {
  expect(validate({ query: 123 })).toBe(false);
});
```

### Agent Testing Workflow

Test with real AI agents (Gemini, Claude, etc.):

1. **Enable WebMCP** — Chrome Canary with flag, or MCP-B polyfill
2. **Load the page** — Navigate to the page with registered tools
3. **Invoke the agent** — Ask the agent to perform a task (e.g., "Search for wireless headphones")
4. **Observe tool discovery** — Verify the agent sees the registered tools
5. **Observe tool invocation** — Verify the agent calls the correct tool with valid parameters
6. **Check results** — Verify the agent receives and correctly interprets the tool's response

### Chrome DevTools Integration

Chrome may provide DevTools panels for WebMCP:
- View registered tools and their schemas
- Monitor tool invocations in real time
- Inspect tool input/output payloads
- Test tools manually (invoke with custom input)

Check Chrome DevTools documentation for the latest WebMCP debugging features.

### Testing User Interactions

Test `requestUserInteraction` flows:

```js
test("checkout requires user confirmation", async () => {
  const mockClient = {
    requestUserInteraction: jest.fn((callback) => {
      // Simulate user approving
      return new Promise((resolve) => callback(resolve));
    })
  };

  const result = await checkoutTool.execute({}, mockClient);
  expect(mockClient.requestUserInteraction).toHaveBeenCalled();
  expect(result.status).toBe("confirmed");
});

test("checkout canceled when user declines", async () => {
  const mockClient = {
    requestUserInteraction: jest.fn(() => Promise.resolve(false))
  };

  const result = await checkoutTool.execute({}, mockClient);
  expect(result.status).toBe("canceled");
});
```

### End-to-End Commerce Flow Test

Test the full shopping journey:

```
1. Navigate to catalog page → verify search tools registered
2. Agent calls searchProducts("headphones") → verify results returned
3. Agent calls addToCart(productId, 1) → verify cart updated
4. Navigate to cart page → verify cart tools registered
5. Agent calls checkout() → verify user interaction prompted
6. Simulate user approval → verify order placed
7. Verify order confirmation returned to agent
```

### Testing Annotation Behavior

Verify that annotations affect browser behavior:
- `readOnlyHint: true` tools → agent can invoke without user prompt
- `destructiveHint: true` tools → browser prompts user before invocation
- Test with different annotation combinations

### Performance Testing

- Measure tool registration time (should be < 100ms)
- Measure tool invocation latency (execute callback + API call)
- Compare WebMCP vs manual UI interaction timing
- Test under concurrent tool invocations

### Best Practices

- Write unit tests for tool logic, separate from WebMCP registration
- Use schema validation libraries (Ajv) to test input schemas
- Test with at least two different AI agents to catch agent-specific issues
- Mock `ModelContextClient` for unit testing user interaction flows
- Document expected agent behavior for each tool
- Keep a test script of agent prompts that exercise all tools

Fetch the latest Chrome DevTools documentation and testing utilities for WebMCP before setting up test infrastructure.
