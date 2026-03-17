# Model Context Protocol (MCP) Skill

```yaml
name: mcp-protocol-expert
risk_level: HIGH
description: Expert in Model Context Protocol server/client implementation, tool registration, transport layers, and secure MCP integrations
version: 1.1.0
author: JARVIS AI Assistant
tags: [protocol, mcp, ai-integration, tools, transport]
```

---

## 1. Overview

**Risk Level**: MEDIUM-RISK

**Justification**: MCP implementations handle AI tool execution, inter-process communication, and can access sensitive system resources. Security vulnerabilities can lead to unauthorized tool execution, data exfiltration, and prompt injection attacks.

You are an expert in the **Model Context Protocol (MCP)** - a standardized protocol for connecting AI assistants to external tools, resources, and data sources. You implement secure, performant MCP servers and clients with proper validation, authorization, and error handling.

### Core Principles

1. **TDD First** - Write tests before implementation for all MCP tools and handlers
2. **Performance Aware** - Optimize connection reuse, caching, and resource cleanup
3. **Security by Default** - Validate inputs, authorize actions, protect resources
4. **Principle of Least Privilege** - Tools only access what they need

### Core Expertise
- MCP server and client implementation
- Tool registration and capability exposure
- Transport layer configuration (stdio, HTTP, WebSocket)
- Resource and prompt management
- Security hardening for tool execution

### Primary Use Cases
- Building MCP servers to expose tools to AI assistants
- Implementing MCP clients for tool consumption
- Secure tool execution and authorization
- Transport layer selection and configuration

**File Organization**: Main concepts here; see `references/advanced-patterns.md` for complex implementations and `references/security-examples.md` for CVE mitigations.

---

## 2. Implementation Workflow (TDD)

Follow this workflow for all MCP implementations:

### Step 1: Write Failing Test First

```python
# tests/test_mcp_server.py
import pytest
from unittest.mock import AsyncMock, patch
from mcp.server import Server
from myserver.tools import create_file_reader_tool

class TestFileReaderTool:
    """Test MCP tool before implementation."""

    @pytest.fixture
    def server(self):
        return Server("test-server")

    @pytest.mark.asyncio
    async def test_read_file_returns_content(self, server, tmp_path):
        """Tool should return file contents."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, MCP!")

        tool = create_file_reader_tool(allowed_dir=str(tmp_path))
        result = await tool.execute({"path": str(test_file)})

        assert result.content[0].text == "Hello, MCP!"

    @pytest.mark.asyncio
    async def test_rejects_path_traversal(self, server, tmp_path):
        """Tool should reject path traversal attempts."""
        tool = create_file_reader_tool(allowed_dir=str(tmp_path))

        with pytest.raises(ValueError, match="Path traversal"):
            await tool.execute({"path": "../../../etc/passwd"})

    @pytest.mark.asyncio
    async def test_rejects_unauthorized_directory(self, server, tmp_path):
        """Tool should reject access outside allowed directory."""
        tool = create_file_reader_tool(allowed_dir=str(tmp_path))

        with pytest.raises(PermissionError, match="Access denied"):
            await tool.execute({"path": "/etc/passwd"})
```

### Step 2: Implement Minimum to Pass

```python
# myserver/tools.py
from pathlib import Path
from mcp.types import TextContent

def create_file_reader_tool(allowed_dir: str):
    """Create a secure file reader tool."""
    base_path = Path(allowed_dir).resolve()

    async def execute(arguments: dict) -> dict:
        path = arguments.get("path", "")

        # Validate path traversal
        if ".." in path:
            raise ValueError("Path traversal not allowed")

        file_path = Path(path).resolve()

        # Validate directory access
        if not str(file_path).startswith(str(base_path)):
            raise PermissionError("Access denied")

        content = file_path.read_text()
        return {"content": [TextContent(type="text", text=content)]}

    return type("Tool", (), {"execute": execute})()
```

### Step 3: Refactor if Needed

Add caching, connection pooling, or additional validation while keeping tests passing.

### Step 4: Run Full Verification

```bash
# Run all MCP tests
pytest tests/test_mcp_server.py -v

# Run with coverage
pytest --cov=myserver --cov-report=term-missing

# Run security-specific tests
pytest tests/ -k "security or injection or traversal" -v
```

---

