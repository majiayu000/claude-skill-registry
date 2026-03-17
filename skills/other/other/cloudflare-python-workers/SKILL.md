---
name: cloudflare-python-workers
description: |
  Build Python APIs on Cloudflare Workers using pywrangler CLI and WorkerEntrypoint class pattern. Includes Python Workflows for multi-step DAG automation. Prevents 11 documented errors.

  Use when: building Python serverless APIs, migrating Python to edge, or troubleshooting async errors, package compatibility, handler pattern mistakes, RPC communication issues.
user-invocable: true
---

# Cloudflare Python Workers

**Status**: Beta (requires `python_workers` compatibility flag)
**Runtime**: Pyodide (Python 3.12+ compiled to WebAssembly)
**Package Versions**: workers-py@1.7.0, workers-runtime-sdk@0.3.1, wrangler@4.58.0
**Last Verified**: 2026-01-21

## Quick Start (5 Minutes)

### 1. Prerequisites

Ensure you have installed:
- [uv](https://docs.astral.sh/uv/#installation) - Python package manager
- [Node.js](https://nodejs.org/) - Required for Wrangler

### 2. Initialize Project

```bash
# Create project directory
mkdir my-python-worker && cd my-python-worker

# Initialize Python project
uv init

# Install pywrangler
uv tool install workers-py

# Initialize Worker configuration
uv run pywrangler init
```

### 3. Create Entry Point

Create `src/entry.py`:

```python
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello from Python Worker!")
```

### 4. Configure wrangler.jsonc

```jsonc
{
  "name": "my-python-worker",
  "main": "src/entry.py",
  "compatibility_date": "2025-12-01",
  "compatibility_flags": ["python_workers"]
}
```

### 5. Run Locally

```bash
uv run pywrangler dev
# Visit http://localhost:8787
```

### 6. Deploy

```bash
uv run pywrangler deploy
```

---

## Migration from Pre-December 2025 Workers

If you created a Python Worker before December 2025, you were limited to built-in packages. With pywrangler (Dec 2025), you can now deploy with external packages.

**Old Approach** (no longer needed):
```python
# Limited to built-in packages only
# Could only use httpx, aiohttp, beautifulsoup4, etc.
# Error: "You cannot yet deploy Python Workers that depend on
# packages defined in requirements.txt [code: 10021]"
```

**New Approach** (pywrangler):
```toml
# pyproject.toml
[project]
dependencies = ["fastapi", "any-pyodide-compatible-package"]
```

```bash
uv tool install workers-py
uv run pywrangler deploy  # Now works!
```

**Historical Timeline**:
- **April 2024 - Dec 2025**: Package deployment completely blocked
- **Dec 8, 2025**: Pywrangler released, enabling package deployment
- **Jan 2026**: Open beta with full package support

**See**: [Package deployment issue history](https://github.com/cloudflare/workers-sdk/issues/6613)

---

## Core Concepts

### WorkerEntrypoint Class Pattern

As of August 2025, Python Workers use a class-based pattern (not global handlers):

```python
from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Access bindings via self.env
        value = await self.env.MY_KV.get("key")

        # Parse request
        url = request.url
        method = request.method

        return Response(f"Method: {method}, URL: {url}")
```

### Accessing Bindings

All Cloudflare bindings are accessed via `self.env`:

```python
class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # D1 Database
        result = await self.env.DB.prepare("SELECT * FROM users").all()

        # KV Storage
        value = await self.env.MY_KV.get("key")
        await self.env.MY_KV.put("key", "value")

        # R2 Object Storage
        obj = await self.env.MY_BUCKET.get("file.txt")

        # Workers AI
        response = await self.env.AI.run("@cf/meta/llama-2-7b-chat-int8", {
            "prompt": "Hello!"
        })

        return Response("OK")
```

**Supported Bindings**:
- D1 (SQL database)
- KV (key-value storage)
- R2 (object storage)
- Workers AI
- Vectorize
- Durable Objects
- Queues
- Analytics Engine

See [Cloudflare Bindings Documentation](https://developers.cloudflare.com/workers/runtime-apis/bindings/) for details.

### Request/Response Handling

```python
from workers import WorkerEntrypoint, Response
import json

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Parse JSON body
        if request.method == "POST":
            body = await request.json()
            return Response(
                json.dumps({"received": body}),
                headers={"Content-Type": "application/json"}
            )

        # Query parameters
        url = URL(request.url)
        name = url.searchParams.get("name", "World")

        return Response(f"Hello, {name}!")
```

### Scheduled Handlers (Cron)

```python
from workers import handler

@handler
async def on_scheduled(event, env, ctx):
    # Run on cron schedule
    print(f"Cron triggered at {event.scheduledTime}")

    # Do work...
    await env.MY_KV.put("last_run", str(event.scheduledTime))
```

Configure in wrangler.jsonc:

```jsonc
{
  "triggers": {
    "crons": ["*/5 * * * *"]  // Every 5 minutes
  }
}
```

---

## Python Workflows

Python Workflows enable durable, multi-step automation with automatic retries and state persistence.

### Why Decorator Pattern?

Python Workflows use the `@step.do()` decorator pattern because **Python does not easily support anonymous callbacks** (unlike JavaScript/TypeScript which allows inline arrow functions). This is a fundamental language difference, not a limitation of Cloudflare's implementation.

**JavaScript Pattern** (doesn't translate):
```javascript
await step.do("my step", async () => {
  // Inline callback
  return result;
});
```

**Python Pattern** (required):
```python
@step.do("my step")
async def my_step():
    # Named function with decorator
    return result

result = await my_step()
```

**Source**: [Python Workflows Blog](https://blog.cloudflare.com/python-workflows/)

### Concurrency with asyncio.gather

Pyodide captures JavaScript promises (thenables) and proxies them as Python awaitables. This enables `Promise.all`-equivalent behavior using standard Python async patterns:

```python
import asyncio

@step.do("step_a")
async def step_a():
    return "A"

@step.do("step_b")
async def step_b():
    return "B"

# Concurrent execution (like Promise.all)
results = await asyncio.gather(step_a(), step_b())
# results = ["A", "B"]
```

**Why This Works**: JavaScript promises from workflow steps are proxied as Python awaitables, allowing standard asyncio concurrency primitives.

**Source**: [Python Workflows Blog](https://blog.cloudflare.com/python-workflows/)

### Basic Workflow

```python
from workers import WorkflowEntrypoint, WorkerEntrypoint, Response

class MyWorkflow(WorkflowEntrypoint):
    async def run(self, event, step):
        # Step 1
        @step.do("fetch data")
        async def fetch_data():
            response = await fetch("https://api.example.com/data")
            return await response.json()

        data = await fetch_data()

        # Step 2: Sleep
        await step.sleep("wait", "10 seconds")

        # Step 3: Process
        @step.do("process data")
        async def process_data():
            return {"processed": True, "count": len(data)}

        result = await process_data()
        return result


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Create workflow instance
        instance = await self.env.MY_WORKFLOW.create()
        return Response(f"Workflow started: {instance.id}")
```

### DAG Dependencies

Define step dependencies for parallel execution:

```python
class MyWorkflow(WorkflowEntrypoint):
    async def run(self, event, step):
        @step.do("step_a")
        async def step_a():
            return "A done"

        @step.do("step_b")
        async def step_b():
            return "B done"

        # step_c waits for both step_a and step_b
        @step.do("step_c", depends=[step_a, step_b], concurrent=True)
        async def step_c(result_a, result_b):
            return f"C received: {result_a}, {result_b}"

        return await step_c()
```

### Workflow Configuration

```jsonc
{
  "compatibility_flags": ["python_workers", "python_workflows"],
  "compatibility_date": "2025-12-01",
  "workflows": [
    {
      "name": "my-workflow",
      "binding": "MY_WORKFLOW",
      "class_name": "MyWorkflow"
    }
  ]
}
```

---

## Package Management

### pyproject.toml Configuration

```toml
[project]
name = "my-python-worker"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "beautifulsoup4",
    "httpx"
]

[dependency-groups]
dev = [
    "workers-py",
    "workers-runtime-sdk"
]
```

### Supported Packages

Python Workers support:
- **Pure Python packages** from PyPI
- **Pyodide packages** (pre-built for WebAssembly)

See [Pyodide packages list](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

### HTTP Clients

Only **async** HTTP libraries work:

```python
# ✅ WORKS - httpx (async)
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")

# ✅ WORKS - aiohttp
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get("https://api.example.com") as response:
        data = await response.json()

# ❌ DOES NOT WORK - requests (sync)
import requests  # Will fail!
```

### Requesting New Packages

Request support for new packages at:
https://github.com/cloudflare/workerd/discussions/categories/python-packages

---

## FFI (Foreign Function Interface)

Access JavaScript APIs from Python via Pyodide's FFI:

### JavaScript Globals

```python
from js import fetch, console, Response as JSResponse

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Use JavaScript fetch
        response = await fetch("https://api.example.com")
        data = await response.json()

        # Console logging
        console.log("Fetched data:", data)

        # Return JavaScript Response
        return JSResponse.new("Hello!")
```

### Type Conversions

**Important**: `to_py()` is a METHOD on JavaScript objects, not a standalone function. Only `to_js()` is a function.

```python
from js import Object
from pyodide.ffi import to_js

# ❌ WRONG - ImportError!
from pyodide.ffi import to_py
python_data = to_py(js_data)

# ✅ CORRECT - to_py() is a method
async def fetch(self, request):
    data = await request.json()  # Returns JS object
    python_data = data.to_py()   # Convert to Python dict

# Convert Python dict to JavaScript object
python_dict = {"name": "test", "count": 42}
js_object = to_js(python_dict, dict_converter=Object.fromEntries)

# Use in Response
return Response(to_js({"status": "ok"}))
```

**Source**: [GitHub Issue #3322](https://github.com/cloudflare/workerd/issues/3322) (Pyodide maintainer clarification)

---

## Known Issues Prevention

This skill prevents **11 documented issues**:

### Issue #1: Legacy Handler Pattern

**Error**: `TypeError: on_fetch is not defined`

**Why**: Handler pattern changed in August 2025.

```python
# ❌ OLD (deprecated)
@handler
async def on_fetch(request):
    return Response("Hello")

# ✅ NEW (current)
class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response("Hello")
```

### Issue #2: Sync HTTP Libraries

**Error**: `RuntimeError: cannot use blocking call in async context`

**Why**: Python Workers run async-only. Sync libraries block the event loop.

```python
# ❌ FAILS
import requests
response = requests.get("https://api.example.com")

# ✅ WORKS
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get("https://api.example.com")
```

### Issue #3: Native/Compiled Packages

**Error**: `ModuleNotFoundError: No module named 'numpy'` (or similar)

**Why**: Only pure Python packages work. Native C extensions are not supported.

**Solution**: Use Pyodide-compatible alternatives or check [Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

### Issue #4: Missing Compatibility Flags

**Error**: `Error: Python Workers require the python_workers compatibility flag`

**Fix**: Add to wrangler.jsonc:

```jsonc
{
  "compatibility_flags": ["python_workers"]
}
```

For Workflows, also add `"python_workflows"`.

### Issue #5: I/O Outside Workflow Steps

**Error**: Workflow state not persisted correctly

**Why**: All I/O must happen inside `@step.do` for durability.

```python
# ❌ BAD - fetch outside step
response = await fetch("https://api.example.com")
@step.do("use data")
async def use_data():
    return await response.json()  # response may be stale on retry

# ✅ GOOD - fetch inside step
@step.do("fetch and use")
async def fetch_and_use():
    response = await fetch("https://api.example.com")
    return await response.json()
```

### Issue #6: Type Serialization Errors

**Error**: `TypeError: Object of type X is not JSON serializable`

**Why**: Workflow step return values must be JSON-serializable.

**Fix**: Convert complex objects before returning:

```python
@step.do("process")
async def process():
    # Convert datetime to string
    return {"timestamp": datetime.now().isoformat()}
```

### Issue #7: Cold Start Performance

**Note**: Python Workers have higher cold starts than JavaScript. With Wasm memory snapshots (Dec 2025), heavy packages like FastAPI and Pydantic now load in **~1 second** (down from ~10 seconds previously), but this is still ~2x slower than JavaScript Workers (~50ms).

**Performance Numbers** (as of Dec 2025):
- **Before snapshots**: ~10 seconds for FastAPI/Pydantic
- **After snapshots**: ~1 second (10x improvement)
- **JavaScript equivalent**: ~50ms

**Mitigation**:
- Minimize top-level imports
- Use lazy loading for heavy packages
- Consider JavaScript Workers for latency-critical paths
- Wasm snapshots automatically improve cold starts (no config needed)

**Source**: [Python Workers Redux Blog](https://blog.cloudflare.com/python-workers-advancements/) | [InfoQ Coverage](https://www.infoq.com/news/2025/12/cloudflare-wasm-python-snapshot/)

### Issue #8: Package Installation Failures

**Error**: `Failed to install package X`

**Causes**:
- Package has native dependencies
- Package not in Pyodide ecosystem
- Network issues during bundling

**Fix**: Check package compatibility, use alternatives, or request support.

### Issue #9: Dev Registry Breaks JS-to-Python RPC

**Error**: `Network connection lost` when calling Python Worker from JavaScript Worker
**Source**: [GitHub Issue #11438](https://github.com/cloudflare/workers-sdk/issues/11438)

**Why It Happens**: Dev registry doesn't properly route RPC calls between separately-run Workers in different terminals.

**Prevention**:
```bash
# ❌ Doesn't work - separate terminals
# Terminal 1: npx wrangler dev (JS worker)
# Terminal 2: npx wrangler dev (Python worker)
# Result: Network connection lost error

# ✅ Works - single wrangler instance
npx wrangler dev -c ts/wrangler.jsonc -c py/wrangler.jsonc
```

Run both workers in a single wrangler instance to enable proper RPC communication.

### Issue #10: HTMLRewriter Memory Limit with Data URLs

**Error**: `TypeError: Parser error: The memory limit has been exceeded`
**Source**: [GitHub Issue #10814](https://github.com/cloudflare/workers-sdk/issues/10814)

**Why It Happens**: Large inline `data:` URLs (>10MB) in HTML trigger parser memory limits. This is NOT about response size—10MB plain text works fine, but 10MB HTML with embedded data URLs fails. Common with Python Jupyter Notebooks that use inline images for plots.

**Prevention**:
```python
# ❌ FAILS - HTMLRewriter triggered on notebook HTML with data: URLs
response = await fetch("https://origin.example.com/notebook.html")
return response  # Crashes if HTML contains large data: URLs

# ✅ WORKS - Stream directly or use text/plain
response = await fetch("https://origin.example.com/notebook.html")
headers = {"Content-Type": "text/plain"}  # Bypass parser
return Response(await response.text(), headers=headers)
```

**Workarounds**:
- Avoid HTMLRewriter on notebook content (stream directly)
- Pre-process notebooks to extract data URLs to external files
- Use `text/plain` content-type to bypass parser

### Issue #11: PRNG Cannot Be Seeded During Initialization

**Error**: Deployment fails with user error
**Source**: [Python Workers Redux Blog](https://blog.cloudflare.com/python-workers-advancements/)

**Why It Happens**: Wasm snapshots don't support PRNG initialization before request handlers. If you call pseudorandom number generator APIs (like `random.seed()`) during module initialization, deployment FAILS.

**Prevention**:
```python
import random

# ❌ FAILS deployment - module-level PRNG call
random.seed(42)

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return Response(str(random.randint(1, 100)))

# ✅ WORKS - PRNG calls inside handlers
class Default(WorkerEntrypoint):
    async def fetch(self, request):
        random.seed(42)  # Initialize inside handler
        return Response(str(random.randint(1, 100)))
```

Only call PRNG functions inside request handlers, not at module level.

---

## Best Practices

### Always Do

- Use `WorkerEntrypoint` class pattern
- Use async HTTP clients (httpx, aiohttp)
- Put all I/O inside workflow steps
- Add `python_workers` compatibility flag
- Use `self.env` for all bindings
- Return JSON-serializable data from workflow steps

### Never Do

- Use sync HTTP libraries (requests)
- Use native/compiled packages
- Perform I/O outside workflow steps
- Use legacy `@handler` decorator for fetch
- Expect JavaScript-level cold start times

---

## Framework Note: FastAPI

FastAPI can work with Python Workers but with limitations:

```python
from fastapi import FastAPI
from workers import WorkerEntrypoint

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        # Route through FastAPI
        return await app(request)
```

**Limitations**:
- Async-only (no sync endpoints)
- No WSGI middleware
- Beta stability

See [Cloudflare FastAPI example](https://developers.cloudflare.com/workers/languages/python/) for details.

---

## Official Documentation

- [Python Workers Overview](https://developers.cloudflare.com/workers/languages/python/)
- [Python Workers Basics](https://developers.cloudflare.com/workers/languages/python/basics/)
- [How Python Workers Work](https://developers.cloudflare.com/workers/languages/python/how-python-workers-work/)
- [Python Packages](https://developers.cloudflare.com/workers/languages/python/packages/)
- [FFI (Foreign Function Interface)](https://developers.cloudflare.com/workers/languages/python/ffi/)
- [Python Workflows](https://developers.cloudflare.com/workflows/python/)
- [Pywrangler CLI](https://github.com/cloudflare/workers-py)
- [Pyodide Package List](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)

---

## Dependencies

```json
{
  "workers-py": "1.7.0",
  "workers-runtime-sdk": "0.3.1",
  "wrangler": "4.58.0"
}
```

**Note**: Always pin versions for reproducible builds. Check [PyPI workers-py](https://pypi.org/project/workers-py/) for latest releases.

---

## Production Validation

- Cloudflare changelog: Dec 8, 2025 (Pywrangler + cold start improvements)
- workers-py 1.7.0: Latest stable (Jan 2026)
- Python Workflows beta: Aug 22, 2025
- Handler pattern change: Aug 14, 2025

**Compatibility Date Guidance**:
- Use `2025-12-01` for new projects (latest features including pywrangler improvements)
- Use `2025-08-01` only if you need to match older production Workers
