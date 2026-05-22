---
name: FastMCP Development
description: Use when creating or modifying Model Context Protocol (MCP) servers with FastMCP framework - guides through tools, resources, prompts, authentication, Claude Desktop integration, and production deployment with Python and TypeScript examples
---

<required>
*CRITICAL* Add the following steps to your Todo list using TodoWrite:

1. Determine server purpose and required components (tools, resources, prompts)

Ask: What functionality does this MCP server provide? What external systems will it integrate with?

2. Create FastMCP server file with basic structure

Use Quick Start template below. Choose Python or TypeScript based on project requirements.

3. Implement tools for LLM-executable functions

Follow Tools section. Include type hints/annotations, validation, error handling.

4. Add resources if data access needed

Follow Resources section. Use URI templates for dynamic resources. Include security validation.

5. Add prompts if workflow guidance needed

Follow Prompts section. Use for multi-step workflows, best practices, templates.

6. Configure Claude Desktop integration

Follow Claude Desktop Integration section. Use fastmcp CLI or manual config. Handle environment variables.

7. Test server locally

Run server in STDIO mode. Test with FastMCP client or Claude Desktop locally.

8. Add authentication for production

Follow Authentication section. Use OAuth for enterprise, token verification for custom auth.

9. Deploy using appropriate transport

STDIO for local tools, HTTP/SSE for network access. Follow Deployment section.

10. Verify integration end-to-end

Test in Claude Desktop. Verify tools appear, resources load, prompts work.

</required>

# When to Use This Skill

**Use this skill when:**
- Creating new MCP servers with FastMCP
- Adding tools, resources, or prompts to existing servers
- Integrating MCP servers with Claude Desktop
- Implementing authentication for production MCP servers
- Deploying MCP servers via STDIO, HTTP, or SSE transports
- Migrating from FastMCP v2 to v3
- Creating custom domain-specific MCP integrations

**Do NOT use this skill when:**
- Building MCP servers in languages other than Python or TypeScript (use official SDK)
- You need maximum control over MCP protocol implementation (use official SDK)
- Creating simple command-line tools without LLM integration (FastMCP is overkill)

# Quick Start

## Minimal Python Example

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo Server 🚀")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.resource("greeting://hello")
def get_greeting() -> str:
    """Get a friendly greeting"""
    return "Hello from FastMCP!"

if __name__ == "__main__":
    mcp.run()
```

**Run it:**
```bash
python server.py
```

## Minimal TypeScript Example

```typescript
import { FastMCP } from "@fastmcp/server";

const mcp = new FastMCP("Demo Server 🚀");

mcp.tool({
  name: "add",
  description: "Add two numbers together",
  parameters: {
    a: { type: "number", description: "First number" },
    b: { type: "number", description: "Second number" }
  },
  execute: async ({ a, b }) => a + b
});

mcp.resource({
  uri: "greeting://hello",
  name: "Greeting",
  description: "Get a friendly greeting",
  read: async () => "Hello from FastMCP!"
});

mcp.run();
```

**Run it:**
```bash
npm install @fastmcp/server
node server.js
```

## Claude Desktop Installation

**Using fastmcp CLI (Recommended):**
```bash
fastmcp install claude-desktop server.py
```

**Manual config** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "--with", "fastmcp", "fastmcp", "run", "/absolute/path/to/server.py"],
      "env": {}
    }
  }
}
```

**Verify**: Restart Claude Desktop, look for hammer icon (🔨) in input box.

---

# Core Concepts

## Tools - LLM-Executable Functions

**What are tools?** Python/TypeScript functions that LLMs can execute to interact with external systems, run code, and access data.

### Python Tool Implementation

```python
from fastmcp import FastMCP, Context
from typing import Annotated
from pydantic import Field

mcp = FastMCP("Data Server")

@mcp.tool(
    description="Analyze dataset statistics",
    tags={"analysis", "statistics"},
    timeout=60.0,
    annotations={"readOnlyHint": True}  # Enables caching, skips confirmation
)
async def analyze_dataset(
    data: Annotated[list[float], Field(description="Numbers to analyze")],
    percentiles: Annotated[list[int], Field(ge=0, le=100)] = [25, 50, 75],
    ctx: Context = None  # Injected automatically
) -> dict:
    """Compute statistical analysis of numeric data."""
    await ctx.info(f"Analyzing {len(data)} data points")
    await ctx.report_progress(progress=50, total=100)

    import statistics
    return {
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "stdev": statistics.stdev(data) if len(data) > 1 else 0,
        "percentiles": {p: sorted(data)[int(len(data) * p / 100)] for p in percentiles}
    }
```

### TypeScript Tool Implementation

```typescript
import { FastMCP, Context } from "@fastmcp/server";

const mcp = new FastMCP("Data Server");

mcp.tool({
  name: "analyze_dataset",
  description: "Compute statistical analysis of numeric data",
  parameters: {
    data: {
      type: "array",
      items: { type: "number" },
      description: "Numbers to analyze"
    },
    percentiles: {
      type: "array",
      items: { type: "number", minimum: 0, maximum: 100 },
      default: [25, 50, 75],
      description: "Percentiles to calculate"
    }
  },
  annotations: { readOnlyHint: true },
  execute: async ({ data, percentiles }, ctx: Context) => {
    await ctx.info(`Analyzing ${data.length} data points`);
    await ctx.reportProgress(50, 100);

    const sorted = [...data].sort((a, b) => a - b);
    const mean = data.reduce((a, b) => a + b) / data.length;
    const median = sorted[Math.floor(sorted.length / 2)];

    return {
      mean,
      median,
      stdev: calculateStdev(data, mean),
      percentiles: Object.fromEntries(
        percentiles.map(p => [p, sorted[Math.floor(sorted.length * p / 100)]])
      )
    };
  }
});
```

