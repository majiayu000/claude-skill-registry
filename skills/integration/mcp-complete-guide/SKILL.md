---
name: mcp-complete-guide
description: Complete 11-phase guide for building production-ready MCP (Model Context Protocol) servers with semantic layer integration. Covers foundation to deployment, including agent-centric design, tool development, testing, error handling, performance optimization, monitoring, security, governance, and semantic layer integration for business metrics. Use when building enterprise-grade MCP servers that integrate with dbt, Tableau, or other semantic layers for Finance SSC, business analytics, or data governance use cases.
---

# Complete MCP Development Guide: Phases 1-11

**A Comprehensive Guide to Building Production-Ready MCP Servers**
*From Foundation to Semantic Layer Integration*

---

## Table of Contents

1. [Phase 1: Foundation & Planning](#phase-1-foundation--planning)
2. [Phase 2: Core Implementation](#phase-2-core-implementation)
3. [Phase 3: Tool Development](#phase-3-tool-development)
4. [Phase 4: Testing & Validation](#phase-4-testing--validation)
5. [Phase 5: Error Handling & Resilience](#phase-5-error-handling--resilience)
6. [Phase 6: Performance Optimization](#phase-6-performance-optimization)
7. [Phase 7: Monitoring & Observability](#phase-7-monitoring--observability)
8. [Phase 8: Documentation & Examples](#phase-8-documentation--examples)
9. [Phase 9: Security & Governance](#phase-9-security--governance)
10. [Phase 10: Production Deployment](#phase-10-production-deployment)
11. [Phase 11: Semantic Layer Integration](#phase-11-semantic-layer-integration)

---

# Phase 1: Foundation & Planning

## Overview

Before writing any code, invest time in deep research and strategic planning. This phase sets the foundation for a high-quality MCP server.

## 1.1 Understand Agent-Centric Design

**Build for Workflows, Not Just API Endpoints:**
- Don't simply wrap existing API endpoints - build thoughtful, high-impact workflow tools
- Consolidate related operations (e.g., `schedule_event` that both checks availability and creates event)
- Focus on tools that enable complete tasks, not just individual API calls
- Consider what workflows agents actually need to accomplish

**Optimize for Limited Context:**
- Agents have constrained context windows - make every token count
- Return high-signal information, not exhaustive data dumps
- Provide "concise" vs "detailed" response format options
- Default to human-readable identifiers over technical codes (names over IDs)

**Design Actionable Error Messages:**
- Error messages should guide agents toward correct usage patterns
- Suggest specific next steps: "Try using filter='active_only' to reduce results"
- Make errors educational, not just diagnostic

**Follow Natural Task Subdivisions:**
- Tool names should reflect how humans think about tasks
- Group related tools with consistent prefixes for discoverability
- Design tools around natural workflows, not just API structure

## 1.2 Study MCP Protocol Documentation

**Load the complete MCP specification:**
```bash
# Fetch the latest MCP protocol documentation
https://modelcontextprotocol.io/llms-full.txt
```

This comprehensive document contains the complete MCP specification and guidelines.

## 1.3 Study Framework Documentation

**For Python implementations:**
- Python SDK Documentation: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- Review FastMCP patterns and best practices

**For Node/TypeScript implementations:**
- TypeScript SDK Documentation: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- Review MCP SDK patterns

## 1.4 Exhaustive API Research

To integrate a service, read through **ALL** available API documentation:
- Official API reference documentation
- Authentication and authorization requirements
- Rate limiting and pagination patterns
- Error responses and status codes
- Available endpoints and their parameters
- Data models and schemas

## 1.5 Create Implementation Plan

Based on your research, create a detailed plan:

**Tool Selection:**
- List the most valuable endpoints/operations to implement
- Prioritize tools that enable the most common and important use cases
- Consider which tools work together to enable complex workflows

**Shared Utilities:**
- Identify common API request patterns
- Plan pagination helpers
- Design filtering and formatting utilities
- Plan error handling strategies

**Input/Output Design:**
- Define input validation models (Pydantic for Python, Zod for TypeScript)
- Design consistent response formats (JSON or Markdown)
- Plan for large-scale usage (thousands of users/resources)
- Implement character limits and truncation strategies (e.g., 25,000 tokens)

**Error Handling Strategy:**
- Plan graceful failure modes
- Design clear, actionable, LLM-friendly error messages
- Consider rate limiting and timeout scenarios
- Handle authentication and authorization errors

---

# Phase 2: Core Implementation

## Overview

With a comprehensive plan in place, begin systematic implementation following language-specific best practices.

## 2.1 Project Structure Setup

### Python Structure
```python
project/
├── src/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── tools.py           # Tool implementations
│   ├── utils.py           # Shared utilities
│   └── models.py          # Pydantic models
├── tests/
│   ├── test_tools.py
│   └── test_utils.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

### TypeScript Structure
```typescript
project/
├── src/
│   ├── index.ts          # Main MCP server
│   ├── tools/            # Tool implementations
│   ├── utils/            # Shared utilities
│   └── types.ts          # Type definitions
├── tests/
├── package.json
├── tsconfig.json
└── README.md
```

## 2.2 Server Initialization

### Python (FastMCP)
```python
from mcp import FastMCP
from pydantic import BaseModel, Field
import httpx
import asyncio

# Initialize server
mcp = FastMCP("your-service-name")

# Module-level constants
CHARACTER_LIMIT = 25000
API_BASE_URL = "https://api.example.com"
```

### TypeScript (MCP SDK)
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server({
  name: "your-service-name",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});
```

## 2.3 Implement Core Infrastructure

**Create shared utilities before implementing tools:**

### API Request Helper
```python
async def make_api_request(
    endpoint: str,
    method: str = "GET",
    params: dict | None = None,
    data: dict | None = None
) -> dict:
    """Make authenticated API request with error handling."""
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=f"{API_BASE_URL}/{endpoint}",
            params=params,
            json=data,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
```

### Response Formatting
```python
def format_response(data: dict, format_type: str = "json") -> str:
    """Format response as JSON or Markdown."""
    if format_type == "json":
        return json.dumps(data, indent=2)
    else:
        # Convert to markdown format
        return convert_to_markdown(data)

def truncate_content(content: str, max_chars: int = CHARACTER_LIMIT) -> str:
    """Truncate content with ellipsis if exceeds limit."""
    if len(content) <= max_chars:
        return content
    return content[:max_chars] + "\n\n[Content truncated...]"
```

### Pagination Helper
```python
async def paginate_results(
    endpoint: str,
    max_results: int = 100,
    page_size: int = 50
) -> list:
    """Fetch paginated results up to max_results."""
    results = []
    page = 1
    
    while len(results) < max_results:
        data = await make_api_request(
            endpoint,
            params={"page": page, "per_page": page_size}
        )
        
        if not data.get("items"):
            break
            
        results.extend(data["items"])
        
        if not data.get("has_more"):
            break
            
        page += 1
    
    return results[:max_results]
```

---

# Phase 3: Tool Development

## Overview

Implement tools systematically, following consistent patterns and best practices.

## 3.1 Tool Implementation Pattern

### Complete Tool Example (Python)
```python
from pydantic import BaseModel, Field
from typing import Literal

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(
        description="Search query string",
        min_length=1,
        max_length=200
    )
    filter_type: Literal["all", "active", "archived"] = Field(
        default="active",
        description="Filter results by status"
    )
    max_results: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Maximum number of results to return"
    )
    response_format: Literal["json", "markdown"] = Field(
        default="markdown",
        description="Format for response data"
    )

@mcp.tool()
async def search_items(
    query: str,
    filter_type: str = "active",
    max_results: int = 50,
    response_format: str = "markdown"
) -> str:
    """
    Search for items matching the query.
    
    This tool searches across all items in the system and returns
    matching results with their key attributes.
    
    Args:
        query: Search query string
        filter_type: Filter by status (all/active/archived)
        max_results: Maximum number of results (1-100)
        response_format: Response format (json/markdown)
    
    Returns:
        Formatted search results with item details
        
    Example:
        >>> search_items("project alpha", filter_type="active", max_results=10)
        Returns active items matching "project alpha"
    
    Hints:
        readOnly: true
        destructive: false
        idempotent: true
        openWorld: true
    """
    try:
        # Validate and prepare request
        params = {
            "q": query,
            "status": filter_type,
            "limit": min(max_results, 100)
        }
        
        # Fetch results
        results = await make_api_request("search", params=params)
        
        # Format response
        formatted = format_response(results, response_format)
        
        # Apply character limit
        return truncate_content(formatted)
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return "No items found matching your query. Try broader search terms."
        elif e.response.status_code == 401:
            return "Authentication failed. Please check API credentials."
        else:
            return f"Search failed: {str(e)}. Please try again."
    except Exception as e:
        return f"Unexpected error during search: {str(e)}"
```

## 3.2 Tool Design Checklist

For each tool, ensure:
- ✅ **Clear Purpose**: One-line description of what the tool does
- ✅ **Input Validation**: Pydantic/Zod schema with constraints
- ✅ **Error Handling**: Graceful handling of all error cases
- ✅ **Actionable Errors**: Error messages guide next steps
- ✅ **Response Formats**: Support JSON and Markdown
- ✅ **Character Limits**: Truncate long responses
- ✅ **Tool Hints**: Add readOnly, destructive, idempotent, openWorld
- ✅ **Type Safety**: Full type hints/types
- ✅ **Documentation**: Comprehensive docstrings/descriptions
- ✅ **Examples**: Usage examples in documentation

## 3.3 Common Tool Patterns

### Read-Only List Tool
```python
@mcp.tool()
async def list_resources(
    limit: int = 50,
    offset: int = 0,
    response_format: str = "markdown"
) -> str:
    """
    List all available resources.
    
    Hints:
        readOnly: true
        destructive: false
        idempotent: true
    """
    results = await paginate_results("resources", max_results=limit)
    return format_response(results, response_format)
```

### Create/Update Tool (Destructive)
```python
@mcp.tool()
async def create_resource(
    name: str,
    description: str,
    metadata: dict | None = None
) -> str:
    """
    Create a new resource.
    
    Hints:
        readOnly: false
        destructive: true
        idempotent: false
    """
    data = {
        "name": name,
        "description": description,
        "metadata": metadata or {}
    }
    
    result = await make_api_request("resources", method="POST", data=data)
    return f"✅ Resource created successfully: {result['id']}"
```

---

# Phase 4: Testing & Validation

## Overview

Comprehensive testing ensures your MCP server works reliably in production scenarios.

## 4.1 Unit Testing

### Python (pytest)
```python
import pytest
from unittest.mock import AsyncMock, patch
from your_server import search_items, make_api_request

@pytest.mark.asyncio
async def test_search_items_success():
    """Test successful search returns formatted results."""
    mock_response = {
        "items": [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "name": "Item 2"}
        ]
    }
    
    with patch('your_server.make_api_request', return_value=mock_response):
        result = await search_items("test query")
        
        assert "Item 1" in result
        assert "Item 2" in result
        assert len(result) < CHARACTER_LIMIT

@pytest.mark.asyncio
async def test_search_items_not_found():
    """Test 404 returns helpful error message."""
    with patch('your_server.make_api_request', side_effect=httpx.HTTPStatusError(
        "Not Found", request=None, response=AsyncMock(status_code=404)
    )):
        result = await search_items("nonexistent")
        
        assert "No items found" in result
        assert "broader search terms" in result
```

## 4.2 Evaluation Creation

Create 10 realistic evaluation questions to test agent effectiveness:

```xml
<evaluation>
  <qa_pair>
    <question>What are the top 5 most active projects in the last 30 days, and who are their lead contributors?</question>
    <answer>Project Alpha (John Doe), Project Beta (Jane Smith), Project Gamma (Bob Johnson), Project Delta (Alice Williams), Project Epsilon (Charlie Brown)</answer>
  </qa_pair>
  
  <!-- More qa_pairs... -->
</evaluation>
```

### Evaluation Requirements

Each question must be:
- **Independent**: Not dependent on other questions
- **Read-only**: Only non-destructive operations required
- **Complex**: Requiring multiple tool calls
- **Realistic**: Based on real use cases
- **Verifiable**: Single, clear answer
- **Stable**: Answer won't change over time

---

# Phase 5: Error Handling & Resilience

## Overview

Robust error handling ensures your MCP server handles failures gracefully and provides actionable feedback.

## 5.1 Error Categories

### Network Errors
```python
async def handle_network_error(error: Exception) -> str:
    """Handle network-related errors with retries."""
    if isinstance(error, httpx.TimeoutException):
        return "Request timed out. The service may be slow - try reducing max_results or try again later."
    elif isinstance(error, httpx.ConnectError):
        return "Cannot connect to service. Please check your network connection and try again."
    else:
        return f"Network error: {str(error)}. Please try again."
```

### Rate Limiting
```python
import time
from functools import wraps

def rate_limit_handler(max_retries: int = 3):
    """Decorator to handle rate limiting with exponential backoff."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:
                        if attempt < max_retries - 1:
                            wait_time = 2 ** attempt  # Exponential backoff
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            return "Rate limit exceeded. Please wait a moment and try again."
                    raise
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool()
@rate_limit_handler(max_retries=3)
async def rate_limited_search(query: str) -> str:
    """Search with automatic rate limit handling."""
    return await search_items(query)
```

## 5.2 Circuit Breaker Pattern

Prevent cascading failures:

```python
class CircuitBreaker:
    """Circuit breaker to prevent cascading failures."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open
    
    def call(self, func):
        """Execute function with circuit breaker protection."""
        async def wrapper(*args, **kwargs):
            if self.state == "open":
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = "half_open"
                else:
                    return "Service temporarily unavailable due to repeated failures. Please try again later."
            
            try:
                result = await func(*args, **kwargs)
                
                if self.state == "half_open":
                    self.state = "closed"
                    self.failure_count = 0
                
                return result
                
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
                
                raise
        
        return wrapper
```

---

# Phase 6: Performance Optimization

## Overview

Optimize your MCP server for speed, efficiency, and scalability.

## 6.1 Caching Strategies

### In-Memory Cache
```python
from functools import lru_cache
from datetime import datetime, timedelta

class TimedCache:
    """Simple timed cache for API responses."""
    
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = timedelta(seconds=ttl_seconds)
    
    def get(self, key: str) -> dict | None:
        """Get cached value if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: dict):
        """Cache value with timestamp."""
        self.cache[key] = (value, datetime.now())

# Global cache instance
api_cache = TimedCache(ttl_seconds=300)

@mcp.tool()
async def cached_search(query: str) -> str:
    """Search with caching for repeated queries."""
    cache_key = f"search:{query}"
    
    # Check cache
    cached_result = api_cache.get(cache_key)
    if cached_result:
        return format_response(cached_result, "markdown") + "\n\n📦 (Cached result)"
    
    # Fetch fresh data
    result = await make_api_request("search", params={"q": query})
    
    # Cache result
    api_cache.set(cache_key, result)
    
    return format_response(result, "markdown")
```

## 6.2 Batch Operations

Process multiple items efficiently:

```python
@mcp.tool()
async def batch_fetch_resources(
    resource_ids: list[str],
    max_concurrent: int = 10
) -> str:
    """Fetch multiple resources concurrently."""
    async def fetch_one(resource_id: str) -> dict:
        """Fetch single resource."""
        try:
            return await make_api_request(f"resources/{resource_id}")
        except Exception as e:
            return {"id": resource_id, "error": str(e)}
    
    # Limit concurrency to avoid overwhelming API
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch_with_limit(resource_id: str):
        async with semaphore:
            return await fetch_one(resource_id)
    
    # Execute concurrent requests
    results = await asyncio.gather(
        *[fetch_with_limit(rid) for rid in resource_ids],
        return_exceptions=True
    )
    
    return format_response(results, "json")
```

---

# Phase 7: Monitoring & Observability

## Overview

Implement comprehensive monitoring to track server performance, errors, and usage patterns.

## 7.1 Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Format logs as JSON for easy parsing."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Setup logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

## 7.2 Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
TOOL_CALLS = Counter(
    'mcp_tool_calls_total',
    'Total number of tool calls',
    ['tool_name', 'status']
)

TOOL_DURATION = Histogram(
    'mcp_tool_duration_seconds',
    'Tool execution duration',
    ['tool_name']
)

ACTIVE_REQUESTS = Gauge(
    'mcp_active_requests',
    'Number of active requests'
)

def instrument_tool(func):
    """Decorator to instrument tools with metrics."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tool_name = func.__name__
        
        ACTIVE_REQUESTS.inc()
        
        with TOOL_DURATION.labels(tool_name=tool_name).time():
            try:
                result = await func(*args, **kwargs)
                TOOL_CALLS.labels(tool_name=tool_name, status='success').inc()
                return result
            except Exception as e:
                TOOL_CALLS.labels(tool_name=tool_name, status='error').inc()
                raise
            finally:
                ACTIVE_REQUESTS.dec()
    
    return wrapper
```

---

# Phase 8: Documentation & Examples

## Overview

Comprehensive documentation ensures developers and users can effectively use your MCP server.

## 8.1 README Template

```markdown
# Your Service MCP Server

High-quality MCP server for [Your Service], enabling AI agents to [primary use case].

## Features

- 🔍 **Search & Discovery**: Semantic search across all resources
- 📊 **Analytics**: Query metrics and generate reports
- ⚡ **Batch Operations**: Process multiple items efficiently
- 🔐 **Secure**: Built-in authentication and access control

## Installation

### Prerequisites
- Python 3.11 or higher
- API token from [Your Service]

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set API token
export YOUR_SERVICE_TOKEN="your-token-here"

# Run server
python src/server.py
```

## Available Tools

### `search_items`
Search for items matching a query.

**Parameters:**
- `query` (string): Search query
- `filter_type` (string): Filter by status
- `max_results` (int): Maximum results

**Example:**
```
search_items(query='machine learning', filter_type='active')
```
```

---

# Phase 9: Security & Governance

## Overview

Implement robust security and governance to protect sensitive data and ensure compliance.

## 9.1 Role-Based Access Control

```python
from enum import Enum

class Role(Enum):
    """User roles."""
    ADMIN = "admin"
    USER = "user"
    READONLY = "readonly"

class Permission(Enum):
    """Permissions."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

ROLE_PERMISSIONS = {
    Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN},
    Role.USER: {Permission.READ, Permission.WRITE},
    Role.READONLY: {Permission.READ}
}

class AccessControl:
    """Access control manager."""
    
    def check_permission(
        self,
        user_id: str,
        required_permission: Permission
    ) -> bool:
        """Check if user has required permission."""
        user_role = self.user_roles.get(user_id, Role.READONLY)
        user_permissions = ROLE_PERMISSIONS[user_role]
        return required_permission in user_permissions
```

## 9.2 Audit Logging

```python
class AuditLogger:
    """Audit log for security and compliance."""
    
    def log_access(
        self,
        user_id: str,
        action: str,
        resource: str,
        status: str,
        details: dict = None
    ):
        """Log access attempt."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "status": status,
            "details": details or {}
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
```

---

# Phase 10: Production Deployment

## Overview

Deploy your MCP server to production with proper infrastructure, monitoring, and operational procedures.

## 10.1 Docker Containerization

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/

# Create non-root user
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

# Run server
CMD ["python", "src/server.py"]
```

## 10.2 Docker Compose

```yaml
version: '3.8'

services:
  mcp-server:
    build: .
    container_name: your-service-mcp
    environment:
      - YOUR_SERVICE_TOKEN=${YOUR_SERVICE_TOKEN}
      - REDIS_URL=redis://redis:6379
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
      - "9090:9090"  # Metrics endpoint
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: mcp-redis
    ports:
      - "6379:6379"
    restart: unless-stopped
```

## 10.3 Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-service-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: your-service-mcp
  template:
    metadata:
      labels:
        app: your-service-mcp
    spec:
      containers:
      - name: mcp-server
        image: your-registry/your-service-mcp:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "500m"
            memory: "256Mi"
          limits:
            cpu: "1000m"
            memory: "512Mi"
```

---

# Phase 11: Semantic Layer Integration

## Overview

This phase covers integrating MCP servers with semantic layers to provide AI agents with reliable, consistent access to business metrics and governed data.

**Use this phase when:**
- Building MCP servers that expose business metrics
- Integrating with dbt, Tableau, Cube.dev, or other semantic layers
- Need consistent metric definitions across systems
- Require governance and lineage tracking
- Supporting AI agents that query business data

## Understanding the Semantic Layer

### What is a Semantic Layer?

A semantic layer is the "source code of business understanding" - a centralized repository that:
- Defines business metrics with consistent calculation logic
- Organizes dimensions and hierarchies
- Establishes relationships between data entities
- Enforces access control and governance
- Provides a single source of truth for analytics

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│         AI Agent (Claude, GPT-4, etc)       │
│  "What was customer churn last quarter?"    │
└────────────────┬────────────────────────────┘
                 │ Natural Language
                 ▼
┌─────────────────────────────────────────────┐
│           MCP Server (This Guide)           │
│                                             │
│  Tools:                                     │
│  - list_metrics()                           │
│  - query_metric(name, dimensions, filters)  │
│  - validate_access(user, metric)            │
│  - get_lineage(metric)                      │
└────────────────┬────────────────────────────┘
                 │ OSI Standard / API
                 ▼
┌─────────────────────────────────────────────┐
│    Semantic Layer (dbt, Tableau, Cube)      │
│                                             │
│  Business Definitions:                      │
│  - Metrics (calculations, aggregations)     │
│  - Dimensions (attributes, hierarchies)     │
│  - Governance (access control, lineage)     │
│  - Relationships (joins, foreign keys)      │
└────────────────┬────────────────────────────┘
                 │ Native SQL/Queries
                 ▼
┌─────────────────────────────────────────────┐
│   Data Warehouse (Snowflake, Databricks)    │
└─────────────────────────────────────────────┘
```

## Business Metric Modeling

### Metric Types

**1. Simple Metrics (Aggregations)**
```yaml
metric:
  name: total_revenue
  type: simple
  sql: SUM(orders.amount)
  description: Total revenue from all orders
```

**2. Derived Metrics (Calculations)**
```yaml
metric:
  name: average_order_value
  type: derived
  sql: SUM(orders.amount) / COUNT(DISTINCT orders.id)
  description: Average value per order
```

**3. Ratio Metrics**
```yaml
metric:
  name: customer_churn_rate
  type: ratio
  numerator: churned_customers
  denominator: total_customers
  sql: COUNT(DISTINCT churned.customer_id) / COUNT(DISTINCT total.customer_id)
  description: Percentage of customers who churned
```

### Finance SSC Example

Here's how to model Finance Shared Service Center metrics:

```yaml
# Month-End Closing Metrics
metrics:
  - name: outstanding_ar
    type: simple
    sql: SUM(CASE WHEN accounts_receivable.status = 'outstanding' THEN amount ELSE 0 END)
    dimensions: [agency, month, customer]
    owner: finance_team
    
  - name: days_sales_outstanding
    type: derived
    sql: (outstanding_ar / (total_revenue / 30))
    dimensions: [agency, month]
    owner: finance_team
    
  - name: bank_reconciliation_variance
    type: simple
    sql: SUM(ABS(bank_statement.amount - book_amount))
    dimensions: [agency, bank_account, month]
    owner: accounting_team

# BIR Compliance Metrics
  - name: withholding_tax_1601c
    type: simple
    sql: SUM(withholding_taxes.amount WHERE form_type = '1601-C')
    dimensions: [agency, month, tax_type]
    owner: tax_team
    
  - name: vat_payable_2550q
    type: derived
    sql: SUM(output_vat) - SUM(input_vat)
    dimensions: [agency, quarter]
    owner: tax_team

# Multi-Agency Dimensions
dimensions:
  - name: agency
    type: categorical
    sql: transactions.agency_code
    values: [RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB]
    
  - name: fiscal_period
    type: time
    sql: transactions.posting_date
    granularities: [day, month, quarter, year]
```

## dbt Semantic Layer Integration

### MCP Server Implementation

```python
from mcp import FastMCP
from pydantic import BaseModel, Field
import httpx
from typing import Literal

mcp = FastMCP("dbt-semantic-layer")

# dbt Semantic Layer configuration
DBT_SEMANTIC_LAYER_URL = os.getenv("DBT_SEMANTIC_LAYER_URL")
DBT_SERVICE_TOKEN = os.getenv("DBT_SERVICE_TOKEN")
DBT_ENVIRONMENT_ID = os.getenv("DBT_ENVIRONMENT_ID")

@mcp.tool()
async def list_business_metrics(
    search: str = "",
    response_format: str = "markdown"
) -> str:
    """
    List all available business metrics from the semantic layer.
    
    Returns a catalog of metrics with their definitions, dimensions,
    and ownership information.
    """
    query = """
    {
      metrics {
        name
        description
        type
        dimensions {
          name
          type
        }
        owner
      }
    }
    """
    
    result = await query_dbt_semantic_layer({"query": query})
    metrics = result["data"]["metrics"]
    
    # Filter by search term if provided
    if search:
        metrics = [
            m for m in metrics
            if search.lower() in m["name"].lower()
            or search.lower() in m["description"].lower()
        ]
    
    if response_format == "markdown":
        output = ["# Available Business Metrics\n"]
        for metric in metrics:
            output.append(f"## {metric['name']}")
            output.append(f"**Type:** {metric['type']}")
            output.append(f"**Description:** {metric['description']}")
            output.append(f"**Owner:** {metric['owner']}\n")
        return "\n".join(output)
    else:
        return json.dumps(metrics, indent=2)

@mcp.tool()
async def query_business_metric(
    metric_name: str,
    group_by: list[str] = [],
    time_period: str = "last_30_days",
    filters: dict = {},
    response_format: str = "markdown"
) -> str:
    """
    Query a business metric with dimensions and filters.
    
    This tool queries the semantic layer to get metric values
    with consistent business definitions and governance.
    
    Args:
        metric_name: Name of the metric (e.g., 'total_revenue')
        group_by: List of dimensions to group by (e.g., ['agency', 'month'])
        time_period: Time period for the query
        filters: Additional filters (e.g., {'agency': 'RIM'})
        response_format: Response format (json/markdown)
    
    Example:
        Query outstanding AR by agency:
        >>> query_business_metric(
                metric_name='outstanding_ar',
                group_by=['agency', 'fiscal_month'],
                time_period='this_year'
            )
    """
    # Convert time period to date range
    date_range = convert_time_period(time_period)
    
    # Build GraphQL query
    query = f"""
    {{
      metric(name: "{metric_name}") {{
        values(
          dimensions: [{",".join(group_by)}]
          dateRange: {{start: "{date_range['start']}", end: "{date_range['end']}"}}
        ) {{
          dimensions {{
            name
            value
          }}
          value
        }}
      }}
    }}
    """
    
    result = await query_dbt_semantic_layer({"query": query})
    data = result["data"]["metric"]["values"]
    
    if response_format == "markdown":
        output = [f"# {metric_name}\n"]
        output.append(f"**Time Period:** {time_period}\n")
        
        if data:
            # Create table
            headers = [d["name"] for d in data[0]["dimensions"]] + ["Value"]
            output.append("| " + " | ".join(headers) + " |")
            output.append("| " + " | ".join(["---"] * len(headers)) + " |")
            
            for row in data:
                values = [d["value"] for d in row["dimensions"]] + [str(row["value"])]
                output.append("| " + " | ".join(values) + " |")
        
        return "\n".join(output)
    else:
        return json.dumps(data, indent=2)
```

## Governance & Access Control

### Metric-Level Access Control

```python
class MetricGovernance:
    """Governance rules for metrics."""
    
    def validate_metric_access(
        self,
        user_id: str,
        metric_name: str
    ) -> tuple[bool, str]:
        """
        Check if user has access to metric.
        
        Returns:
            (allowed, reason) tuple
        """
        metric_config = self.config["metrics"].get(metric_name)
        
        if not metric_config:
            return False, f"Metric '{metric_name}' not found"
        
        # Check user role
        user_role = self.get_user_role(user_id)
        allowed_roles = metric_config.get("allowed_roles", [])
        
        if user_role not in allowed_roles:
            return False, f"Access denied. Required roles: {', '.join(allowed_roles)}"
        
        return True, "Access granted"

governance = MetricGovernance()

@mcp.tool()
async def secure_query_metric(
    metric_name: str,
    group_by: list[str] = [],
    user_id: str = None
) -> str:
    """
    Query metric with governance enforcement.
    
    Validates user access before executing query.
    """
    if not user_id:
        return "Error: User ID required for authentication"
    
    # Validate access
    allowed, reason = governance.validate_metric_access(user_id, metric_name)
    
    if not allowed:
        return f"Access Denied: {reason}"
    
    # Execute query
    return await query_business_metric(
        metric_name=metric_name,
        group_by=group_by
    )
```

## Real-World Finance SSC Example

### Complete Implementation

```python
@mcp.tool()
async def get_month_end_closing_status(
    fiscal_month: str,
    agencies: list[str] = None
) -> str:
    """
    Get month-end closing status across all agencies.
    
    Returns comprehensive status including:
    - Outstanding AR by agency
    - Bank reconciliation status
    - Days sales outstanding
    - Variance analysis
    
    Args:
        fiscal_month: Month in YYYY-MM format (e.g., '2025-10')
        agencies: Optional list of agencies to filter (RIM, CKVC, BOM, etc)
    """
    if not agencies:
        agencies = ["RIM", "CKVC", "BOM", "JPAL", "JLI", "JAP", "LAS", "RMQB"]
    
    output = [f"# Month-End Closing Status: {fiscal_month}\n"]
    
    # Query Outstanding AR
    ar_result = await query_business_metric(
        metric_name="outstanding_ar",
        group_by=["agency"],
        filters={"fiscal_month": fiscal_month, "agency": agencies},
        time_period="this_month"
    )
    output.append("## Outstanding Accounts Receivable")
    output.append(ar_result)
    
    # Query DSO
    dso_result = await query_business_metric(
        metric_name="days_sales_outstanding",
        group_by=["agency"],
        filters={"fiscal_month": fiscal_month, "agency": agencies},
        time_period="this_month"
    )
    output.append("## Days Sales Outstanding")
    output.append(dso_result)
    
    return "\n".join(output)

@mcp.tool()
async def get_bir_compliance_summary(
    quarter: str,
    form_types: list[str] = None
) -> str:
    """
    Get BIR compliance summary for tax filing.
    
    Returns summary of all BIR forms due including:
    - Form 2550Q (VAT)
    - Form 1601-C (Withholding Tax)
    - Form 1601-EQ (Quarterly EWT)
    - Amounts by agency
    """
    if not form_types:
        form_types = ["2550Q", "1601-C", "1601-EQ"]
    
    output = [f"# BIR Compliance Summary: {quarter}\n"]
    
    # Query VAT Payable
    if "2550Q" in form_types:
        vat_result = await query_business_metric(
            metric_name="vat_payable_2550q",
            group_by=["agency"],
            filters={"quarter": quarter},
            time_period="this_quarter"
        )
        output.append("## Form 2550Q - VAT Payable")
        output.append(vat_result)
    
    # Query Withholding Tax
    if "1601-C" in form_types:
        wht_result = await query_business_metric(
            metric_name="withholding_tax_1601c",
            group_by=["agency", "tax_type"],
            filters={"quarter": quarter},
            time_period="this_quarter"
        )
        output.append("## Form 1601-C - Withholding Tax")
        output.append(wht_result)
    
    return "\n".join(output)
```

---

## Summary

This complete 11-phase guide provides everything needed to build production-ready MCP servers with semantic layer integration:

### Phase Coverage

**Foundation (Phases 1-4):**
- Deep research and planning
- Core implementation patterns
- Systematic tool development
- Comprehensive testing

**Production Readiness (Phases 5-8):**
- Error handling and resilience
- Performance optimization
- Monitoring and observability
- Documentation and examples

**Enterprise Features (Phases 9-11):**
- Security and governance
- Production deployment
- Semantic layer integration

### When to Use This Guide

Use this comprehensive guide when:
- Building enterprise-grade MCP servers
- Integrating with semantic layers (dbt, Tableau, Cube)
- Need consistent metric definitions across systems
- Require governance and access control
- Supporting AI agents querying business data
- Building Finance SSC or business analytics systems

### Resources

**MCP Protocol:**
- https://modelcontextprotocol.io/llms-full.txt

**dbt Semantic Layer:**
- https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-semantic-layer

**Finance SSC Use Cases:**
- Multi-agency metric consistency (RIM, CKVC, BOM, JPAL, JLI, JAP, LAS, RMQB)
- Month-end closing standardized calculations
- BIR compliance governed tax metric definitions

---

**All 11 Phases Complete! Build world-class MCP servers with semantic layer integration.** 🎯
