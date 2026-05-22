---
name: aws-strands-agents-agentcore
description: Use when working with AWS Strands Agents SDK or Amazon Bedrock AgentCore platform for building AI agents. Provides architecture guidance, implementation patterns, deployment strategies, observability, quality evaluations, multi-agent orchestration, and MCP server integration.
---

# AWS Strands Agents & AgentCore

## Overview

**AWS Strands Agents SDK**: Open-source Python framework for building AI agents with model-driven orchestration (minimal code, model decides tool usage)

**Amazon Bedrock AgentCore**: Enterprise platform for deploying, operating, and scaling agents in production

**Relationship**: Strands SDK runs standalone OR with AgentCore platform services. AgentCore is optional but provides enterprise features (8hr runtime, streaming, memory, identity, observability).

---

## Quick Start Decision Tree

### What are you building?

**Single-purpose agent**:
- Event-driven (S3, SQS, scheduled) → Lambda deployment
- Interactive with streaming → AgentCore Runtime
- API endpoint (stateless) → Lambda

**Multi-agent system**:
- Deterministic workflow → Graph Pattern
- Autonomous collaboration → Swarm Pattern
- Simple delegation → Agent-as-Tool Pattern

**Tool/Integration Server (MCP)**:
- **ALWAYS** deploy to ECS/Fargate or AgentCore Runtime
- **NEVER Lambda** (stateful, needs persistent connections)

See **[architecture.md](references/architecture.md)** for deployment examples.

---

## Critical Constraints

### MCP Server Requirements

1. **Transport**: MUST use `streamable-http` (NOT `stdio`)
2. **Endpoint**: MUST be at `0.0.0.0:8000/mcp`
3. **Deployment**: MUST be ECS/Fargate or AgentCore Runtime (NEVER Lambda)
4. **Headers**: Must accept `application/json` and `text/event-stream`

**Why**: MCP servers are stateful and need persistent connections. Lambda is ephemeral and unsuitable.

See **[limitations.md](references/limitations.md)** for details.

### Tool Count Limits

- Models struggle with > 50-100 tools
- **Solution**: Implement semantic search for dynamic tool loading

See **[patterns.md](references/patterns.md)** for implementation.

### Token Management

- Claude 4.5: 200K context (use ~180K max)
- Long conversations REQUIRE conversation managers
- Multi-agent costs multiply 5-10x

See **[limitations.md](references/limitations.md)** for strategies.

---

## Deployment Decision Matrix

| Component              | Lambda         | ECS/Fargate | AgentCore Runtime |
|------------------------|----------------|-------------|-------------------|
| **Stateless Agents**   | ✅ Perfect      | ❌ Overkill  | ❌ Overkill        |
| **Interactive Agents** | ❌ No streaming | ⚠️ Possible  | ✅ Ideal           |
| **MCP Servers**        | ❌ NEVER        | ✅ Standard  | ✅ With features   |
| **Duration**           | < 15 minutes   | Unlimited   | Up to 8 hours     |
| **Cold Starts**        | Yes (30-60s)   | No          | No                |

---

## Multi-Agent Pattern Selection

| Pattern           | Complexity | Predictability | Cost | Use Case                 |
|-------------------|------------|----------------|------|--------------------------|
| **Single Agent**  | Low        | High           | 1x   | Most tasks               |
| **Agent as Tool** | Low        | High           | 2-3x | Simple delegation        |
| **Graph**         | High       | Very High      | 3-5x | Deterministic workflows  |
| **Swarm**         | Medium     | Low            | 5-8x | Autonomous collaboration |

**Recommendation**: Start with single agents, evolve as needed.

See **[architecture.md](references/architecture.md)** for examples.

---

## When to Read Reference Files

### [patterns.md](references/patterns.md)
- Base agent factory patterns (reusable components)
- MCP server registry patterns (tool catalogues)
- Semantic tool search (> 50 tools)
- Tool design best practices
- Security patterns
- Testing patterns

