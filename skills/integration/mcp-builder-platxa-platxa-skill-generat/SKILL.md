---
name: mcp-builder
description: >-
  Guide for building production-quality MCP (Model Context Protocol) servers
  that connect LLMs to external APIs and services. Covers the full lifecycle
  from protocol research through implementation, testing, and evaluation.
  Supports both TypeScript (MCP SDK with Zod) and Python (FastMCP with
  Pydantic). Use when creating a new MCP server or improving an existing one.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Task
  - AskUserQuestion
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - guide
    - mcp
    - api-integration
    - typescript
    - python
  provenance:
    upstream_source: "mcp-builder"
    upstream_sha: "16447833d14a897d97233d30accfd295e40a28e9"
    regenerated_at: "2026-02-04T19:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# MCP Server Development Guide

Build MCP servers that give LLMs reliable access to external APIs through well-designed tools, resources, and structured outputs.

## Overview

An MCP (Model Context Protocol) server exposes tools, resources, and prompts over a standardized transport so any compatible LLM client can call them. Quality is measured by how effectively an LLM with no prior context can use your server to complete real tasks.

**What you will learn:**

- MCP protocol architecture: tools, resources, transports, annotations
- Designing tool schemas that LLMs can discover and call correctly
- Implementing servers in TypeScript (MCP SDK + Zod) or Python (FastMCP + Pydantic)
- Testing with MCP Inspector and writing evaluation harnesses

**Prerequisites:**

- Familiarity with the target API you plan to integrate
- Node.js >= 18 (TypeScript) or Python >= 3.10 (Python)
- Basic understanding of async/await patterns

## Learning Path

### Level 1: Protocol Fundamentals

**Concept**: MCP defines a JSON-RPC 2.0 protocol between clients (LLMs) and servers (your code). Servers declare capabilities: tools (functions the LLM can call), resources (data the LLM can read), and prompts (reusable templates).

**Key protocol pages** (fetch with `.md` suffix for markdown):

```
https://modelcontextprotocol.io/specification/draft.md
https://modelcontextprotocol.io/sitemap.xml
```

**Transport selection:**

| Criterion     | stdio               | Streamable HTTP       |
|---------------|----------------------|-----------------------|
| Deployment    | Local subprocess     | Remote web service    |
| Clients       | Single               | Multiple concurrent   |
| Session model | One process per user | Stateless per request |
| Use when      | CLI tools, desktop   | Cloud, multi-tenant   |

stdio servers must never write to stdout (use stderr for logging). Avoid SSE transport -- it is deprecated in favour of streamable HTTP.

**Tool design principles:**

- Prefix tool names with the service: `github_create_issue`, not `create_issue`
- Use snake_case: `search_users`, `get_channel_info`
- Write descriptions that match actual behaviour -- LLMs rely on them for selection
- Annotate every tool: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`
- Return actionable errors: tell the LLM what to try next, not just what failed

**Practice**: Fetch the MCP specification overview and identify the three capability types and two transport mechanisms.

### Level 2: Implementation

**Concept**: Pick a language, scaffold the project, implement tools with validated inputs and structured outputs.

**Naming conventions:**

- Python servers: `{service}_mcp` (e.g. `slack_mcp`)
- TypeScript servers: `{service}-mcp-server` (e.g. `slack-mcp-server`)

**TypeScript quick start** (see `references/typescript-implementation.md` for full guide):

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({ name: "acme-mcp-server", version: "1.0.0" });

const SearchInput = z.object({
  query: z.string().min(1).describe("Search term"),
  limit: z.number().int().min(1).max(100).default(20),
}).strict();

server.registerTool("acme_search", {
  title: "Search Acme",
  description: "Search Acme records by keyword. Returns matching items with IDs.",
  inputSchema: SearchInput,
  annotations: { readOnlyHint: true, destructiveHint: false,
                 idempotentHint: true, openWorldHint: true },
}, async ({ query, limit }) => {
  const data = await acmeApi.search(query, limit);
  return {
    content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    structuredContent: data,
  };
});
```

Use `registerTool`, `registerResource`, `registerPrompt` -- not the deprecated `server.tool()` API.

**Python quick start** (see `references/python-implementation.md` for full guide):

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("acme_mcp")

class SearchInput(BaseModel):
    query: str = Field(..., min_length=1, description="Search term")
    limit: int = Field(default=20, ge=1, le=100)

@mcp.tool(name="acme_search", annotations={
    "readOnlyHint": True, "destructiveHint": False,
    "idempotentHint": True, "openWorldHint": True,
})
async def acme_search(params: SearchInput) -> str:
    """Search Acme records by keyword. Returns matching items with IDs."""
    data = await acme_api.search(params.query, params.limit)
    return json.dumps(data, indent=2)
```

**Shared infrastructure patterns:**

1. Centralise API client and auth in a single module
2. Create a reusable error handler that maps HTTP status codes to actionable messages
3. Implement pagination helpers returning `has_more`, `next_offset`, `total_count`
4. Support both markdown (default) and JSON response formats via a `response_format` parameter
5. Add a `CHARACTER_LIMIT` constant (e.g. 25000) and truncate oversized responses with a message

**Practice**: Scaffold a project for your target API, register one read-only tool, and verify it compiles.

### Level 3: Testing and Evaluation

**Concept**: Verify your server works mechanically (build, lint, type-check) then measure how well an LLM can actually use it to answer hard questions.

**Mechanical checks:**

```bash
# TypeScript
npm run build            # must succeed
npx @modelcontextprotocol/inspector   # interactive tool testing