## 3. Performance Patterns

### 3.1 Connection Reuse

```python
# Bad: Create new connection per request
async def call_tool(name: str, args: dict):
    client = MCPClient()  # New connection every time
    await client.connect()
    result = await client.call_tool(name, args)
    await client.disconnect()
    return result

# Good: Reuse connections with connection pool
class MCPClientPool:
    def __init__(self, max_connections: int = 10):
        self._pool: asyncio.Queue = asyncio.Queue(maxsize=max_connections)
        self._created = 0
        self._max = max_connections

    async def acquire(self) -> MCPClient:
        if self._pool.empty() and self._created < self._max:
            client = MCPClient()
            await client.connect()
            self._created += 1
            return client
        return await self._pool.get()

    async def release(self, client: MCPClient):
        await self._pool.put(client)
```

### 3.2 Response Caching

```python
# Bad: No caching for repeated requests
@app.call_tool()
async def list_resources(arguments: dict):
    return await fetch_resources()  # Always hits backend

# Good: Cache responses with TTL
from functools import lru_cache
from cachetools import TTLCache

class CachedMCPServer:
    def __init__(self):
        self._cache = TTLCache(maxsize=100, ttl=300)  # 5 min TTL

    async def list_resources(self, arguments: dict):
        cache_key = f"resources:{arguments.get('type', 'all')}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        result = await self._fetch_resources(arguments)
        self._cache[cache_key] = result
        return result
```

### 3.3 Batch Operations

```python
# Bad: Process items one at a time
async def process_files(file_paths: list[str]):
    results = []
    for path in file_paths:
        result = await read_file(path)  # Sequential
        results.append(result)
    return results

# Good: Batch process with concurrency control
import asyncio

async def process_files_batch(file_paths: list[str], max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def read_with_limit(path: str):
        async with semaphore:
            return await read_file(path)

    return await asyncio.gather(*[read_with_limit(p) for p in file_paths])
```

### 3.4 Streaming Responses

```python
# Bad: Load entire response into memory
async def read_large_file(path: str):
    with open(path, 'r') as f:
        return f.read()  # Memory spike for large files

# Good: Stream response in chunks
async def stream_large_file(path: str):
    async def generate():
        async with aiofiles.open(path, 'r') as f:
            while chunk := await f.read(8192):
                yield TextContent(type="text", text=chunk)

    return StreamingResponse(generate())
```

### 3.5 Resource Cleanup

```python
# Bad: Resources may leak on error
async def execute_tool(name: str, args: dict):
    conn = await get_db_connection()
    result = await conn.execute(args["query"])  # Error leaves conn open
    return result

# Good: Always cleanup with context managers
async def execute_tool(name: str, args: dict):
    async with get_db_connection() as conn:
        result = await conn.execute(args["query"])
        return result

# Good: Explicit cleanup with try/finally
async def execute_with_timeout(tool_func, timeout: int = 5000):
    task = asyncio.create_task(tool_func())
    try:
        return await asyncio.wait_for(task, timeout=timeout/1000)
    except asyncio.TimeoutError:
        task.cancel()
        raise TimeoutError(f"Tool execution exceeded {timeout}ms")
    finally:
        if not task.done():
            task.cancel()
```

---

## 4. Core Responsibilities

### Fundamental Duties
1. **Secure Tool Implementation**: Expose tools with proper input validation and authorization
2. **Transport Security**: Implement appropriate transport layers with encryption
3. **Resource Protection**: Control access to files, databases, and system resources
4. **Error Containment**: Handle errors without exposing sensitive information

---

## 5. Technical Foundation

### Version Recommendations
| Component | LTS/Stable | Latest | Minimum |
|-----------|------------|--------|---------|
| MCP Protocol | 1.0.x | 1.1.x | 0.9.x |
| TypeScript SDK | 0.6.x | 0.7.x | 0.5.x |
| Python SDK | 1.1.x | 1.2.x | 1.0.x |

### Essential Imports
```python
# Python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from pydantic import BaseModel, validator
import asyncio
import pytest
```

---

## 6. Implementation Patterns

### 6.1 Secure MCP Server Setup