### [observability.md](references/observability.md)
- **AWS AgentCore Observability Platform** setup
- Runtime-hosted vs self-hosted configuration
- Session tracking for multi-turn conversations
- OpenTelemetry setup
- Cost tracking hooks
- Production observability patterns

### [evaluations.md](references/evaluations.md)
- **AWS AgentCore Evaluations** - Quality assessment with LLM-as-a-Judge
- 13 built-in evaluators (Helpfulness, Correctness, GoalSuccessRate, etc.)
- Custom evaluators with your own prompts and models
- Online (continuous) and on-demand evaluation modes
- CloudWatch integration and alerting

### [limitations.md](references/limitations.md)
- MCP server deployment issues
- Tool selection problems (> 50 tools)
- Token overflow
- Lambda limitations
- Multi-agent cost concerns
- Throttling errors
- Cold start latency

---

#-Driven Philosophy

**Key Concept**: Strands Agents delegates orchestration to the model rather than requiring explicit control flow code.

```python
# Traditional: Manual orchestration (avoid)
while not done:
    if needs_research:
        result = research_tool()
    elif needs_analysis:
        result = analysis_tool()

# Strands: Model decides (prefer)
agent = Agent(
    system_prompt="You are a research analyst. Use tools to answer questions.",
    tools=[research_tool, analysis_tool]
)
result = agent("What are the top tech trends?")
 automatically orchestrates: research_tool → analysis_tool → respond
```

---

# Selection

**Primary Provider**: Anthropic Claude via AWS Bedrock

**Model ID Format**: `anthropic.claude-{model}-{version}`

**Current Models** (as of January 2025):
- `anthropic.claude-sonnet-4-5-20250929-v1:0` - Production
- `anthropic.claude-haiku-4-5-20251001-v1:0` - Fast/economical
- `anthropic.claude-opus-4-5-20250514-v1:0` - Complex reasoning

**Check Latest Models**:
```bash
aws bedrock list-foundation-models --by-provider anthropic \
  --query 'modelSummaries[*].[modelId,modelName]' --output table
```

---

## Quick Examples

### Basic Agent

```python
from strands import Agent
from strands.models import BedrockModel
from strands.session import DynamoDBSessionManager
from strands.agent.conversation_manager import SlidingWindowConversationManager

agent = Agent(
    agent_id="my-agent",
    model=BedrockModel(model_id="anthropic.claude-sonnet-4-5-20250929-v1:0"),
    system_prompt="You are helpful.",
    tools=[tool1, tool2],
    session_manager=DynamoDBSessionManager(table_name="sessions"),
    conversation_manager=SlidingWindowConversationManager(max_messages=20)
)

result = agent("Process this request")
```

See **[patterns.md](references/patterns.md)** for base agent factory patterns.

### MCP Server (ECS/Fargate)

```python
from mcp.server import FastMCP
import psycopg2.pool

# Persistent connection pool (why Lambda won't work)
db_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, host="db.internal")

mcp = FastMCP("Database Tools")

@mcp.tool()
def query_database(sql: str) -> dict:
    conn = db_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return {"status": "success", "rows": cursor.fetchall()}
    finally:
        db_pool.putconn(conn)

# CRITICAL: streamable-http mode
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

See **[architecture.md](references/architecture.md)** for deployment details.

### Tool Error Handling

```python
from strands import tool

@tool
def safe_tool(param: str) -> dict:
    """Always return structured results, never raise exceptions."""
    try:
        result = operation(param)
        return {"status": "success", "content": [{"text": str(result)}]}
    except Exception as e:
        return {"status": "error", "content": [{"text": f"Failed: {str(e)}"}]}
```

See **[patterns.md](references/patterns.md)** for tool design patterns.

### Observability

**AgentCore Runtime (Automatic)**:
```python
# Install with OTEL support
# pip install 'strands-agents[otel]'
# Add 'aws-opentelemetry-distro' to requirements.txt