### Tool Annotations for Client Behavior

```python
annotations={
    "readOnlyHint": True,      # Skip confirmation, enable caching
    "destructiveHint": True,   # Warn users before execution
    "idempotentHint": True,    # Safe to retry
    "openWorldHint": True      # Accesses unpredictable external data
}
```

### Tool Error Handling

```python
from fastmcp import ToolError

@mcp.tool()
def query_database(sql: str) -> list[dict]:
    """Execute read-only SQL queries"""
    if not sql.upper().startswith("SELECT"):
        raise ToolError("Only SELECT queries allowed")

    try:
        return execute_query(sql)
    except DatabaseError as e:
        raise ToolError(f"Query failed: {str(e)}")
```

---

## Resources - Read-Only Data Access

**What are resources?** Data or files that MCP clients can read - like GET endpoints in REST APIs, providing data without side effects.

### Static Python Resource

```python
from fastmcp.resources import TextResource

mcp.add_resource(
    TextResource(
        uri="config://database",
        name="Database Config",
        description="Current database configuration",
        text='{"host": "localhost", "port": 5432}'
    )
)
```

### Dynamic Python Resource with URI Templates

```python
from fastmcp.resources import ResourceResult, ResourceContent

# Simple parameter (single path segment)
@mcp.resource("weather://{city}/current")
async def get_weather(city: str) -> str:
    """Get current weather for a city"""
    if not is_valid_city(city):
        raise ResourceError(f"Invalid city: {city}")

    data = await fetch_weather(city)
    return json.dumps({"city": city, "temp": data.temp, "conditions": data.conditions})

# Wildcard parameter (multiple segments)
@mcp.resource("path://{filepath*}")
async def get_file_content(filepath: str, ctx: Context) -> str:
    """Read file contents with security validation"""
    # Matches: path://docs/server/resources.mdx
    full_path = os.path.abspath(filepath)

    # Security: Prevent directory traversal
    if not full_path.startswith(ALLOWED_BASE_PATH):
        raise ResourceError("Access denied: path outside allowed directory")

    if not os.path.exists(full_path):
        raise ResourceError(f"File not found: {filepath}")

    await ctx.info(f"Reading file: {filepath}")

    async with aiofiles.open(full_path, 'r') as f:
        content = await f.read()

    return content

# Query parameters (optional configuration)
@mcp.resource("data://{id}{?format}")
def get_data(id: str, format: str = "json") -> str:
    """Get data in specified format"""
    # Matches: data://123?format=xml
    data = fetch_data(id)
    if format == "xml":
        return convert_to_xml(data)
    return json.dumps(data)
```

### TypeScript Resource with URI Templates

```typescript
mcp.resource({
  uri: "weather://{city}/current",
  name: "Current Weather",
  description: "Get current weather for a city",
  read: async ({ city }, ctx) => {
    if (!isValidCity(city)) {
      throw new ResourceError(`Invalid city: ${city}`);
    }

    const data = await fetchWeather(city);
    return JSON.stringify({ city, temp: data.temp, conditions: data.conditions });
  }
});

// File system resource with security
mcp.resource({
  uri: "path://{filepath*}",
  name: "File Content",
  description: "Read file contents",
  read: async ({ filepath }, ctx) => {
    const fullPath = path.resolve(filepath);

    // Security: Prevent directory traversal
    if (!fullPath.startsWith(ALLOWED_BASE_PATH)) {
      throw new ResourceError("Access denied");
    }

    await ctx.info(`Reading file: ${filepath}`);
    return await fs.promises.readFile(fullPath, 'utf-8');
  }
});
```

### Multiple Content Types

```python
@mcp.resource("data://users")
def get_users() -> ResourceResult:
    """Get user data in multiple formats"""
    return ResourceResult(
        contents=[
            ResourceContent(
                content='[{"id": 1, "name": "Alice"}]',
                mime_type="application/json"
            ),
            ResourceContent(
                content="# Users\nTotal: 1 user",
                mime_type="text/markdown"
            ),
        ],
        meta={"total": 1, "cached": True}
    )
```

---

## Prompts - Reusable Message Templates

**What are prompts?** Message templates that help LLMs generate structured, purposeful responses - "best practices encoded into your server."

### Basic Python Prompt

```python
from fastmcp import FastMCP
from fastmcp.prompts import Message, PromptResult

mcp = FastMCP("Prompt Server")

@mcp.prompt()
def ask_about_topic(topic: str) -> str:
    """Generate a user message asking for explanation"""
    return f"Can you please explain the concept of '{topic}' in simple terms?"
```

### Advanced Python Prompt with Multi-Message Conversation

```python
@mcp.prompt(
    name="code_review_workflow",
    description="Complete code review with security analysis",
    tags={"security", "code-quality"}
)
def code_review(code: str, language: str = "python") -> PromptResult:
    """Security-focused code review workflow"""
    return PromptResult(
        messages=[
            Message(
                role="user",
                content=f"Review this {language} code for security issues:\n```{language}\n{code}\n```"
            ),
            Message(
                role="assistant",
                content="I'll analyze this systematically for security vulnerabilities."
            ),
            Message(
                role="user",
                content="Focus especially on SQL injection, XSS, and authentication bypass."
            )
        ],
        description="Security-focused code review with systematic analysis",
        meta={"priority": "high", "review_type": "security"}
    )
```

### TypeScript Prompt Implementation