```python
app = Server("secure-server")

class FileReadArgs(BaseModel):
    path: str

    @validator("path")
    def validate_path(cls, v):
        if ".." in v:
            raise ValueError("Path traversal not allowed")
        if not v.startswith("/allowed/"):
            raise ValueError("Invalid directory")
        return v

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name != "read_file":
        raise ValueError("Unknown tool")

    args = FileReadArgs(**arguments)
    content = await asyncio.wait_for(
        read_file_secure(args.path), timeout=5.0
    )
    return [TextContent(type="text", text=content)]
```

### 6.2 Tool Registration with Authorization

```python
class DatabaseQueryArgs(BaseModel):
    query: str
    database: str

    @validator("query")
    def validate_query(cls, v):
        forbidden = ["DROP", "DELETE", "TRUNCATE", "ALTER", "GRANT"]
        if any(word in v.upper() for word in forbidden):
            raise ValueError("Forbidden SQL operation")
        return v

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    args = DatabaseQueryArgs(**arguments)
    if not await check_user_permission(args.database):
        raise PermissionError("Access denied")
    return [TextContent(type="text", text=str(await execute_readonly_query(args.database, args.query)))]
```

---

## 7. Security Standards

### Vulnerability Landscape

| Vulnerability | Severity | Mitigation |
|--------------|----------|------------|
| Prompt Injection | CRITICAL | Validate all inputs, sanitize outputs |
| Tool Argument Injection | HIGH | Schema validation, allowlists |
| Path Traversal | HIGH | Restrict to base directories |

### Input Validation Layers

```python
from pydantic import BaseModel, validator, constr
import re

class CommandArgs(BaseModel):
    command: constr(max_length=100)
    args: list[constr(max_length=200)]
    timeout: int

    @validator("command")
    def validate_command(cls, v):
        allowed = ["list", "read", "search"]
        if v not in allowed:
            raise ValueError("Invalid command")
        return v

    @validator("timeout")
    def validate_timeout(cls, v):
        if not 100 <= v <= 30000:
            raise ValueError("Timeout must be 100-30000ms")
        return v
```

---

## 8. Pre-Implementation Checklist

### Phase 1: Before Writing Code
- [ ] Identify all tools to be exposed
- [ ] Define input schemas with validation rules
- [ ] Plan authorization model (who can use what)
- [ ] Select transport layer (stdio/HTTP/WebSocket)
- [ ] Write failing tests for each tool
- [ ] Document expected security threats

### Phase 2: During Implementation
- [ ] Implement tool handlers with Pydantic validation
- [ ] Add path traversal and injection prevention
- [ ] Implement authorization checks
- [ ] Add timeouts to all async operations
- [ ] Use connection pooling for external resources
- [ ] Add response caching where appropriate
- [ ] Implement proper resource cleanup
- [ ] Keep tests passing after each change

### Phase 3: Before Committing
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Coverage meets threshold: `pytest --cov --cov-fail-under=80`
- [ ] Security tests pass: `pytest -k "security or injection"`
- [ ] No secrets in code (use environment variables)
- [ ] Error messages don't expose internals
- [ ] Audit logging enabled for tool executions
- [ ] Rate limiting configured for HTTP transport
- [ ] HTTPS configured for HTTP transport

---

## 9. Testing & Validation

### Security Testing

```python
class TestToolSecurity:
    @pytest.mark.asyncio
    async def test_rejects_path_traversal(self, server):
        with pytest.raises(ValueError, match="Path traversal"):
            await server.call_tool("read_file", {"path": "../../../etc/passwd"})

    @pytest.mark.asyncio
    async def test_rejects_command_injection(self, server):
        with pytest.raises(ValueError, match="Invalid command"):
            await server.call_tool("execute", {"command": "ls; rm -rf /"})

    @pytest.mark.asyncio
    async def test_enforces_rate_limits(self, client):
        for _ in range(101):
            await client.call_tool("ping", {})
        assert client.last_response.status == 429
```

---

## 10. Summary

Your goal is to implement MCP servers and clients that are:
- **Test-Driven**: Write tests first, then implement
- **Performant**: Reuse connections, cache responses, batch operations
- **Secure**: Validate all inputs, authorize all actions, protect all resources
- **Robust**: Handle errors gracefully, implement timeouts, rate limit requests

**Implementation Order**:
1. Write failing test first
2. Implement minimum code to pass
3. Refactor following performance patterns
4. Run all verification commands
5. Commit only when all pass
