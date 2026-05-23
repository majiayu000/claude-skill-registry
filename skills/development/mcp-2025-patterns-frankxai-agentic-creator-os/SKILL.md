---
name: mcp-2025-patterns
description: Current best practices for Model Context Protocol server design, implementation, and integration. Updated patterns for 2025 MCP ecosystem including multi-server orchestration, security, and performance.
version: 1.0.0
last_updated: 2025-12-19
external_version: "MCP Specification 2025"
changelog: |
  - 1.0.0: Initial skill with 2025 MCP patterns and best practices
---

# MCP 2025 Patterns

This skill covers current best practices for Model Context Protocol (MCP) server design, implementation, and integration as of late 2025.

---

## MCP Architecture Fundamentals

### Core Concepts
```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code (Host)                        │
├─────────────────────────────────────────────────────────────┤
│  MCP Client Layer                                           │
│  ├── Server Discovery & Connection                          │
│  ├── Tool Registration & Invocation                         │
│  ├── Resource Management                                    │
│  └── Prompt Templates                                       │
├─────────────────────────────────────────────────────────────┤
│  MCP Servers (Multiple)                                     │
│  ├── github-mcp (repositories, issues, PRs)                 │
│  ├── notion-mcp (pages, databases, blocks)                  │
│  ├── linear-mcp (issues, projects, cycles)                  │
│  ├── custom-mcp (your domain-specific tools)                │
│  └── ...                                                    │
└─────────────────────────────────────────────────────────────┘
```

### MCP Server Components

1. **Tools**: Functions the AI can invoke
2. **Resources**: Data the AI can read
3. **Prompts**: Template prompts for common tasks
4. **Notifications**: Server-to-client events

---

## Server Design Patterns

### Pattern 1: Single Responsibility Server
```typescript
// Good: Focused server for one domain
const server = new MCPServer({
  name: "github-mcp",
  version: "1.0.0"
});

// Tools all relate to GitHub
server.addTool("create_issue", createIssueHandler);
server.addTool("list_pulls", listPullsHandler);
server.addTool("merge_pr", mergePRHandler);
```

### Pattern 2: Resource-First Design
```typescript
// Define resources before tools
server.addResource({
  uri: "github://repos/{owner}/{repo}",
  name: "Repository",
  description: "GitHub repository data and metadata",
  mimeType: "application/json"
});

// Tools operate on resources
server.addTool({
  name: "get_repo",
  description: "Fetch repository details",
  inputSchema: {
    type: "object",
    properties: {
      owner: { type: "string" },
      repo: { type: "string" }
    },
    required: ["owner", "repo"]
  }
});
```

### Pattern 3: Hierarchical Tool Organization
```typescript
// Organize tools by domain/action
const tools = {
  // Issues domain
  "issues_create": createIssue,
  "issues_update": updateIssue,
  "issues_list": listIssues,
  "issues_close": closeIssue,

  // PRs domain
  "pulls_create": createPR,
  "pulls_merge": mergePR,
  "pulls_review": reviewPR,

  // Repos domain
  "repos_list": listRepos,
  "repos_create": createRepo
};
```

---

## Tool Design Best Practices

### Clear, Action-Oriented Names
```typescript
// Good: Clear action + noun
"create_issue"
"list_repositories"
"merge_pull_request"
"search_code"

// Bad: Vague or ambiguous
"do_github"
"handle_request"
"process_data"
```

### Comprehensive Input Schemas
```typescript
server.addTool({
  name: "create_issue",
  description: "Create a new GitHub issue with title, body, labels, and assignees",
  inputSchema: {
    type: "object",
    properties: {
      owner: {
        type: "string",
        description: "Repository owner (user or org)"
      },
      repo: {
        type: "string",
        description: "Repository name"
      },
      title: {
        type: "string",
        description: "Issue title",
        minLength: 1,
        maxLength: 256
      },
      body: {
        type: "string",
        description: "Issue body (Markdown supported)"
      },
      labels: {
        type: "array",
        items: { type: "string" },
        description: "Labels to apply"
      },
      assignees: {
        type: "array",
        items: { type: "string" },
        description: "GitHub usernames to assign"
      }
    },
    required: ["owner", "repo", "title"]
  }
});
```