```typescript
mcp.prompt({
  name: "code_review_workflow",
  description: "Complete code review with security analysis",
  parameters: {
    code: { type: "string", description: "Code to review" },
    language: { type: "string", default: "python" }
  },
  execute: async ({ code, language }) => {
    return {
      messages: [
        {
          role: "user",
          content: `Review this ${language} code for security issues:\n\`\`\`${language}\n${code}\n\`\`\``
        },
        {
          role: "assistant",
          content: "I'll analyze this systematically for security vulnerabilities."
        },
        {
          role: "user",
          content: "Focus especially on SQL injection, XSS, and authentication bypass."
        }
      ],
      description: "Security-focused code review",
      meta: { priority: "high", review_type: "security" }
    };
  }
});
```

---

## Context - MCP Capabilities Access

**What is Context?** Dependency-injected object providing access to logging, progress tracking, resource/prompt management, LLM operations, and request metadata.

### Context Capabilities

| Category | Methods | Purpose |
|----------|---------|---------|
| **Logging** | `debug()`, `info()`, `warning()`, `error()` | Send log messages to clients |
| **Progress** | `report_progress(progress, total)` | Update clients on long-running ops |
| **Resources** | `list_resources()`, `read_resource(uri)` | Access other resources |
| **Prompts** | `list_prompts()`, `get_prompt(name, args)` | Retrieve prompt templates |
| **LLM** | `sample(prompt, temperature)` | Request client LLM generation |
| **User Input** | `elicit(question, response_type)` | Request structured user input |
| **State** | `set_state()`, `get_state()`, `delete_state()` | Persist data across requests |
| **Metadata** | `request_id`, `client_id`, `session_id` | Request context information |

### Python Context Example

```python
from fastmcp import FastMCP, Context
from fastmcp.dependencies import CurrentContext

@mcp.tool()
async def process_data(data_uri: str, ctx: Context = CurrentContext()) -> dict:
    """Process data with full context capabilities"""
    await ctx.info(f"Processing {data_uri}")

    # Read another resource
    resources = await ctx.read_resource(data_uri)
    content = resources[0].text

    # Report progress
    await ctx.report_progress(progress=25, total=100)

    # Use LLM for analysis
    summary = await ctx.sample(f"Summarize this data concisely: {content[:500]}")

    await ctx.report_progress(progress=75, total=100)

    # Store state for next request
    await ctx.set_state("last_processed", data_uri)

    await ctx.report_progress(progress=100, total=100)

    return {
        "result": summary.text,
        "request_id": ctx.request_id,
        "timestamp": ctx.timestamp
    }
```

### TypeScript Context Example

```typescript
mcp.tool({
  name: "process_data",
  description: "Process data with full context capabilities",
  parameters: {
    data_uri: { type: "string", description: "URI of data to process" }
  },
  execute: async ({ data_uri }, ctx) => {
    await ctx.info(`Processing ${data_uri}`);

    // Read resource
    const resources = await ctx.readResource(data_uri);
    const content = resources[0].text;

    // Report progress
    await ctx.reportProgress(25, 100);

    // Use LLM
    const summary = await ctx.sample(`Summarize this data: ${content.slice(0, 500)}`);

    await ctx.reportProgress(75, 100);

    // Store state
    await ctx.setState("last_processed", data_uri);

    await ctx.reportProgress(100, 100);

    return {
      result: summary.text,
      request_id: ctx.requestId,
      timestamp: ctx.timestamp
    };
  }
});
```

**Critical**: Context is scoped to a single request. State persists across requests, but context object itself is recreated per request.

---

# Claude Desktop Integration

## Installation Methods

### Method 1: FastMCP CLI (Recommended)

```bash
# Basic installation
fastmcp install claude-desktop server.py

# With dependencies
fastmcp install claude-desktop server.py \
    --with pandas \
    --with requests \
    --env API_KEY=your_key

# With requirements file
fastmcp install claude-desktop server.py \
    --with-requirements requirements.txt \
    --env-file .env
```

### Method 2: Manual Configuration

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": [
        "run",
        "--with", "fastmcp",
        "--with", "pandas",
        "fastmcp",
        "run",
        "/absolute/path/to/server.py"
      ],
      "env": {
        "API_KEY": "your_value",
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

**TypeScript/Node.js config:**
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/server.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

## Critical Requirements

⚠️ **Environment Isolation**: Claude Desktop runs servers in completely isolated environment with **no access to your shell environment**

⚠️ **Must explicitly pass environment variables** via `--env` or `--env-file`

⚠️ **Absolute paths required** for server files (relative paths will fail)

⚠️ **uv must be installed** and available in PATH for Python servers

## Verification

1. Save config file
2. **Restart Claude Desktop completely** (quit and reopen)
3. Look for hammer icon (🔨) in input box
4. Type a message to see if tools appear in suggestions

## Troubleshooting

**No hammer icon appears:**
- Check config file syntax (use JSON validator)
- Verify absolute path to server file
- Check `uv` is installed: `which uv`
- Look at Claude Desktop logs (Help → View Logs)

**Hammer icon appears but tools don't work:**
- Check environment variables are passed correctly
- Verify dependencies are installed
- Check server logs for errors
- Test server standalone: `python server.py`

**Environment variables not working:**
- Don't rely on shell environment (it won't be loaded)
- Pass ALL required env vars explicitly in config
- Use `--env-file` to load from `.env` file

---

# Authentication and Security

## Default is Insecure

⚠️ **FastMCP defaults to HTTP with no authentication or encryption**

🔒 **For production: ALWAYS use HTTPS/TLS and require authentication**

## OAuth Authentication (Python)

```python
from fastmcp import FastMCP
from fastmcp.auth import GoogleOAuth, GitHubOAuth, AzureOAuth

