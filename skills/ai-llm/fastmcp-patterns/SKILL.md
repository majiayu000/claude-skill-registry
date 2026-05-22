---
name: fastmcp-patterns
description: FastMCP server patterns for building MCP servers. Use when implementing MCP tools, resources, or server configuration.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# FastMCP Patterns

## Server Setup with Lifespan

```python
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP

@asynccontextmanager
async def lifespan(server: FastMCP):
    """Initialize resources on startup, cleanup on shutdown."""
    driver = create_neo4j_driver(config)
    driver.verify_connectivity()

    try:
        yield {"driver": driver, "config": config}
    finally:
        driver.close()

mcp = FastMCP(
    "requirements-graphrag-mcp",
    lifespan=lifespan,
)
```

## Tool Registration

### Basic Tool with Pydantic Validation

```python
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")

@mcp.tool()
async def semantic_search(input: SearchInput) -> list[dict]:
    """Search articles using semantic similarity."""
    driver = mcp.state["driver"]
    return await execute_vector_search(driver, input.query, input.limit)
```

### Tool with Annotations

```python
from mcp.server.fastmcp import Context

@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "openWorldHint": False,
    }
)
async def get_schema(ctx: Context) -> dict:
    """Get database schema. Read-only operation."""
    driver = ctx.state["driver"]
    return await fetch_schema(driver)
```

## Resource Registration

```python
@mcp.resource("schema://database")
async def database_schema() -> str:
    """Expose database schema as a resource."""
    driver = mcp.state["driver"]
    schema = await fetch_schema(driver)
    return json.dumps(schema, indent=2)
```

## Error Handling Pattern

```python
from requirements_graphrag_api.exceptions import (
    Neo4jConnectionError,
    QueryExecutionError,
)

@mcp.tool()
async def execute_cypher(query: str) -> dict:
    """Execute a Cypher query."""
    try:
        driver = mcp.state["driver"]
        return await run_query(driver, query)
    except Neo4jConnectionError as e:
        return {"error": "Database connection failed", "details": str(e)}
    except QueryExecutionError as e:
        return {"error": "Query execution failed", "details": str(e)}
```

## Configuration Pattern

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AppConfig:
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    neo4j_database: str = "neo4j"
    neo4j_max_connection_pool_size: int = 5

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            neo4j_uri=os.environ["NEO4J_URI"],
            neo4j_username=os.environ["NEO4J_USERNAME"],
            neo4j_password=os.environ["NEO4J_PASSWORD"],
            neo4j_database=os.environ.get("NEO4J_DATABASE", "neo4j"),
        )
```

## Entry Point

```python
# src/requirements_graphrag_api/__main__.py
from requirements_graphrag_api.server import mcp

def main():
    mcp.run()

if __name__ == "__main__":
    main()
```

## pyproject.toml Script

```toml
[project.scripts]
requirements-graphrag-api = "requirements_graphrag_api.__main__:main"
```
