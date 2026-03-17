---
name: deepagents-implementation
description: Implements agents using Deep Agents. Use when building agents with create_deep_agent, configuring backends, defining subagents, adding middleware, or setting up human-in-the-loop workflows.
---

# Deep Agents Implementation

## Core Concepts

Deep Agents provides a batteries-included agent harness built on LangGraph:

- **`create_deep_agent`**: Factory function that creates a configured agent
- **Middleware**: Injected capabilities (filesystem, todos, subagents, summarization)
- **Backends**: Pluggable file storage (state, filesystem, store, composite)
- **Subagents**: Isolated task execution via the `task` tool

The agent returned is a compiled LangGraph `StateGraph`, compatible with streaming, checkpointing, and LangGraph Studio.

## Essential Imports

```python
# Core
from deepagents import create_deep_agent

# Subagents
from deepagents import CompiledSubAgent

# Backends
from deepagents.backends import (
    StateBackend,       # Ephemeral (default)
    FilesystemBackend,  # Real disk
    StoreBackend,       # Persistent cross-thread
    CompositeBackend,   # Route paths to backends
)

# LangGraph (for checkpointing, store, streaming)
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.memory import InMemoryStore

# LangChain (for custom models, tools)
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
```

## Basic Usage

### Minimal Agent

```python
from deepagents import create_deep_agent

# Uses Claude Sonnet 4 by default
agent = create_deep_agent()

result = agent.invoke({"messages": [{"role": "user", "content": "Hello!"}]})
```

### With Custom Tools

```python
from langchain_core.tools import tool
from deepagents import create_deep_agent

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    return tavily_client.search(query)

agent = create_deep_agent(
    tools=[web_search],
    system_prompt="You are a research assistant. Search the web to answer questions.",
)

result = agent.invoke({"messages": [{"role": "user", "content": "What is LangGraph?"}]})
```

### With Custom Model

```python
from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent

# OpenAI
model = init_chat_model("openai:gpt-4o")

# Or Anthropic with custom settings
from langchain_anthropic import ChatAnthropic
model = ChatAnthropic(model_name="claude-sonnet-4-5-20250929", max_tokens=8192)

agent = create_deep_agent(model=model)
```

### With Checkpointing (Persistence)

```python
from langgraph.checkpoint.memory import InMemorySaver
from deepagents import create_deep_agent

agent = create_deep_agent(checkpointer=InMemorySaver())

# Must provide thread_id with checkpointer
config = {"configurable": {"thread_id": "user-123"}}
result = agent.invoke({"messages": [...]}, config)

# Resume conversation
result = agent.invoke({"messages": [{"role": "user", "content": "Follow up"}]}, config)
```

## Streaming

The agent supports all LangGraph stream modes.

### Stream Updates

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Write a report"}]},
    stream_mode="updates"
):
    print(chunk)  # {"node_name": {"key": "value"}}
```

### Stream Messages (Token-by-Token)

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Explain quantum computing"}]},
    stream_mode="messages"
):
    # Real-time token streaming
    print(chunk.content, end="", flush=True)
```

### Async Streaming

```python
async for chunk in agent.astream(
    {"messages": [...]},
    stream_mode="updates"
):
    print(chunk)
```

### Multiple Stream Modes

```python
for mode, chunk in agent.stream(
    {"messages": [...]},
    stream_mode=["updates", "messages"]
):
    if mode == "messages":
        print("Token:", chunk.content)
    else:
        print("Update:", chunk)
```

## Backend Configuration

### StateBackend (Default - Ephemeral)

Files stored in agent state, persist within thread only.

```python
# Implicit - this is the default
agent = create_deep_agent()

# Explicit
from deepagents.backends import StateBackend
agent = create_deep_agent(backend=lambda rt: StateBackend(rt))
```

### FilesystemBackend (Real Disk)

Read/write actual files on disk. Enables `execute` tool for shell commands.

```python
from deepagents.backends import FilesystemBackend

agent = create_deep_agent(
    backend=FilesystemBackend(root_dir="/path/to/project"),
)
```

### StoreBackend (Persistent Cross-Thread)

Uses LangGraph Store for persistence across conversations.

```python
from langgraph.store.memory import InMemoryStore
from deepagents.backends import StoreBackend

store = InMemoryStore()

agent = create_deep_agent(
    backend=lambda rt: StoreBackend(rt),
    store=store,  # Required for StoreBackend
)
```

### CompositeBackend (Hybrid Routing)

Route different paths to different backends.

```python
from langgraph.store.memory import InMemoryStore
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend

store = InMemoryStore()

agent = create_deep_agent(
    backend=CompositeBackend(
        default=StateBackend(),           # /workspace/* → ephemeral
        routes={
            "/memories/": StoreBackend(store=store),     # persistent
            "/preferences/": StoreBackend(store=store), # persistent
        },
    ),
    store=store,
)

# Files under /memories/ persist across all conversations
# Files under /workspace/ are ephemeral per-thread
```

## Subagents

### Using the Default General-Purpose Agent

By default, a `general-purpose` subagent is available with all main agent tools.

```python
agent = create_deep_agent(tools=[web_search])

# The agent can now delegate via the `task` tool:
# task(subagent_type="general-purpose", prompt="Research topic X in depth")
```

### Defining Custom Subagents

