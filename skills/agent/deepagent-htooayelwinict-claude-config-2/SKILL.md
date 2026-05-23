---
name: deepagent
description: Expert guidance for DeepAgents framework - simplified agent creation with tool integration for LangChain/LangGraph workflows.
---

# DeepAgent Skill

Use this skill when working with the DeepAgents framework for simplified AI agent creation.

## Core Concepts

### 1. Creating a DeepAgent
```python
from deepagents import create_deep_agent

# Basic agent with default settings
agent = create_deep_agent()

# With custom model
agent = create_deep_agent(model="gpt-4o")

# With custom system prompt
agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    system_prompt="You are an expert Python developer."
)
```

### 2. Adding Tools
```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"Weather in {city}: 72°F, sunny"

@tool
def search_docs(query: str) -> str:
    """Search documentation for information."""
    return f"Found docs about: {query}"

# Create agent with tools
agent = create_deep_agent(
    model="gpt-4o",
    tools=[get_weather, search_docs]
)
```

### 3. Tool Functions from Modules
```python
# Define tools in a module
# tools.py
def calculate(expression: str) -> float:
    """Evaluate a math expression."""
    return eval(expression)

def fetch_data(url: str) -> dict:
    """Fetch JSON data from URL."""
    import requests
    return requests.get(url).json()

# Use in agent
from myproject import tools

agent = create_deep_agent(
    tools=[tools.calculate, tools.fetch_data]
)
```

### 4. Invoking the Agent
```python
# Simple invoke
response = agent.invoke({"messages": [("human", "What's the weather in NYC?")]})

# With message history
from langchain_core.messages import HumanMessage, AIMessage

messages = [
    HumanMessage(content="Hello!"),
    AIMessage(content="Hi! How can I help?"),
    HumanMessage(content="What's 2+2?")
]
response = agent.invoke({"messages": messages})
```

### 5. Streaming Responses
```python
# Stream output
for chunk in agent.stream({"messages": [("human", "Tell me a story")]}):
    print(chunk)

# Async streaming
async for chunk in agent.astream({"messages": messages}):
    print(chunk)
```

## Integration Patterns

### With LangChain LCEL
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# DeepAgent as part of larger chain
prompt = ChatPromptTemplate.from_template("Summarize: {text}")

chain = (
    {"text": lambda x: x["input"]}
    | prompt
    | agent
    | StrOutputParser()
)
```

### With LangGraph
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Use DeepAgent as a node
def agent_node(state: State):
    result = agent.invoke({"messages": state["messages"]})
    return {"messages": result["messages"]}

workflow = StateGraph(State)
workflow.add_node("agent", agent_node)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

app = workflow.compile()
```

### Sysadmin Tool Integration
```python
from sysadmin_tool.agent import create_deepagent, get_deepagent_tools

# Get pre-configured sysadmin tools
tools = get_deepagent_tools()
# Returns: [system_info, disk_usage, memory_info, top_processes, service_action, tail_log]

# Create specialized sysadmin agent
sysadmin_agent = create_deepagent(
    model="gpt-4o",
    system_prompt="You are a system administrator assistant. Help users monitor and manage their systems safely."
)

# Invoke for system tasks
response = sysadmin_agent.invoke({
    "messages": [("human", "Check disk usage on /")]
})
```

## Custom Agent Patterns

### Research Agent
```python
@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    # Implementation
    pass

@tool
def read_url(url: str) -> str:
    """Read content from a URL."""
    # Implementation
    pass

research_agent = create_deep_agent(
    model="gpt-4o",
    tools=[web_search, read_url],
    system_prompt="""You are a research assistant. 
    Search for information and provide well-sourced answers.
    Always cite your sources."""
)
```

### Code Assistant Agent
```python
@tool
def run_python(code: str) -> str:
    """Execute Python code and return output."""
    # Safe execution implementation
    pass

@tool
def read_file(path: str) -> str:
    """Read a file from the filesystem."""
    # Implementation
    pass

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    # Implementation
    pass

code_agent = create_deep_agent(
    model="claude-sonnet-4-20250514",
    tools=[run_python, read_file, write_file],
    system_prompt="""You are an expert programmer.
    Help users write, debug, and improve code.
    Always explain your changes."""
)
```

### Multi-Tool Agent
```python
# Combine tools from multiple sources
from sysadmin_tool.agent import get_deepagent_tools

sysadmin_tools = get_deepagent_tools()
custom_tools = [web_search, read_url]
all_tools = sysadmin_tools + custom_tools

comprehensive_agent = create_deep_agent(
    model="gpt-4o",
    tools=all_tools,
    system_prompt="You are a versatile assistant with system admin and research capabilities."
)
```

## Best Practices

1. **Tool Design** - Keep tools focused and well-documented with clear docstrings
2. **Error Handling** - Tools should return informative error messages
3. **System Prompts** - Be specific about agent capabilities and limitations
4. **Safety** - Implement safeguards for destructive operations
5. **Logging** - Add callback handlers for debugging and monitoring
6. **Testing** - Test tools individually before combining

## Common Tool Patterns

### Safe Tool Execution
```python
@tool
def safe_execute(command: str) -> str:
    """Execute a whitelisted command."""
    allowed = ["ls", "pwd", "whoami", "date"]
    cmd = command.split()[0]
    if cmd not in allowed:
        return f"Error: '{cmd}' is not allowed"
    # Execute safely
    pass
```

### Tool with Confirmation
```python
@tool
def delete_file(path: str, confirm: bool = False) -> str:
    """Delete a file. Requires confirm=True."""
    if not confirm:
        return f"To delete {path}, call with confirm=True"
    # Delete file
    pass
```

## Installation
```bash
pip install deepagents langchain langchain-openai
# Or with all extras
pip install deepagents[all]
```
