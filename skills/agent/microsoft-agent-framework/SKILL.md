---
name: microsoft-agent-framework
version: 0.1.0
description: |
  Comprehensive knowledge of Microsoft Agent Framework for building production AI agents and workflows.
  Auto-activates for agent building, workflow design, AutoGen migration, and enterprise AI tasks.
---

# Microsoft Agent Framework Skill

**Version**: 0.1.0-preview | **Last Updated**: 2025-11-15 | **Framework Version**: 0.1.0-preview
**Languages**: Python 3.10+, C# (.NET 8.0+) | **License**: MIT

## Quick Reference

Microsoft Agent Framework is an open-source platform for building production AI agents and workflows, unifying AutoGen's simplicity with Semantic Kernel's enterprise features.

**Core Capabilities**: AI Agents (stateful conversations, tool integration) | Workflows (graph-based orchestration, parallel processing) | Enterprise features (telemetry, middleware, MCP support)

**Installation**:

- Python: `pip install agent-framework --pre`
- C#: `dotnet add package Microsoft.Agents.AI --prerelease`

**Repository**: https://github.com/microsoft/agent-framework (5.1k stars)

---

## When to Use This Skill

Use Microsoft Agent Framework when you need:

1. **Production AI Agents** with enterprise features (telemetry, middleware, structured outputs)
2. **Multi-Agent Orchestration** via graph-based workflows with conditional routing
3. **Tool/Function Integration** with approval workflows and error handling
4. **Cross-Platform Development** requiring both Python and C# implementations
5. **Research-to-Production Pipeline** leveraging AutoGen + Semantic Kernel convergence

**Integration with amplihack**: Use Agent Framework for **stateful conversational agents** and **complex orchestration**. Use amplihack's native agent system for **stateless task delegation** and **simple orchestration**. See `@integration/decision-framework.md` for detailed guidance.

---

## Core Concepts

### 1. AI Agents

Stateful conversational entities that process messages, call tools, and maintain context.

**Python Example**:

```python
from agents_framework import Agent, ModelClient

# Create agent with model
agent = Agent(
    name="assistant",
    model=ModelClient(model="gpt-4"),
    instructions="You are a helpful assistant"
)

# Single-turn conversation
response = await agent.run(message="Hello!")
print(response.content)

# Multi-turn with thread
from agents_framework import Thread
thread = Thread()
response = await agent.run(thread=thread, message="What's 2+2?")
response = await agent.run(thread=thread, message="Double that")
```

**C# Example**:

```csharp
using Microsoft.Agents.AI;

var agent = new Agent(
    name: "assistant",
    model: new ModelClient(model: "gpt-4"),
    instructions: "You are a helpful assistant"
);

var response = await agent.RunAsync("Hello!");
Console.WriteLine(response.Content);
```

### 2. Tools & Functions

Extend agent capabilities by providing callable functions.

**Python Example**:

```python
from agents_framework import function_tool

@function_tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = Agent(
    name="assistant",
    model=ModelClient(model="gpt-4"),
    tools=[get_weather]
)

response = await agent.run(message="What's the weather in Seattle?")
# Agent automatically calls get_weather() and responds with result
```

**C# Example**:

```csharp
[FunctionTool]
public static string GetWeather(string location)
{
    return $"Weather in {location}: Sunny, 72°F";
}

var agent = new Agent(
    name: "assistant",
    model: new ModelClient(model: "gpt-4"),
    tools: new[] { typeof(Tools).GetMethod("GetWeather") }
);
```

### 3. Workflows

Graph-based orchestration for multi-agent systems with conditional routing and parallel execution.

**Python Example**:

```python
from agents_framework import Workflow, GraphWorkflow

# Define workflow graph
workflow = GraphWorkflow()

# Add agents as nodes
workflow.add_node("researcher", research_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("reviewer", review_agent)

# Define edges (control flow)
workflow.add_edge("researcher", "writer")  # Sequential
workflow.add_edge("writer", "reviewer")

# Conditional routing
def should_revise(state):
    return state.get("needs_revision", False)

workflow.add_conditional_edge(
    "reviewer",
    should_revise,
    {"revise": "writer", "done": "END"}
)

# Execute workflow
result = await workflow.run(initial_message="Research AI trends")
```

**C# Example**:

```csharp
var workflow = new GraphWorkflow();

workflow.AddNode("researcher", researchAgent);
workflow.AddNode("writer", writerAgent);
workflow.AddNode("reviewer", reviewAgent);

workflow.AddEdge("researcher", "writer");
workflow.AddEdge("writer", "reviewer");

var result = await workflow.RunAsync("Research AI trends");
```

### 4. Context & State Management

Maintain conversation history and shared state across agents.

**Python**:

```python
from agents_framework import Thread, ContextProvider

# Thread maintains conversation history
thread = Thread()
await agent.run(thread=thread, message="Remember: My name is Alice")
await agent.run(thread=thread, message="What's my name?")  # "Alice"

# Custom context provider
class DatabaseContext(ContextProvider):
    async def get_context(self, thread_id: str):
        return await db.fetch_history(thread_id)

    async def save_context(self, thread_id: str, messages):
        await db.save_history(thread_id, messages)

agent = Agent(model=model, context_provider=DatabaseContext())
```

### 5. Middleware & Telemetry

Add cross-cutting concerns like logging, auth, and monitoring.

**Python**:

```python
from agents_framework import Middleware
from opentelemetry import trace

# Custom middleware
class LoggingMiddleware(Middleware):
    async def process(self, message, next_handler):
        print(f"Processing: {message.content}")
        response = await next_handler(message)
        print(f"Response: {response.content}")
        return response

# OpenTelemetry integration
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("agent-run"):
    response = await agent.run(message="Hello")
```

**C#**:

