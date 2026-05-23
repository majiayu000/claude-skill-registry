---
name: mcp-advanced-patterns
description: Advanced MCP patterns for tool composition, resource management, and scaling. Build custom MCP servers, compose tools, manage resources efficiently. Use when composing MCP tools or scaling MCP servers.
version: 1.0.0
author: SkillForge
context: fork
agent: llm-integrator
tags: [mcp, tools, resources, scaling, servers, composition, 2026]
user-invocable: false
---

# MCP Advanced Patterns

Advanced Model Context Protocol patterns for production-grade MCP implementations.

> **FastMCP 2.14.x** (Jan 2026): Enterprise auth, OpenAPI/FastAPI generation, server composition, proxying. Python 3.10-3.13.

## Overview

- Composing multiple tools into orchestrated workflows
- Managing resource lifecycle and caching efficiently
- Scaling MCP servers horizontally with load balancing
- Building custom MCP servers with middleware and transports
- Implementing auto-enable thresholds for context management

## Tool Composition Pattern

```python
from dataclasses import dataclass
from typing import Any, Callable, Awaitable

@dataclass
class ComposedTool:
    """Combine multiple tools into a single pipeline operation."""
    name: str
    tools: dict[str, Callable[..., Awaitable[Any]]]
    pipeline: list[str]

    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute tool pipeline sequentially."""
        result = input_data
        for tool_name in self.pipeline:
            tool = self.tools[tool_name]
            result = await tool(result)
        return result

# Example: Search + Summarize composition
search_summarize = ComposedTool(
    name="search_and_summarize",
    tools={
        "search": search_documents,
        "summarize": summarize_content,
    },
    pipeline=["search", "summarize"]
)
```

## FastMCP Server with Lifecycle

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from mcp.server.fastmcp import Context, FastMCP

@dataclass
class AppContext:
    """Typed application context with shared resources."""
    db: Database
    cache: CacheService
    config: dict

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage server startup and shutdown lifecycle."""
    # Initialize on startup
    db = await Database.connect()
    cache = await CacheService.connect()

    try:
        yield AppContext(db=db, cache=cache, config={"timeout": 30})
    finally:
        # Cleanup on shutdown
        await cache.disconnect()
        await db.disconnect()

mcp = FastMCP("Production Server", lifespan=app_lifespan)

@mcp.tool()
def query_data(sql: str, ctx: Context) -> str:
    """Execute query using shared connection."""
    app_ctx = ctx.request_context.lifespan_context
    return app_ctx.db.query(sql)
```

## Auto-Enable Thresholds (CC 2.1.9)

Configure MCP servers to auto-enable/disable based on context window usage:

```yaml
# .claude/settings.json
mcp:
  context7:
    enabled: auto:75    # High-value docs, keep available longer
  sequential-thinking:
    enabled: auto:60    # Complex reasoning needs room
  memory:
    enabled: auto:90    # Knowledge graph - preserve until compaction
  playwright:
    enabled: auto:50    # Browser-heavy, disable early
```

**Threshold Guidelines:**
| Threshold | Use Case | Rationale |
|-----------|----------|-----------|
| auto:90 | Critical persistence | Keep until context nearly full |
| auto:75 | High-value reference | Preserve for complex tasks |
| auto:60 | Reasoning tools | Need headroom for output |
| auto:50 | Resource-intensive | Disable early to free context |

## Resource Management

```python
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Any

class MCPResourceManager:
    """Manage MCP resources with caching and lifecycle."""

    def __init__(self, cache_ttl: timedelta = timedelta(minutes=15)):
        self.resources: dict[str, Any] = {}
        self.cache_ttl = cache_ttl
        self.last_access: dict[str, datetime] = {}

    def get_resource(self, uri: str) -> Any:
        """Get resource with access time tracking."""
        if uri in self.resources:
            self.last_access[uri] = datetime.now()
            return self.resources[uri]

        resource = self._load_resource(uri)
        self.resources[uri] = resource
        self.last_access[uri] = datetime.now()
        return resource

    def cleanup_stale(self) -> int:
        """Remove stale resources. Returns count of removed."""
        now = datetime.now()
        stale = [
            uri for uri, last in self.last_access.items()
            if now - last > self.cache_ttl
        ]
        for uri in stale:
            del self.resources[uri]
            del self.last_access[uri]
        return len(stale)
```

## Horizontal Scaling

```python
import asyncio
from typing import List

class MCPLoadBalancer:
    """Load balance across multiple MCP server instances."""

    def __init__(self, servers: List[str]):
        self.servers = servers
        self.current = 0
        self.health: dict[str, bool] = {s: True for s in servers}

    async def get_healthy_server(self) -> str:
        """Round-robin with health check."""
        for _ in range(len(self.servers)):
            server = self.servers[self.current]
            self.current = (self.current + 1) % len(self.servers)
            if self.health[server]:
                return server
        raise RuntimeError("No healthy servers available")

    async def health_check_loop(self):
        """Periodic health check for all servers."""
        while True:
            for server in self.servers:
                try:
                    self.health[server] = await self._ping(server)
                except Exception:
                    self.health[server] = False
            await asyncio.sleep(30)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Transport | Streamable HTTP for web, stdio for CLI |
| Lifecycle | Always use lifespan for resource management |
| Composition | Chain tools via pipeline pattern |
| Scaling | Health-checked round-robin for redundancy |
| Auto-enable | Use auto:N thresholds per server criticality |

## Common Mistakes

- No lifecycle management (resource leaks)
- Missing health checks in load balancing
- Hardcoded server endpoints
- No graceful degradation on server failure
- Ignoring context window thresholds

## Related Skills

- `function-calling` - LLM tool integration patterns
- `resilience-patterns` - Circuit breakers and retries
- `connection-pooling` - Database connection management
- `streaming-api-patterns` - Real-time streaming

## Capability Details

### tool-composition
**Keywords:** tool composition, pipeline, orchestration, chain tools
**Solves:**
- Combine multiple tools into workflows
- Sequential tool execution
- Tool result passing

### resource-management
**Keywords:** resource, cache, lifecycle, cleanup, ttl
**Solves:**
- Manage resource lifecycle
- Implement resource caching
- Clean up stale resources

### scaling-strategies
**Keywords:** scale, load balance, horizontal, health check, redundancy
**Solves:**
- Scale MCP servers horizontally
- Implement health-checked load balancing
- Handle server failures gracefully

### server-building
**Keywords:** server, fastmcp, lifespan, middleware, transport
**Solves:**
- Build production MCP servers
- Manage server lifecycle
- Configure transports and middleware

### auto-enable-thresholds
**Keywords:** auto-enable, context window, threshold, auto:N
**Solves:**
- Configure MCP auto-enable/disable
- Manage context window usage
- Optimize MCP server availability
