---
name: mcp-tool-design
description: >
  Best practices for designing MCP tools including naming conventions, input schemas,
  error responses, pagination, idempotency, and descriptions. Use when the user is
  designing tools for an MCP server, writing tool schemas, handling tool errors,
  or needs guidance on tool naming and input validation patterns.
---

# MCP Tool Design

Best practices for designing well-structured, reliable MCP tools. Covers naming,
schemas, error handling, pagination, idempotency, and effective descriptions.

## When to Use
- User is designing new tools for an MCP server
- User is writing JSON Schema for tool inputs
- User needs pagination or idempotency patterns
- User wants guidance on tool naming or descriptions
- User is handling errors in MCP tool responses

## Core Patterns

### Naming Conventions

Use snake_case, verb-first names. Group related tools with a common prefix.

```typescript
// Good: verb_noun pattern, clear scope
server.tool("search_issues", ...);
server.tool("create_issue", ...);
server.tool("update_issue", ...);
server.tool("list_repositories", ...);
server.tool("get_file_contents", ...);

// Bad: inconsistent, vague, or noun-first
server.tool("issues", ...);          // What action?
server.tool("doSearch", ...);        // camelCase
server.tool("repository-list", ...); // kebab-case, noun-first
```

### Writing Effective Descriptions

Descriptions tell Claude WHEN and WHY to use the tool. Be specific and directive.

```typescript
// Good: explains purpose, trigger conditions, and constraints
server.tool(
  "search_codebase",
  "Search for code patterns across the repository using regex. " +
  "Use this when the user asks to find functions, classes, imports, " +
  "or specific code patterns. Supports file type filtering. " +
  "Returns up to 50 matches per call -- use pagination for more.",
  schema,
  handler
);

// Bad: vague, tells Claude nothing useful
server.tool(
  "search",
  "Searches for things.",
  schema,
  handler
);
```

### Input Schema Design

Use JSON Schema with descriptive property names, descriptions, and constraints.

```typescript
import { z } from "zod";

server.tool(
  "search_issues",
  "Search GitHub issues by query, state, and labels.",
  {
    query: z.string()
      .describe("Search query string. Searches title and body text."),
    state: z.enum(["open", "closed", "all"])
      .default("open")
      .describe("Filter by issue state. Default: open."),
    labels: z.array(z.string())
      .optional()
      .describe("Filter by label names. Returns issues matching ALL labels."),
    limit: z.number()
      .int()
      .min(1)
      .max(100)
      .default(20)
      .describe("Maximum results to return. Range: 1-100. Default: 20."),
    cursor: z.string()
      .optional()
      .describe("Pagination cursor from a previous response.")
  },
  handler
);
```

### Error Response Patterns

Return structured errors with the `isError` flag so Claude can reason and recover.

```typescript
server.tool("get_file", "Read a file by path.", { path: z.string() }, async ({ path }) => {
  // Validate input
  if (path.includes("..")) {
    return {
      isError: true,
      content: [{ type: "text", text: "Path traversal not allowed. Use absolute paths within the project." }]
    };
  }

  try {
    const content = await fs.readFile(path, "utf-8");
    return {
      content: [{ type: "text", text: content }]
    };
  } catch (error) {
    if (error.code === "ENOENT") {
      return {
        isError: true,
        content: [{ type: "text", text: `File not found: ${path}. Check the path and try again.` }]
      };
    }
    return {
      isError: true,
      content: [{ type: "text", text: `Failed to read file: ${error.message}` }]
    };
  }
});
```

### Pagination Pattern

Use cursor-based pagination for tools that return large result sets.

```typescript
server.tool(
  "list_commits",
  "List commits for a repository branch. Returns 20 commits per page with a cursor for pagination.",
  {
    repo: z.string().describe("Repository name in owner/repo format."),
    branch: z.string().default("main").describe("Branch name. Default: main."),
    cursor: z.string().optional().describe("Pagination cursor from previous response.")
  },
  async ({ repo, branch, cursor }) => {
    const page = cursor ? decodeCursor(cursor) : 1;
    const commits = await fetchCommits(repo, branch, page, 20);
    const hasMore = commits.length === 20;

    const result = {
      commits: commits.map(c => ({
        sha: c.sha,
        message: c.message,
        author: c.author,
        date: c.date
      })),
      next_cursor: hasMore ? encodeCursor(page + 1) : null,
      has_more: hasMore
    };

    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
    };
  }
);
```

### Idempotency Pattern

Design tools so repeated calls with the same input produce the same result.

```typescript
server.tool(
  "set_config",
  "Set a configuration value. Idempotent -- calling with the same key and value multiple times has no additional effect.",
  {
    key: z.string().describe("Configuration key."),
    value: z.string().describe("Configuration value.")
  },
  async ({ key, value }) => {
    const current = await getConfig(key);
    if (current === value) {
      return {
        content: [{ type: "text", text: `Config "${key}" already set to "${value}". No change needed.` }]
      };
    }

    await setConfig(key, value);
    return {
      content: [{ type: "text", text: `Config "${key}" set to "${value}".` }]
    };
  }
);
```

## Anti-Patterns
- Tool names longer than 64 characters (may be truncated or rejected)
- Missing `required` array in raw JSON Schema (Claude may skip required fields)
- Descriptions that say "This tool does X" instead of "Use this when..."
- Returning HTML or binary data as text content (use appropriate MIME types)
- Tools with more than 10-15 parameters (split into multiple focused tools)
- Not including pagination for tools that can return unbounded results
- Destructive tools without confirmation (delete, drop, reset)
- Using generic error messages like "Something went wrong" without actionable guidance

## Quick Reference

| Aspect | Guideline |
|--------|-----------|
| Name format | `snake_case`, verb_noun, max 64 chars |
| Description | Explain WHEN to use, not just what it does |
| Parameters | Include type, description, defaults, constraints |
| Required fields | Always specify in schema |
| Pagination | Cursor-based, 20-50 items per page |
| Errors | Use `isError: true`, give actionable messages |
| Idempotency | Same input = same result for write operations |
| Tool count | Prefer many focused tools over few large ones |

Description template:
```
"[Action description]. Use when [trigger conditions]. [Constraints/limits]. [Returns description]."
```
