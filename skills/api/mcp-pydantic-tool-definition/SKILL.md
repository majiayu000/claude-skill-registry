---
name: mcp-pydantic-tool-definition
version: "1.0"
description: >
  Pydantic V2 models are the single source of truth for MCP tool schemas.
  PROACTIVELY activate for: (1) defining tool input/output schemas, (2) strict mode validation, (3) JSON schema generation.
  Triggers: "pydantic schema", "tool schema", "strict mode"
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

# MCP Pydantic Tool Definition Skill

## Metadata (Tier 1)

**Keywords**: pydantic, strict mode, input schema, tool schema, validation

**File Patterns**: **/schemas.py, **/tools/*.py

**Modes**: backend_python

---

## Instructions (Tier 2)

### Schema-First Development Pattern

**CRITICAL**: Pydantic V2 models are the **single source of truth** for MCP tool schemas.

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class ToolInput(BaseModel):
    """Input schema for tool - becomes inputSchema automatically."""
    model_config = ConfigDict(strict=True)

    query: str = Field(..., description="Search query string")
    limit: int = Field(10, ge=1, le=100, description="Max results")
    filter: Literal["all", "code", "docs"] = "all"

# JSON Schema generated automatically
schema = ToolInput.model_json_schema()
# {
#   "type": "object",
#   "properties": {
#     "query": {"type": "string", "description": "Search query string"},
#     "limit": {"type": "integer", "minimum": 1, "maximum": 100, ...},
#     "filter": {"type": "string", "enum": ["all", "code", "docs"]}
#   },
#   "required": ["query"]
# }
```

### Strict Mode (MANDATORY)

**ConfigDict(strict=True)** prevents silent type coercion.

```python
# ❌ WITHOUT STRICT MODE
class Input(BaseModel):
    count: int

# Silent coercion: "10" → 10
input = Input(count="10")  # Works, but dangerous!

# ✅ WITH STRICT MODE
class Input(BaseModel):
    model_config = ConfigDict(strict=True)
    count: int

# Validation error: no coercion
input = Input(count="10")  # ❌ ValidationError!
input = Input(count=10)    # ✅ OK
```

### Field Validation

```python
from pydantic import Field, field_validator, model_validator

class SearchInput(BaseModel):
    model_config = ConfigDict(strict=True)

    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Custom query validation."""
        if len(v.split()) > 50:
            raise ValueError("Query too complex (max 50 terms)")
        return v.strip()

    @model_validator(mode="after")
    def validate_pagination(self) -> "SearchInput":
        """Cross-field validation."""
        if self.offset + self.limit > 10000:
            raise ValueError("Pagination limit exceeded")
        return self
```

### Complex Types

```python
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

class FileFilter(BaseModel):
    model_config = ConfigDict(strict=True)

    pattern: str = Field(..., description="Glob pattern")
    exclude_dirs: list[str] = Field(default_factory=list)
    max_size_mb: int | None = Field(None, ge=1, le=1000)

class AdvancedSearchInput(BaseModel):
    model_config = ConfigDict(strict=True)

    # Union types
    target: str | FileFilter

    # Literal enums
    mode: Literal["exact", "fuzzy", "regex"]

    # Bounded integers
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]

    # Optional with default
    case_sensitive: bool = True

    # Nested models
    filters: list[FileFilter] = Field(default_factory=list)
```

### Output Schemas

```python
class SearchResult(BaseModel):
    """Output schema for search tool."""
    model_config = ConfigDict(strict=True)

    file_path: str
    line_number: int
    match_text: str
    confidence: float = Field(ge=0.0, le=1.0)

class SearchOutput(BaseModel):
    """Top-level output schema."""
    model_config = ConfigDict(strict=True)

    results: list[SearchResult]
    total_count: int
    execution_time_ms: int

# Usage in tool handler
async def execute_search(input: SearchInput) -> SearchOutput:
    results = await perform_search(input)

    return SearchOutput(
        results=results,
        total_count=len(results),
        execution_time_ms=42
    )
```

### Tool Registration Pattern

```python
from tools.schemas import SearchInput, SearchOutput

@server.list_tools()
async def list_tools():
    """Register tools with auto-generated schemas."""
    return [
        {
            "name": "search_code",
            "description": "Search codebase with advanced filters",
            "inputSchema": SearchInput.model_json_schema()
        }
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute tool with Pydantic validation."""
    if name == "search_code":
        # Automatic validation via Pydantic
        input_data = SearchInput(**arguments)

        # Type-safe execution
        output = await execute_search(input_data)

        # Serialize output to JSON
        return output.model_dump()

    raise ValueError(f"Unknown tool: {name}")
```

### JSON Schema Customization

```python
from pydantic import BaseModel, ConfigDict, Field

class CustomSchemaInput(BaseModel):
    model_config = ConfigDict(
        strict=True,
        # Custom JSON Schema metadata
        json_schema_extra={
            "examples": [
                {"query": "async def", "limit": 10}
            ]
        }
    )

    query: str = Field(
        ...,
        description="Search query",
        json_schema_extra={
            "examples": ["async def", "class MyClass"]
        }
    )
```

### Validation Error Handling

```python
from pydantic import ValidationError

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        input_data = SearchInput(**arguments)
        return await execute_search(input_data)

    except ValidationError as e:
        # Convert Pydantic errors to MCP errors
        error_details = []
        for error in e.errors():
            error_details.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })

        raise McpError(
            code=-32602,  # Invalid params
            message=f"Validation failed: {error_details}"
        )
```

### Anti-Patterns

❌ **Manual JSON Schema Writing**
```python
# WRONG
schema = {
    "type": "object",
    "properties": {"query": {"type": "string"}}
}
```

❌ **Missing Strict Mode**
```python
# WRONG - allows type coercion
class Input(BaseModel):
    count: int  # No ConfigDict(strict=True)
```

❌ **Ignoring Validation Errors**
```python
# WRONG
try:
    input_data = Input(**arguments)
except ValidationError:
    pass  # Silent failure!
```

❌ **Using BaseModel Without ConfigDict**
```python
# WRONG
class Input(BaseModel):
    value: str  # Missing model_config
```

---

## Resources (Tier 3)

**Pydantic V2 Docs**: https://docs.pydantic.dev/latest/
**Strict Mode Guide**: https://docs.pydantic.dev/latest/concepts/strict_mode/
**Field Validators**: https://docs.pydantic.dev/latest/concepts/validators/
**JSON Schema**: https://docs.pydantic.dev/latest/concepts/json_schema/
