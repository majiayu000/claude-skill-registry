---
name: mcp-development
description: Guide for creating MCP (Model Context Protocol) servers that enable LLMs to interact with external services. Use when building MCP servers, integrating external APIs, implementing tool servers, or creating agent capabilities. Covers TypeScript/Python patterns, tool design, and evaluation creation.
---

# MCP Server Development

Create MCP servers that enable LLMs to interact with external services through well-designed tools.

## Development Phases

### Phase 1: Research & Planning

**Understand the API:**
- Review service's API documentation
- Identify key endpoints, auth requirements, data models
- Use Context7 or Firecrawl as needed

**Tool Selection:**
- Prioritize comprehensive API coverage over workflow shortcuts
- List endpoints to implement, starting with most common operations
- Balance single-operation tools (flexible) vs workflow tools (convenient)

**Load Framework Docs:**
- TypeScript SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- Python SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

### Phase 2: Implementation

**Recommended Stack:**
- **Language**: TypeScript (best SDK support, good for agent-generated code)
- **Transport**: Streamable HTTP for remote, stdio for local

**Project Structure (TypeScript):**
```
my-mcp-server/
├── src/
│   ├── index.ts          # Server entry point
│   ├── tools/            # Tool implementations
│   └── utils/            # Shared utilities
├── package.json
└── tsconfig.json
```

**Tool Implementation Pattern:**
```typescript
server.registerTool({
  name: "service_operation",
  description: "Concise description of what this does",
  inputSchema: z.object({
    param: z.string().describe("What this parameter is for"),
    optional: z.number().optional().describe("Optional config"),
  }),
  outputSchema: z.object({
    result: z.string(),
    metadata: z.object({ count: z.number() }),
  }),
  annotations: {
    readOnlyHint: true,      // Doesn't modify state
    destructiveHint: false,  // Doesn't delete data
    idempotentHint: true,    // Safe to retry
    openWorldHint: false,    // Bounded result set
  },
  async execute({ param, optional }) {
    // Implementation with proper error handling
    const result = await apiClient.doOperation(param);
    return {
      structuredContent: { result: result.data, metadata: { count: 1 } },
      content: [{ type: "text", text: `Operation completed: ${result.data}` }],
    };
  },
});
```

### Phase 3: Review & Test

**Code Quality:**
- No duplicated code (DRY principle)
- Consistent error handling with actionable messages
- Full type coverage
- Clear tool descriptions

**Testing:**
```bash
# TypeScript - verify compilation
npm run build

# Test with MCP Inspector
npx @modelcontextprotocol/inspector

# Python - verify syntax
python -m py_compile your_server.py
```

### Phase 4: Evaluations

Create 10 evaluation questions to test effectiveness:

**Question Requirements:**
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations
- **Complex**: Require multiple tool calls
- **Realistic**: Based on real use cases
- **Verifiable**: Single, clear answer
- **Stable**: Answer won't change over time

**Format:**
```xml
<evaluation>
  <qa_pair>
    <question>Find all repositories with more than 100 stars 
    that were created this year. What is the total star count?</question>
    <answer>1547</answer>
  </qa_pair>
</evaluation>
```

## Tool Design Best Practices

### Naming Convention

Use consistent prefixes with action-oriented names:
```
✅ github_create_issue, github_list_repos, github_get_user
✅ slack_send_message, slack_list_channels
❌ createIssue, listRepos (inconsistent)
❌ issue, repos (not action-oriented)
```

### Descriptions

```typescript
// ❌ Too vague
description: "Gets data from the API"

// ✅ Specific and helpful
description: "Retrieves repository metadata including stars, forks, and last commit date. Returns structured data for analysis."
```

### Error Messages

Guide agents toward solutions:
```typescript
// ❌ Generic error
throw new Error("Request failed");

// ✅ Actionable error
throw new Error(
  "Repository not found. Verify the owner/repo format (e.g., 'anthropics/sdk'). " +
  "Use github_search_repos to find the correct repository name."
);
```

### Pagination

Support filtering and pagination for list operations:
```typescript
inputSchema: z.object({
  query: z.string().optional().describe("Filter results"),
  limit: z.number().default(20).describe("Max results to return"),
  cursor: z.string().optional().describe("Pagination cursor from previous response"),
}),
```

### Output Schemas

Define structured output for better agent understanding:
```typescript
outputSchema: z.object({
  items: z.array(z.object({
    id: z.string(),
    name: z.string(),
    metadata: z.record(z.unknown()),
  })),
  nextCursor: z.string().optional(),
  totalCount: z.number(),
}),
```

## Tool Annotations Reference

| Annotation | Description | Example |
|------------|-------------|---------|
| `readOnlyHint` | Tool doesn't modify external state | List operations, queries |
| `destructiveHint` | Tool permanently deletes data | Delete operations |
| `idempotentHint` | Multiple calls produce same result | Get by ID, upsert |
| `openWorldHint` | Results may change between calls | Real-time data feeds |

## Common Patterns

### API Client Setup
```typescript
const client = {
  baseUrl: process.env.API_URL,
  headers: { Authorization: `Bearer ${process.env.API_KEY}` },
  
  async request<T>(path: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers: { ...this.headers, ...options?.headers },
    });
    if (!response.ok) {
      throw new Error(`API error: ${response.status} - ${await response.text()}`);
    }
    return response.json();
  },
};
```

### Batch Operations
```typescript
// Allow operating on multiple items efficiently
inputSchema: z.object({
  ids: z.array(z.string()).max(100).describe("IDs to process (max 100)"),
}),
```

### Dry Run Support
```typescript
inputSchema: z.object({
  changes: z.array(ChangeSchema),
  dryRun: z.boolean().default(false).describe("Preview changes without applying"),
}),
```
