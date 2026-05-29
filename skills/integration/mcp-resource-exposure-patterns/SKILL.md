---
name: mcp-resource-exposure-patterns
version: "1.0"
description: >
  Resources provide read-only context to Claude using URI-based identification.
  PROACTIVELY activate for: (1) exposing data as MCP resources, (2) URI scheme design, (3) list_resources implementation.
  Triggers: "mcp resources", "uri patterns", "read_resource"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# MCP Resource Exposure Patterns Skill

## Metadata (Tier 1)

**Keywords**: resources, uri, context provisioning, list_resources, read_resource

**File Patterns**: **/resources/*.py, **/providers.py

**Modes**: backend_python

---

## Instructions (Tier 2)

### Resources vs Tools

**Resources** (app-controlled):
- Provide **read-only context** to Claude
- URI-based identification
- Examples: documentation, logs, database schemas, API specs

**Tools** (model-controlled):
- Perform **actions with side effects**
- Require explicit invocation by Claude
- Examples: create_file, execute_query, send_email

**Rule**: If it's read-only context provisioning → Resource. If it performs an action → Tool.

### URI Patterns

Resources use **URI schemes** for identification:

```python
# File resources
"file:///project/README.md"
"file:///docs/api/authentication.md"

# Database resources
"db:///schemas/users"
"db:///tables/orders/schema"

# API resources
"api:///endpoints/v1/users"
"api:///swagger.json"

# Log resources
"log:///app/2024-01-15"
"log:///errors/recent"

# Custom schemes
"config:///settings/database"
"metric:///cpu/usage"
```

### list_resources Implementation

```python
from pydantic import BaseModel, ConfigDict
from typing import Literal

class ResourceDescriptor(BaseModel):
    """Resource metadata returned by list_resources."""
    model_config = ConfigDict(strict=True)

    uri: str
    name: str
    mimeType: str
    description: str | None = None

@server.list_resources()
async def list_resources() -> list[dict]:
    """List all available resources."""
    resources = []

    # File-based resources
    docs_dir = Path("docs")
    if docs_dir.exists():
        for md_file in docs_dir.rglob("*.md"):
            resources.append(
                ResourceDescriptor(
                    uri=f"file:///{md_file}",
                    name=md_file.stem,
                    mimeType="text/markdown",
                    description=f"Documentation: {md_file.stem}"
                ).model_dump()
            )

    # Database schema resources
    db_schemas = await get_database_schemas()
    for schema in db_schemas:
        resources.append(
            ResourceDescriptor(
                uri=f"db:///schemas/{schema.name}",
                name=f"{schema.name} Schema",
                mimeType="application/json",
                description=f"Database schema for {schema.name}"
            ).model_dump()
        )

    return resources
```

### read_resource Implementation

```python
import aiofiles
from pathlib import Path

class ResourceContent(BaseModel):
    """Content returned by read_resource."""
    model_config = ConfigDict(strict=True)

    uri: str
    text: str | None = None
    blob: str | None = None  # Base64 encoded binary
    mimeType: str

@server.read_resource()
async def read_resource(uri: str) -> dict:
    """Read resource content by URI."""

    # Validate URI scheme
    if uri.startswith("file:///"):
        return await read_file_resource(uri)
    elif uri.startswith("db:///"):
        return await read_database_resource(uri)
    elif uri.startswith("log:///"):
        return await read_log_resource(uri)
    else:
        raise ValueError(f"Unsupported URI scheme: {uri}")

async def read_file_resource(uri: str) -> dict:
    """Read file-based resource."""
    # Security: validate path
    path = uri.removeprefix("file://")
    path = Path(path).resolve()

    # Prevent path traversal
    if ".." in str(path):
        raise ValueError("Path traversal not allowed")

    if not path.exists():
        raise FileNotFoundError(f"Resource not found: {uri}")

    # Async file reading
    async with aiofiles.open(path, "r") as f:
        content = await f.read()

    return {
        "contents": [
            ResourceContent(
                uri=uri,
                text=content,
                mimeType=get_mime_type(path)
            ).model_dump()
        ]
    }
```

### Dynamic Resources

