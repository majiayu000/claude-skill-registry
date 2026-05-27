---
name: code-standards
description: Standard code patterns, conventions, and testing practices for Kubani. Reference this when writing new code, tests, or reviewing existing code.
---

# Code Standards

Standard code patterns, conventions, and testing practices for Kubani.

## Configuration Access

### ✅ Correct Pattern

```python
from kubani.framework.config import get_config

def my_function():
    config = get_config()
    url = config.llm.api_url
    timeout = config.temporal.activity_timeout
```

### ❌ Avoid

```python
import os

def my_function():
    url = os.getenv("LLM_API_URL", "http://localhost:8000")
```

## MCP Client Usage

### ✅ Correct Pattern

```python
from kubani.framework.mcp import get_mcp_client

async def store_learning(content: str):
    client = get_mcp_client()
    await client.memory.store_learning(
        agent_id="my-agent",
        learning_type="pattern",
        content=content,
        confidence=0.85,
    )
```

### ❌ Avoid

```python
import httpx

async def store_learning(content: str):
    async with httpx.AsyncClient() as client:
        await client.post("http://memory-mcp:8083/tools/store_learning", ...)
```

## Agent Creation

### ✅ Correct Pattern

```python
from strands import Agent, tool

def create_my_agent():
    factory = get_agent_factory()
    return factory.create_agent(AgentConfig(
        name="my-agent",
        description="Does something useful",
        system_prompt="You are a helpful assistant.",
        tools=[my_tool],
    ))
```

### ❌ Avoid

```python
from strands import Agent

def create_my_agent():
    return Agent(
        model="...",
        system_prompt="...",
        # Missing standard configuration
    )
```

## Skill Loading

### ✅ Correct Pattern

```python
from kubani.skills import get_skill_library

async def find_relevant_skill(context: dict):
    library = get_skill_library()
    skill = await library.find_skill(
        category="k8s/diagnostic",
        triggers=context.get("triggers", []),
    )
    return skill
```

## Error Handling

### ✅ Correct Pattern

```python
import logging
from kubani.framework.exceptions import AgentError, SkillNotFoundError

logger = logging.getLogger(__name__)

async def execute_skill(skill_name: str):
    try:
        skill = await library.get_skill(skill_name)
        result = await skill.execute()
        return result
    except SkillNotFoundError:
        logger.warning(f"Skill not found: {skill_name}")
        return None
    except AgentError as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        raise
```

### ❌ Avoid

```python
async def execute_skill(skill_name: str):
    try:
        skill = await library.get_skill(skill_name)
        return await skill.execute()
    except Exception:
        pass  # Silent failure
```

## Temporal Workflows

### ✅ Correct Pattern

```python
from datetime import timedelta
from temporalio import workflow, activity

@activity.defn
async def investigate_pod(pod_name: str) -> dict:
    """Activity with clear input/output types."""
    # Implementation
    return {"status": "healthy"}

@workflow.defn
class RemediationWorkflow:
    @workflow.run
    async def run(self, input: RemediationInput) -> RemediationResult:
        # Use activities with explicit timeouts
        diagnosis = await workflow.execute_activity(
            investigate_pod,
            input.pod_name,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                maximum_attempts=3,
                initial_interval=timedelta(seconds=1),
            ),
        )
        return RemediationResult(diagnosis=diagnosis)
```

## Pydantic Models

### ✅ Correct Pattern

```python
from pydantic import BaseModel, Field

class PodDiagnosis(BaseModel):
    """Diagnosis result for a Kubernetes pod."""
    
    pod_name: str = Field(..., description="Name of the pod")
    namespace: str = Field(..., description="Kubernetes namespace")
    status: str = Field(..., description="Current pod status")
    issues: list[str] = Field(default_factory=list, description="Identified issues")
    recommendations: list[str] = Field(default_factory=list, description="Recommended actions")
    
    class Config:
        extra = "forbid"  # Catch typos in field names
```

## Logging

### ✅ Correct Pattern

```python
import logging
import structlog

# Use structlog for structured logging
logger = structlog.get_logger(__name__)

async def process_event(event: dict):
    logger.info(
        "processing_event",
        event_type=event["type"],
        event_id=event["id"],
    )
    
    try:
        result = await handle_event(event)
        logger.info(
            "event_processed",
            event_id=event["id"],
            result_status=result.status,
        )
    except Exception as e:
        logger.error(
            "event_processing_failed",
            event_id=event["id"],
            error=str(e),
            exc_info=True,
        )
        raise
```

## Testing

