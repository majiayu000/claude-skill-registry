---
name: strands-agents
description: Build AI agents with the Strands Agents SDK, an open-source framework from AWS. Use when building autonomous agents, creating custom tools with @tool decorator, orchestrating multi-agent systems (swarm, graph, agents-as-tools), integrating MCP servers, or deploying agents to production. Supports Amazon Bedrock, Anthropic API, OpenAI, Ollama, and other model providers.
---

# Strands Agents SDK

Build AI agents using the model-driven Strands Agents SDK. Agents consist of three components: a model, tools, and a prompt.

## Installation

```bash
pip install strands-agents strands-agents-tools --break-system-packages
```

## Basic Agent

```python
from strands import Agent

agent = Agent(system_prompt="You are a helpful assistant.")
response = agent("Hello, how can you help me?")
print(response)
```

## Custom Tools

Use `@tool` decorator to convert Python functions into agent tools:

```python
from strands import Agent, tool

@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate rectangle area.
    
    Args:
        length: Rectangle length
        width: Rectangle width
    
    Returns:
        Area of the rectangle
    """
    return length * width

agent = Agent(tools=[calculate_area])
agent("What is the area of a 5x3 rectangle?")
```

Key requirements for tools:
- Clear docstring (used by LLM to understand when/how to use the tool)
- Type hints for all parameters and return value
- Descriptive parameter names

### Class-Based Tools

For tools that share state or resources:

```python
from strands import Agent, tool

class DatabaseTools:
    def __init__(self, connection_string: str):
        self.conn = self._connect(connection_string)
    
    def _connect(self, conn_str):
        return {"connected": True, "db": conn_str}
    
    @tool
    def query(self, sql: str) -> dict:
        """Execute SQL query.
        
        Args:
            sql: SQL query to execute
        """
        return {"results": f"Query: {sql}", "connection": self.conn}

db = DatabaseTools("postgres://...")
agent = Agent(tools=[db.query])
```

## Model Providers

Default is Amazon Bedrock with Claude. Configure alternatives:

```python
from strands import Agent
from strands.models import BedrockModel
from strands.models.ollama import OllamaModel
from strands.models.anthropic import AnthropicModel

# Amazon Bedrock (default)
agent = Agent(model=BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-west-2"
))

# Anthropic API (set ANTHROPIC_API_KEY env var)
agent = Agent(model=AnthropicModel(
    client_args={"api_key": "<KEY>"},
    model_id="claude-sonnet-4-20250514",
    max_tokens=1028
))

# Ollama (local)
agent = Agent(model=OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1"
))
```

## MCP Integration

Connect to Model Context Protocol servers for external tools:

```python
from strands import Agent
from strands.tools.mcp import MCPClient

# Stdio transport
mcp = MCPClient(transport="stdio", command="npx", args=["-y", "@modelcontextprotocol/server-filesystem"])

agent = Agent(tools=[mcp])
agent("List files in the current directory")
```

## Multi-Agent Patterns

### Agents as Tools

Wrap specialized agents as tools for an orchestrator:

```python
from strands import Agent, tool

@tool
def research_assistant(query: str) -> str:
    """Research factual information.
    
    Args:
        query: Research question
    """
    researcher = Agent(system_prompt="You are a research expert.")
    return str(researcher(query))

@tool  
def code_assistant(task: str) -> str:
    """Write and explain code.
    
    Args:
        task: Coding task description
    """
    coder = Agent(system_prompt="You are a coding expert.")
    return str(coder(task))

orchestrator = Agent(
    system_prompt="Route tasks to the appropriate specialist.",
    tools=[research_assistant, code_assistant]
)
```

### Swarm

Autonomous agent collaboration with shared context:

```python
from strands import Agent
from strands.multiagent import Swarm

researcher = Agent(name="researcher", system_prompt="You research topics thoroughly.")
analyst = Agent(name="analyst", system_prompt="You analyze data and findings.")
writer = Agent(name="writer", system_prompt="You write clear reports.")

swarm = Swarm([researcher, analyst, writer])
result = swarm("Research AI trends and write a summary report")
```

Swarms enable emergent intelligence through:
- Shared working memory
- Autonomous handoffs between agents
- Dynamic task delegation

### Graph

Deterministic workflows with defined execution order:

```python
from strands import Agent
from strands.multiagent import GraphBuilder

researcher = Agent(name="researcher", system_prompt="Research the topic.")
reviewer = Agent(name="reviewer", system_prompt="Review and fact-check.")
writer = Agent(name="writer", system_prompt="Write the final output.")

builder = GraphBuilder()
builder.add_node(researcher, "research")
builder.add_node(reviewer, "review") 
builder.add_node(writer, "write")
builder.add_edge("research", "review")
builder.add_edge("review", "write")
builder.set_entry_point("research")

graph = builder.build()
result = graph("Write a report on quantum computing")
```

#### Conditional Edges

```python
def needs_revision(state):
    return "needs revision" in state.results.get("review", {}).get("output", "").lower()

builder.add_edge("review", "research", condition=needs_revision)  # Loop back
builder.add_edge("review", "write", condition=lambda s: not needs_revision(s))
```

## Streaming

### Callback Handler

```python
from strands import Agent
from strands.handlers import PrintingCallbackHandler

agent = Agent(callback_handler=PrintingCallbackHandler())
agent("Tell me a story")
```

### Async Iterator

```python
import asyncio
from strands import Agent

async def stream_response():
    agent = Agent()
    async for event in agent.stream_async("Tell me a story"):
        if hasattr(event, 'data'):
            print(event.data, end="", flush=True)

asyncio.run(stream_response())
```

## Session Management

Persist conversations across sessions:

```python
from strands import Agent
from strands.session import FileSessionManager

session_mgr = FileSessionManager(session_id="user-123", base_dir="./sessions")
agent = Agent(session_manager=session_mgr)

agent("Remember my name is Alice")
# Later session...
agent("What's my name?")  # Recalls "Alice"
```

## Built-in Tools

The `strands-agents-tools` package provides:
- `calculator` - Math operations
- `current_time` - Get current time
- `http_request` - Make HTTP requests
- `file_read`, `file_write`, `editor` - File operations
- `python_repl` - Execute Python code
- `shell` - Run shell commands
- `memory` - Store/retrieve information
- `retrieve` - RAG retrieval
- `mcp_client` - Dynamic MCP server connections

```python
from strands import Agent
from strands_tools import calculator, current_time, file_read

agent = Agent(tools=[calculator, current_time, file_read])
```

## Pattern Selection Guide

| Pattern | Use When |
|---------|----------|
| Single Agent | Simple tasks, direct tool use |
| Agents as Tools | Hierarchical delegation, clear specialist roles |
| Swarm | Exploration, brainstorming, emergent solutions |
| Graph | Deterministic workflows, conditional logic, loops |

## References

For detailed API documentation and advanced patterns, see:
- `references/model-providers.md` - Complete model provider configurations
- `references/multi-agent-patterns.md` - Advanced multi-agent architectures
