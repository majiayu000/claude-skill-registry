---
name: mcp-server
description: Build MCP (Model Context Protocol) servers for CasareRPA integrations using Python FastMCP. Covers server structure, tool design, error handling, and RPA-specific patterns. See references/ for detailed guides. Use when: creating MCP servers, tool design, error handling, RPA-specific patterns, FastMCP, Context logging, lifespan hooks.
---

# MCP Server Builder

Build Model Context Protocol servers for RPA integrations.

## Quick Start

```python
from fastmcp import FastMCP, Context
from typing import Dict, Any

mcp = FastMCP(
    name="CasareRPA Integration",
    instructions="Execute and manage RPA workflows"
)

@mcp.tool()
async def execute_workflow(
    workflow_id: str,
    ctx: Context
) -> Dict[str, Any]:
    """Execute a CasareRPA workflow by ID.

    Args:
        workflow_id: UUID of the workflow to execute
        ctx: FastMCP context for logging

    Returns:
        Execution result with status and output
    """
    await ctx.info(f"Executing workflow: {workflow_id}")
    # Implementation details in references/python-mcp.md
    return {"status": "success", "workflow_id": workflow_id}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Server Structure

```
src/casare_rpa/infrastructure/mcp/
├── __init__.py
├── server.py           # FastMCP server instance
├── tools/              # Tool implementations
│   ├── workflow.py     # Workflow execution tools
│   ├── robot.py        # Robot control tools
│   └── monitoring.py   # Status and monitoring
└── resources/          # MCP resources
    └── status.py       # Server status resources
```

## Key Concepts

| Concept | Description | Reference |
|---------|-------------|-----------|
| Tools | Callable functions for LLMs | `references/mcp-best-practices.md` |
| Resources | Static/dynamic data endpoints | `references/mcp-best-practices.md` |
| Context | Logging, progress reporting | `references/python-mcp.md` |
| Lifespan | Startup/shutdown hooks | `references/python-mcp.md` |
| Error Handling | Graceful failure patterns | `references/mcp-best-practices.md` |

## Tool Naming

Use verb_noun pattern matching RPA operations:
- `execute_workflow`, `list_workflows`, `stop_workflow`
- `get_robot_status`, `start_robot`, `pause_robot`
- `read_variable`, `set_variable`, `list_variables`

## Error Handling

Always wrap external calls and use Context for logging:

```python
@mcp.tool()
async def safe_operation(param: str, ctx: Context) -> Dict[str, Any]:
    try:
        result = await external_api_call(param)
        await ctx.info(f"Operation completed: {param}")
        return {"status": "success", "data": result}
    except ValueError as e:
        await ctx.error(f"Validation failed: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        await ctx.error(f"Unexpected error: {e}")
        return {"status": "error", "message": "Operation failed"}
```

## RPA-Specific Patterns

### Long-Running Operations
Use progress reporting for workflow execution:
```python
await ctx.report_progress(5, 10)  # 5/10 complete
```

### Resource Cleanup
Use lifespan for connections:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastMCP):
    # Startup: connect to orchestrator
    await orchestrator.connect()
    yield
    # Shutdown: cleanup
    await orchestrator.disconnect()

mcp = FastMCP("RPA Server", lifespan=lifespan)
```

## Testing

```bash
# Development with inspector
fastmcp dev server.py

# Run tests
pytest tests/infrastructure/mcp/ -v
```

## References

| File | Content |
|------|---------|
| `references/mcp-best-practices.md` | Tool design, naming, error patterns |
| `references/python-mcp.md` | FastMCP-specific patterns |
| `references/evaluation.md` | Testing and evaluation checklist |

## See Also

- `.brain/systemPatterns.md` - CasareRPA architecture patterns
- `src/casare_rpa/infrastructure/orchestrator/` - Workflow orchestration
- `docs/developer-guide/architecture/mcp-integration.md` - Full integration guide
