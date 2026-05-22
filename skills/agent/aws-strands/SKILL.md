---
name: aws-strands
description: Build AI agents with Strands Agents SDK. Use when developing model-agnostic agents, implementing ReAct patterns, creating multi-agent systems, or building production agents on AWS. Triggers on Strands, Strands SDK, model-agnostic agent, ReAct agent.
---

# Strands Agents SDK

Build model-agnostic AI agents with the Strands framework.

## Installation

```bash
pip install strands-agents strands-agents-tools
# Or with npm
npm install @strands-agents/sdk
```

## Quick Start

```python
from strands import Agent
from strands.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Implementation
    return f"Weather in {city}: 72°F, Sunny"

agent = Agent(
    model="anthropic.claude-3-sonnet",
    tools=[get_weather]
)

response = agent("What's the weather in Seattle?")
print(response)
```

## TypeScript/JavaScript

```typescript
import { Agent, tool } from '@strands-agents/sdk';

const getWeather = tool({
  name: 'get_weather',
  description: 'Get current weather for a city',
  parameters: {
    city: { type: 'string', description: 'City name' }
  },
  handler: async ({ city }) => {
    return `Weather in ${city}: 72°F, Sunny`;
  }
});

const agent = new Agent({
  model: 'anthropic.claude-3-sonnet',
  tools: [getWeather]
});

const response = await agent.run('What\'s the weather in Seattle?');
```

## Model Agnostic

Strands works with any LLM:

```python
from strands import Agent

# Anthropic (default)
agent = Agent(model="anthropic.claude-3-sonnet")

# OpenAI
agent = Agent(model="openai.gpt-4o")

# Amazon Bedrock
agent = Agent(model="amazon.titan-text-premier")

# Custom endpoint
agent = Agent(
    model="custom",
    endpoint="https://your-model-endpoint.com",
    api_key="..."
)
```

## Tool Definition Patterns

### Decorator Style
```python
from strands.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the product database.
    
    Args:
        query: Search query string
        limit: Maximum results to return
    """
    # Implementation
    return results
```

### Class Style
```python
from strands.tools import Tool

class DatabaseSearchTool(Tool):
    name = "search_database"
    description = "Search the product database"
    
    def parameters(self):
        return {
            "query": {"type": "string", "description": "Search query"},
            "limit": {"type": "integer", "default": 10}
        }
    
    def run(self, query: str, limit: int = 10):
        return self.db.search(query, limit)
```

## ReAct Pattern

Built-in ReAct (Reasoning + Acting) support:

```python
from strands import Agent, ReActStrategy

agent = Agent(
    model="anthropic.claude-3-sonnet",
    tools=[search_tool, calculate_tool],
    strategy=ReActStrategy(
        max_iterations=10,
        verbose=True
    )
)

# Agent will reason through complex multi-step tasks
response = agent("""
    Find the top 3 products in our database, 
    calculate their average price,
    and recommend if we should adjust pricing.
""")
```

## Multi-Agent Systems

```python
from strands import Agent, MultiAgentOrchestrator

# Specialist agents
researcher = Agent(
    name="researcher",
    model="anthropic.claude-3-sonnet",
    tools=[web_search, document_reader],
    system_prompt="You are a research specialist."
)

analyst = Agent(
    name="analyst",
    model="anthropic.claude-3-sonnet",
    tools=[data_analyzer, chart_generator],
    system_prompt="You are a data analyst."
)

writer = Agent(
    name="writer",
    model="anthropic.claude-3-sonnet",
    tools=[document_writer],
    system_prompt="You are a technical writer."
)

# Orchestrator
orchestrator = MultiAgentOrchestrator(
    agents=[researcher, analyst, writer],
    routing="supervisor"  # or "round_robin", "intent"
)

response = orchestrator.run(
    "Research AI trends, analyze the data, and write a report"
)
```

## Streaming Responses

```python
from strands import Agent

agent = Agent(model="anthropic.claude-3-sonnet")

# Stream response
for chunk in agent.stream("Explain quantum computing"):
    print(chunk, end="", flush=True)
```

## Memory Management

```python
from strands import Agent
from strands.memory import ConversationMemory, SemanticMemory

agent = Agent(
    model="anthropic.claude-3-sonnet",
    memory=[
        ConversationMemory(max_turns=10),
        SemanticMemory(embedding_model="text-embedding-3-small")
    ]
)

# Memory persists across calls
agent("My name is Alice")
agent("What's my name?")  # Remembers: "Your name is Alice"
```

## AgentCore Integration

Use Strands with AWS Bedrock AgentCore:

```python
from strands import Agent
from strands.tools import tool
import boto3

agentcore_client = boto3.client('bedrock-agentcore')

@tool
def query_cloudwatch(metric_name: str, namespace: str) -> dict:
    """Query CloudWatch metrics via AgentCore Gateway."""
    return agentcore_client.invoke_tool(
        tool_name="cloudwatch_query",
        parameters={"metric": metric_name, "namespace": namespace}
    )

agent = Agent(
    model="anthropic.claude-3-sonnet",
    tools=[query_cloudwatch]
)
```

## Official Use Cases

Strands is featured in AWS AgentCore samples:

**A2A Multi-Agent Incident Response**: Uses Strands for monitoring agent
```bash
cd amazon-bedrock-agentcore-samples/02-use-cases/A2A-multi-agent-incident-response
# Monitoring agent uses Strands SDK for CloudWatch, logs, metrics
```

## Resources

- **Official Samples**: https://github.com/awslabs/amazon-bedrock-agentcore-samples
- **A2A Use Case**: https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases/A2A-multi-agent-incident-response
- **Integrations**: https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/03-integrations
