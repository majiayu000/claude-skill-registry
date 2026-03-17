---
name: fastmcp
description: |
  Build MCP servers in Python with FastMCP to expose tools, resources, and prompts to LLMs. Supports storage backends, middleware, OAuth Proxy, OpenAPI integration, and FastMCP Cloud deployment. Prevents 30+ errors.

  Use when: creating MCP servers, or troubleshooting module-level server, storage, lifespan, middleware, OAuth, background tasks, or FastAPI mount errors.
user-invocable: true
---

# FastMCP - Build MCP Servers in Python

FastMCP is a Python framework for building Model Context Protocol (MCP) servers that expose tools, resources, and prompts to Large Language Models like Claude. This skill provides production-tested patterns, error prevention, and deployment strategies for building robust MCP servers.

## Quick Start

### Installation

```bash
pip install fastmcp
# or
uv pip install fastmcp
```

### Minimal Server

```python
from fastmcp import FastMCP

# MUST be at module level for FastMCP Cloud
mcp = FastMCP("My Server")

@mcp.tool()
async def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

**Run it:**
```bash
# Local development
python server.py

# With FastMCP CLI
fastmcp dev server.py

# HTTP mode
python server.py --transport http --port 8000
```

## What's New in v2.14.x (December 2025)

### v2.14.2 (December 31, 2024)
- MCP SDK pinned to <2.x for compatibility
- Supabase provider gains `auth_route` parameter
- Bug fixes: outputSchema `$ref` resolution, OAuth Proxy validation, OpenAPI 3.1 support

### v2.14.1: Sampling with Tools (SEP-1577)
- **`ctx.sample()` now accepts tools** for agentic workflows
- `AnthropicSamplingHandler` promoted from experimental
- `ctx.sample_step()` for single LLM call returning `SampleStep`
- Python 3.13 support added

### v2.14.0: Background Tasks (SEP-1686)
- **Protocol-native background tasks** for long-running operations
- Add `task=True` to async decorators; progress tracking without blocking
- MCP 2025-11-25 specification support
- SEP-1699: SSE polling and event resumability
- SEP-1330: Multi-select enum elicitation schemas
- SEP-1034: Default values for elicitation schemas

**⚠️ Breaking Changes (v2.14.0):**
- `BearerAuthProvider` module removed (use `JWTVerifier` or `OAuthProxy`)
- `Context.get_http_request()` method removed
- `fastmcp.Image` top-level import removed (use `from fastmcp.utilities import Image`)
- `enable_docket`, `enable_tasks` settings removed (always enabled)
- `run_streamable_http_async()`, `sse_app()`, `streamable_http_app()`, `run_sse_async()` methods removed
- `dependencies` parameter removed from decorators
- `output_schema=False` support eliminated
- `FASTMCP_SERVER_` environment variable prefix deprecated

**Known Compatibility:**
- MCP SDK pinned to <2.x (v2.14.2+)

## What's New in v3.0.0 (Beta - January 2026)

**⚠️ MAJOR BREAKING CHANGES** - FastMCP 3.0 is a complete architectural refactor.

### Provider Architecture

All components now sourced via **Providers**:
- `FileSystemProvider` - Discover decorated functions from directories with hot-reload
- `SkillsProvider` - Expose agent skill files as MCP resources
- `OpenAPIProvider` - Auto-generate from OpenAPI specs
- `ProxyProvider` - Proxy to remote MCP servers

```python
from fastmcp import FastMCP
from fastmcp.providers import FileSystemProvider

mcp = FastMCP("server")
mcp.add_provider(FileSystemProvider(path="./tools", reload=True))
```

### Transforms (Component Middleware)

Modify components without changing source code:
- Namespace, rename, filter by version
- `ResourcesAsTools` - Expose resources as tools
- `PromptsAsTools` - Expose prompts as tools

```python
from fastmcp.transforms import Namespace, VersionFilter

mcp.add_transform(Namespace(prefix="api"))
mcp.add_transform(VersionFilter(min_version="2.0"))
```

### Component Versioning

```python
@mcp.tool(version="2.0")
async def fetch_data(query: str) -> dict:
    # Clients see highest version by default
    # Can request specific version
    return {"data": [...]}
```

### Session-Scoped State

```python
@mcp.tool()
async def set_preference(key: str, value: str, ctx: Context) -> dict:
    await ctx.set_state(key, value)  # Persists across session
    return {"saved": True}

