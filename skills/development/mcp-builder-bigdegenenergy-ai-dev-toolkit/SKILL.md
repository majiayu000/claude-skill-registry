---
name: mcp-builder
description: Guide for building Model Context Protocol (MCP) servers - tool definitions, resource handling, transport protocols, and testing. Auto-triggers when working with MCP.
---

# MCP Builder Skill

## MCP Architecture

### Core Concepts

| Concept       | Description                                    |
| ------------- | ---------------------------------------------- |
| **Server**    | Exposes tools and resources to AI clients      |
| **Tool**      | A function the AI can call (with input schema) |
| **Resource**  | Read-only data the AI can access (files, URLs) |
| **Prompt**    | Reusable prompt templates                      |
| **Transport** | Communication layer (stdio or SSE)             |

### Transport Protocols

| Transport | Use Case                     | Pros                 | Cons               |
| --------- | ---------------------------- | -------------------- | ------------------ |
| **stdio** | Local CLI tools, Claude Code | Simple, fast, secure | Local only         |
| **SSE**   | Remote/web servers           | Network accessible   | More complex setup |

## Building a Python MCP Server

### Project Setup

```bash
uv init my-mcp-server
cd my-mcp-server
uv add mcp
```

### Minimal Server

```python
# server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_docs(query: str, limit: int = 5) -> str:
    """Search documentation by keyword.

    Args:
        query: Search query string
        limit: Maximum results to return
    """
    results = do_search(query, limit)
    return "\n".join(f"- {r.title}: {r.snippet}" for r in results)

@mcp.resource("docs://{topic}")
def get_doc(topic: str) -> str:
    """Get documentation for a specific topic."""
    return load_doc(topic)

@mcp.prompt()
def summarize_prompt(content: str) -> str:
    """Create a summarization prompt."""
    return f"Summarize the following content:\n\n{content}"

if __name__ == "__main__":
    mcp.run()
```

### Tool Design Best Practices

```python
# GOOD: Clear name, typed params, docstring with Args
@mcp.tool()
def get_user_orders(
    user_id: str,
    status: str = "all",
    limit: int = 10,
) -> str:
    """Fetch orders for a specific user.

    Args:
        user_id: The user's unique identifier
        status: Filter by order status (all, pending, shipped, delivered)
        limit: Maximum number of orders to return (1-100)
    """
    ...

# BAD: Vague name, no types, no docs
@mcp.tool()
def get_data(params):
    ...
```

### Tool Patterns

| Pattern                  | When to Use                                        |
| ------------------------ | -------------------------------------------------- |
| Single-purpose tools     | Always preferred - one tool, one job               |
| Typed parameters         | Always - gives the AI clear input schema           |
| Descriptive docstrings   | Always - AI reads these to understand tool purpose |
| String return values     | Default - return formatted text                    |
| Error messages in return | Prefer over raising exceptions                     |

## Building a TypeScript MCP Server

### Project Setup

```bash
npx @anthropic-ai/create-mcp-server my-server
cd my-server
npm install
```

### Minimal Server

```typescript
import { McpServer } from "@anthropic-ai/sdk/mcp";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

server.tool(
  "search_docs",
  "Search documentation by keyword",
  {
    query: { type: "string", description: "Search query" },
    limit: { type: "number", description: "Max results", default: 5 },
  },
  async ({ query, limit }) => {
    const results = await doSearch(query, limit);
    return {
      content: [{ type: "text", text: formatResults(results) }],
    };
  },
);

server.resource("docs", "docs://{topic}", async (uri) => {
  const topic = uri.pathname;
  return {
    contents: [{ uri: uri.href, text: await loadDoc(topic) }],
  };
});

server.run();
```

## Configuration

### Claude Code Integration (.mcp.json)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/server", "server.py"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

### Claude Desktop Integration

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-server"],
      "env": {}
    }
  }
}
```

## Testing MCP Servers

### Manual Testing with MCP Inspector

```bash
# Install inspector
npx @anthropic-ai/mcp-inspector

# Connect to your server
npx @anthropic-ai/mcp-inspector uv run server.py
```

### Unit Testing Tools

```python
import pytest
from server import mcp

@pytest.mark.asyncio
async def test_search_docs():
    result = await mcp.call_tool("search_docs", {
        "query": "authentication",
        "limit": 3,
    })
    assert len(result) > 0
    assert "authentication" in result.lower()

@pytest.mark.asyncio
async def test_get_doc():
    result = await mcp.read_resource("docs://getting-started")
    assert "Getting Started" in result
```

## Common MCP Server Patterns

### Database Access

```python
# IMPORTANT: Use a read-only database user/role for security.
# String-based SQL validation (e.g., startswith("SELECT")) is NOT
# sufficient — it can be bypassed with CTEs, stacked queries, etc.

from sqlalchemy import create_engine, text

# Connection uses a read-only database role
read_engine = create_engine(READ_ONLY_DATABASE_URL)

@mcp.tool()
def query_database(sql: str) -> str:
    """Run a read-only SQL query against the database.

    Args:
        sql: SQL SELECT query. Connection uses a read-only DB role.
    """
    with read_engine.connect() as conn:
        results = conn.execute(text(sql))
        return format_as_table(results)
```

### External API Wrapper

```python
@mcp.tool()
def search_github_issues(
    repo: str,
    query: str,
    state: str = "open",
) -> str:
    """Search GitHub issues in a repository.

    Args:
        repo: Repository in owner/name format
        query: Search query for issue titles and bodies
        state: Issue state filter (open, closed, all)
    """
    issues = github_client.search_issues(repo, query, state)
    return "\n".join(
        f"#{i.number} [{i.state}] {i.title}" for i in issues
    )
```

### File System Access

```python
@mcp.tool()
def read_project_file(path: str) -> str:
    """Read a file from the project directory.

    Args:
        path: Relative path from project root (no .. traversal allowed)
    """
    safe_path = resolve_safe_path(PROJECT_ROOT, path)
    return safe_path.read_text()
```

## Security Considerations

- Validate all tool inputs (never trust AI-provided parameters)
- Use read-only database connections where possible
- Restrict file access to project directories (prevent path traversal)
- Never expose secrets in tool responses
- Rate limit expensive operations
- Log all tool invocations for audit

## Activation Triggers

This skill auto-activates when prompts contain:

- "mcp", "model context protocol", "mcp server"
- "fastmcp", "mcp tool", "mcp resource"
- ".mcp.json", "mcp config", "mcp inspector"

## Integration

- **@ai-engineer** agent: LLM application development
- **api-design** skill: Tool API design patterns
- **security-review** skill: Securing MCP servers