```csharp
public class LoggingMiddleware : IMiddleware
{
    public async Task<Message> ProcessAsync(Message message, Func<Message, Task<Message>> next)
    {
        Console.WriteLine($"Processing: {message.Content}");
        var response = await next(message);
        Console.WriteLine($"Response: {response.Content}");
        return response;
    }
}
```

---

## Common Patterns

### Human-in-the-Loop Approval

```python
from agents_framework import HumanInTheLoop

@function_tool
def delete_file(path: str) -> str:
    """Delete a file (requires approval)."""
    return f"Deleted {path}"

# Add approval wrapper
delete_file_with_approval = HumanInTheLoop(
    tool=delete_file,
    approval_prompt="Approve deletion of {path}?"
)

agent = Agent(tools=[delete_file_with_approval])
```

### Parallel Agent Execution

```python
workflow = GraphWorkflow()

# Add multiple agents
workflow.add_node("analyst1", analyst_agent)
workflow.add_node("analyst2", analyst_agent)
workflow.add_node("synthesizer", synthesis_agent)

# Parallel execution
workflow.add_edge("START", ["analyst1", "analyst2"])  # Both run in parallel
workflow.add_edge(["analyst1", "analyst2"], "synthesizer")  # Wait for both

result = await workflow.run(message="Analyze market trends")
```

### Structured Output Generation

```python
from pydantic import BaseModel

class WeatherReport(BaseModel):
    location: str
    temperature: float
    conditions: str

agent = Agent(
    model=model,
    instructions="Generate weather reports",
    response_format=WeatherReport
)

response = await agent.run(message="Weather in Seattle")
report: WeatherReport = response.parsed
print(f"{report.location}: {report.temperature}°F, {report.conditions}")
```

### Error Handling & Retries

```python
from agents_framework import RetryPolicy

agent = Agent(
    model=model,
    retry_policy=RetryPolicy(
        max_retries=3,
        backoff_factor=2.0,
        exceptions=[TimeoutError, ConnectionError]
    )
)

try:
    response = await agent.run(message="Hello")
except Exception as e:
    print(f"Failed after retries: {e}")
```

---

## Integration with amplihack

### Decision Framework

**Use Microsoft Agent Framework when**:

- Building stateful conversational agents (multi-turn dialogue)
- Need enterprise features (telemetry, middleware, auth)
- Complex multi-agent orchestration with conditional routing
- Cross-platform requirements (Python + C#)
- Integration with Microsoft ecosystem (Azure, M365)

**Use amplihack native agents when**:

- Stateless task delegation (code review, analysis)
- Simple sequential/parallel orchestration
- File-based operations and local tooling
- Rapid prototyping without infrastructure
- Token-efficient skill-based architecture

**Hybrid Approach**:

```python
# Use amplihack for orchestration
from claude import Agent as ClaudeAgent

orchestrator = ClaudeAgent("orchestrator.md")

# Delegate to Agent Framework for stateful agents
from agents_framework import Agent, Thread

conversational_agent = Agent(
    model=ModelClient(model="gpt-4"),
    instructions="Maintain conversation context"
)

thread = Thread()
response1 = await conversational_agent.run(thread=thread, message="Start task")
response2 = await conversational_agent.run(thread=thread, message="Continue")

# Use amplihack for final synthesis
result = orchestrator.process({"responses": [response1, response2]})
```

See `@integration/amplihack-integration.md` for complete patterns.

---

## Quick Start Workflow

1. **Install**: `pip install agent-framework --pre` (Python) or `dotnet add package Microsoft.Agents.AI --prerelease` (C#)

2. **Create Basic Agent**:

   ```python
   from agents_framework import Agent, ModelClient

   agent = Agent(
       name="assistant",
       model=ModelClient(model="gpt-4"),
       instructions="You are a helpful assistant"
   )

   response = await agent.run(message="Hello!")
   ```

3. **Add Tools**:

   ```python
   @function_tool
   def calculate(expr: str) -> float:
       return eval(expr)

   agent = Agent(model=model, tools=[calculate])
   ```

4. **Build Workflow**:

   ```python
   workflow = GraphWorkflow()
   workflow.add_node("agent1", agent1)
   workflow.add_node("agent2", agent2)
   workflow.add_edge("agent1", "agent2")
   result = await workflow.run(message="Task")
   ```

5. **Add Telemetry**:
   ```python
   from opentelemetry import trace
   tracer = trace.get_tracer(__name__)
   with tracer.start_as_current_span("agent-run"):
       response = await agent.run(message="Hello")
   ```

---

## Reference Documentation

For detailed information, see:

- `@reference/01-overview.md` - Architecture, components, use cases
- `@reference/02-agents.md` - Agent creation, lifecycle, advanced features
- `@reference/03-workflows.md` - Workflow patterns, executors, checkpointing
- `@reference/04-tools-functions.md` - Tool definition, approval workflows, error handling
- `@reference/05-context-middleware.md` - Context providers, middleware patterns, auth
- `@reference/06-telemetry-monitoring.md` - OpenTelemetry, logging, debugging
- `@reference/07-advanced-patterns.md` - Multi-agent patterns, streaming, DevUI

## Working Examples

- `@examples/01-basic-agent.py` - Simple conversational agent
- `@examples/02-tool-integration.py` - Agent with function calling
- `@examples/03-simple-workflow.py` - Multi-agent workflow
- `@examples/04-basic-agent.cs` - C# agent implementation
- `@examples/05-tool-integration.cs` - C# tool integration
- `@examples/06-simple-workflow.cs` - C# workflow example

## Maintenance

Check framework freshness: `python @scripts/check-freshness.py`

Current version tracking: `@metadata/version-tracking.json`

---

**Token Count**: ~4,200 tokens (under 4,800 limit)