### Structured Output Formats
```typescript
// Return structured, predictable data
async function createIssue(params) {
  const issue = await github.issues.create({...});

  return {
    success: true,
    issue: {
      number: issue.number,
      url: issue.html_url,
      title: issue.title,
      state: issue.state,
      created_at: issue.created_at
    },
    // Include actionable next steps
    suggested_actions: [
      `Add labels: /api/issues/${issue.number}/labels`,
      `Assign team: /api/issues/${issue.number}/assignees`
    ]
  };
}
```

---

## Security Patterns

### Pattern 1: Credential Isolation
```typescript
// Store credentials in environment, not code
const server = new MCPServer({
  name: "secure-server"
});

// Validate env vars at startup
const requiredEnv = ["API_KEY", "API_SECRET"];
for (const key of requiredEnv) {
  if (!process.env[key]) {
    throw new Error(`Missing required env var: ${key}`);
  }
}

// Never log or expose credentials
server.addTool("secure_action", async (params) => {
  // Use env vars directly, never pass as params
  const client = new APIClient({
    key: process.env.API_KEY // Not from params
  });
});
```

### Pattern 2: Input Validation
```typescript
import { z } from "zod";

const CreateIssueSchema = z.object({
  owner: z.string().regex(/^[a-zA-Z0-9-]+$/),
  repo: z.string().regex(/^[a-zA-Z0-9._-]+$/),
  title: z.string().min(1).max(256),
  body: z.string().max(65536).optional()
});

server.addTool("create_issue", async (params) => {
  // Validate before processing
  const validated = CreateIssueSchema.parse(params);

  // Safe to use validated data
  return await github.issues.create(validated);
});
```

### Pattern 3: Rate Limiting
```typescript
import { RateLimiter } from "rate-limiter";

const limiter = new RateLimiter({
  tokensPerInterval: 100,
  interval: "minute"
});

server.addTool("api_call", async (params) => {
  // Check rate limit before proceeding
  if (!await limiter.tryRemoveTokens(1)) {
    return {
      success: false,
      error: "Rate limit exceeded. Try again in a minute.",
      retry_after: 60
    };
  }

  return await performAPICall(params);
});
```

### Pattern 4: Audit Logging
```typescript
server.addTool("sensitive_action", async (params, context) => {
  // Log all sensitive operations
  await auditLog({
    action: "sensitive_action",
    params: sanitize(params), // Remove secrets
    user: context.user,
    timestamp: new Date().toISOString(),
    result: "pending"
  });

  try {
    const result = await performAction(params);
    await auditLog.update({ result: "success" });
    return result;
  } catch (error) {
    await auditLog.update({ result: "error", error: error.message });
    throw error;
  }
});
```

---

## Multi-Server Orchestration

### Pattern 1: Server Composition
```typescript
// In Claude Code settings, compose servers:
{
  "mcpServers": {
    "github": {
      "command": "mcp-github",
      "env": { "GITHUB_TOKEN": "..." }
    },
    "linear": {
      "command": "mcp-linear",
      "env": { "LINEAR_API_KEY": "..." }
    },
    "notion": {
      "command": "mcp-notion",
      "env": { "NOTION_TOKEN": "..." }
    }
  }
}
```

### Pattern 2: Cross-Server Workflows
```markdown
When handling complex tasks, coordinate across servers:

1. Get issue from GitHub (github-mcp)
2. Create linked Linear ticket (linear-mcp)
3. Update project doc in Notion (notion-mcp)
4. Comment back on GitHub with links (github-mcp)

Claude orchestrates automatically based on task.
```

### Pattern 3: Server Health Monitoring
```typescript
// Each server should expose health endpoint
server.addTool("health_check", async () => {
  const checks = await Promise.all([
    checkAPIConnection(),
    checkDatabaseConnection(),
    checkCacheConnection()
  ]);

  return {
    status: checks.every(c => c.ok) ? "healthy" : "degraded",
    checks: checks,
    timestamp: new Date().toISOString()
  };
});
```

---

## Performance Patterns

