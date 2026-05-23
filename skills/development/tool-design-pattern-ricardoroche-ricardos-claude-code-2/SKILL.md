---
name: tool-design-pattern
description: Automatically applies when creating AI tool functions. Ensures proper schema design, input validation, error handling, context access, and comprehensive testing.
---

# AI Tool Design Pattern Enforcer

When creating tools for AI agents (LangChain, function calling, etc.), follow these design patterns.

## ✅ Standard Tool Pattern

```python
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# 1. Define input schema
class SearchInput(BaseModel):
    """Input schema for search tool."""

    query: str = Field(..., description="Search query string")
    max_results: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results to return"
    )
    filter_type: Optional[str] = Field(
        None,
        description="Optional filter type (e.g., 'recent', 'popular')"
    )

# 2. Implement tool function
@tool(args_schema=SearchInput)
def search_database(query: str, max_results: int = 10, filter_type: Optional[str] = None) -> str:
    """
    Search database for relevant information.

    Use this tool when user asks to find, search, or look up information.
    Returns JSON string with search results.

    Args:
        query: Search query string
        max_results: Maximum number of results (1-100)
        filter_type: Optional filter (recent, popular)

    Returns:
        JSON string with results or error message
    """
    request_id = str(uuid.uuid4())

    try:
        # Log tool invocation
        logger.info(
            f"TOOL_CALL: search_database | "
            f"query={query[:50]} | "
            f"request_id={request_id}"
        )

        # Validate inputs
        if not query or not query.strip():
            return json.dumps({
                "error": "Query cannot be empty",
                "request_id": request_id
            })

        # Execute search
        results = _execute_search(query, max_results, filter_type)

        # Return structured response
        return json.dumps({
            "results": results,
            "total": len(results),
            "request_id": request_id
        })

    except Exception as e:
        logger.error(f"Tool error | request_id={request_id}", exc_info=True)
        return json.dumps({
            "error": "Search failed",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        })

# 3. Helper implementation
def _execute_search(query: str, max_results: int, filter_type: Optional[str]) -> List[dict]:
    """Internal search implementation."""
    # Actual search logic
    pass
```

## Tool Schema Design

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional

class EmailToolInput(BaseModel):
    """Well-designed tool input schema."""

    recipient: str = Field(
        ...,
        description="Email address of recipient (e.g., user@example.com)"
    )

    subject: str = Field(
        ...,
        description="Email subject line",
        min_length=1,
        max_length=200
    )

    body: str = Field(
        ...,
        description="Email body content",
        min_length=1
    )

    priority: Literal["low", "normal", "high"] = Field(
        default="normal",
        description="Email priority level"
    )

    attach_invoice: bool = Field(
        default=False,
        description="Whether to attach invoice PDF"
    )

    @field_validator('recipient')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "recipient": "customer@example.com",
                "subject": "Order Confirmation",
                "body": "Thank you for your order!",
                "priority": "normal",
                "attach_invoice": True
            }
        }
```

## Error Handling Pattern

```python
import uuid
from datetime import datetime
import json

