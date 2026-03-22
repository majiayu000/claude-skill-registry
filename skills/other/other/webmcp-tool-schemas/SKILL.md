---
name: webmcp-tool-schemas
description: Design JSON Schemas for WebMCP tool inputs and outputs — proper types, constraints, nested objects, and agent-friendly documentation. Use when defining or refining tool schemas for agent consumption.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# WebMCP Tool Schema Design

## Before writing code

**Fetch live docs**:
1. Fetch `https://webmachinelearning.github.io/webmcp/` for the `inputSchema` specification and any constraints
2. Web-search `webmcp inputSchema JSON Schema requirements` for schema format details
3. Web-search `JSON Schema draft specification` for the JSON Schema version used by WebMCP
4. Web-search `webmcp tool schema best practices` for community guidance

## Conceptual Architecture

### Role of Schemas in WebMCP

The `inputSchema` in a tool definition serves two purposes:
1. **Agent guidance** — The agent reads the schema to understand what parameters to provide
2. **Input validation** — The browser validates agent-provided input against the schema before calling `execute`

### Schema Structure

WebMCP uses standard JSON Schema. Each tool's `inputSchema` is a JSON Schema object:

```js
inputSchema: {
  type: "object",
  properties: {
    paramName: { type: "string", description: "What this parameter is" },
    // ...more properties
  },
  required: ["paramName"]
}
```

### Property Types

| JSON Schema Type | Use For | Example |
|-----------------|---------|---------|
| `string` | Text, IDs, codes | Product ID, search query, coupon code |
| `number` | Decimal values | Price, weight, rating |
| `integer` | Whole numbers | Quantity, page number |
| `boolean` | True/false flags | In-stock filter, gift wrap option |
| `array` | Lists | Product IDs, selected categories |
| `object` | Nested structures | Address, payment details |

### Description Annotations

Always add `description` to properties — agents use these to decide what values to provide:

```js
properties: {
  query: {
    type: "string",
    description: "Search keywords for product catalog"
  },
  maxPrice: {
    type: "number",
    description: "Maximum price in USD. Omit to search all prices."
  }
}
```

### Constraints

Use JSON Schema constraints to guide agent input:
- `minLength` / `maxLength` for strings
- `minimum` / `maximum` for numbers
- `enum` for fixed value sets
- `pattern` for regex validation
- `minItems` / `maxItems` for arrays
- `default` for optional parameters with defaults

### Commerce Schema Patterns

**Product search:**
```js
{
  type: "object",
  properties: {
    query: { type: "string", description: "Search keywords" },
    category: { type: "string", enum: ["electronics", "clothing", "home"] },
    maxPrice: { type: "number", minimum: 0 },
    sortBy: { type: "string", enum: ["relevance", "price_asc", "price_desc", "rating"] }
  },
  required: ["query"]
}
```

**Add to cart:**
```js
{
  type: "object",
  properties: {
    productId: { type: "string", description: "Product identifier" },
    quantity: { type: "integer", minimum: 1, maximum: 99, default: 1 },
    variant: { type: "string", description: "Size, color, or variant ID" }
  },
  required: ["productId"]
}
```

**Shipping address:**
```js
{
  type: "object",
  properties: {
    street: { type: "string" },
    city: { type: "string" },
    state: { type: "string" },
    zipCode: { type: "string", pattern: "^[0-9]{5}(-[0-9]{4})?$" },
    country: { type: "string", enum: ["US", "CA", "UK"] }
  },
  required: ["street", "city", "state", "zipCode", "country"]
}
```

### Output Conventions

While WebMCP doesn't formally specify an output schema, tools should return predictable JSON:
- Always include a `status` or `success` field
- Return structured data, not HTML or plain text
- Include pagination info for list results (`total`, `page`, `pageSize`)
- Return error objects with `code` and `message` for failures

### Schema Design Principles

1. **Minimal surface** — Only require parameters the tool actually needs
2. **Descriptive** — Every property should have a `description`
3. **Constrained** — Use `enum`, `minimum`, `maximum` to prevent invalid inputs
4. **Flat when possible** — Avoid deep nesting; agents handle flat schemas better
5. **Consistent** — Use the same naming conventions across all tools (camelCase)
6. **No sensitive data** — Never ask for passwords, SSNs, or full card numbers in schemas

Fetch the WebMCP spec for the exact JSON Schema version supported and any WebMCP-specific constraints before designing schemas.