### ✅ Correct Pattern

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_mcp_client():
    """Fixture for mocking MCP client."""
    with patch("kubani.framework.mcp.get_mcp_client") as mock:
        client = AsyncMock()
        mock.return_value = client
        yield client

@pytest.mark.asyncio
async def test_store_learning(mock_mcp_client):
    """Test learning storage with mocked MCP client."""
    mock_mcp_client.memory.store_learning.return_value = {"id": "learning-123"}
    
    result = await store_learning("test content")
    
    assert result["id"] == "learning-123"
    mock_mcp_client.memory.store_learning.assert_called_once_with(
        agent_id="my-agent",
        learning_type="pattern",
        content="test content",
        confidence=0.85,
    )
```

## Type Hints

### ✅ Correct Pattern

```python
from typing import Optional
from collections.abc import Sequence

async def find_skills(
    category: str,
    triggers: Sequence[str],
    limit: int = 10,
) -> list[Skill]:
    """Find skills matching the given criteria.
    
    Args:
        category: Skill category (e.g., "k8s/diagnostic")
        triggers: List of trigger conditions
        limit: Maximum number of skills to return
        
    Returns:
        List of matching skills, ordered by relevance
    """
    ...
```

## Async Patterns

### ✅ Correct Pattern

```python
import asyncio

async def process_items(items: list[str]) -> list[dict]:
    """Process items concurrently with controlled parallelism."""
    semaphore = asyncio.Semaphore(10)  # Limit concurrent operations
    
    async def process_one(item: str) -> dict:
        async with semaphore:
            return await do_processing(item)
    
    results = await asyncio.gather(
        *[process_one(item) for item in items],
        return_exceptions=True,
    )
    
    # Handle exceptions
    successful = []
    for item, result in zip(items, results):
        if isinstance(result, Exception):
            logger.error(f"Failed to process {item}: {result}")
        else:
            successful.append(result)
    
    return successful
```

## MCP Server Implementation

### ✅ Correct Pattern

```python
from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("my-mcp-server")

@mcp.tool()
async def my_tool(
    param1: str,
    param2: int = 10,
) -> dict:
    """Tool description for LLM understanding.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    """
    result = await _do_work(param1, param2)
    return {"status": "success", "result": result}

async def _do_work(param1: str, param2: int) -> str:
    """Internal implementation."""
    ...

if __name__ == "__main__":
    mcp.run()
```

See `kubani/mcp/servers/discord/` and `kubani/mcp/servers/temporal/` for real examples.

## File Organization

### ✅ Correct Structure

```
agents/my-agent/
├── src/my_agent/
│   ├── __init__.py
│   ├── worker.py           # Entry point
│   ├── config.py           # Agent-specific config (uses unified)
│   ├── federated/          # Sub-agents
│   │   ├── __init__.py
│   │   ├── explorer.py
│   │   └── executor.py
│   ├── workflows/          # Temporal workflows
│   │   ├── __init__.py
│   │   └── remediation.py
│   ├── activities/         # Temporal activities
│   │   ├── __init__.py
│   │   └── investigate.py
│   └── models/             # Pydantic models
│       ├── __init__.py
│       └── diagnosis.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_explorer.py
│   └── test_workflows.py
├── pyproject.toml
└── README.md
```

## Import Order

### ✅ Correct Pattern

```python
# Standard library
import asyncio
import logging
from datetime import timedelta
from typing import Optional

# Third-party
import structlog
from pydantic import BaseModel
from temporalio import workflow

# Local - kubani framework
from strands import Agent, tool
from kubani.framework.config import get_config
from kubani.framework.mcp import get_mcp_client

# Local - same package
from .models import PodDiagnosis
from .activities import investigate_pod
```

## Testing Conventions

### Test Structure

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with real services
├── e2e/            # End-to-end tests
└── conftest.py     # Shared fixtures
```

### Key Fixtures

```python
@pytest.fixture
def test_config():
    """Provide test configuration."""
    with patch.dict("os.environ", {"KUBANI_ENVIRONMENT": "test"}):
        from kubani.framework.config import get_config, reload_config
        reload_config()
        yield get_config()

@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for isolated testing."""
    with patch("kubani.framework.mcp.get_mcp_client") as mock:
        client = AsyncMock()
        client.memory.store_learning.return_value = {"id": "learning-123"}
        client.temporal.list_workflows.return_value = []
        mock.return_value = client
        yield client
```

### Best Practices

- Use `pytest.mark.asyncio` for async tests
- Use `pytest.mark.parametrize` for data-driven tests
- Follow Arrange-Act-Assert pattern
- Descriptive names: `test_critic_identifies_memory_leak_pattern`
- Mock external services, not internal logic
- Run with `just test` or `kubani test <agent>`