### Pattern 1: Connection Pooling
```typescript
// Reuse connections across requests
const pool = new ConnectionPool({
  max: 10,
  idleTimeout: 30000
});

server.addTool("db_query", async (params) => {
  const conn = await pool.acquire();
  try {
    return await conn.query(params.sql);
  } finally {
    pool.release(conn);
  }
});
```

### Pattern 2: Caching
```typescript
import { LRUCache } from "lru-cache";

const cache = new LRUCache({
  max: 1000,
  ttl: 1000 * 60 * 5 // 5 minutes
});

server.addTool("get_user", async (params) => {
  const cacheKey = `user:${params.id}`;

  // Check cache first
  const cached = cache.get(cacheKey);
  if (cached) return cached;

  // Fetch and cache
  const user = await fetchUser(params.id);
  cache.set(cacheKey, user);
  return user;
});
```

### Pattern 3: Batch Operations
```typescript
// Support batch operations to reduce round trips
server.addTool("batch_create_issues", async (params) => {
  const { issues } = params;

  // Process in parallel with concurrency limit
  const results = await pMap(
    issues,
    issue => createIssue(issue),
    { concurrency: 5 }
  );

  return {
    created: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length,
    results
  };
});
```

---

## Error Handling

### Structured Error Responses
```typescript
class MCPError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.code = code;
    this.details = details;
  }

  toResponse() {
    return {
      success: false,
      error: {
        code: this.code,
        message: this.message,
        details: this.details,
        recoverable: this.isRecoverable(),
        suggested_action: this.getSuggestedAction()
      }
    };
  }
}

// Usage
throw new MCPError(
  "RATE_LIMITED",
  "GitHub API rate limit exceeded",
  {
    limit: 5000,
    remaining: 0,
    reset_at: "2025-12-19T12:00:00Z"
  }
);
```

### Graceful Degradation
```typescript
server.addTool("enriched_search", async (params) => {
  const results = await primarySearch(params);

  // Try to enrich, but don't fail if enrichment fails
  try {
    return await enrichResults(results);
  } catch (enrichError) {
    console.warn("Enrichment failed, returning basic results", enrichError);
    return {
      ...results,
      enrichment_status: "failed",
      enrichment_error: enrichError.message
    };
  }
});
```

---

## Testing Patterns

### Unit Testing Tools
```typescript
import { describe, it, expect, vi } from "vitest";

describe("create_issue tool", () => {
  it("creates issue with valid params", async () => {
    const mockGithub = vi.fn().mockResolvedValue({
      number: 123,
      html_url: "https://github.com/..."
    });

    const result = await createIssueTool({
      owner: "test",
      repo: "test-repo",
      title: "Test issue"
    }, { github: mockGithub });

    expect(result.success).toBe(true);
    expect(result.issue.number).toBe(123);
  });

  it("validates required params", async () => {
    await expect(createIssueTool({ owner: "test" }))
      .rejects.toThrow("Missing required: repo, title");
  });
});
```

### Integration Testing
```typescript
describe("MCP Server Integration", () => {
  let server;
  let client;

  beforeAll(async () => {
    server = await startMCPServer();
    client = await connectMCPClient(server.url);
  });

  it("lists available tools", async () => {
    const tools = await client.listTools();
    expect(tools).toContain("create_issue");
    expect(tools).toContain("list_repositories");
  });

  it("executes tool and returns result", async () => {
    const result = await client.callTool("health_check", {});
    expect(result.status).toBe("healthy");
  });
});
```

---

## FrankX System Integration

### Current MCP Servers in Use
- **github-mcp**: Repository management, issues, PRs
- **linear-mcp**: Project management, issues, cycles
- **notion-mcp**: Documentation, databases, pages
- **nano-banana-mcp**: Image generation
- **n8n-mcp**: Workflow automation
- **playwright-mcp**: Browser automation

### Best Practices for FrankX
1. **Server per domain**: Keep MCPs focused (GitHub for code, Linear for tasks)
2. **Consistent naming**: `mcp__<server>__<action>` format
3. **Graceful fallbacks**: If MCP unavailable, suggest alternative
4. **Context awareness**: Use right MCP for right task automatically

---

*MCP servers extend Claude's capabilities with real-world integrations. Design them with clear responsibility, robust error handling, and security in mind.*
