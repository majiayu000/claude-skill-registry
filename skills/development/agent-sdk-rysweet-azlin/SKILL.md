---
name: claude-agent-sdk
description: Comprehensive knowledge of Claude Agent SDK architecture, tools, hooks, skills, and production patterns. Auto-activates for agent building, SDK integration, tool design, and MCP server tasks.
version: 1.0.0
last_updated: 2025-11-15
source_urls:
  - https://docs.claude.com/en/docs/agent-sdk/overview
  - https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
  - https://docs.claude.com/en/docs/agent-sdk/skills
  - https://github.com/kenneth-liao/claude-agent-sdk-intro
activation_keywords:
  - agent sdk
  - claude agent
  - sdk tools
  - agent hooks
  - mcp server
  - subagent
  - agent loop
  - agent permissions
  - agent skill
auto_activate: true
token_budget: 4500
---

# Claude Agent SDK - Comprehensive Skill

## Overview

The **Claude Agent SDK** is Anthropic's official framework for building production-ready AI agents with Claude. It provides a high-level abstraction over the Messages API, handling the agent loop, tool orchestration, context management, and extended-thinking patterns automatically.

### When to Use the Agent SDK

**Use the Agent SDK when:**

- Building autonomous agents that need to use tools iteratively
- Implementing agentic workflows with verification and iteration
- Creating subagent hierarchies for complex task decomposition
- Integrating MCP (Model Context Protocol) servers for standardized tools
- Need production patterns like hooks, permissions, and context management

**Don't use when:**

- Simple single-turn API calls suffice (use Messages API directly)
- No tool use required (standard chat)
- Custom agent loop logic needed (SDK loop is opinionated)

### Language Support

- **Python**: `claude-agents` package (recommended for most use cases)
- **TypeScript**: `@anthropics/agent-sdk` package (Node.js environments)

Both implementations share the same core concepts and API patterns.

## Quick Start

### Installation

**Python:**

```bash
pip install claude-agents
```

**TypeScript:**

```bash
npm install @anthropics/agent-sdk
```

### Authentication

Set your API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or pass it explicitly in code:

```python
from claude_agents import Agent

agent = Agent(api_key="your-api-key-here")
```

### Basic Agent Creation

**Python Example:**

```python
from claude_agents import Agent

# Create agent with default settings
agent = Agent(
    model="claude-sonnet-4-5-20250929",
    system="You are a helpful assistant focused on accuracy."
)

# Run simple task
result = agent.run("What is 2+2?")
print(result.response)
```

**TypeScript Example:**

```typescript
import { Agent } from "@anthropics/agent-sdk";

const agent = new Agent({
  model: "claude-sonnet-4-5-20250929",
  system: "You are a helpful assistant focused on accuracy.",
});

const result = await agent.run("What is 2+2?");
console.log(result.response);
```

### First Tool Example

Tools extend agent capabilities with external functions:

**Python:**

```python
from claude_agents import Agent
from claude_agents.tools import Tool

# Define custom tool
def get_weather(location: str) -> dict:
    """Get weather for a location."""
    return {"location": location, "temp": 72, "condition": "sunny"}

weather_tool = Tool(
    name="get_weather",
    description="Get current weather for a location",
    input_schema={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    },
    function=get_weather
)

# Agent with custom tool
agent = Agent(
    model="claude-sonnet-4-5-20250929",
    tools=[weather_tool]
)

result = agent.run("What's the weather in San Francisco?")
print(result.response)
```

## Core Concepts Reference

### The Agent Loop

The SDK manages a complete agent loop automatically:

1. **Input Processing**: User message + system prompt + tools
2. **Model Invocation**: Claude generates response (text or tool calls)
3. **Tool Execution**: SDK executes requested tools, handles results
4. **Iteration**: Results fed back to model, continues until completion
5. **Output**: Final response with full conversation history

**Key Properties:**

- Automatic iteration until task completion or max turns
- Built-in error handling and retry logic
- Context management with automatic compaction options
- Token budget tracking and optimization

### Context Management

The SDK manages conversation context automatically:

**Context Components:**

- System prompt (persistent instructions)
- Conversation history (user messages + assistant responses)
- Tool definitions (available capabilities)
- Tool results (execution outputs)

**Subagents for Context Isolation:**