```python
from deepagents import create_deep_agent

research_agent = {
    "name": "researcher",
    "description": "Conducts deep research on complex topics with web search",
    "system_prompt": """You are an expert researcher.
    Search thoroughly, cross-reference sources, and synthesize findings.""",
    "tools": [web_search, document_reader],
}

code_agent = {
    "name": "coder",
    "description": "Writes, reviews, and debugs code",
    "system_prompt": "You are an expert programmer. Write clean, tested code.",
    "tools": [code_executor, linter],
    "model": "openai:gpt-4o",  # Optional: different model per subagent
}

agent = create_deep_agent(
    subagents=[research_agent, code_agent],
    system_prompt="Delegate research to the researcher and coding to the coder.",
)
```

### Pre-compiled LangGraph Subagents

Use existing LangGraph graphs as subagents.

```python
from deepagents import CompiledSubAgent, create_deep_agent
from langgraph.prebuilt import create_react_agent

# Existing graph
custom_graph = create_react_agent(
    model="anthropic:claude-sonnet-4-5-20250929",
    tools=[specialized_tool],
    prompt="Custom workflow instructions",
)

agent = create_deep_agent(
    subagents=[CompiledSubAgent(
        name="custom-workflow",
        description="Runs my specialized analysis workflow",
        runnable=custom_graph,
    )]
)
```

### Subagent with Custom Middleware

```python
from langchain.agents.middleware import AgentMiddleware

class LoggingMiddleware(AgentMiddleware):
    def transform_response(self, response):
        print(f"Subagent response: {response}")
        return response

agent_spec = {
    "name": "logged-agent",
    "description": "Agent with extra logging",
    "system_prompt": "You are helpful.",
    "tools": [],
    "middleware": [LoggingMiddleware()],  # Added after default middleware
}
```

## Human-in-the-Loop

### Basic Interrupt Configuration

Pause execution before specific tools for human approval.

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    tools=[send_email, delete_file, web_search],
    interrupt_on={
        "send_email": True,      # Simple interrupt
        "delete_file": True,     # Require approval before delete
        # web_search not listed - runs without approval
    },
    checkpointer=checkpointer,   # Required for interrupts
)
```

### Interrupt with Options

```python
agent = create_deep_agent(
    tools=[send_email],
    interrupt_on={
        "send_email": {
            "allowed_decisions": ["approve", "edit", "reject"]
        },
    },
    checkpointer=checkpointer,
)

# Invoke - will pause at send_email
config = {"configurable": {"thread_id": "user-123"}}
result = agent.invoke({"messages": [...]}, config)

# Check state
state = agent.get_state(config)
if state.next:  # Has pending interrupt
    # Resume with approval
    from langgraph.types import Command
    agent.invoke(Command(resume={"approved": True}), config)

    # Or resume with edit
    agent.invoke(Command(resume={"edited_args": {"to": "new@email.com"}}), config)

    # Or reject
    agent.invoke(Command(resume={"rejected": True}), config)
```

### Interrupt on Subagent Tools

```python
# Interrupts apply to subagents too
agent = create_deep_agent(
    subagents=[research_agent],
    interrupt_on={
        "web_search": True,  # Interrupt even when subagent calls it
    },
    checkpointer=checkpointer,
)
```

## Custom Middleware

### Middleware Structure

```python
from langchain.agents.middleware.types import (
    AgentMiddleware,
    ModelRequest,
    ModelResponse,
)
from langchain_core.tools import tool

class MyMiddleware(AgentMiddleware):
    # Tools to inject
    tools = []

    # System prompt content to inject
    system_prompt = ""

    def transform_request(self, request: ModelRequest) -> ModelRequest:
        """Modify request before sending to model."""
        return request

    def transform_response(self, response: ModelResponse) -> ModelResponse:
        """Modify response after receiving from model."""
        return response
```

### Injecting Tools via Middleware

```python
from langchain_core.tools import tool

@tool
def get_current_time() -> str:
    """Get the current time."""
    from datetime import datetime
    return datetime.now().isoformat()

class TimeMiddleware(AgentMiddleware):
    tools = [get_current_time]
    system_prompt = "You have access to get_current_time for time-sensitive tasks."

agent = create_deep_agent(middleware=[TimeMiddleware()])
```

### Context Injection Middleware

```python
class UserContextMiddleware(AgentMiddleware):
    def __init__(self, user_preferences: dict):
        self.user_preferences = user_preferences

    @property
    def system_prompt(self):
        return f"User preferences: {self.user_preferences}"

agent = create_deep_agent(
    middleware=[UserContextMiddleware({"theme": "dark", "language": "en"})]
)
```

### Response Logging Middleware

```python
import logging

class LoggingMiddleware(AgentMiddleware):
    def transform_response(self, response: ModelResponse) -> ModelResponse:
        logging.info(f"Agent response: {response.messages[-1].content[:100]}...")
        return response

agent = create_deep_agent(middleware=[LoggingMiddleware()])
```

## MCP Tool Integration

Connect MCP (Model Context Protocol) servers to provide additional tools.

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from deepagents import create_deep_agent

async def main():
    mcp_client = MultiServerMCPClient({
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"],
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_TOKEN": os.environ["GITHUB_TOKEN"]},
        },
    })

    mcp_tools = await mcp_client.get_tools()

    agent = create_deep_agent(tools=mcp_tools)

    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": "List my repos"}]}
    ):
        print(chunk)
```

## Additional References

For detailed reference documentation, see:

- **[Built-in Tools Reference](references/tools.md)** - Complete list of tools available on every agent (filesystem, task management, subagent delegation) with path requirements
- **[Common Patterns](references/patterns.md)** - Production-ready examples including research agents with memory, code assistants with disk access, multi-specialist teams, and production PostgreSQL setup