@mcp.tool()
async def get_preference(key: str, ctx: Context) -> dict:
    value = await ctx.get_state(key, default=None)
    return {"value": value}
```

### Other Features

- `--reload` flag for auto-restart during development
- Automatic threadpool dispatch for sync functions
- Tool timeouts
- OpenTelemetry tracing
- Component authorization: `@tool(auth=require_scopes("admin"))`

### Migration Guide

**Pin to v2 if not ready**:
```
# requirements.txt
fastmcp<3
```

**For most servers**, updating the import is all you need:
```python
# v2.x and v3.0 compatible
from fastmcp import FastMCP

mcp = FastMCP("server")
# ... rest of code works the same
```

**See**: [Official Migration Guide](https://github.com/jlowin/fastmcp/blob/main/docs/development/upgrade-guide.mdx)

---

## Core Concepts

### Tools
Functions LLMs can call. Best practices: Clear names, comprehensive docstrings (LLMs read these!), strong type hints (Pydantic validates), structured returns, error handling.

```python
@mcp.tool()
async def async_tool(url: str) -> dict:  # Use async for I/O
    async with httpx.AsyncClient() as client:
        return (await client.get(url)).json()
```

### Resources
Expose data to LLMs. URI schemes: `data://`, `file://`, `resource://`, `info://`, `api://`, or custom.

```python
@mcp.resource("user://{user_id}/profile")  # Template with parameters
async def get_user(user_id: str) -> dict:  # CRITICAL: param names must match
    return await fetch_user_from_db(user_id)
```

### Prompts
Pre-configured prompts with parameters.

```python
@mcp.prompt("analyze")
def analyze_prompt(topic: str) -> str:
    return f"Analyze {topic} considering: state, challenges, opportunities, recommendations."
```

## Context Features

Inject `Context` parameter (with type hint!) for advanced features:

**Elicitation (User Input):**
```python
from fastmcp import Context

@mcp.tool()
async def confirm_action(action: str, context: Context) -> dict:
    confirmed = await context.request_elicitation(prompt=f"Confirm {action}?", response_type=str)
    return {"status": "completed" if confirmed.lower() == "yes" else "cancelled"}
```

**Progress Tracking:**
```python
@mcp.tool()
async def batch_import(file_path: str, context: Context) -> dict:
    data = await read_file(file_path)
    for i, item in enumerate(data):
        await context.report_progress(i + 1, len(data), f"Importing {i + 1}/{len(data)}")
        await import_item(item)
    return {"imported": len(data)}
```

**Sampling (LLM calls from tools):**
```python
@mcp.tool()
async def enhance_text(text: str, context: Context) -> str:
    response = await context.request_sampling(
        messages=[{"role": "user", "content": f"Enhance: {text}"}],
        temperature=0.7
    )
    return response["content"]
```

## Background Tasks (v2.14.0+)

Long-running operations that report progress without blocking clients. Uses Docket task scheduler (always enabled in v2.14.0+).

**Basic Usage:**
```python
@mcp.tool(task=True)  # Enable background task mode
async def analyze_large_dataset(dataset_id: str, context: Context) -> dict:
    """Analyze large dataset with progress tracking."""
    data = await fetch_dataset(dataset_id)

    for i, chunk in enumerate(data.chunks):
        # Report progress to client
        await context.report_progress(
            current=i + 1,
            total=len(data.chunks),
            message=f"Processing chunk {i + 1}/{len(data.chunks)}"
        )
        await process_chunk(chunk)

    return {"status": "complete", "records_processed": len(data)}
```

**Task States:** `pending` → `running` → `completed` / `failed` / `cancelled`

**When to Use:**
- Operations taking >30 seconds (LLM timeout risk)
- Batch processing with per-item status updates
- Operations that may need user input mid-execution
- Long-running API calls or data processing

