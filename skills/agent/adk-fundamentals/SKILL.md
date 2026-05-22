---
name: adk-fundamentals
description: |
  Foundational knowledge for creating ADK (Agent Development Kit) agents including environment setup, project structure, and basic agent scaffolding.
  MUST BE USED for: new ADK agent creation, ADK project setup, environment configuration, AdkApp initialization, and understanding core ADK architecture.
  Keywords: create adk agent, new agent, setup adk, adk project, environment setup, AdkApp, agent scaffolding.
---

# ADK Fundamentals: Agent Scaffolding and Setup

## Core Principles

The Google Agent Development Kit (ADK) is an open-source Python framework for building production-grade AI agents with Vertex AI integration. ADK provides structured patterns for tool creation, state management, and multi-agent orchestration.

## Environment Setup (Required Pattern)

### Step 1: Create Python Environment with uv

ADK requires Python 3.13+ and modern dependency management. Use `uv` for fast, reliable environment setup:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project directory
mkdir my-agent-project
cd my-agent-project

# Initialize Python 3.13 project
uv init --python 3.13

# Install ADK
uv pip install google-adk

# Install supporting libraries
uv pip install pydantic>=2.12 python-dotenv asyncio
```

### Step 2: Configure Vertex AI Environment

Create a `.env` file for Vertex AI configuration:

```bash
# .env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=True

# Optional: Authentication
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

Load environment variables in your code:

```python
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
```

## Basic Agent Structure (Canonical Pattern)

### Minimal ADK Agent

```python
"""
Example ADK agent with Vertex AI integration.
"""
import asyncio
from google import genai
from google.genai import types

async def main() -> None:
    """Run the basic ADK agent."""
    # Initialize Vertex AI client
    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION
    )

    # Create a simple agent
    model_id = "gemini-2.0-flash-exp"

    # Generate response
    response = await client.aio.models.generate_content(
        model=model_id,
        contents="Hello, how can you help me today?"
    )

    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

### Agent with Tools (Production Pattern)

```python
"""
ADK agent with custom tools.
"""
import asyncio
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from google import genai
from google.genai import types

# Define tool schema with Pydantic (MANDATORY)
class WeatherRequest(BaseModel):
    """Request schema for weather tool."""
    model_config = ConfigDict(strict=True, frozen=True)

    location: str = Field(description="City name or location")
    units: str = Field(
        default="celsius",
        description="Temperature units: celsius or fahrenheit"
    )

# Define tool function (MUST be async for I/O)
async def get_weather(request: WeatherRequest) -> dict[str, any]:
    """
    Get current weather for a location.

    Args:
        request: Weather request with location and units

    Returns:
        Weather data dictionary
    """
    # Simulate API call (replace with actual weather API)
    return {
        "location": request.location,
        "temperature": 22,
        "units": request.units,
        "conditions": "sunny"
    }

async def main() -> None:
    """Run agent with tools."""
    client = genai.Client(vertexai=True)

    # Create tool from function
    weather_tool = types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_weather",
                description="Get current weather for a location",
                parameters=WeatherRequest.model_json_schema()
            )
        ]
    )

    # Create agent with tools
    model = "gemini-2.0-flash-exp"
    chat = client.aio.chats.create(
        model=model,
        config=types.GenerateContentConfig(
            tools=[weather_tool],
            temperature=0.7
        )
    )

    # Send message
    response = await chat.send_message(
        "What's the weather in San Francisco?"
    )

    # Handle tool calls
    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                # Execute tool
                result = await get_weather(
                    WeatherRequest(**part.function_call.args)
                )

                # Send result back to agent
                response = await chat.send_message(
                    types.Content(
                        parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=part.function_call.name,
                                response=result
                            )
                        )]
                    )
                )

    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

## Project Directory Structure (Recommended)

Organize ADK projects with clear separation:

```
my-adk-agent/
├── .env                    # Environment configuration
├── .env.example           # Template for environment variables
├── pyproject.toml         # Python dependencies (uv)
├── README.md              # Project documentation
├── src/
│   ├── __init__.py
│   ├── agent.py           # Main agent definition
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather.py     # Weather tool
│   │   └── search.py      # Search tool
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── models.py      # Pydantic schemas
│   └── config.py          # Configuration management
└── tests/
    ├── __init__.py
    ├── test_agent.py
    └── test_tools.py
```

## Key ADK Concepts

### 1. LlmAgent vs WorkflowAgent

**LlmAgent**: For dynamic, reasoning-based tasks
- Model decides next action based on context
- Suitable for open-ended conversations
- Flexible tool selection

**WorkflowAgent**: For deterministic processes
- Hardcoded execution flow
- Suitable for repeatable workflows
- Predictable behavior

### 2. Session State

Share data between tool calls:

```python
from google.genai import types

# In tool function
async def save_preference(
    context: types.ToolContext,
    preference: str
) -> dict:
    """Save user preference to session state."""
    context.state["user_preference"] = preference
    return {"status": "saved"}

# Another tool can access state
async def get_preference(context: types.ToolContext) -> str:
    """Retrieve user preference from session state."""
    return context.state.get("user_preference", "default")
```

### 3. Memory Service

For long-term memory across sessions:

```python
# Configure memory service
config = types.GenerateContentConfig(
    memory_service=types.MemoryService(
        collection_name="user_memories",
        max_memories=100
    )
)
```

## Anti-Patterns to Avoid

### ❌ Blocking I/O in Tools
```python
# BAD: Synchronous I/O
def get_data():
    response = requests.get(url)  # Blocks event loop
    return response.json()

# GOOD: Async I/O
async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### ❌ Not Using Pydantic for Tool Schemas
```python
# BAD: Manual schema definition
tool_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"}
    }
}

# GOOD: Pydantic BaseModel
class LocationRequest(BaseModel):
    model_config = ConfigDict(strict=True)
    location: str

tool_schema = LocationRequest.model_json_schema()
```

### ❌ Missing Error Handling
```python
# BAD: No error handling
async def risky_operation():
    return await api_call()

# GOOD: Comprehensive error handling
async def safe_operation() -> dict | None:
    try:
        return await asyncio.wait_for(
            api_call(),
            timeout=10.0
        )
    except TimeoutError:
        logger.error("Operation timed out")
        return None
    except Exception as e:
        logger.exception(f"Operation failed: {e}")
        return None
```

## When to Use This Skill

Activate this skill when:
- Creating a new ADK agent project
- Setting up Vertex AI environment
- Understanding ADK architecture fundamentals
- Scaffolding agent structure
- Configuring agent tools

## Integration Points

This skill is a **foundational dependency** for:
- `adk-tool-authoring-with-pydantic`: Tool creation builds on this foundation
- `agent-orchestration`: Multi-agent patterns extend single-agent basics
- `rag-patterns`: RAG integration requires basic agent structure

## Related Resources

For deeper understanding:
- **Google ADK Documentation**: https://google.github.io/adk-docs/
- **ADK Python GitHub**: https://github.com/google/adk-python
- **ADK Foundation Codelab**: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
- **Vertex AI Quickstart**: https://cloud.google.com/vertex-ai/generative-ai/docs/agent-development-kit/quickstart
- **Pydantic V2 Strict Mode**: See `agentient-python-core/pydantic-v2-strict` skill
- **Async Patterns**: See `agentient-python-core/async-patterns` skill