```python
@server.list_resources()
async def list_resources() -> list[dict]:
    """List resources with dynamic content."""

    # Current date logs (past 7 days)
    resources = []
    for days_ago in range(7):
        date = datetime.now() - timedelta(days=days_ago)
        date_str = date.strftime("%Y-%m-%d")

        resources.append(
            ResourceDescriptor(
                uri=f"log:///app/{date_str}",
                name=f"App Logs - {date_str}",
                mimeType="text/plain",
                description=f"Application logs for {date_str}"
            ).model_dump()
        )

    return resources

@server.read_resource()
async def read_resource(uri: str) -> dict:
    """Read dynamic log resource."""
    if uri.startswith("log:///app/"):
        date_str = uri.removeprefix("log:///app/")
        log_content = await fetch_logs_for_date(date_str)

        return {
            "contents": [
                ResourceContent(
                    uri=uri,
                    text=log_content,
                    mimeType="text/plain"
                ).model_dump()
            ]
        }
```

### MIME Type Detection

```python
import mimetypes

def get_mime_type(path: Path) -> str:
    """Determine MIME type from file extension."""
    mime_type, _ = mimetypes.guess_type(str(path))

    # Fallback mapping
    if mime_type is None:
        extension_map = {
            ".md": "text/markdown",
            ".json": "application/json",
            ".yaml": "text/yaml",
            ".yml": "text/yaml",
            ".log": "text/plain",
            ".sql": "application/sql"
        }
        mime_type = extension_map.get(path.suffix, "text/plain")

    return mime_type
```

### Security Validation

```python
from pathlib import Path

class UriValidator:
    """Validate resource URIs for security."""

    @staticmethod
    def validate_file_uri(uri: str, allowed_roots: list[Path]) -> Path:
        """Validate file URI against allowed roots."""
        path = uri.removeprefix("file://")
        resolved = Path(path).resolve()

        # Check path traversal
        if ".." in str(path):
            raise ValueError("Path traversal not allowed")

        # Check against allowed roots
        if not any(resolved.is_relative_to(root) for root in allowed_roots):
            raise ValueError(f"Access denied: {uri}")

        return resolved

# Usage
@server.read_resource()
async def read_resource(uri: str) -> dict:
    if uri.startswith("file:///"):
        allowed_roots = [
            Path("/project/docs"),
            Path("/project/config")
        ]
        path = UriValidator.validate_file_uri(uri, allowed_roots)
        # Proceed with reading
```

### Binary Resources

```python
import base64

async def read_binary_resource(uri: str) -> dict:
    """Read binary resource (images, PDFs, etc.)."""
    path = Path(uri.removeprefix("file://"))

    async with aiofiles.open(path, "rb") as f:
        binary_content = await f.read()

    # Base64 encode binary data
    encoded = base64.b64encode(binary_content).decode("utf-8")

    return {
        "contents": [
            ResourceContent(
                uri=uri,
                blob=encoded,  # Use blob for binary
                mimeType=get_mime_type(path)
            ).model_dump()
        ]
    }
```

### Database Schema Resources

```python
@server.read_resource()
async def read_resource(uri: str) -> dict:
    """Read database schema resource."""
    if uri.startswith("db:///schemas/"):
        table_name = uri.removeprefix("db:///schemas/")

        # Fetch schema asynchronously
        schema = await fetch_table_schema(table_name)

        schema_json = {
            "table": table_name,
            "columns": [
                {
                    "name": col.name,
                    "type": col.type,
                    "nullable": col.nullable,
                    "primary_key": col.primary_key
                }
                for col in schema.columns
            ]
        }

        return {
            "contents": [
                ResourceContent(
                    uri=uri,
                    text=json.dumps(schema_json, indent=2),
                    mimeType="application/json"
                ).model_dump()
            ]
        }
```

### Anti-Patterns

❌ **Using Tools for Read-Only Operations**
```python
# WRONG - should be a resource
@server.call_tool()
async def call_tool(name, args):
    if name == "read_docs":  # This should be a resource!
        return await read_documentation()
```

❌ **Missing URI Validation**
```python
# WRONG - security risk
path = uri.removeprefix("file://")
content = open(path).read()  # No validation!
```

❌ **Synchronous File I/O**
```python
# WRONG - blocking operation
with open(path, "r") as f:  # Should use aiofiles
    content = f.read()
```

❌ **Hardcoded Resource List**
```python
# WRONG - not dynamic
@server.list_resources()
async def list_resources():
    return [{"uri": "file:///README.md"}]  # Should scan filesystem
```

---

## Resources (Tier 3)

**MCP Resources Spec**: https://spec.modelcontextprotocol.io/specification/server/resources/
**aiofiles Docs**: https://github.com/Tinche/aiofiles
**URI RFC**: https://datatracker.ietf.org/doc/html/rfc3986
