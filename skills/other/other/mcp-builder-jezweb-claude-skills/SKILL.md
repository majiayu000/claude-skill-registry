---
name: mcp-builder
description: >
  Build MCP servers in Python with FastMCP. Workflow: define tools and resources,
  build server, test locally, deploy to FastMCP Cloud or Docker.
  Use when creating MCP servers, exposing tools/resources/prompts to LLMs,
  building Claude integrations, or troubleshooting FastMCP module-level server,
  storage, lifespan, middleware, OAuth, or deployment errors.
compatibility: claude-code-only
---

# MCP Builder

Build a working MCP server from a description of the tools you need. Produces a deployable Python server using FastMCP.

## Workflow

### Step 1: Define What to Expose

Ask what the server needs to provide:

- **Tools** — Functions Claude can call (API wrappers, calculations, file operations)
- **Resources** — Data Claude can read (database records, config, documents)
- **Prompts** — Reusable prompt templates with parameters

A brief like "MCP server for querying our customer database" is enough.

### Step 2: Scaffold the Server

```bash
pip install fastmcp
```

Copy and customise `assets/basic-server.py`:

```python
from fastmcp import FastMCP

# MUST be at module level for FastMCP Cloud
mcp = FastMCP("My Server")

@mcp.tool()
async def search_customers(query: str) -> str:
    """Search customers by name or email."""
    # Implementation here
    return f"Found customers matching: {query}"

@mcp.resource("customers://{customer_id}")
async def get_customer(customer_id: str) -> str:
    """Get customer details by ID."""
    return f"Customer {customer_id} details"

if __name__ == "__main__":
    mcp.run()
```

### Step 3: Add Companion CLI Scripts (Optional)

For Claude Code terminal use, add scripts alongside the MCP server:

```
my-mcp-server/
├── src/index.ts          # MCP server (for Claude.ai)
├── scripts/
│   ├── search.ts         # CLI version of search tool
│   └── _shared.ts        # Shared auth/config
├── SCRIPTS.md            # Documents available scripts
└── package.json
```

CLI scripts provide file I/O, batch processing, and richer output that MCP can't.
See `assets/SCRIPTS-TEMPLATE.md` and `assets/script-template.ts` for TypeScript templates.

### Step 4: Test Locally

```bash
# Run server directly
python server.py

# With FastMCP dev mode (auto-reload)
fastmcp dev server.py

# HTTP mode for remote clients
python server.py --transport http --port 8000

# Test with MCP Inspector
fastmcp dev server.py --with-editable .
```

### Step 5: Deploy

**FastMCP Cloud** (simplest):
```bash
fastmcp deploy server.py --name my-server
```

**Docker** (self-hosted):
See `references/cloud-deployment.md` for Dockerfile patterns.

**Cloudflare Workers** (edge):
See the cloudflare-worker-builder skill for Workers-based MCP servers.

---

## Critical Patterns

### Module-Level Server Instance

FastMCP Cloud requires the server instance at module level:

```python
# CORRECT
mcp = FastMCP("My Server")

@mcp.tool()
def my_tool(): ...

# WRONG — Cloud can't find the server
def create_server():
    mcp = FastMCP("My Server")
    return mcp
```

### Type Annotations Required

FastMCP uses type annotations to generate tool schemas:

```python
@mcp.tool()
async def search(
    query: str,           # Required parameter
    limit: int = 10,      # Optional with default
    tags: list[str] = []  # Complex types supported
) -> str:
    """Docstring becomes the tool description."""
    ...
```

### Error Handling

Return errors as strings, don't raise exceptions:

```python
@mcp.tool()
async def get_data(id: str) -> str:
    try:
        result = await fetch_data(id)
        return json.dumps(result)
    except NotFoundError:
        return f"Error: No data found for ID {id}"
```

---

## Asset Files

- `assets/basic-server.py` — Minimal FastMCP server template
- `assets/self-contained-server.py` — Server with storage and middleware
- `assets/tools-examples.py` — Tool patterns and type annotations
- `assets/resources-examples.py` — Resource URI patterns
- `assets/prompts-examples.py` — Prompt template patterns
- `assets/client-example.py` — MCP client usage
- `assets/SCRIPTS-TEMPLATE.md` — CLI companion docs template
- `assets/script-template.ts` — TypeScript CLI script template

## Reference Files

- `references/common-errors.md` — 30+ documented errors with fixes
- `references/cli-commands.md` — FastMCP CLI reference
- `references/cloud-deployment.md` — Deployment patterns (Cloud, Docker, Workers)
- `references/production-patterns.md` — Auth, middleware, storage backends
- `references/integration-patterns.md` — FastAPI mount, OpenAPI import
- `references/context-features.md` — Lifespan, dependency injection
