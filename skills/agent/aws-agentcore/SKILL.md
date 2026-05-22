---
name: aws-agentcore
description: Build AI agents with AWS Bedrock AgentCore. Use when developing agents on AWS infrastructure, creating tool-use patterns, implementing agent orchestration, or integrating with Bedrock models. Triggers on keywords like AgentCore, Bedrock Agent, AWS agent, Lambda tools.
---

# AWS Bedrock AgentCore

Build production-grade AI agents on AWS infrastructure.

## Quick Start

```python
import boto3
from agentcore import Agent, Tool

# Initialize AgentCore client
client = boto3.client('bedrock-agent-runtime')

# Define a tool
@Tool(name="search_database", description="Search the product database")
def search_database(query: str, limit: int = 10) -> dict:
    # Tool implementation
    return {"results": [...]}

# Create agent
agent = Agent(
    model_id="anthropic.claude-3-sonnet",
    tools=[search_database],
    instructions="You are a helpful product search assistant."
)

# Invoke agent
response = agent.invoke("Find laptops under $1000")
```

## AgentCore Components

AgentCore provides these primitives:

| Component | Purpose |
|-----------|---------|
| **Runtime** | Serverless agent execution (framework-agnostic) |
| **Gateway** | Convert APIs/Lambda to MCP-compatible tools |
| **Memory** | Multi-strategy memory (semantic, user preference) |
| **Identity** | Auth with Cognito, Okta, Google, EntraID |
| **Tools** | Code Interpreter, Browser Tool |
| **Observability** | Deep analysis and tracing |

## Lambda Tool Integration

```python
# Lambda function as tool
import json

def lambda_handler(event, context):
    action = event.get('actionGroup')
    function = event.get('function')
    parameters = event.get('parameters', [])
    
    # Parse parameters
    params = {p['name']: p['value'] for p in parameters}
    
    if function == 'get_weather':
        result = get_weather(params['city'])
    elif function == 'book_flight':
        result = book_flight(params['origin'], params['destination'])
    
    return {
        'response': {
            'actionGroup': action,
            'function': function,
            'functionResponse': {
                'responseBody': {
                    'TEXT': {'body': json.dumps(result)}
                }
            }
        }
    }
```

## Agent Orchestration

```python
from agentcore import SupervisorAgent, SubAgent

# Create specialized sub-agents
research_agent = SubAgent(
    name="researcher",
    model_id="anthropic.claude-3-sonnet",
    instructions="You research and gather information."
)

writer_agent = SubAgent(
    name="writer", 
    model_id="anthropic.claude-3-sonnet",
    instructions="You write clear, engaging content."
)

# Create supervisor
supervisor = SupervisorAgent(
    model_id="anthropic.claude-3-opus",
    sub_agents=[research_agent, writer_agent],
    routing_strategy="supervisor"  # or "intent_classification"
)

response = supervisor.invoke("Write a blog post about AI agents")
```

## Guardrails Integration

```python
from agentcore import Agent, Guardrail

# Define guardrail
guardrail = Guardrail(
    guardrail_id="my-guardrail-id",
    guardrail_version="1"
)

agent = Agent(
    model_id="anthropic.claude-3-sonnet",
    guardrails=[guardrail],
    tools=[...],
)
```

## AgentCore Gateway

Convert existing APIs to MCP-compatible tools:

```python
# gateway_setup.py
from bedrock_agentcore import GatewayClient

gateway = GatewayClient()

# Create gateway from OpenAPI spec
gateway.create_target(
    name="my-api",
    type="OPENAPI",
    openapi_spec_path="./api-spec.yaml"
)

# Create gateway from Lambda function
gateway.create_target(
    name="my-lambda-tool",
    type="LAMBDA",
    function_arn="arn:aws:lambda:us-east-1:123456789:function:my-tool"
)
```

## AgentCore Memory

```python
from agentcore import Agent, Memory

# Create memory with multiple strategies
memory = Memory(
    name="customer-support-memory",
    strategies=["semantic", "user_preference"]
)

agent = Agent(
    model_id="anthropic.claude-3-sonnet",
    memory=memory,
    tools=[...],
)

# Memory persists across sessions
response = agent.invoke(
    "What did we discuss last time?",
    session_id="user-123"
)
```

## Official Use Cases Repository

AWS provides production-ready implementations:

**Repository**: https://github.com/awslabs/amazon-bedrock-agentcore-samples

### Available Use Cases (`02-use-cases/`)

| Use Case | Description |
|----------|-------------|
| **A2A Multi-Agent Incident Response** | Agent-to-Agent with Strands + OpenAI SDK |
| **Customer Support Assistant** | Memory, Knowledge Base, Google OAuth |
| **Market Trends Agent** | LangGraph with browser tools |
| **DB Performance Analyzer** | PostgreSQL integration |
| **Device Management Agent** | IoT with Cognito auth |
| **Enterprise Web Intelligence** | Browser tools for research |
| **Text to Python IDE** | AgentCore Code Interpreter |
| **Video Games Sales Assistant** | Amplify + CDK deployment |

### Quick Start with Use Cases
```bash
git clone https://github.com/awslabs/amazon-bedrock-agentcore-samples.git
cd amazon-bedrock-agentcore-samples/02-use-cases/customer-support-assistant
# Follow README for deployment
```

## Resources

- **Official Samples**: https://github.com/awslabs/amazon-bedrock-agentcore-samples
- **Use Cases**: https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/02-use-cases
- **Tutorials**: https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/01-tutorials