@tool
def robust_tool(param: str) -> str:
    """Tool with comprehensive error handling."""
    request_id = str(uuid.uuid4())

    # Input validation
    if not param:
        return json.dumps({
            "error": "Parameter is required",
            "error_code": "INVALID_INPUT",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        })

    try:
        # Main logic
        result = process_data(param)

        return json.dumps({
            "success": True,
            "data": result,
            "request_id": request_id
        })

    except ValidationError as e:
        return json.dumps({
            "error": str(e),
            "error_code": "VALIDATION_ERROR",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        })

    except ExternalAPIError as e:
        logger.error(f"External API failed | request_id={request_id}", exc_info=True)
        return json.dumps({
            "error": "External service unavailable",
            "error_code": "SERVICE_ERROR",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Unexpected error | request_id={request_id}", exc_info=True)
        return json.dumps({
            "error": "An unexpected error occurred",
            "error_code": "INTERNAL_ERROR",
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        })
```

## Context Access Pattern

```python
from typing import Any

@tool
def context_aware_tool(query: str, context: Optional[dict] = None) -> str:
    """
    Tool that uses conversation context.

    Args:
        query: User query
        context: Optional context from agent (user_id, session_id, etc.)

    Returns:
        JSON string with results
    """
    # Extract context safely
    user_id = context.get("user_id") if context else None
    session_id = context.get("session_id") if context else None

    logger.info(
        f"Tool called | user_id={user_id} | "
        f"session_id={session_id} | query={query[:50]}"
    )

    # Use context in logic
    if user_id:
        # Personalized response
        results = fetch_user_data(user_id, query)
    else:
        # Generic response
        results = fetch_generic_data(query)

    return json.dumps({"results": results})
```

## Async Tool Pattern

```python
from langchain.tools import tool
import httpx

@tool
async def async_api_tool(query: str) -> str:
    """
    Async tool for external API calls.

    Use async for I/O-bound operations to improve performance.
    """
    request_id = str(uuid.uuid4())

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.example.com/search",
                params={"q": query},
                timeout=10.0
            )
            response.raise_for_status()

            return json.dumps({
                "results": response.json(),
                "request_id": request_id
            })

    except httpx.TimeoutException:
        return json.dumps({
            "error": "Request timed out",
            "request_id": request_id
        })
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "error": f"API error: {e.response.status_code}",
            "request_id": request_id
        })
```

## Testing Tools

```python
import pytest
from unittest.mock import patch, Mock

def test_search_tool_success():
    """Test successful search."""
    result = search_database(query="test query", max_results=5)
    data = json.loads(result)

    assert "results" in data
    assert "request_id" in data
    assert data["total"] >= 0

def test_search_tool_empty_query():
    """Test validation error."""
    result = search_database(query="", max_results=10)
    data = json.loads(result)

    assert "error" in data
    assert data["error"] == "Query cannot be empty"

@patch('module.httpx.get')
def test_async_tool_timeout(mock_get):
    """Test timeout handling."""
    mock_get.side_effect = httpx.TimeoutException("Timeout")

    result = async_api_tool(query="test")
    data = json.loads(result)

    assert "error" in data
    assert "timed out" in data["error"].lower()

@pytest.mark.asyncio
async def test_async_tool_success():
    """Test async tool success path."""
    with patch('module.httpx.AsyncClient') as mock_client:
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_response.raise_for_status = Mock()

        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        result = await async_api_tool("test query")
        data = json.loads(result)

        assert "results" in data
```

## ❌ Anti-Patterns

```python
# ❌ No input schema
@tool
def bad_tool(param):  # No type hints, no schema!
    pass

# ❌ Returning plain strings
@tool
def bad_tool(param: str) -> str:
    return "Error: something went wrong"  # Not structured!

# ❌ No error handling
@tool
def bad_tool(param: str) -> str:
    result = external_api_call(param)  # What if this fails?
    return result

# ❌ Exposing sensitive data
@tool
def bad_tool(user_id: str) -> str:
    logger.info(f"Processing user {user_id}")  # PII leak!
    return json.dumps({"user_id": user_id})

# ❌ No validation
@tool
def bad_tool(email: str) -> str:
    send_email(email)  # What if email is invalid?
    return "Sent"
```

## Best Practices Checklist

- ✅ Define Pydantic input schema with descriptions
- ✅ Add comprehensive docstring (when to use, what it returns)
- ✅ Include field descriptions in schema
- ✅ Add input validation
- ✅ Use structured JSON responses
- ✅ Include request_id in all responses
- ✅ Add proper error handling with try/except
- ✅ Log tool invocations (with PII redaction)
- ✅ Use async for I/O-bound operations
- ✅ Write comprehensive tests (success, error, edge cases)
- ✅ Add examples in schema
- ✅ Keep tools focused (single responsibility)

## Auto-Apply

When creating tools:
1. Define Pydantic input schema with Field descriptions
2. Add `@tool` decorator with args_schema
3. Write comprehensive docstring
4. Add input validation
5. Use try/except for error handling
6. Return structured JSON with request_id
7. Log invocations (redact PII)
8. Write tests for success and error cases

## Related Skills

- pydantic-models - For input schemas
- structured-errors - For error responses
- async-await-checker - For async tools
- pytest-patterns - For testing tools
- docstring-format - For tool documentation
- pii-redaction - For logging