```python
# Spawn subagent with isolated context
with agent.subagent(
    system="You are a code reviewer focused on security.",
    tools=[security_scan_tool]
) as reviewer:
    review = reviewer.run("Review this code for vulnerabilities: ...")

# Subagent context doesn't pollute parent
```

**Context Compaction:**
When approaching token limits, the SDK can automatically summarize earlier conversation turns while preserving critical information.

### Tools System

Tools are the agent's interface to external capabilities.

**Built-in Tools:**

- `bash`: Execute shell commands
- `read_file`: Read file contents
- `write_file`: Write data to files
- `edit_file`: Modify existing files
- `glob`: File pattern matching
- `grep`: Content search

**Custom Tool Schema:**

```python
Tool(
    name="tool_name",              # Unique identifier
    description="What it does",    # Clear capability description
    input_schema={                 # JSON Schema for parameters
        "type": "object",
        "properties": {...},
        "required": [...]
    },
    function=callable              # Python function or async function
)
```

**MCP Integration:**
The SDK can use Model Context Protocol (MCP) servers as tool providers:

```python
from claude_agents import Agent
from claude_agents.mcp import MCPClient

# Connect to MCP server
mcp_client = MCPClient("npx", ["-y", "@modelcontextprotocol/server-filesystem"])

agent = Agent(
    model="claude-sonnet-4-5-20250929",
    mcp_clients=[mcp_client]
)
```

### Permissions System

Control which tools agents can access:

**Allowed Tools (Whitelist):**

```python
agent = Agent(
    model="claude-sonnet-4-5-20250929",
    tools=[tool1, tool2, tool3, tool4],
    allowed_tools=["tool1", "tool2"]  # Only these can be used
)
```

**Disallowed Tools (Blacklist):**

```python
agent = Agent(
    model="claude-sonnet-4-5-20250929",
    tools=[tool1, tool2, tool3],
    disallowed_tools=["tool3"]  # All except tool3
)
```

**Permission Modes:**

- `"strict"`: Agent MUST get permission before tool use (via hooks)
- `"permissive"`: Agent can use allowed tools freely (default)

### Hooks System

Hooks provide lifecycle event interception for observability, validation, and control.

**Available Hooks:**

- `PreToolUseHook`: Before tool execution (validation, logging, blocking)
- `PostToolUseHook`: After tool execution (logging, result modification)
- `PreSubagentStartHook`: Before subagent spawns (context setup)
- `PostSubagentStopHook`: After subagent completes (result processing)

**Basic Hook Example:**

```python
from claude_agents.hooks import PreToolUseHook

class LoggingHook(PreToolUseHook):
    async def execute(self, context):
        print(f"Tool: {context.tool_name}")
        print(f"Args: {context.tool_input}")
        return context  # Allow execution

agent = Agent(
    model="claude-sonnet-4-5-20250929",
    hooks=[LoggingHook()]
)
```

**Blocking Tool Use:**

```python
class ValidationHook(PreToolUseHook):
    async def execute(self, context):
        if context.tool_name == "bash" and "rm -rf" in context.tool_input.get("command", ""):
            raise PermissionError("Destructive command blocked")
        return context
```

## Common Patterns

### File Operations

```python
from claude_agents import Agent

agent = Agent(
    model="claude-sonnet-4-5-20250929",
    allowed_tools=["read_file", "write_file", "glob"]
)

result = agent.run(
    "Read all Python files in ./src and create a summary in summary.md"
)
```

### Code Execution

```python
agent = Agent(
    model="claude-sonnet-4-5-20250929",
    allowed_tools=["bash"]
)

result = agent.run(
    "Run the test suite and analyze any failures"
)
```

### Agentic Search (Gather-Act Pattern)

```python
# Agent automatically gathers information iteratively
search_agent = Agent(
    model="claude-sonnet-4-5-20250929",
    tools=[web_search_tool, read_url_tool]
)

result = search_agent.run(
    "Research the latest developments in quantum computing and summarize key papers"
)
```

### Subagent Delegation

```python
main_agent = Agent(model="claude-sonnet-4-5-20250929")

# Delegate specialized task to subagent
with main_agent.subagent(
    system="You are an expert data analyzer.",
    tools=[analyze_csv_tool, plot_tool]
) as analyzer:
    analysis = analyzer.run("Analyze sales_data.csv and create visualizations")

# Results available to main agent
main_agent.run(f"Based on this analysis: {analysis.response}, what actions should we take?")
```

### Error Handling