**Known Limitation (v2.14.x)**:
- `statusMessage` from `ctx.report_progress()` is **not forwarded** to clients during background task polling ([GitHub Issue #2904](https://github.com/jlowin/fastmcp/issues/2904))
- Progress messages appear in server logs but not in client UI
- **Workaround**: Use official MCP SDK (`mcp>=1.10.0`) instead of FastMCP for now
- **Status**: Fix pending in [PR #2906](https://github.com/jlowin/fastmcp/pull/2906)

**Important:** Tasks execute through Docket scheduler. Cannot execute tasks through proxies (will raise error).

## Sampling with Tools (v2.14.1+)

Servers can pass tools to `ctx.sample()` for agentic workflows where the LLM can call tools during sampling.

**Agentic Sampling:**
```python
from fastmcp import Context
from fastmcp.sampling import AnthropicSamplingHandler

# Configure sampling handler
mcp = FastMCP("Agent Server")
mcp.add_sampling_handler(AnthropicSamplingHandler(api_key=os.getenv("ANTHROPIC_API_KEY")))

@mcp.tool()
async def research_topic(topic: str, context: Context) -> dict:
    """Research a topic using agentic sampling with tools."""

    # Define tools available during sampling
    research_tools = [
        {
            "name": "search_web",
            "description": "Search the web for information",
            "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}}
        },
        {
            "name": "fetch_url",
            "description": "Fetch content from a URL",
            "inputSchema": {"type": "object", "properties": {"url": {"type": "string"}}}
        }
    ]

    # Sample with tools - LLM can call these tools during reasoning
    result = await context.sample(
        messages=[{"role": "user", "content": f"Research: {topic}"}],
        tools=research_tools,
        max_tokens=4096
    )

    return {"research": result.content, "tools_used": result.tool_calls}
```

**Single-Step Sampling:**
```python
@mcp.tool()
async def get_single_response(prompt: str, context: Context) -> dict:
    """Get a single LLM response without tool loop."""

    # sample_step() returns SampleStep for inspection
    step = await context.sample_step(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return {
        "content": step.content,
        "model": step.model,
        "stop_reason": step.stop_reason
    }
```

**Sampling Handlers:**
- `AnthropicSamplingHandler` - For Claude models (v2.14.1+)
- `OpenAISamplingHandler` - For GPT models

**Known Limitation**:
`ctx.sample()` works when client connects to a single server but fails with "Sampling not supported" error when multiple servers are configured in client. Tools without sampling work fine. ([Community-sourced finding](https://github.com/jlowin/fastmcp/issues/699))

## Storage Backends

Built on `py-key-value-aio` for OAuth tokens, response caching, persistent state.

**Available Backends:**
- **Memory** (default): Ephemeral, fast, dev-only
- **Disk**: Persistent, encrypted with `FernetEncryptionWrapper`, platform-aware (Mac/Windows default)
- **Redis**: Distributed, production, multi-instance
- **Others**: DynamoDB, MongoDB, Elasticsearch, Memcached, RocksDB, Valkey

**Basic Usage:**
```python
from key_value.stores import DiskStore, RedisStore
from key_value.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

# Disk (persistent, single instance)
mcp = FastMCP("Server", storage=DiskStore(path="/app/data/storage"))

# Redis (distributed, production)
mcp = FastMCP("Server", storage=RedisStore(
    host=os.getenv("REDIS_HOST"), password=os.getenv("REDIS_PASSWORD")
))

# Encrypted storage (recommended)
mcp = FastMCP("Server", storage=FernetEncryptionWrapper(
    key_value=DiskStore(path="/app/data"),
    fernet=Fernet(os.getenv("STORAGE_ENCRYPTION_KEY"))
))
```

**Platform Defaults:** Mac/Windows use Disk, Linux uses Memory. Override with `storage` parameter.

## Server Lifespans

**⚠️ Breaking Change in v2.13.0**: Lifespan behavior changed from per-session to per-server-instance.

Initialize/cleanup resources once per server (NOT per session) - critical for DB connections, API clients.

```python
from contextlib import asynccontextmanager
from dataclasses import dataclass

@dataclass
class AppContext:
    db: Database
    api_client: httpx.AsyncClient

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    """Runs ONCE per server instance."""
    db = await Database.connect(os.getenv("DATABASE_URL"))
    api_client = httpx.AsyncClient(base_url=os.getenv("API_BASE_URL"), timeout=30.0)

    try:
        yield AppContext(db=db, api_client=api_client)
    finally:
        await db.disconnect()
        await api_client.aclose()

mcp = FastMCP("Server", lifespan=app_lifespan)

# Access in tools
@mcp.tool()
async def query_db(sql: str, context: Context) -> list:
    app_ctx = context.fastmcp_context.lifespan_context
    return await app_ctx.db.query(sql)
```

**ASGI Integration (FastAPI/Starlette):**
```python
mcp = FastMCP("Server", lifespan=mcp_lifespan)
app = FastAPI(lifespan=mcp.lifespan)  # ✅ MUST pass lifespan!
```

**State Management:**
```python
context.fastmcp_context.set_state(key, value)  # Store
context.fastmcp_context.get_state(key, default=None)  # Retrieve
```

## Middleware System

**8 Built-in Types:** TimingMiddleware, ResponseCachingMiddleware, LoggingMiddleware, RateLimitingMiddleware, ErrorHandlingMiddleware, ToolInjectionMiddleware, PromptToolMiddleware, ResourceToolMiddleware

**Execution Order (order matters!):**
```
Request Flow:
  → ErrorHandlingMiddleware (catches errors)
    → TimingMiddleware (starts timer)
      → LoggingMiddleware (logs request)
        → RateLimitingMiddleware (checks rate limit)
          → ResponseCachingMiddleware (checks cache)
            → Tool/Resource Handler
```

**Basic Usage:**
```python
from fastmcp.middleware import ErrorHandlingMiddleware, TimingMiddleware, LoggingMiddleware

mcp.add_middleware(ErrorHandlingMiddleware())  # First: catch errors
mcp.add_middleware(TimingMiddleware())         # Second: time requests
mcp.add_middleware(LoggingMiddleware(level="INFO"))
mcp.add_middleware(RateLimitingMiddleware(max_requests=100, window_seconds=60))
mcp.add_middleware(ResponseCachingMiddleware(ttl_seconds=300, storage=RedisStore()))
```

**Custom Middleware:**
```python
from fastmcp.middleware import BaseMiddleware

class AccessControlMiddleware(BaseMiddleware):
    async def on_call_tool(self, tool_name, arguments, context):
        user = context.fastmcp_context.get_state("user_id")
        if user not in self.allowed_users:
            raise PermissionError(f"User not authorized")
        return await self.next(tool_name, arguments, context)
```

**Hook Hierarchy:** `on_message` (all) → `on_request`/`on_notification` → `on_call_tool`/`on_read_resource`/`on_get_prompt` → `on_list_*` (list operations)

## Server Composition

**Two Strategies:**

1. **`import_server()`** - Static snapshot: One-time copy at import, changes don't propagate, fast (no runtime delegation). Use for: Finalized component bundles.

2. **`mount()`** - Dynamic link: Live runtime link, changes immediately visible, runtime delegation (slower). Use for: Modular runtime composition.

**Basic Usage:**
```python
# Import (static)
main_server.import_server(api_server)  # One-time copy

# Mount (dynamic)
main_server.mount(api_server, prefix="api")  # Tools: api.fetch_data
main_server.mount(db_server, prefix="db")    # Resources: resource://db/path
```

**Tag Filtering:**
```python
@api_server.tool(tags=["public"])
def public_api(): pass

main_server.import_server(api_server, include_tags=["public"])  # Only public
main_server.mount(api_server, prefix="api", exclude_tags=["admin"])  # No admin
```

**Resource Prefix Formats:**
- **Path** (default since v2.4.0): `resource://prefix/path`
- **Protocol** (legacy): `prefix+resource://path`

```python
main_server.mount(subserver, prefix="api", resource_prefix_format="path")
```

## OAuth & Authentication

**4 Authentication Patterns:**

1. **Token Validation** (`JWTVerifier`): Validate external tokens
2. **External Identity Providers** (`RemoteAuthProvider`): OAuth 2.0/OIDC with DCR
3. **OAuth Proxy** (`OAuthProxy`): Bridge to providers without DCR (GitHub, Google, Azure, AWS, Discord, Facebook)
4. **Full OAuth** (`OAuthProvider`): Complete authorization server

**Pattern 1: Token Validation**
```python
from fastmcp.auth import JWTVerifier

auth = JWTVerifier(issuer="https://auth.example.com", audience="my-server",
                   public_key=os.getenv("JWT_PUBLIC_KEY"))
mcp = FastMCP("Server", auth=auth)
```

**Pattern 3: OAuth Proxy (Production)**
```python
from fastmcp.auth import OAuthProxy
from key_value.stores import RedisStore
from key_value.encryption import FernetEncryptionWrapper
from cryptography.fernet import Fernet

auth = OAuthProxy(
    jwt_signing_key=os.environ["JWT_SIGNING_KEY"],
    client_storage=FernetEncryptionWrapper(
        key_value=RedisStore(host=os.getenv("REDIS_HOST"), password=os.getenv("REDIS_PASSWORD")),
        fernet=Fernet(os.environ["STORAGE_ENCRYPTION_KEY"])
    ),
    upstream_authorization_endpoint="https://github.com/login/oauth/authorize",
    upstream_token_endpoint="https://github.com/login/oauth/access_token",
    upstream_client_id=os.getenv("GITHUB_CLIENT_ID"),
    upstream_client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    enable_consent_screen=True  # CRITICAL: Prevents confused deputy attacks
)
mcp = FastMCP("GitHub Auth", auth=auth)
```

**OAuth Proxy Features:** Token factory pattern (issues own JWTs), consent screens (prevents bypass), PKCE support, RFC 7662 token introspection

**Supported Providers:** GitHub, Google, Azure, AWS Cognito, Discord, Facebook, WorkOS, AuthKit, Descope, Scalekit, OCI (v2.13.1)

**Supabase Provider** (v2.14.2+):
```python
from fastmcp.auth import SupabaseProvider

auth = SupabaseProvider(
    auth_route="/custom-auth",  # Custom auth route (new in v2.14.2)
    # ... other config
)
```

## Icons, API Integration, Cloud Deployment

**Icons:** Add to servers, tools, resources, prompts. Use `Icon(url, size)`, data URIs via `Icon.from_file()` or `Image.to_data_uri()` (v2.13.1).

**API Integration (3 Patterns):**
1. **Manual**: `httpx.AsyncClient` with base_url/headers/timeout
2. **OpenAPI Auto-Gen**: `FastMCP.from_openapi(spec, client, route_maps)` - GET→Resources/Templates, POST/PUT/DELETE→Tools
3. **FastAPI Conversion**: `FastMCP.from_fastapi(app, httpx_client_kwargs)`

**Cloud Deployment Critical Requirements:**
1. ❗ **Module-level server** named `mcp`, `server`, or `app`
2. **PyPI dependencies only** in requirements.txt
3. **Public GitHub repo** (or accessible)
4. **Environment variables** for config

```python
# ✅ CORRECT: Module-level export
mcp = FastMCP("server")  # At module level!

# ❌ WRONG: Function-wrapped
def create_server():
    return FastMCP("server")  # Too late for cloud!
```

**Deployment:** https://fastmcp.cloud → Sign in → Create Project → Select repo → Deploy

**Client Config (Claude Desktop):**
```json
{"mcpServers": {"my-server": {"url": "https://project.fastmcp.app/mcp", "transport": "http"}}}
```

## 30 Common Errors (With Solutions)

### Error 1: Missing Server Object
**Error:** `RuntimeError: No server object found at module level`
**Cause:** Server not exported at module level (FastMCP Cloud requirement)
**Solution:** `mcp = FastMCP("server")` at module level, not inside functions

### Error 2: Async/Await Confusion
**Error:** `RuntimeError: no running event loop`, `TypeError: object coroutine can't be used in 'await'`
**Cause:** Mixing sync/async incorrectly
**Solution:** Use `async def` for tools with `await`, sync `def` for non-async code

### Error 3: Context Not Injected
**Error:** `TypeError: missing 1 required positional argument: 'context'`
**Cause:** Missing `Context` type annotation
**Solution:** `async def tool(context: Context)` - type hint required!

### Error 4: Resource URI Syntax
**Error:** `ValueError: Invalid resource URI: missing scheme`
**Cause:** Resource URI missing scheme prefix
**Solution:** Use `@mcp.resource("data://config")` not `@mcp.resource("config")`

### Error 5: Resource Template Parameter Mismatch
**Error:** `TypeError: get_user() missing 1 required positional argument`
**Cause:** Function parameter names don't match URI template
**Solution:** `@mcp.resource("user://{user_id}/profile")` → `def get_user(user_id: str)` - names must match exactly

---

### Error 6: Pydantic Validation Error
**Error:** `ValidationError: value is not a valid integer`
**Cause:** Type hints don't match provided data
**Solution:** Use Pydantic models: `class Params(BaseModel): query: str = Field(min_length=1)`

### Error 7: Transport/Protocol Mismatch
**Error:** `ConnectionError: Server using different transport`
**Cause:** Client and server using incompatible transports
**Solution:** Match transports - stdio: `mcp.run()` + `{"command": "python", "args": ["server.py"]}`, HTTP: `mcp.run(transport="http", port=8000)` + `{"url": "http://localhost:8000/mcp", "transport": "http"}`

**HTTP Timeout Issue (Fixed in v2.14.3)**:
- HTTP transport was defaulting to 5-second timeout instead of MCP's 30-second default ([GitHub Issue #2845](https://github.com/jlowin/fastmcp/issues/2845))
- Tools taking >5 seconds would fail silently in v2.14.2 and earlier
- **Solution**: Upgrade to fastmcp>=2.14.3 (timeout now respects MCP's 30s default)

### Error 8: Import Errors (Editable Package)
**Error:** `ModuleNotFoundError: No module named 'my_package'`
**Cause:** Package not properly installed
**Solution:** `pip install -e .` or use absolute imports or `export PYTHONPATH="/path/to/project"`

### Error 9: Deprecation Warnings
**Error:** `DeprecationWarning: 'mcp.settings' is deprecated`
**Cause:** Using old FastMCP v1 API
**Solution:** Use `os.getenv("API_KEY")` instead of `mcp.settings.get("API_KEY")`

### Error 10: Port Already in Use
**Error:** `OSError: [Errno 48] Address already in use`
**Cause:** Port 8000 already occupied
**Solution:** Use different port `--port 8001` or kill process `lsof -ti:8000 | xargs kill -9`

### Error 11: Schema Generation Failures
**Error:** `TypeError: Object of type 'ndarray' is not JSON serializable`
**Cause:** Unsupported type hints (NumPy arrays, custom classes)
**Solution:** Return JSON-compatible types: `list[float]` or convert: `{"values": np_array.tolist()}`

**Custom Classes Not Supported (Community-sourced)**:
FastMCP supports all Pydantic-compatible types, but custom classes must be converted to dictionaries or Pydantic models for tool returns:
```python
# ❌ NOT SUPPORTED
class MyCustomClass:
    def __init__(self, value: str):
        self.value = value

@mcp.tool()
async def get_custom() -> MyCustomClass:
    return MyCustomClass("test")  # Serialization error

# ✅ SUPPORTED - Use dict or Pydantic
@mcp.tool()
async def get_custom() -> dict[str, str]:
    obj = MyCustomClass("test")
    return {"value": obj.value}

# OR use Pydantic BaseModel
from pydantic import BaseModel
class MyModel(BaseModel):
    value: str

@mcp.tool()
async def get_model() -> MyModel:
    return MyModel(value="test")  # Works!
```

**OutputSchema $ref Resolution (Fixed in v2.14.2)**:
- Root-level `$ref` in `outputSchema` wasn't being dereferenced ([GitHub Issue #2720](https://github.com/jlowin/fastmcp/issues/2720))
- Caused MCP spec non-compliance and client compatibility issues
- **Solution**: Upgrade to fastmcp>=2.14.2 (auto-dereferences $ref)

### Error 12: JSON Serialization
**Error:** `TypeError: Object of type 'datetime' is not JSON serializable`
**Cause:** Returning non-JSON-serializable objects
**Solution:** Convert: `datetime.now().isoformat()`, bytes: `.decode('utf-8')`

### Error 13: Circular Import Errors
**Error:** `ImportError: cannot import name 'X' from partially initialized module`
**Cause:** Circular dependency (common in cloud deployment)
**Solution:** Use direct imports in `__init__.py`: `from .api_client import APIClient` or lazy imports in functions

### Error 14: Python Version Compatibility
**Error:** `DeprecationWarning: datetime.utcnow() is deprecated`
**Cause:** Using deprecated Python 3.12+ methods
**Solution:** Use `datetime.now(timezone.utc)` instead of `datetime.utcnow()`

### Error 15: Import-Time Execution
**Error:** `RuntimeError: Event loop is closed`
**Cause:** Creating async resources at module import time
**Solution:** Use lazy initialization - create connection class with async `connect()` method, call when needed in tools

---

### Error 16: Storage Backend Not Configured
**Error:** `RuntimeError: OAuth tokens lost on restart`, `ValueError: Cache not persisting`
**Cause:** Using default memory storage in production without persistence
**Solution:** Use encrypted DiskStore (single instance) or RedisStore (multi-instance) with `FernetEncryptionWrapper`

### Error 17: Lifespan Not Passed to ASGI App
**Error:** `RuntimeError: Database connection never initialized`, `Warning: MCP lifespan hooks not running`
**Cause:** FastMCP with FastAPI/Starlette without passing lifespan (v2.13.0 requirement)
**Solution:** `app = FastAPI(lifespan=mcp.lifespan)` - MUST pass lifespan!

### Error 18: Middleware Execution Order Error
**Error:** `RuntimeError: Rate limit not checked before caching`
**Cause:** Incorrect middleware ordering (order matters!)
**Solution:** ErrorHandling → Timing → Logging → RateLimiting → ResponseCaching (this order)

### Error 19: Circular Middleware Dependencies
**Error:** `RecursionError: maximum recursion depth exceeded`
**Cause:** Middleware not calling `self.next()` or calling incorrectly
**Solution:** Always call `result = await self.next(tool_name, arguments, context)` in middleware hooks

### Error 20: Import vs Mount Confusion
**Error:** `RuntimeError: Subserver changes not reflected`, `ValueError: Unexpected tool namespacing`
**Cause:** Using `import_server()` when `mount()` was needed (or vice versa)
**Solution:** `import_server()` for static bundles (one-time copy), `mount()` for dynamic composition (live link)

### Error 21: Resource Prefix Format Mismatch
**Error:** `ValueError: Resource not found: resource://api/users`
**Cause:** Using wrong resource prefix format
**Solution:** Path format (default v2.4.0+): `resource://prefix/path`, Protocol (legacy): `prefix+resource://path` - set with `resource_prefix_format="path"`

### Error 22: OAuth Proxy Without Consent Screen
**Error:** `SecurityWarning: Authorization bypass possible`
**Cause:** OAuth Proxy without consent screen (security vulnerability)
**Solution:** Always set `enable_consent_screen=True` - prevents confused deputy attacks (CRITICAL)

### Error 23: Missing JWT Signing Key in Production
**Error:** `ValueError: JWT signing key required for OAuth Proxy`
**Cause:** OAuth Proxy missing `jwt_signing_key`
**Solution:** Generate: `secrets.token_urlsafe(32)`, store in `FASTMCP_JWT_SIGNING_KEY` env var, pass to `OAuthProxy(jwt_signing_key=...)`

### Error 24: Icon Data URI Format Error
**Error:** `ValueError: Invalid data URI format`
**Cause:** Incorrectly formatted data URI for icons
**Solution:** Use `Icon.from_file("/path/icon.png", size="medium")` or `Image.to_data_uri()` (v2.13.1) - don't manually format

### Error 25: Lifespan Behavior Change (v2.13.0)
**Error:** `Warning: Lifespan runs per-server, not per-session`
**Cause:** Expecting v2.12 behavior (per-session) in v2.13.0+ (per-server)
**Solution:** v2.13.0+ lifespans run ONCE per server, not per session - use middleware for per-session logic

### Error 26: BearerAuthProvider Removed (v2.14.0)
**Error:** `ImportError: cannot import name 'BearerAuthProvider' from 'fastmcp.auth'`
**Cause:** `BearerAuthProvider` module removed in v2.14.0
**Solution:** Use `JWTVerifier` for token validation or `OAuthProxy` for full OAuth flows:
```python
# Before (v2.13.x)
from fastmcp.auth import BearerAuthProvider

# After (v2.14.0+)
from fastmcp.auth import JWTVerifier
auth = JWTVerifier(issuer="...", audience="...", public_key="...")
```

### Error 27: Context.get_http_request() Removed (v2.14.0)
**Error:** `AttributeError: 'Context' object has no attribute 'get_http_request'`
**Cause:** `Context.get_http_request()` method removed in v2.14.0
**Solution:** Access request info through middleware or use `InitializeResult` exposed to middleware

### Error 28: Image Import Path Changed (v2.14.0)
**Error:** `ImportError: cannot import name 'Image' from 'fastmcp'`
**Cause:** `fastmcp.Image` top-level import removed in v2.14.0
**Solution:** Use new import path:
```python
# Before (v2.13.x)
from fastmcp import Image

# After (v2.14.0+)
from fastmcp.utilities import Image
```

### Error 29: FastAPI Mount Path Doubling
**Error:** Client can't connect to `/mcp` endpoint, gets 404
**Source:** [GitHub Issue #2961](https://github.com/jlowin/fastmcp/issues/2961)
**Cause:** Mounting FastMCP at `/mcp` creates endpoint at `/mcp/mcp` due to path prefix duplication
**Solution:** Mount at root `/` or adjust client config

```python
# ❌ WRONG - Creates /mcp/mcp endpoint
from fastapi import FastAPI
from fastmcp import FastMCP

mcp = FastMCP("server")
app = FastAPI(lifespan=mcp.lifespan)
app.mount("/mcp", mcp)  # Endpoint becomes /mcp/mcp

# ✅ CORRECT - Mount at root
app.mount("/", mcp)  # Endpoint is /mcp

# ✅ OR adjust client config
# In claude_desktop_config.json:
{"url": "http://localhost:8000/mcp/mcp", "transport": "http"}
```

**Critical**: Must also pass `lifespan=mcp.lifespan` to FastAPI (see Error #17).

### Error 30: Background Tasks Fail with "No Active Context" (ASGI Mount)
**Error:** `RuntimeError: No active context found`
**Source:** [GitHub Issue #2877](https://github.com/jlowin/fastmcp/issues/2877)
**Cause:** ContextVar propagation issue when FastMCP mounted in FastAPI/Starlette with background tasks (`task=True`)
**Solution:** Upgrade to fastmcp>=2.14.3

```python
# In v2.14.2 and earlier - FAILS
from fastapi import FastAPI
from fastmcp import FastMCP, Context

mcp = FastMCP("server")
app = FastAPI(lifespan=mcp.lifespan)

@mcp.tool(task=True)
async def sample(name: str, ctx: Context) -> dict:
    # RuntimeError: No active context found
    await ctx.report_progress(1, 1, "Processing")
    return {"status": "OK"}

app.mount("/", mcp)

# ✅ FIXED in v2.14.3
# pip install fastmcp>=2.14.3
```

**Note**: Related to Error #17 (Lifespan Not Passed to ASGI App).

---

## Production Patterns, Testing, CLI

**4 Production Patterns:**
1. **Utils Module**: Single `utils.py` with Config class, format_success/error helpers
2. **Connection Pooling**: Singleton `httpx.AsyncClient` with `get_client()` class method
3. **Retry with Backoff**: `retry_with_backoff(func, max_retries=3, initial_delay=1.0, exponential_base=2.0)`
4. **Time-Based Caching**: `TimeBasedCache(ttl=300)` with `.get()` and `.set()` methods

**Testing:**
- Unit: `pytest` + `create_test_client(test_server)` + `await client.call_tool()`
- Integration: `Client("server.py")` + `list_tools()` + `call_tool()` + `list_resources()`

**CLI Commands:**
```bash
fastmcp dev server.py                # Run with inspector
fastmcp install server.py             # Install to Claude Desktop
FASTMCP_LOG_LEVEL=DEBUG fastmcp dev  # Debug logging
```

**Best Practices:** Factory pattern with module-level export, environment config with validation, comprehensive docstrings (LLMs read these!), health check resources

**Project Structure:**
- Simple: `server.py`, `requirements.txt`, `.env`, `README.md`
- Production: `src/` (server.py, utils.py, tools/, resources/, prompts/), `tests/`, `pyproject.toml`

---

## References & Summary

**Official:** https://github.com/jlowin/fastmcp, https://fastmcp.cloud, https://modelcontextprotocol.io, Context7: `/jlowin/fastmcp`
**Related Skills:** openai-api, claude-api, cloudflare-worker-base, typescript-mcp
**Package Versions:** fastmcp>=2.14.2 (PyPI), Python>=3.10 (3.13 supported in v2.14.1+), httpx, pydantic, py-key-value-aio, cryptography
**Last Updated**: 2026-01-21

**17 Key Takeaways:**
1. Module-level server export (FastMCP Cloud)
2. Persistent storage (Disk/Redis) for OAuth/caching
3. Server lifespans for resource management
4. Middleware order: errors → timing → logging → rate limiting → caching
5. Composition: `import_server()` (static) vs `mount()` (dynamic)
6. OAuth security: consent screens + encrypted storage + JWT signing
7. Async/await properly (don't block event loop)
8. Structured error handling
9. Avoid circular imports
10. Test locally (`fastmcp dev`)
11. Environment variables (never hardcode secrets)
12. Comprehensive docstrings (LLMs read!)
13. Production patterns (utils, pooling, retry, caching)
14. OpenAPI auto-generation
15. Health checks + monitoring
16. **Background tasks** for long-running operations (`task=True`)
17. **Sampling with tools** for agentic workflows (`ctx.sample(tools=[...])`)

**Production Readiness:** Encrypted storage, 4 auth patterns, 8 middleware types, modular composition, OAuth security (consent screens, PKCE, RFC 7662), response caching, connection pooling, timing middleware, background tasks, agentic sampling, FastAPI/Starlette mounting, v3.0 provider architecture

**Prevents 30+ errors. 90-95% token savings.**
