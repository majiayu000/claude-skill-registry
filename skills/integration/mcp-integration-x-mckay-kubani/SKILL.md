---
name: mcp-integration
description: MCP server development, usage, and integration patterns. Use when developing new MCP servers or integrating existing ones with agents.
---

# MCP Integration

Guide for developing and using MCP servers in Kubani.

## Available MCP Servers

| Server | Purpose | Location |
|--------|---------|----------|
| temporal-mcp | Workflow orchestration | `kubani/mcp/servers/temporal/` |
| qdrant-mcp | Vector search | `kubani/mcp/servers/qdrant/` |
| memory-mcp | Unified memory (Qdrant + Neo4j + Redis) | `kubani/mcp/servers/memory/` |
| discord-mcp | Discord integration | `kubani/mcp/servers/discord/` |
| skills-mcp | Skills registry | `kubani/mcp/servers/skills/` |

## Using MCP in Agents

```python
from kubani.framework.mcp import get_mcp_client

client = get_mcp_client()

# Memory operations
await client.memory.store_learning(agent_id="k8s-monitor", ...)

# Temporal operations
workflows = await client.temporal.list_workflows(status="running")

# Discord operations
await client.discord.send_embed(channel_id=..., title="Alert", ...)

# Qdrant operations
results = await client.qdrant.search_vectors(collection="skills", ...)
```

## Creating a New MCP Server

### Template (Python FastMCP)

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-mcp-server")

@mcp.tool()
async def my_tool(param: str) -> dict:
    """Tool description for LLM understanding."""
    return {"result": param}

if __name__ == "__main__":
    mcp.run()
```

### Project Structure

```
kubani/mcp/servers/my-server/
├── src/my_mcp/
│   ├── __init__.py
│   ├── server.py      # MCP server implementation
│   └── models.py      # Pydantic models
├── tests/
├── pyproject.toml
└── README.md
```

### Tool Design Best Practices

1. **Workflow-oriented**: Tools should be agent-centric, not thin API wrappers
2. **Descriptive docstrings**: These become the tool descriptions Claude sees
3. **Error handling**: Return structured errors with suggestions, don't raise
4. **Annotations**: Use `readOnlyHint`, `destructiveHint`, `idempotentHint`
5. **Actionable output**: Curate responses — highlight issues, suggest actions

### Registration

Add to `.claude/mcp.json` for Claude Code, or register for cluster use:

```bash
kubani mcp register my-mcp-server
```

### Deployment

MCP servers run as cluster services via Kubernetes deployments in `infrastructure/gitops/apps/mcp-servers/`.
