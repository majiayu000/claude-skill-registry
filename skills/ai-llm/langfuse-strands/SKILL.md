---
name: langfuse-strands
description: Integrate Langfuse observability with AWS Strands Agents for comprehensive tracing, monitoring, and debugging of AI agent applications. Use when building Strands agents that need production observability, when debugging agent behavior, when tracking costs/latency/token usage, or when setting up OpenTelemetry-based tracing for Strands.
---

# Langfuse + Strands Agents Observability

Integrate Langfuse's open-source LLM observability platform with AWS Strands Agents using OpenTelemetry.

## Core Integration Pattern

```python
import os
import base64
from strands import Agent
from strands.telemetry import StrandsTelemetry
from strands.models.bedrock import BedrockModel

# 1. Configure Langfuse credentials
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_BASE_URL"] = "https://cloud.langfuse.com"  # EU default
# os.environ["LANGFUSE_BASE_URL"] = "https://us.cloud.langfuse.com"  # US region

# 2. Configure OTEL exporter for Langfuse
LANGFUSE_AUTH = base64.b64encode(
    f"{os.environ['LANGFUSE_PUBLIC_KEY']}:{os.environ['LANGFUSE_SECRET_KEY']}".encode()
).decode()
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{os.environ['LANGFUSE_BASE_URL']}/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# 3. Initialize telemetry BEFORE creating agent
strands_telemetry = StrandsTelemetry().setup_otlp_exporter()

# 4. Create agent with trace attributes
agent = Agent(
    model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0"),
    system_prompt="Your system prompt here",
    trace_attributes={
        "session.id": "unique-session-id",
        "user.id": "user@example.com",
        "langfuse.tags": ["production", "customer-support"]
    }
)

# 5. Run agent - traces automatically sent to Langfuse
result = agent("User query here")
```

## Installation

```bash
pip install strands-agents[otel] langfuse
# Optional: pip install strands-agents-tools for pre-built tools
```

## Key Configuration Reference

### Trace Attributes

Pass these in `trace_attributes` when creating an Agent:

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `session.id` | Group related conversations | `"chat-abc123"` |
| `user.id` | Track per-user metrics | `"user@domain.com"` |
| `langfuse.tags` | Filter/organize in UI | `["prod", "v2"]` |

### Model Providers

Strands supports multiple providers. Configure the model before passing to Agent:

```python
# Amazon Bedrock (default)
from strands.models.bedrock import BedrockModel
model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")

# Anthropic direct
from strands.models.anthropic import AnthropicModel
model = AnthropicModel(model_id="claude-sonnet-4-20250514")

# OpenAI
from strands.models.openai import OpenAIModel
model = OpenAIModel(model_id="gpt-4o")

# Ollama (local)
from strands.models.ollama import OllamaModel
model = OllamaModel(model_id="llama3")
```

## Common Patterns

### Adding Custom Tools

```python
from strands import Agent, tool

@tool
def search_database(query: str) -> str:
    """Search the customer database."""
    # Tool implementation
    return f"Results for: {query}"

agent = Agent(
    model=model,
    tools=[search_database],
    trace_attributes={"session.id": "..."}
)
```

### Combining with Langfuse SDK for Custom Spans

```python
from langfuse import observe, get_client

langfuse = get_client()

@observe()
def my_pipeline(user_input: str):
    # Pre-processing traced as custom span
    processed = preprocess(user_input)
    
    # Strands agent call - automatically traced
    result = agent(processed)
    
    # Post-processing traced as custom span
    return postprocess(result)
```

### Multi-Agent Orchestration

```python
from strands import Agent
from strands.multiagent import AgentTool

# Create specialized agents
researcher = Agent(model=model, system_prompt="Research specialist...")
writer = Agent(model=model, system_prompt="Writing specialist...")

# Orchestrator can delegate to sub-agents
orchestrator = Agent(
    model=model,
    system_prompt="Coordinate research and writing tasks...",
    tools=[
        AgentTool(researcher, name="researcher"),
        AgentTool(writer, name="writer")
    ],
    trace_attributes={"session.id": "multi-agent-session"}
)
```

## Langfuse Dashboard Features

After traces flow to Langfuse, use these features:

- **Trace View**: See full agent execution flow, tool calls, LLM generations
- **Cost Tracking**: Monitor token usage and costs per trace/session/user
- **Latency Analysis**: Identify slow operations via timeline view
- **Session Grouping**: View multi-turn conversations together
- **Filtering**: Use tags, user IDs, session IDs to filter traces
- **Evaluation**: Add scores to traces for quality monitoring

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No traces appearing | Verify OTEL environment variables are set before `StrandsTelemetry()` call |
| Auth errors | Check public/secret key pair matches Langfuse project |
| Missing tool spans | Ensure tools use `@tool` decorator from strands |
| Bedrock access denied | Enable model access in AWS Bedrock console |

## Additional Resources

- See `references/advanced-patterns.md` for async patterns, AgentCore deployment, and evaluation with Ragas
- See `references/environment-setup.md` for complete environment variable reference