# Python
python -m py_compile your_server.py
# Use MCP Inspector for interactive testing
```

**Evaluation harness** (see `references/evaluation-guide.md` for full details):

Write 10 questions that require multiple tool calls, cover read-only operations, and have stable single-value answers verifiable by string comparison.

```xml
<evaluation>
  <qa_pair>
    <question>Find the repository archived in Q3 2023 that previously had the most
    forks. What was its primary language?</question>
    <answer>Python</answer>
  </qa_pair>
</evaluation>
```

Run the harness:

```bash
python scripts/evaluation.py \
  -t stdio -c node -a dist/index.js \
  -e API_KEY=xxx \
  evaluation.xml
```

Review accuracy, per-question feedback, and tool call counts to identify where tool descriptions or schemas need improvement.

**Practice**: Write three evaluation questions for your server and verify their answers manually.

## Best Practices

### Do

- Fetch the MCP spec and SDK README at the start of every project
- Use Zod `.strict()` (TypeScript) or Pydantic `extra='forbid'` (Python) to reject unknown fields
- Define `outputSchema` and return `structuredContent` alongside `text` content
- Register resources for static or template-based data access (URI templates)
- Use context injection (`ctx` in FastMCP) for progress reporting and logging
- Use lifespan management for persistent database connections or config
- Bind local streamable HTTP servers to `127.0.0.1`, validate `Origin` headers

### Avoid

- Deprecated APIs: `server.tool()`, `server.setRequestHandler(ListToolsRequestSchema, ...)`
- Generic tool names without service prefix (`send_message` instead of `slack_send_message`)
- Exposing internal errors -- return helpful messages, log details to stderr
- Loading all results into memory -- always paginate and respect `limit`
- Using `any` (TypeScript) or skipping type hints (Python)
- SSE transport (deprecated; use streamable HTTP for remote servers)

## Common Questions

### Q: When should I choose TypeScript over Python?

**A**: TypeScript has broader SDK support, better compatibility with execution environments like MCPB, and static typing that catches schema mismatches at compile time. Choose Python when the target API has a dominant Python client library or your team is Python-first.

### Q: How do I handle authentication?

**A**: Store API keys in environment variables, validate on server startup, and fail fast with a clear error if missing. For OAuth 2.1 flows, validate access tokens before processing each request and only accept tokens intended for your server.

### Q: Tools or Resources -- which should I use?

**A**: Use tools for operations with complex parameters, validation logic, or side effects. Use resources for data access via simple URI templates (`file://docs/{name}`). Resources are cheaper to call and better for static or semi-static content.

### Q: My tool returns too much data and the LLM loses context. What do I do?

**A**: Add a `CHARACTER_LIMIT` constant, truncate with a message suggesting filters or pagination. Support a `limit` parameter on every listing tool. Consider a `response_format` parameter so the LLM can request compact JSON instead of verbose markdown.

## Examples

### Example 1: Build an MCP Server for a REST API

```
User: Build an MCP server for the Acme project management API
Assistant:
  1. Fetches MCP spec overview and SDK README
  2. Reviews Acme API docs (endpoints, auth, data models)
  3. Scaffolds acme-mcp-server/ with package.json, tsconfig.json, src/
  4. Implements shared API client with auth and error handling
  5. Registers tools: acme_list_projects, acme_get_project, acme_search_tasks,
     acme_create_task, acme_update_task
  6. Adds annotations, Zod schemas with .strict(), pagination
  7. Runs npm run build, tests with MCP Inspector
  8. Writes 10 evaluation questions, runs harness, iterates on descriptions
```

### Example 2: Add a New Tool to an Existing Server

```
User: Add a tool to search issues by label and date range
Assistant:
  1. Reads existing server code to understand patterns
  2. Defines Zod/Pydantic schema with label, start_date, end_date, limit
  3. Implements acme_search_issues with pagination and both response formats
  4. Sets annotations (readOnlyHint: true, idempotentHint: true)
  5. Rebuilds, tests the new tool with MCP Inspector
  6. Adds an evaluation question exercising the date range filter
```

## Quality Checklist

When your MCP server is complete, verify:

- [ ] Server name follows convention (`{service}_mcp` or `{service}-mcp-server`)
- [ ] All tools have service-prefixed snake_case names
- [ ] All tools have `title`, `description`, `inputSchema`, and `annotations`
- [ ] Input schemas use Zod `.strict()` or Pydantic `extra='forbid'`
- [ ] Descriptions document parameters, return schema, error cases, and usage examples
- [ ] Error messages are actionable with suggested next steps
- [ ] Pagination implemented with `limit`, `offset`, `has_more`, `total_count`
- [ ] Large responses truncated at `CHARACTER_LIMIT` with guidance
- [ ] No duplicated code -- API client, error handler, and formatters are shared
- [ ] Build succeeds (`npm run build` or `python -m py_compile`)
- [ ] At least 10 evaluation questions written and verified

## References

Load these on demand when deeper implementation detail is needed:

- **MCP best practices**: `references/mcp-best-practices.md` -- naming, pagination, transport, security, annotations
- **TypeScript guide**: `references/typescript-implementation.md` -- project setup, Zod schemas, registerTool patterns, complete example
- **Python guide**: `references/python-implementation.md` -- FastMCP setup, Pydantic models, context injection, complete example
- **Evaluation guide**: `references/evaluation-guide.md` -- question design, harness usage, output format