# Google OAuth
mcp = FastMCP(
    name="Secure Server",
    auth=GoogleOAuth(
        client_id="your-client-id.apps.googleusercontent.com",
        client_secret="your-client-secret"
    )
)

# GitHub OAuth
mcp = FastMCP(
    name="Secure Server",
    auth=GitHubOAuth(
        client_id="your-client-id",
        client_secret="your-client-secret"
    )
)

# Azure OAuth
mcp = FastMCP(
    name="Secure Server",
    auth=AzureOAuth(
        client_id="your-client-id",
        client_secret="your-client-secret",
        tenant_id="your-tenant-id"
    )
)
```

## Token Verification (Python)

```python
from fastmcp.auth import TokenVerifier

def verify_jwt(token: str) -> bool:
    """Verify JWT token against your auth system"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("authorized") == True
    except jwt.InvalidTokenError:
        return False

mcp = FastMCP(
    name="Secure Server",
    auth=TokenVerifier(verify_token=verify_jwt)
)
```

## TypeScript Authentication

```typescript
import { FastMCP } from "@fastmcp/server";
import { GoogleOAuth } from "@fastmcp/auth";

const mcp = new FastMCP({
  name: "Secure Server",
  auth: new GoogleOAuth({
    clientId: "your-client-id",
    clientSecret: "your-client-secret"
  })
});
```

## Security Best Practices

```python
mcp = FastMCP(
    name="Production Server",
    auth=GoogleOAuth(...),
    mask_error_details=True,  # Don't leak internal errors to clients
    allowed_origins=["https://your-domain.com"],  # CORS restrictions
    rate_limit={"requests_per_minute": 100}  # Rate limiting
)

@mcp.tool()
def query_database(sql: str) -> list[dict]:
    """Secure database query with validation"""
    # Input validation
    if not sql.upper().startswith("SELECT"):
        raise ToolError("Only SELECT queries allowed")

    # SQL injection prevention
    if any(keyword in sql.upper() for keyword in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        raise ToolError("Destructive SQL keywords not allowed")

    # Parameterized queries
    return execute_query(sql, use_prepared=True)

@mcp.resource("file://{path*}")
def read_file(path: str) -> str:
    """Secure file access with path validation"""
    # Prevent directory traversal
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(ALLOWED_BASE_DIR):
        raise ResourceError("Access denied: path outside allowed directory")

    # Check permissions
    if not os.access(abs_path, os.R_OK):
        raise ResourceError("Access denied: insufficient permissions")

    return open(abs_path).read()
```

---

# Advanced Patterns

## Dependency Injection

```python
from fastmcp.dependencies import Depends

def get_user_id() -> str:
    """Hidden from LLM schema, injected at runtime"""
    return "user_123"

def get_db_connection():
    """Dependency injection for database"""
    return DatabaseConnection()

@mcp.tool()
def get_user_details(
    user_id: str = Depends(get_user_id),
    db = Depends(get_db_connection)
) -> str:
    """Tool receives injected dependencies transparently"""
    return db.fetch_user(user_id)
```

## Server Composition

```python
from fastmcp import FastMCP

# Combine multiple servers
weather_server = FastMCP("Weather")
database_server = FastMCP("Database")

main = FastMCP("Unified Server")
main.add_server(weather_server, prefix="weather")
main.add_server(database_server, prefix="db")

# Exposes: weather:get_forecast, db:query_users
if __name__ == "__main__":
    main.run()
```

## Remote Server Proxying

```python
from fastmcp.server import create_proxy
from fastmcp.auth import BearerAuth

# Create proxy to remote MCP server
proxy = create_proxy(
    "https://api.example.com/mcp/sse",
    name="Remote Server Proxy",
    auth=BearerAuth(token="your-api-token")
)

if __name__ == "__main__":
    proxy.run()
```

## Dynamic Component Management

```python
# Add/remove components at runtime
mcp.add_tool(my_function)
mcp.remove_tool("tool_name")

# Control visibility
mcp.disable(tags={"admin"})  # Hide admin tools
mcp.enable(tags={"public"}, only=True)  # Allowlist mode

# Clients automatically notified via notifications/tools/list_changed
```

## Testing with Client

```python
import asyncio
from fastmcp import FastMCP, Client

mcp = FastMCP("Test Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# Test your server
async def test_server():
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 5, "b": 3})
        assert result == 8
        print("✅ Test passed")

asyncio.run(test_server())
```

---

# Common Pitfalls

## 1. Environment Isolation in Claude Desktop

**Problem**: Server can't find API keys or dependencies

```python
# ❌ BAD: Relies on shell environment
api_key = os.getenv("API_KEY")  # Will be None in Claude Desktop!
```

**Solution**: Explicitly pass environment variables in config

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "--with", "fastmcp", "fastmcp", "run", "server.py"],
      "env": {
        "API_KEY": "actual_value_here"
      }
    }
  }
}
```

## 2. Relative Paths in Config

**Problem**: Server file not found

```json
// ❌ BAD: Relative path
"args": ["fastmcp", "run", "./server.py"]
```

**Solution**: Use absolute paths

```json
// ✅ GOOD: Absolute path
"args": ["fastmcp", "run", "/Users/alice/projects/mcp-server/server.py"]
```

## 3. Functions with *args or **kwargs

**Problem**: FastMCP can't generate schema

```python
# ❌ BAD: Can't extract parameter schema
@mcp.tool()
def process(*args, **kwargs):
    pass
```

**Solution**: Use explicit parameters

```python
# ✅ GOOD: Explicit parameters with types
@mcp.tool()
def process(data: list[str], options: dict[str, any] = {}) -> dict:
    pass
```

## 4. Context Scoped to Single Request

**Problem**: Expecting context to persist

```python
# ❌ BAD: Context won't persist across requests
@mcp.tool()
async def step1(ctx: Context):
    ctx.user_data = "some value"  # Lost after request ends

@mcp.tool()
async def step2(ctx: Context):
    return ctx.user_data  # Will fail - different context instance
```

**Solution**: Use context state methods

```python
# ✅ GOOD: Use state persistence
@mcp.tool()
async def step1(ctx: Context):
    await ctx.set_state("user_data", "some value")

@mcp.tool()
async def step2(ctx: Context):
    return await ctx.get_state("user_data")
```

## 5. Default Security is Insecure

**Problem**: Production server with no authentication

```python
# ❌ BAD: No auth, HTTP only
mcp = FastMCP("Production Server")
mcp.run(transport="http", port=8000)
```

**Solution**: Always use auth and HTTPS

```python
# ✅ GOOD: OAuth with HTTPS
mcp = FastMCP(
    "Production Server",
    auth=GoogleOAuth(client_id="...", client_secret="...")
)
mcp.run(transport="http", port=8443, ssl_certfile="cert.pem", ssl_keyfile="key.pem")
```

## 6. Async/Sync Confusion

**Problem**: Mixing async/sync incorrectly

```python
# ❌ BAD: Blocking I/O in async function
@mcp.tool()
async def fetch_data(url: str) -> str:
    return requests.get(url).text  # Blocks event loop!
```

**Solution**: Use async libraries or sync tools

```python
# ✅ GOOD: Async I/O
@mcp.tool()
async def fetch_data(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# ✅ ALSO GOOD: Sync tool (FastMCP runs in thread pool)
@mcp.tool()
def fetch_data_sync(url: str) -> str:
    return requests.get(url).text  # FastMCP handles threading
```

## 7. Not Handling Tool Errors

**Problem**: Unhandled exceptions leak to clients

```python
# ❌ BAD: Raw exception
@mcp.tool()
def divide(a: int, b: int) -> float:
    return a / b  # ZeroDivisionError leaks
```

**Solution**: Catch and raise ToolError

```python
# ✅ GOOD: Clean error handling
from fastmcp import ToolError

@mcp.tool()
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ToolError("Cannot divide by zero")
    return a / b
```

---

# Deployment

## Transport Options

### STDIO (Default) - For Claude Desktop and Local Tools

```python
# Python
if __name__ == "__main__":
    mcp.run()  # Defaults to STDIO
```

```bash
# Run directly
python server.py
```

**Use when:**
- Integrating with Claude Desktop
- Building local command-line tools
- Single-user scenarios

### HTTP - For Network Access

```python
# Python
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

```typescript
// TypeScript
mcp.run({ transport: "http", host: "0.0.0.0", port: 8000 });
```

**Use when:**
- Multiple clients need access
- Deploying to cloud services
- Need RESTful interface

### SSE (Server-Sent Events) - For Streaming

```python
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

**Use when:**
- Need long-lived connections
- Real-time updates/streaming
- Better than HTTP for persistent connections

## Production Deployment Checklist

- [ ] **Authentication enabled** (OAuth or token verification)
- [ ] **HTTPS/TLS configured** (SSL certificates)
- [ ] **Error masking enabled** (`mask_error_details=True`)
- [ ] **Input validation** on all tools and resources
- [ ] **Rate limiting** configured
- [ ] **Logging** configured to monitoring system
- [ ] **Health check endpoint** implemented
- [ ] **Environment variables** managed securely (not in code)
- [ ] **Dependencies pinned** to specific versions
- [ ] **CORS configured** if web clients will connect
- [ ] **Resource limits** set (memory, CPU, timeout)
- [ ] **Monitoring and alerting** configured

## Production Server Template (Python)

```python
from fastmcp import FastMCP
from fastmcp.auth import GoogleOAuth
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Production server with security
mcp = FastMCP(
    name="Production API Server",
    auth=GoogleOAuth(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    ),
    mask_error_details=True,
    rate_limit={"requests_per_minute": 100},
    allowed_origins=["https://app.example.com"]
)

@mcp.tool(timeout=30.0)
async def secure_operation(data: str, ctx: Context) -> dict:
    """Production-ready tool with full security"""
    try:
        # Log request
        logger.info(f"Request {ctx.request_id}: processing {len(data)} bytes")

        # Validate input
        if len(data) > 10000:
            raise ToolError("Data too large (max 10KB)")

        # Process
        result = await process_data(data)

        # Log success
        logger.info(f"Request {ctx.request_id}: success")

        return {"result": result, "request_id": ctx.request_id}

    except Exception as e:
        logger.error(f"Request {ctx.request_id}: error - {str(e)}")
        raise ToolError("Processing failed")

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        ssl_certfile=os.getenv("SSL_CERT"),
        ssl_keyfile=os.getenv("SSL_KEY")
    )
```

## Production Server Template (TypeScript)

```typescript
import { FastMCP } from "@fastmcp/server";
import { GoogleOAuth } from "@fastmcp/auth";

const mcp = new FastMCP({
  name: "Production API Server",
  auth: new GoogleOAuth({
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!
  }),
  maskErrorDetails: true,
  rateLimit: { requestsPerMinute: 100 },
  allowedOrigins: ["https://app.example.com"]
});

mcp.tool({
  name: "secure_operation",
  description: "Production-ready tool",
  parameters: { data: { type: "string" } },
  timeout: 30000,
  execute: async ({ data }, ctx) => {
    try {
      console.log(`Request ${ctx.requestId}: processing ${data.length} bytes`);

      if (data.length > 10000) {
        throw new Error("Data too large");
      }

      const result = await processData(data);

      console.log(`Request ${ctx.requestId}: success`);

      return { result, request_id: ctx.requestId };
    } catch (e) {
      console.error(`Request ${ctx.requestId}: error - ${e}`);
      throw new Error("Processing failed");
    }
  }
});

mcp.run({
  transport: "http",
  host: "0.0.0.0",
  port: parseInt(process.env.PORT || "8443"),
  sslCert: process.env.SSL_CERT,
  sslKey: process.env.SSL_KEY
});
```

---

# FastMCP v3 Beta Features

> **Note**: FastMCP v3 is in beta as of January 2026. For production systems, pin to v2.x.x stable release.

## What's New in v3

### 1. Improved Type System

```python
# v3: Better type inference
from fastmcp import FastMCP
from typing import Literal

@mcp.tool()
def process(mode: Literal["fast", "accurate", "balanced"]) -> dict:
    # v3 automatically generates enum schema
    pass
```

### 2. Enhanced Context API

```python
# v3: New context methods
@mcp.tool()
async def advanced_tool(ctx: Context) -> dict:
    # Structured logging with levels
    await ctx.log(level="INFO", message="Starting", tags={"module": "processor"})

    # Batch operations
    resources = await ctx.batch_read_resources(["uri1", "uri2", "uri3"])

    # Enhanced state with TTL
    await ctx.set_state("cache", data, ttl=3600)  # Expire after 1 hour
```

### 3. Middleware Support

```python
# v3: Request/response middleware
async def auth_middleware(request, call_next):
    if not validate_token(request.headers.get("Authorization")):
        raise UnauthorizedError()
    return await call_next(request)

mcp = FastMCP("Server", middleware=[auth_middleware])
```

### 4. Plugin System

```python
# v3: Plugin architecture
from fastmcp.plugins import MetricsPlugin, CachePlugin

mcp = FastMCP(
    "Server",
    plugins=[
        MetricsPlugin(export_to="prometheus"),
        CachePlugin(backend="redis", ttl=300)
    ]
)
```

## Breaking Changes from v2

| Feature | v2 | v3 |
|---------|----|----|
| **Import path** | `from fastmcp import FastMCP` | Same (no change) |
| **Tool decorator** | `@mcp.tool()` | `@mcp.tool()` (signature changed) |
| **Context injection** | `ctx: Context = None` | `ctx: Context` (required if used) |
| **Error classes** | `ToolError`, `ResourceError` | Same + `UnauthorizedError` |
| **Auth configuration** | `auth` parameter | `auth` + `authorization` |

## Migration Guide: v2 → v3

### Step 1: Update Dependencies

```bash
# Pin to v2 (stable)
pip install fastmcp~=2.11.0

# Upgrade to v3 (beta)
pip install fastmcp~=3.0.0-beta
```

### Step 2: Update Tool Signatures

```python
# v2
@mcp.tool()
def my_tool(param: str, ctx: Context = None) -> str:
    pass

# v3: Context must be explicitly typed (no default None)
@mcp.tool()
def my_tool(param: str, ctx: Context) -> str:
    pass
```

### Step 3: Update Context Method Calls

```python
# v2
await ctx.report_progress(50, 100)

# v3: Same syntax (no change)
await ctx.report_progress(50, 100)
```

### Step 4: Update Authentication

```python
# v2
from fastmcp.auth import GoogleOAuth
mcp = FastMCP("Server", auth=GoogleOAuth(...))

# v3: Enhanced auth configuration
from fastmcp.auth import GoogleOAuth, RoleBasedAuth
mcp = FastMCP(
    "Server",
    auth=GoogleOAuth(...),
    authorization=RoleBasedAuth(roles=["admin", "user"])
)
```

### Step 5: Test Thoroughly

```python
# Run full test suite before deploying v3
pytest tests/
```

## Version Compatibility Matrix

| Feature | v2.11.x | v3.0.0-beta | Status |
|---------|---------|-------------|--------|
| Basic tools | ✅ | ✅ | Stable |
| Resources | ✅ | ✅ | Stable |
| Prompts | ✅ | ✅ | Stable |
| Context API | ✅ | ✅ Enhanced | Enhanced in v3 |
| OAuth | ✅ | ✅ Enhanced | Enhanced in v3 |
| Middleware | ❌ | ✅ | New in v3 |
| Plugins | ❌ | ✅ | New in v3 |
| Batch operations | ❌ | ✅ | New in v3 |

**Recommendation**: Use v2.11.x for production, evaluate v3 beta in staging environments.

---

# Integration with Creating-Skills Workflow

This FastMCP skill composes with the `creating-skills` workflow for creating custom domain-specific MCP skills.

## When to Combine Both Skills

**Use FastMCP skill alone when:**
- Building one-off MCP servers
- Integrating specific APIs or data sources
- Quick prototyping

**Use both skills together when:**
- Creating reusable MCP patterns for your team
- Building domain-specific skill templates (e.g., "Database MCP Skill", "API Wrapper MCP Skill")
- Packaging MCP servers as distributable skills

## Workflow: Creating Custom MCP-Based Skill

1. **User requests custom skill**: "Create a skill for working with our company's API using MCP"

2. **Creating-skills skill activates**:
   - Gathers requirements about the API
   - Determines skill structure
   - Creates skill directory

3. **Creating-skills delegates to FastMCP skill**:
   - FastMCP skill provides MCP server implementation
   - Creates tools for API endpoints
   - Creates resources for data access
   - Adds authentication

4. **Creating-skills wraps as reusable skill**:
   - Packages MCP server as SKILL.md
   - Adds checklist for using the skill
   - Documents activation triggers
   - Creates usage examples

5. **Result**: Custom skill that other team members can use to work with the API via MCP

## Example: Creating "Company CRM MCP Skill"

```markdown
# Input to creating-skills
"Create a skill for working with our Salesforce CRM using MCP"

# Creating-skills output (using FastMCP skill for implementation)
.claude/skills/salesforce-crm/
├── SKILL.md                    # Skill instructions
├── server.py                   # FastMCP server (from this skill)
└── config.json                 # Claude Desktop config

# server.py (generated using FastMCP skill patterns)
from fastmcp import FastMCP, Context
from salesforce_api import SalesforceClient

mcp = FastMCP("Salesforce CRM")

@mcp.tool()
async def search_contacts(query: str) -> list[dict]:
    """Search contacts in Salesforce"""
    client = SalesforceClient(os.getenv("SALESFORCE_TOKEN"))
    return await client.search_contacts(query)

@mcp.resource("crm://contacts/{contact_id}")
async def get_contact(contact_id: str) -> str:
    """Get contact details"""
    client = SalesforceClient(os.getenv("SALESFORCE_TOKEN"))
    contact = await client.get_contact(contact_id)
    return json.dumps(contact)

if __name__ == "__main__":
    mcp.run()

# SKILL.md (created by creating-skills, references FastMCP patterns)
---
name: Salesforce CRM
description: Work with Salesforce CRM via MCP tools and resources
---

<required>
1. Install FastMCP skill server in Claude Desktop
2. Configure SALESFORCE_TOKEN environment variable
3. Use tools: search_contacts, get_contact
4. Use resources: crm://contacts/{id}
</required>
```

## Reference Pattern

When creating-skills needs MCP implementation, it should reference this skill:

```markdown
# In creating-skills SKILL.md
For MCP server implementation, follow patterns from FastMCP skill:
- Tools: /home/elvis/.claude/skills/fastmcp/SKILL.md#tools
- Resources: /home/elvis/.claude/skills/fastmcp/SKILL.md#resources
- Authentication: /home/elvis/.claude/skills/fastmcp/SKILL.md#authentication
```

---

# Complete Examples

## Example 1: Database Integration Server (Python)

```python
from fastmcp import FastMCP, Context, ToolError
from fastmcp.auth import GoogleOAuth
import asyncpg
import os

mcp = FastMCP(
    "Database Server",
    auth=GoogleOAuth(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    )
)

async def get_db_pool():
    """Dependency: Database connection pool"""
    return await asyncpg.create_pool(os.getenv("DATABASE_URL"))

@mcp.tool(
    description="Execute read-only SQL queries",
    annotations={"readOnlyHint": True}
)
async def query(sql: str, ctx: Context) -> list[dict]:
    """Execute SELECT queries with security validation"""
    # Validate SQL
    sql_upper = sql.upper().strip()
    if not sql_upper.startswith("SELECT"):
        raise ToolError("Only SELECT queries allowed")

    if any(keyword in sql_upper for keyword in ["DROP", "DELETE", "UPDATE", "INSERT"]):
        raise ToolError("Destructive SQL not allowed")

    await ctx.info(f"Executing query: {sql[:50]}...")

    # Execute with connection pool
    pool = await get_db_pool()
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql)
            return [dict(row) for row in rows]
    except Exception as e:
        await ctx.error(f"Query failed: {str(e)}")
        raise ToolError(f"Query execution failed: {str(e)}")

@mcp.resource("db://tables")
async def list_tables(ctx: Context) -> str:
    """List all database tables"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row["table_name"] for row in rows]
        return json.dumps({"tables": tables})

