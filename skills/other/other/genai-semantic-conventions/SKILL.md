---
name: genai:semantic-conventions
description: OpenTelemetry GenAI semantic conventions for agent instrumentation - the standard attributes for LLM observability
---

# OpenTelemetry GenAI Semantic Conventions

Reference for instrumenting agents with OpenTelemetry GenAI semantic conventions.

**Spec**: https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Architecture

```
Agent (gen_ai.* only) → OTEL Collector → Transform → Phoenix (llm.*) + MLflow (mlflow.trace.*)
```

Agents emit **only** `gen_ai.*` attributes. The OTEL Collector transforms these to:
- **OpenInference format** (`llm.*`) for Phoenix
- **MLflow metadata** (`mlflow.trace.*`) for MLflow session tracking

## Core Attributes

### Request Attributes (on LLM call spans)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.system` | string | GenAI provider/system | `openai`, `anthropic`, `langchain` |
| `gen_ai.request.model` | string | Model requested | `gpt-4`, `claude-3-opus` |
| `gen_ai.request.max_tokens` | int | Max tokens to generate | `1024` |
| `gen_ai.request.temperature` | float | Sampling temperature | `0.7` |
| `gen_ai.request.top_p` | float | Nucleus sampling | `0.9` |

### Response Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.response.model` | string | Model that responded | `gpt-4-0613` |
| `gen_ai.response.id` | string | Response identifier | `chatcmpl-abc123` |
| `gen_ai.response.finish_reasons` | string[] | Why generation stopped | `["stop"]` |
| `gen_ai.usage.input_tokens` | int | Prompt tokens | `150` |
| `gen_ai.usage.output_tokens` | int | Completion tokens | `250` |

### Conversation/Session Attributes

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.conversation.id` | string | Session/conversation ID | `uuid-123-456` |
| `gen_ai.prompt` | string | User prompt (truncated) | `What is the weather?` |
| `gen_ai.completion` | string | Response (truncated) | `The weather is sunny` |

### Agent Attributes (custom, for A2A agents)

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `gen_ai.agent.name` | string | Agent name | `weather-assistant` |
| `gen_ai.agent.id` | string | Agent/task ID | `task-uuid-789` |

## Python Usage

### Auto-instrumentation (Recommended)

```python
# Install: pip install opentelemetry-instrumentation-openai
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

# Instruments all OpenAI SDK calls automatically
OpenAIInstrumentor().instrument()
```

### Manual Span Attributes

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span(
    "gen_ai.agent.invoke",
    attributes={
        "gen_ai.conversation.id": context_id,
        "gen_ai.agent.name": "my-agent",
        "gen_ai.system": "langchain",
        "gen_ai.request.model": "gpt-4",
        "gen_ai.prompt": user_input[:500],  # Truncate for size
    }
) as span:
    # Agent logic here
    result = await agent.run(user_input)

    # Add response attributes
    span.set_attribute("gen_ai.completion", str(result)[:500])
```

### Adding to Existing Span

```python
current_span = trace.get_current_span()
if current_span and current_span.is_recording():
    current_span.set_attribute("gen_ai.conversation.id", session_id)
    current_span.set_attribute("gen_ai.agent.name", "weather-assistant")
```

## OTEL Collector Transforms

The collector transforms `gen_ai.*` to target formats:

### GenAI → OpenInference (Phoenix)

| GenAI Attribute | OpenInference Attribute |
|-----------------|------------------------|
| `gen_ai.request.model` | `llm.model_name` |
| `gen_ai.usage.input_tokens` | `llm.token_count.prompt` |
| `gen_ai.usage.output_tokens` | `llm.token_count.completion` |
| `gen_ai.system` | `llm.provider`, `llm.system` |

### GenAI → MLflow

| GenAI Attribute | MLflow Metadata |
|-----------------|-----------------|
| `gen_ai.conversation.id` | `mlflow.trace.session` (resource) |
| Span name `gen_ai.agent.*` | `mlflow.spanType=AGENT` |
| Span with `gen_ai.request.model` | `mlflow.spanType=LLM` |
| Span name `gen_ai.tool.*` | `mlflow.spanType=TOOL` |

## Span Naming Conventions

Use GenAI operation names for spans:

| Operation | Span Name |
|-----------|-----------|
| Agent invocation | `gen_ai.agent.invoke` |
| LLM chat completion | `gen_ai.chat` |
| Tool call | `gen_ai.tool.{tool_name}` |
| Embedding | `gen_ai.embeddings` |

## Best Practices

1. **Always set `gen_ai.conversation.id`** for session tracking in MLflow
2. **Truncate prompts/completions** to ~500 chars to avoid span size issues
3. **Use auto-instrumentation** when available (OpenAI, Anthropic SDKs)
4. **Add manual attributes** for custom agent spans
5. **Never emit OpenInference (`llm.*`) directly** - let the collector transform

## Dependencies

```toml
# pyproject.toml
dependencies = [
    "opentelemetry-sdk",
    "opentelemetry-exporter-otlp",
    "opentelemetry-instrumentation-openai>=0.34b0",  # For OpenAI auto-instrumentation
]
```

## Related Skills

- `auth:otel-oauth2-exporter` - Configure OTel Collector with OAuth2
- `k8s:health` - Platform health including observability components
- [OpenTelemetry GenAI Spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [MLflow Tracing](https://mlflow.org/docs/latest/llms/tracing/index.html)
- [OpenInference Spec](https://github.com/Arize-ai/openinference)
