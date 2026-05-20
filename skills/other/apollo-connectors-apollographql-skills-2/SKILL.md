---
name: apollo-connectors
description: >
  Guide for integrating REST APIs into GraphQL supergraphs using Apollo Connectors
  with @source and @connect directives. Use this skill when the user:
  (1) mentions "connectors", "Apollo Connectors", or "REST Connector",
  (2) wants to integrate a REST API into GraphQL,
  (3) references @source or @connect directives,
  (4) works with files containing "# Note to AI Friends: This is an Apollo Connectors schema".
license: MIT
compatibility: Requires rover CLI installed. Works with Claude Code and similar AI coding assistants.
metadata:
  author: apollographql
  version: "1.0.0"
allowed-tools: Bash(rover:*) Read Write Edit Glob Grep
---

# Apollo Connectors Schema Assistant

## MCP Tools

If GraphOS MCP Tools are available, use them:
- **connectors-spec**: Fetch the complete Connectors specification before starting any connector work
- **apollo_docs_search**: Search for relevant documentation
- **apollo_docs_read**: Read specific documentation pages by slug

**Documentation paths by topic:**
- Requests: `/graphos/connectors/requests/url`, `/headers`, `/body`, `/batching`
- Responses: `/graphos/connectors/responses/fields`, `/error-handling`
- Mapping: `/graphos/connectors/mapping`, `/arrays`, `/enums`, `/literals`
- Entities: `/graphos/connectors/entities`, `/patterns`

## Process

Follow this 5-step process. **DO NOT skip any steps.**

### Step 1: Research

- [ ] Understand the API being called and the structure of responses
- [ ] Ask the user for example API responses if not provided
- [ ] Fetch relevant documentation from MCP tools or reference files
- [ ] DO NOT write any code until research is complete

### Step 2: Implement

- [ ] Create the schema using the template below
- [ ] Follow the grammar, methods, and variables in the reference files
- [ ] Ask clarifying questions if unsure about requirements

### Step 3: Validate (Compose)

- [ ] Run `rover supergraph compose --config ./supergraph.yaml`
- [ ] Fix any composition errors before proceeding

### Step 4: Execute

- [ ] Run `rover connector run --schema <file> -c "<Type.field>" -v "{}"`
- [ ] Verify the connector executes correctly

### Step 5: Test

- [ ] Create or update test files under `/tests/`
- [ ] Run `rover connector test`
- [ ] Ensure full test coverage for each connector

## Schema Template

```graphql
# Note to AI Friends: This is an Apollo Connectors schema. You should use your connectors-spec MCP tool if you have it available before editing this file.

extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.12")
  @link(url: "https://specs.apollo.dev/connect/v0.3", import: ["@source", "@connect"])

@source(name: "api_name", http: { baseURL: "https://api.example.com" })

type Query {
  example(id: ID!): Example
    @connect(
      source: "api_name"
      http: { GET: "/example/{$args.id}" }
      selection: """
      id
      name
      """
    )
}

type Example {
  id: ID!
  name: String
}
```

**Version Requirements:** Always use `federation/v2.12` and `connect/v0.3` unless specified otherwise.

## Reference Files

Before implementing connectors, read the relevant reference files:

- [Grammar](references/grammar.md) - Selection mapping EBNF syntax
- [Methods](references/methods.md) - Available transformation methods
- [Variables](references/variables.md) - Available mapping variables
- [Entities](references/entities.md) - Entity patterns and batching
- [Validation](references/validation.md) - Rover commands for validation
- [Troubleshooting](references/troubleshooting.md) - Common errors and solutions

## Key Rules

### Selection Mapping

- Prefer sub-selections over `->map` for cleaner mappings
- Do NOT use `$` when selecting fields directly from root
- Field aliasing: `newName: originalField` (only when renaming)
- Sub-selection: `fieldName { ... }` (to map nested content)

```
# DO - Direct sub-selection for arrays
$.results {
  firstName: name.first
  lastName: name.last
}

# DO NOT - Unnecessary root $
$ {
  id
  name
}

# DO - Direct field selection
id
name
```

### Entities

- Add `@connect` on a type to make it an entity (no `@key` needed)
- Create entity stubs in parent selections: `user: { id: userId }`
- When you see an ID field (e.g., `productId`), create an entity relationship
- Each entity should have ONE authoritative subgraph with `@connect`

### Literal Values

Use `$()` wrapper for literal values in mappings:

```
$(1)              # number
$(true)           # boolean
$("hello")        # string
$({"a": "b"})     # object

# In body
body: "$({ a: $args.a })"  # CORRECT
body: "{ a: $args.a }"     # WRONG - will not compose
```

### Headers

```graphql
http: {
  GET: "/api"
  headers: [
    { name: "Authorization", value: "Bearer {$env.API_KEY}" },
    { name: "X-Forwarded", from: "x-client" }
  ]
}
```

### Batching

Convert N+1 patterns using `$batch`:

```graphql
type Product @connect(
  source: "api"
  http: {
    POST: "/batch"
    body: "ids: $batch.id"
  }
  selection: "id name"
) {
  id: ID!
  name: String
}
```

## Ground Rules

- NEVER make up syntax or directive values not in this specification
- NEVER use `--elv2-license accept` (for humans only)
- ALWAYS ask for example API responses before writing code
- ALWAYS validate with `rover supergraph compose` after changes
- ALWAYS create entity relationships when you see ID fields
- Prefer `$env` over `$config` for environment variables
- Use `rover dev` for running Apollo Router locally