@mcp.resource("db://tables/{table_name}/schema")
async def get_schema(table_name: str, ctx: Context) -> str:
    """Get table schema information"""
    # Prevent SQL injection in table name
    if not table_name.replace("_", "").isalnum():
        raise ResourceError("Invalid table name")

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position
        """, table_name)

        schema = [
            {
                "column": row["column_name"],
                "type": row["data_type"],
                "nullable": row["is_nullable"] == "YES"
            }
            for row in rows
        ]
        return json.dumps({"table": table_name, "schema": schema})

if __name__ == "__main__":
    mcp.run()
```

## Example 2: File System Server (TypeScript)

```typescript
import { FastMCP, Context, ToolError, ResourceError } from "@fastmcp/server";
import { GoogleOAuth } from "@fastmcp/auth";
import * as fs from "fs/promises";
import * as path from "path";

const ALLOWED_BASE = process.env.ALLOWED_DIR || "/home/user/documents";

const mcp = new FastMCP({
  name: "File System Server",
  auth: new GoogleOAuth({
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!
  })
});

// Tool: List directory
mcp.tool({
  name: "list_directory",
  description: "List files and directories",
  parameters: {
    path: { type: "string", description: "Directory path", default: "." }
  },
  execute: async ({ path: dirPath }, ctx) => {
    const fullPath = path.resolve(ALLOWED_BASE, dirPath);

    // Security: Prevent directory traversal
    if (!fullPath.startsWith(ALLOWED_BASE)) {
      throw new ToolError("Access denied");
    }

    await ctx.info(`Listing directory: ${dirPath}`);

    const entries = await fs.readdir(fullPath, { withFileTypes: true });

    return {
      path: dirPath,
      entries: entries.map(e => ({
        name: e.name,
        type: e.isDirectory() ? "directory" : "file"
      }))
    };
  }
});

// Tool: Search files
mcp.tool({
  name: "search_files",
  description: "Search for files by name pattern",
  parameters: {
    pattern: { type: "string", description: "Glob pattern (e.g., *.txt)" },
    directory: { type: "string", default: ".", description: "Directory to search" }
  },
  execute: async ({ pattern, directory }, ctx) => {
    await ctx.info(`Searching for ${pattern} in ${directory}`);

    const fullPath = path.resolve(ALLOWED_BASE, directory);

    if (!fullPath.startsWith(ALLOWED_BASE)) {
      throw new ToolError("Access denied");
    }

    const results = await searchFiles(fullPath, pattern);

    return {
      pattern,
      directory,
      matches: results.length,
      files: results
    };
  }
});

// Resource: Read file contents
mcp.resource({
  uri: "file://{filepath*}",
  name: "File Content",
  description: "Read file contents",
  read: async ({ filepath }, ctx) => {
    const fullPath = path.resolve(ALLOWED_BASE, filepath);

    // Security validation
    if (!fullPath.startsWith(ALLOWED_BASE)) {
      throw new ResourceError("Access denied");
    }

    try {
      await ctx.info(`Reading file: ${filepath}`);
      const content = await fs.readFile(fullPath, "utf-8");
      return content;
    } catch (e) {
      throw new ResourceError(`Failed to read file: ${e.message}`);
    }
  }
});

// Prompt: File analysis workflow
mcp.prompt({
  name: "analyze_file",
  description: "Analyze file content and generate report",
  parameters: {
    filepath: { type: "string", description: "Path to file" }
  },
  execute: async ({ filepath }) => {
    return {
      messages: [
        {
          role: "user",
          content: `Analyze the file at ${filepath} and provide:`
        },
        {
          role: "user",
          content: `1. File size and format\n2. Content summary\n3. Key findings\n4. Recommendations`
        }
      ]
    };
  }
});

mcp.run();
```

---

# Templates

## Basic Tool Template (Python)

```python
from fastmcp import FastMCP, Context, ToolError

@mcp.tool(
    description="[What this tool does]",
    annotations={"readOnlyHint": True}  # or destructiveHint, etc.
)
async def tool_name(
    param1: str,  # Required parameter
    param2: int = 10,  # Optional with default
    ctx: Context = None  # Context injection
) -> dict:
    """[Detailed docstring for LLM]"""
    try:
        # 1. Validate inputs
        if not param1:
            raise ToolError("param1 is required")

        # 2. Log operation
        await ctx.info(f"Processing: {param1}")

        # 3. Report progress for long operations
        await ctx.report_progress(50, 100)

        # 4. Execute logic
        result = do_something(param1, param2)

        # 5. Return structured data
        return {"result": result, "param1": param1}

    except Exception as e:
        await ctx.error(f"Tool failed: {str(e)}")
        raise ToolError(f"Operation failed: {str(e)}")
```

## Basic Resource Template (Python)

```python
from fastmcp import ResourceError

@mcp.resource("namespace://{param}/path")
async def resource_name(param: str, ctx: Context) -> str:
    """[Docstring describing what data this returns]"""
    try:
        # 1. Validate parameters
        if not is_valid(param):
            raise ResourceError(f"Invalid parameter: {param}")

        # 2. Security checks
        if not has_permission(param):
            raise ResourceError("Access denied")

        # 3. Fetch data
        data = fetch_data(param)

        # 4. Return as string (JSON for structured data)
        return json.dumps(data)

    except Exception as e:
        raise ResourceError(f"Failed to fetch data: {str(e)}")
```

## Production Server Template (Python)

```python
#!/usr/bin/env python3
from fastmcp import FastMCP, Context, ToolError
from fastmcp.auth import GoogleOAuth
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create secure server
mcp = FastMCP(
    name=os.getenv("SERVER_NAME", "Production Server"),
    auth=GoogleOAuth(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
    ),
    mask_error_details=True,
    rate_limit={"requests_per_minute": int(os.getenv("RATE_LIMIT", "100"))},
)

# Add your tools, resources, prompts here

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8443"))
    transport = os.getenv("TRANSPORT", "http")

    logger.info(f"Starting server on {transport}:{port}")

    mcp.run(
        transport=transport,
        host="0.0.0.0",
        port=port,
        ssl_certfile=os.getenv("SSL_CERT"),
        ssl_keyfile=os.getenv("SSL_KEY")
    )
```

---

# References

## Official Documentation

- [FastMCP Documentation](https://gofastmcp.com) - Complete guides and API reference
- [FastMCP GitHub](https://github.com/jlowin/fastmcp) - Source code and examples
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2025-11-25) - Official MCP spec

## Integration Guides

- [Claude Desktop Integration](https://gofastmcp.com/integrations/claude-desktop) - Integration guide
- [FastMCP Cloud](https://fastmcp.cloud) - One-click deployment platform

## Community

- [FastMCP Discord](https://discord.gg/uu8dJCgttd) - Active support and discussions
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers) - Example servers

## Learning Resources

- [Building MCP Servers with FastMCP - DataCamp](https://www.datacamp.com/tutorial/building-mcp-server-client-fastmcp)
- [FastMCP Tutorial - MCPcat](https://mcpcat.io/guides/building-mcp-server-python-fastmcp/)

---

# Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| **Python** | 3.8+ | 3.11+ |
| **Node.js** | 16+ | 20+ (LTS) |
| **FastMCP (Python)** | 2.11.0 | 2.11.x (stable) |
| **FastMCP (TypeScript)** | 2.0.0 | 2.x (stable) |
| **uv** | 0.1.0+ | Latest |
| **Claude Desktop** | Any | Latest |

**Production Recommendation**: Pin FastMCP to specific minor version (e.g., `fastmcp~=2.11.0`) to avoid breaking changes.

---

# Skill Metadata

**Created**: January 2026
**FastMCP Version**: v2.11.0 / v3.0.0-beta
**Languages**: Python, TypeScript
**Integration**: Claude Desktop, FastMCP Cloud
**Status**: Production Ready