```python
from claude_agents import Agent, AgentError

agent = Agent(model="claude-sonnet-4-5-20250929")

try:
    result = agent.run("Your task here", max_turns=10)
except AgentError as e:
    print(f"Agent failed: {e}")
    print(f"Turns completed: {e.turns_completed}")
    print(f"Last message: {e.last_message}")
```

### Verification Pattern

```python
# Agent can self-verify results
agent = Agent(
    model="claude-sonnet-4-5-20250929",
    tools=[calculator_tool, verify_tool]
)

result = agent.run(
    "Calculate the compound interest for $10000 at 5% for 10 years. "
    "Verify your calculation by computing it a second way."
)
```

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Deep understanding of agent loop internals
- Complete API reference for all SDK features
- Detailed tool schema specifications
- Permission and security configuration options
- Comprehensive hooks reference with all event types
- Skills system implementation details

**examples.md** - Read when you need:

- Working code examples for specific patterns
- Tool implementation templates
- Hook implementation examples
- Advanced patterns (subagents, verification, error recovery)
- Integration examples with existing systems

**patterns.md** - Read when you need:

- Production-ready architectural patterns
- Agent loop optimization strategies (Gather, Act, Verify, Iterate)
- Context management best practices
- Tool design principles
- Security patterns and anti-patterns
- Performance optimization techniques

**drift-detection.md** - Read when you need:

- Understanding how this skill stays current
- Implementing drift detection for other skills
- Update workflow and validation processes
- Self-validation mechanisms

### Integration with Amplihack

The Agent SDK skill integrates with the Amplihack framework:

**Creating Amplihack Agents with SDK:**

```python
# In .claude/agents/amplihack/specialized/my_agent.md
# Use Agent SDK patterns for tool-using agents
from claude_agents import Agent
from claude_agents.tools import Tool

def create_specialized_agent():
    return Agent(
        model="claude-sonnet-4-5-20250929",
        system="<agent_role_from_md>",
        tools=[...],  # Custom tools for this agent
        hooks=[...]   # Logging, validation hooks
    )
```

**Using MCP Servers in Amplihack:**

```python
# Integrate MCP tools into Amplihack workflow
from claude_agents.mcp import MCPClient

mcp_client = MCPClient("npx", ["-y", "@modelcontextprotocol/server-github"])

agent = Agent(
    model="claude-sonnet-4-5-20250929",
    mcp_clients=[mcp_client]
)

# Agent can now use GitHub MCP tools
result = agent.run("Create a GitHub issue for the bug we just found")
```

**Hooks for Amplihack Observability:**

```python
# Log all agent actions to Amplihack runtime logs
class AmplihackLoggingHook(PreToolUseHook):
    async def execute(self, context):
        log_to_amplihack_runtime(
            session_id=get_current_session(),
            tool=context.tool_name,
            input=context.tool_input
        )
        return context
```

## Quick Reference

### Essential Commands

```python
# Basic agent
agent = Agent(model="claude-sonnet-4-5-20250929")
result = agent.run("task")

# With tools
agent = Agent(model="...", tools=[tool1, tool2])

# With permissions
agent = Agent(model="...", allowed_tools=["tool1"])

# With hooks
agent = Agent(model="...", hooks=[LogHook()])

# Subagent
with agent.subagent(system="...") as sub:
    result = sub.run("subtask")

# MCP integration
from claude_agents.mcp import MCPClient
mcp = MCPClient("npx", ["-y", "mcp-server-name"])
agent = Agent(model="...", mcp_clients=[mcp])
```

### Common Tool Patterns

```python
# File operations
tools=["read_file", "write_file", "glob"]

# Code execution
tools=["bash"]

# All built-in
tools=["bash", "read_file", "write_file", "edit_file", "glob", "grep"]
```

### Token Budget Recommendations

- Simple tasks: 4K-8K tokens
- Complex tasks: 16K-32K tokens
- Research/analysis: 64K-128K tokens
- Maximum context: 200K tokens (model dependent)

## Next Steps

1. **Start Simple**: Create a basic agent with built-in tools
2. **Add Custom Tools**: Implement tools for your specific domain
3. **Add Hooks**: Implement logging and validation
4. **Use Subagents**: Delegate specialized tasks
5. **Integrate MCP**: Use standardized tool servers
6. **Optimize**: Tune context, permissions, and verification patterns

For complete API details, see `reference.md`.
For working code, see `examples.md`.
For production patterns, see `patterns.md`.