from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
agent = Agent(...)  # Automatically instrumented

@app.entrypoint
def handler(payload):
    return agent(payload["prompt"])
```

**Self-Hosted**:
```bash
export AGENT_OBSERVABILITY_ENABLED=true
export OTEL_PYTHON_DISTRO=aws_distro
export OTEL_RESOURCE_ATTRIBUTES="service.name=my-agent"

opentelemetry-instrument python agent.py
```

**General OpenTelemetry**:
```python
from strands.observability import StrandsTelemetry

# Development
telemetry = StrandsTelemetry().setup_console_exporter()

# Production
telemetry = StrandsTelemetry().setup_otlp_exporter()
```

See **[observability.md](references/observability.md)** for detailed patterns.

---

## Session Storage Selection

```
Local dev         → FileSystem
Lambda agents     → S3 or DynamoDB
ECS agents        → DynamoDB
Interactive chat  → AgentCore Memory
Knowledge bases   → AgentCore Memory
```

See **[architecture.md](references/architecture.md)** for storage backend comparison.

---

## When to Use AgentCore Platform vs SDK Only

### Use Strands SDK Only
- Simple, stateless agents
- Tight cost control required
- No enterprise features needed
- Want deployment flexibility

### Use Strands SDK + AgentCore Platform
- Need 8-hour runtime support
- Streaming responses required
- Enterprise security/compliance
- Cross-session intelligence needed
- Want managed infrastructure

See **[architecture.md](references/architecture.md)** for platform service details.

---

## Common Anti-Patterns

1. ❌ **Overloading agents with > 50 tools** → Use semantic search
2. ❌ **No conversation management** → Implement SlidingWindow or Summarising
3. ❌ **Deploying MCP servers to Lambda** → Use ECS/Fargate
4. ❌ **No timeout configuration** → Set execution limits everywhere
5. ❌ **Ignoring token limits** → Implement conversation managers
6. ❌ **No cost monitoring** → Implement cost tracking from day one

See **[patterns.md](references/patterns.md)** and **[limitations.md](references/limitations.md)** for details.

---

## Production Checklist

Before deploying:

- [ ] Conversation management configured
- [ ] **AgentCore Observability enabled** or OpenTelemetry configured
- [ ] **AgentCore Evaluations configured** for quality monitoring
- [ ] Observability hooks implemented
- [ ] Cost tracking enabled
- [ ] Error handling in all tools
- [ ] Security permissions validated
- [ ] MCP servers deployed to ECS/Fargate
- [ ] Timeout limits set
- [ ] Session backend configured (DynamoDB for production)
- [ ] CloudWatch alarms configured

---

## Reference Files Navigation

- **[architecture.md](references/architecture.md)** - Deployment patterns, multi-agent orchestration, session storage, AgentCore services
- **[patterns.md](references/patterns.md)** - Foundation components, tool design, security, testing, performance optimisation
- **[limitations.md](references/limitations.md)** - Known constraints, workarounds, mitigation strategies, challenges
- **[observability.md](references/observability.md)** - AgentCore Observability platform, ADOT, GenAI dashboard, OpenTelemetry, hooks, cost tracking
- **[evaluations.md](references/evaluations.md)** - AgentCore Evaluations, built-in evaluators, custom evaluators, quality monitoring

---

## Key Takeaways

1. **MCP servers MUST use streamable-http, NEVER Lambda**
2. **Use semantic search for > 15 tools**
3. **Always implement conversation management**
4. **Multi-agent costs multiply 5-10x** (track from day one)
5. **Set timeout limits everywhere**
6. **Error handling in tools is non-negotiable**
7. **Lambda for stateless, AgentCore for interactive**
8. **AgentCore Observability and Evaluations for production**
9. **Start simple, evolve complexity**
10. **Security by default**
11. **Separate config from code**
