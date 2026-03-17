---
name: agent-communication-protocol
description: Open protocol for AI agent interoperability enabling standardized communication between agents, applications, and humans across different frameworks
version: 1.1.0
tags: [acp, agents, interoperability, protocol, rest-api, python-sdk, multi-agent, beeai, linux-foundation, orchestration, agentic-workflows]
---

# Agent Communication Protocol (ACP)

ACP is an open protocol for agent interoperability that solves the growing challenge of connecting AI agents, applications, and humans. It enables standardized communication across different frameworks and infrastructures.

## Key Features

- **REST-Based Design** - Straightforward HTTP endpoints (not JSON-RPC)
- **Multi-Modal** - Supports text, images, audio, video, and any MIME type
- **Async-First** - Built primarily for asynchronous communication with sync support
- **Streaming** - Real-time Server-Sent Events (SSE) for incremental updates
- **Stateful/Stateless** - Sessions for maintaining state across interactions
- **Offline Discovery** - Agents remain discoverable through embedded metadata
- **Framework Agnostic** - Works with BeeAI, LangGraph, CrewAI, LlamaIndex, and more

## Installation

```bash
# Create new project with uv
uv init --python '>=3.11' my_acp_project
cd my_acp_project

# Add ACP SDK
uv add acp-sdk

# Or with pip
pip install acp-sdk
```

## Quick Start: Creating an Agent

### Basic Echo Agent

```python
import asyncio
from collections.abc import AsyncGenerator

from acp_sdk.models import Message
from acp_sdk.server import Context, RunYield, RunYieldResume, Server

server = Server()

@server.agent()
async def echo(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    """Echoes everything"""
    for message in input:
        await asyncio.sleep(0.5)
        yield {"thought": "I should echo everything"}
        await asyncio.sleep(0.5)
        yield message

server.run()
```

Run with:
```bash
uv run agent.py
```

Server starts at `http://localhost:8000`.

### Agent with Metadata

```python
@server.agent(
    name="data-analyzer",
    description="Analyzes datasets and generates insights"
)
async def DataAnalyzerAgent(
    input: list[Message], context: Context
) -> AsyncGenerator[RunYield, RunYieldResume]:
    # Implementation
    yield str(response.object)
```

## Agent Manifest

The Agent Manifest describes agent properties for discovery and interoperability.

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Unique RFC 1123 DNS label (1-63 chars) | `"chat"` |
| `description` | Human-readable summary | `"Conversational agent with memory"` |
| `input_content_types` | Supported input MIME types | `["text/plain", "application/json"]` |
| `output_content_types` | Supported output MIME types | `["text/plain", "*/*"]` |

### Optional Metadata

```python
@server.agent(
    name="my-agent",
    description="My custom agent",
    metadata={
        "license": "Apache-2.0",
        "programming_language": "python",
        "framework": "beeai",
        "domains": ["finance", "analytics"],
        "capabilities": [
            {"name": "analysis", "description": "Data analysis"}
        ],
        "recommended_models": ["ollama:llama3.1", "openai:gpt-4o"],
        "author": {"name": "Developer", "email": "dev@example.com"}
    }
)
```

## Message Structure

Messages are the fundamental communication units consisting of ordered parts.

### Message Roles

- `user` - User-originated messages
- `agent` - Generic agent communications
- `agent/{name}` - Specific agent (e.g., `agent/image-analyzer`)

### Message Parts

| Attribute | Required | Details |
|-----------|----------|---------|
| `content_type` | Yes | MIME type (e.g., `text/plain`, `image/png`) |
| `content` OR `content_url` | Yes | Inline or URL-referenced data |
| `content_encoding` | No | `"plain"` (default) or `"base64"` |
| `name` | No | Makes part an Artifact |
| `metadata` | No | Citations, trajectories |

### Common MIME Types

- `text/plain` - Plain text
- `application/json` - Structured data
- `image/png`, `image/jpeg` - Images
- `application/pdf` - Documents
- `*/*` - Any content type

## REST API Endpoints

### Discovery

```bash
# List all agents
curl http://localhost:8000/agents

# Get specific agent manifest
curl http://localhost:8000/agents/{name}
```

### Run Management

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/runs` | Create and start new run |
| `GET` | `/runs/{run_id}` | Get run status |
| `POST` | `/runs/{run_id}` | Resume awaiting run |
| `POST` | `/runs/{run_id}/cancel` | Cancel run |
| `GET` | `/runs/{run_id}/events` | List run events |

### Execution Modes

**Synchronous** - Blocks until completion:
```bash
curl -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "echo",
    "input": [{"role": "user", "parts": [{"content_type": "text/plain", "content": "Hello"}]}],
    "mode": "sync"
  }'
```

**Asynchronous** - Returns run_id for polling:
```bash
curl -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "echo", "input": [...], "mode": "async"}'

# Check status
curl http://localhost:8000/runs/{run_id}
```

**Streaming** - Server-Sent Events:
```bash
curl -N -H "Accept: text/event-stream" -X POST http://localhost:8000/runs \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "echo", "input": [...], "mode": "stream"}'
```

## Python SDK Client

### Basic Client Usage

```python
import asyncio
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

async def example() -> None:
    async with Client(base_url="http://localhost:8000") as client:
        # Synchronous execution
        run = await client.run_sync(
            agent="echo",
            input=[
                Message(
                    parts=[MessagePart(
                        content="Hello from client!",
                        content_type="text/plain"
                    )]
                )
            ],
        )
        print(run.output)

if __name__ == "__main__":
    asyncio.run(example())
```

### Agent Discovery

```python
async with Client(base_url="http://localhost:8000") as client:
    async for agent in client.agents():
        print(f"Agent: {agent.name}")
        print(f"Description: {agent.description}")
```

### Asynchronous Execution

```python
async with Client(base_url="http://localhost:8000") as client:
    run = await client.run_async(agent="echo", input=[...])

    # Poll for completion
    result = await client.run_status(run_id=run.run_id)
```

### Streaming Execution

```python
async with Client(base_url="http://localhost:8000") as client:
    async for event in client.run_stream(agent="echo", input=[...]):
        print(event)
```

## Agent Run Lifecycle

### Run States

| State | Description |
|-------|-------------|
| `created` | Run initiated, processing not started |
| `in-progress` | Agent actively processing |
| `awaiting` | Paused, waiting for client input |
| `completed` | Successfully finished |
| `cancelling` | Cancellation in progress |
| `cancelled` | Run terminated |
| `failed` | Error occurred |

### State Machine

```
created → in-progress → completed
                     → failed
                     → cancelling → cancelled
                     → awaiting → in-progress (resume)
                                → failed (timeout)
                                → cancelling → cancelled
```

### Await Mechanism

Agents can pause execution to request additional input:

```python
@server.agent()
async def interactive_agent(input: list[Message], context: Context):
    # Process initial input
    yield {"thought": "Need clarification"}

    # Pause and wait for client
    response = yield AwaitInput(prompt="Please provide more details")

    # Continue with additional input
    yield process_response(response)
```

## Stateful Agents with Sessions

### Client-Side Sessions

```python
async with Client(base_url="http://localhost:8000") as client:
    async with client.session() as session:
        # First interaction
        run1 = await session.run_sync(
            agent="chat",
            input=[Message(parts=[MessagePart(content="Hello")])]
        )

        # Second interaction - same session, agent remembers context
        run2 = await session.run_sync(
            agent="chat",
            input=[Message(parts=[MessagePart(content="What did I just say?")])]
        )
```

### Server-Side Session Access

```python
@server.agent()
async def stateful_agent(input: list[Message], context: Context):
    # Load conversation history
    history = [message async for message in context.session.load_history()]

    # Load persisted state
    state = await context.session.load_state()

    # Process with context
    response = process_with_history(input, history, state)

    # Update state
    context.session.state = await context.session.store_state(new_state)

    yield response
```

## Agent Discovery Methods

### 1. Basic Discovery (Online)

Query running ACP servers directly:
```bash
curl http://localhost:8000/agents
```

```python
async for agent in client.agents():
    print(agent)
```

### 2. Open Discovery (Well-Known URL)

Agents publish metadata at standardized URLs:
```
https://your-domain.com/.well-known/agent.yml
```

### 3. Registry-Based Discovery

Centralized registry for discovering agents across multiple servers.

### 4. Embedded Discovery (Offline)

Metadata embedded in distribution packages (container image labels) for disconnected environments.

## Generating Artifacts

Artifacts are named message parts representing files, images, or structured outputs.

### Image Artifact

```python
import base64
from io import BytesIO
from PIL import Image
from acp_sdk.models import Artifact

@server.agent()
async def image_generator(input: list[Message], context: Context):
    # Create image
    img = Image.new('RGB', (100, 100), color='red')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    yield Artifact(
        name="generated.png",
        content=base64.b64encode(buffer.read()).decode("utf-8"),
        content_encoding="base64",
        content_type="image/png"
    )
```

### JSON Artifact

```python
import json
from acp_sdk.models import Artifact

@server.agent()
async def data_agent(input: list[Message], context: Context):
    data = {"results": [1, 2, 3], "status": "complete"}

    yield Artifact(
        name="results.json",
        content=json.dumps(data, indent=2),
        content_type="application/json"
    )
```

## Message Metadata

### Citation Metadata

For source attribution in RAG agents:

```python
MessagePart(
    content="AI adoption increased by 40%",
    content_type="text/plain",
    metadata={
        "kind": "citation",
        "url": "https://example.com/study",
        "title": "AI Adoption Study 2024",
        "start_index": 0,
        "end_index": 32
    }
)
```

### Trajectory Metadata

For transparency and debugging:

```python
MessagePart(
    content="The weather in SF is 72°F",
    content_type="text/plain",
    metadata={
        "kind": "trajectory",
        "tool_name": "weather_api",
        "tool_input": {"location": "San Francisco, CA"},
        "tool_output": {"temperature": 72, "condition": "sunny"}
    }
)
```

## Wrapping Existing Agents

Integrate any existing agent into ACP regardless of framework:

```python
from acp_sdk.server import Server, Context
from acp_sdk.models import Message

server = Server()

@server.agent()
async def wrapped_agent(input: list[Message], context: Context):
    """Wraps an existing LangChain/CrewAI/custom agent"""

    # Extract text from ACP message
    user_input = input[0].parts[0].content

    # Call your existing agent
    result = await your_existing_agent.run(user_input)

    # Yield as ACP message
    yield Message(parts=[MessagePart(
        content=result,
        content_type="text/plain"
    )])

server.run()
```

## Architecture Patterns

### Single-Agent

```
Client → HTTP → ACP Server → Agent
```

### Multi-Agent Single Server

```
Client → HTTP → ACP Server → Agent A
                          → Agent B
                          → Agent C
```

### Distributed Multi-Server

```
Client → Agent Registry → Server 1 → Agent A
                       → Server 2 → Agent B
                       → Server 3 → Agent C
```

### Router Agent Pattern

```
Client → Router Agent → Decompose task
                     → Route to specialists
                     → Aggregate responses
```

## Example Agents

The ACP repository includes 13 reference implementations:

| Example | Framework | Description |
|---------|-----------|-------------|
| Basic Server/Client | ACP SDK | Standalone implementations |
| Chat Agent | BeeAI | ReAct with tools, memory, structured output |
| Slack Agent | BeeAI + MCP | Slack integration via ACP |
| RAG Agent | LlamaIndex | Document retrieval and synthesis |
| Prompt Chaining | BeeAI | Marketing copy → Translation pipeline |
| Dynamic Routing | BeeAI | Language-specific translation routing |
| Handoff Pattern | BeeAI | Delegation to specialized agents |
| Canvas Agent | BeeAI | Artifact generation for files |
| Song Writer | CrewAI | Multi-agent collaboration |
| GPT Researcher | Custom | Real-time research progress |
| Greeting Agent | LangGraph | Context-aware greetings |
| Agent Generator | ACP | Dynamically creates other agents |
| Story Writer | OpenAI | Short story generation |

## Best Practices

### Agent Design

1. **Clear descriptions** - Agent docstrings become manifest descriptions
2. **Explicit content types** - Declare input/output MIME types
3. **Async generators** - Use `yield` for streaming intermediate results
4. **Error handling** - Return meaningful error messages

### Message Handling

1. **Validate content types** - Check incoming MIME types
2. **Use artifacts for files** - Named parts for downloadable content
3. **Include metadata** - Citations and trajectories for transparency

### Session Management

1. **Use sessions for context** - Maintain conversation history
2. **Store minimal state** - Keep session state lightweight
3. **Handle timeouts** - Implement graceful timeout handling

### Discovery

1. **Publish manifests** - Use well-known URLs for open discovery
2. **Rich metadata** - Include capabilities, domains, tags
3. **Version agents** - Track changes with semantic versioning

## Resources

- **Specification**: https://agentcommunicationprotocol.dev
- **GitHub**: https://github.com/i-am-bee/acp
- **Python SDK**: https://github.com/i-am-bee/acp/tree/main/python
- **OpenAPI Spec**: https://github.com/i-am-bee/acp/blob/main/docs/spec/openapi.yaml
- **BeeAI Platform**: Reference implementation

## Governance

ACP is an open standard under the **Linux Foundation**, developed alongside BeeAI as its reference implementation. Community-driven development ensures vendor-neutral evolution.

## Comparison with MCP

| Feature | ACP | MCP |
|---------|-----|-----|
| Focus | Agent-to-agent interop | Tool/resource integration |
| Transport | HTTP REST | JSON-RPC, stdio, SSE |
| Discovery | Built-in (manifest, registry) | External |
| Sessions | Native support | Not built-in |
| Multi-modal | Native (MIME types) | Limited |
| Governance | Linux Foundation | Anthropic |

ACP and MCP are **complementary** - ACP handles agent communication while MCP provides tool integration. ACP includes MCP extension support for exposing agent tools.

## AI Agent Fundamentals

Understanding AI agents helps design effective ACP-based systems.

### What is an AI Agent?

An AI agent is a system that **autonomously performs tasks** by designing workflows with available tools. Unlike simple chatbots, agents handle decision-making, problem-solving, and environmental interaction through three stages:

1. **Goal Initialization & Planning** - Decompose complex goals into subtasks
2. **Reasoning with Tools** - Leverage databases, APIs, other agents to bridge knowledge gaps
3. **Learning & Reflection** - Refine responses through feedback and store solutions

### Agent Types (Complexity Spectrum)

| Type | Characteristics | ACP Use Case |
|------|-----------------|--------------|
| **Simple Reflex** | Rule-based responses; no memory | Basic request handlers |
| **Model-Based Reflex** | Maintains internal world model | Context-aware agents |
| **Goal-Based** | Searches for action sequences | Task orchestrators |
| **Utility-Based** | Maximizes reward across paths | Optimization agents |
| **Learning** | Autonomous knowledge expansion | Adaptive systems |

### Agentic vs Non-Agentic Systems

| Aspect | Non-Agentic (Chatbot) | Agentic (ACP Agent) |
|--------|----------------------|---------------------|
| Tools | None | Full tool access |
| Memory | Session only | Persistent state |
| Reasoning | Single response | Multi-step planning |
| Autonomy | Requires user input | Self-directed |
| Adaptation | Static | Learns from feedback |

## Reasoning Paradigms

### ReAct Pattern (Think-Act-Observe)

Step-by-step problem resolution with continuous context updates:

```python
@server.agent()
async def react_agent(input: list[Message], context: Context):
    """ReAct agent with think-act-observe loop"""

    # Think: Analyze the request
    yield {"thought": "Analyzing user request for data analysis"}

    # Act: Call tool
    data = await fetch_data_tool(input[0].parts[0].content)
    yield {"thought": f"Retrieved {len(data)} records"}

    # Observe: Process results
    analysis = analyze(data)
    yield {"thought": "Analysis complete, formatting response"}

    # Final output
    yield Message(parts=[MessagePart(
        content=json.dumps(analysis),
        content_type="application/json"
    )])
```

### ReWOO Pattern (Upfront Planning)

Plan all steps before execution, reducing token usage:

```python
@server.agent()
async def rewoo_agent(input: list[Message], context: Context):
    """ReWOO agent with upfront planning"""

    # Plan phase: Generate complete execution plan
    plan = [
        {"step": 1, "action": "fetch_data", "params": {...}},
        {"step": 2, "action": "transform", "params": {...}},
        {"step": 3, "action": "summarize", "params": {...}}
    ]
    yield {"plan": plan}

    # Execute phase: Run all steps
    results = []
    for step in plan:
        result = await execute_step(step)
        results.append(result)

    yield Message(parts=[MessagePart(
        content=json.dumps(results[-1]),
        content_type="application/json"
    )])
```

## Multi-Agent Orchestration

### Hierarchical Agent Architecture

```
                    ┌─────────────────┐
                    │  Orchestrator   │
                    │  (Goal-Based)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Research Agent │ │  Analysis Agent │ │  Writer Agent   │
│  (Learning)     │ │  (Utility)      │ │  (Model-Based)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Orchestrator Agent Example

```python
@server.agent(
    name="orchestrator",
    description="Coordinates specialized agents for complex tasks"
)
async def orchestrator(input: list[Message], context: Context):
    """Multi-agent orchestrator using ACP"""

    # Decompose task
    task = input[0].parts[0].content
    subtasks = await decompose_task(task)

    yield {"thought": f"Decomposed into {len(subtasks)} subtasks"}

    # Route to specialist agents
    async with Client(base_url="http://localhost:8000") as client:
        results = []
        for subtask in subtasks:
            agent = select_specialist(subtask)
            run = await client.run_sync(
                agent=agent,
                input=[Message(parts=[MessagePart(
                    content=subtask["description"],
                    content_type="text/plain"
                )])]
            )
            results.append(run.output)
            yield {"thought": f"Completed: {subtask['name']}"}

    # Aggregate responses
    final = synthesize_results(results)
    yield Message(parts=[MessagePart(
        content=final,
        content_type="text/plain"
    )])
```

### Agent-to-Agent Communication

```python
@server.agent()
async def delegating_agent(input: list[Message], context: Context):
    """Agent that delegates to other ACP agents"""

    async with Client(base_url="http://localhost:8000") as client:
        # Discover available agents
        specialists = []
        async for agent in client.agents():
            if "analysis" in agent.description.lower():
                specialists.append(agent.name)

        yield {"thought": f"Found {len(specialists)} analysis agents"}

        # Delegate to best match
        if specialists:
            run = await client.run_sync(
                agent=specialists[0],
                input=input
            )
            yield run.output[0]
        else:
            yield Message(parts=[MessagePart(
                content="No suitable agent found",
                content_type="text/plain"
            )])
```

## Production Safety Patterns

### Activity Logging

```python
import logging
from datetime import datetime

logger = logging.getLogger("acp_audit")

@server.agent()
async def audited_agent(input: list[Message], context: Context):
    """Agent with comprehensive activity logging"""

    run_id = context.run_id
    start_time = datetime.utcnow()

    # Log start
    logger.info(f"[{run_id}] Agent started", extra={
        "run_id": run_id,
        "input_size": len(input),
        "timestamp": start_time.isoformat()
    })

    try:
        # Process
        result = await process(input)

        # Log tool usage
        logger.info(f"[{run_id}] Tool called", extra={
            "run_id": run_id,
            "tool": "process",
            "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
        })

        yield result

    except Exception as e:
        logger.error(f"[{run_id}] Agent failed: {e}", extra={
            "run_id": run_id,
            "error": str(e)
        })
        raise

    finally:
        logger.info(f"[{run_id}] Agent completed", extra={
            "run_id": run_id,
            "duration_ms": (datetime.utcnow() - start_time).total_seconds() * 1000
        })
```

### Interruptibility (Graceful Cancellation)

```python
import asyncio

@server.agent()
async def interruptible_agent(input: list[Message], context: Context):
    """Agent that supports graceful interruption"""

    for i, step in enumerate(processing_steps):
        # Check for cancellation between steps
        if context.is_cancelled:
            yield {"thought": "Cancellation requested, stopping gracefully"}
            # Cleanup resources
            await cleanup()
            return

        yield {"thought": f"Processing step {i+1}/{len(processing_steps)}"}

        # Use asyncio.shield for critical operations
        result = await asyncio.shield(step.execute())

        yield {"progress": (i + 1) / len(processing_steps)}

    yield final_result
```

### Human Approval Gates

```python
@server.agent()
async def approval_agent(input: list[Message], context: Context):
    """Agent requiring human approval for high-impact actions"""

    action = parse_action(input)

    # Check if action requires approval
    if action.requires_approval:
        yield {"thought": "This action requires human approval"}

        # Pause and wait for approval
        approval = yield AwaitInput(
            prompt=f"Approve action: {action.description}? (yes/no)",
            metadata={"action_type": action.type, "impact": "high"}
        )

        if approval.lower() != "yes":
            yield Message(parts=[MessagePart(
                content="Action cancelled by user",
                content_type="text/plain"
            )])
            return

    # Execute approved action
    result = await action.execute()
    yield result
```

### Preventing Infinite Loops

```python
MAX_ITERATIONS = 10
MAX_TOOL_CALLS = 50

@server.agent()
async def bounded_agent(input: list[Message], context: Context):
    """Agent with loop prevention"""

    iterations = 0
    tool_calls = 0
    seen_states = set()

    while not is_complete():
        iterations += 1

        # Iteration limit
        if iterations > MAX_ITERATIONS:
            yield {"warning": "Max iterations reached"}
            break

        # State cycle detection
        current_state = hash(frozenset(context.state.items()))
        if current_state in seen_states:
            yield {"warning": "Cycle detected, breaking loop"}
            break
        seen_states.add(current_state)

        # Tool call limit
        if tool_calls >= MAX_TOOL_CALLS:
            yield {"warning": "Max tool calls reached"}
            break

        result = await process_step()
        tool_calls += result.tool_call_count

        yield {"thought": f"Iteration {iterations}, tools: {tool_calls}"}

    yield final_result()
```

## Enterprise Use Cases

### Cross-Platform Integration

Connect agents across different business systems:

```python
@server.agent(
    name="crm-integration",
    description="Integrates CRM, analytics, and support systems",
    metadata={
        "domains": ["sales", "support", "analytics"],
        "capabilities": [
            {"name": "customer-lookup", "description": "Find customer data"},
            {"name": "ticket-creation", "description": "Create support tickets"},
            {"name": "report-generation", "description": "Generate analytics reports"}
        ]
    }
)
async def crm_agent(input: list[Message], context: Context):
    """Enterprise CRM integration agent"""
    # Implementation
    pass
```

### Agent Replacement Pattern

Swap agents seamlessly in production:

```python
# Old agent (being replaced)
@server.agent(name="search-v1", description="Legacy search")
async def search_v1(input, context):
    return legacy_search(input)

# New agent (replacement) - same interface
@server.agent(name="search-v2", description="AI-powered search")
async def search_v2(input, context):
    return ai_search(input)

# Client code unchanged - just update agent name
run = await client.run_sync(agent="search-v2", input=input)
```

### Inter-Organizational Collaboration

Secure agent partnerships between companies:

```python
@server.agent(
    name="partner-gateway",
    description="Secure gateway for partner agent access",
    metadata={
        "security": {
            "auth": "oauth2",
            "allowed_origins": ["partner-a.com", "partner-b.com"],
            "rate_limit": "100/hour"
        }
    }
)
async def partner_agent(input: list[Message], context: Context):
    """Agent for inter-organizational communication"""

    # Verify partner identity
    partner_id = context.metadata.get("partner_id")
    if not validate_partner(partner_id):
        yield Message(parts=[MessagePart(
            content="Unauthorized",
            content_type="text/plain"
        )])
        return

    # Process partner request with audit
    yield {"audit": f"Partner {partner_id} request received"}
    result = await process_partner_request(input)
    yield result
```

## Protocol Ecosystem

ACP works alongside other agent communication standards:

| Protocol | Purpose | Relationship to ACP |
|----------|---------|---------------------|
| **ACP** | Agent-to-agent interop | Core protocol |
| **MCP** | Agent-to-tool integration | Complementary (ACP supports MCP extension) |
| **A2A** | Direct agent messaging | Alternative for peer-to-peer |
| **Agent Client Protocol** | Editor-to-agent | Different domain (IDE integration) |

### Using ACP with MCP Tools

```python
from acp_sdk.extensions import MCPExtension

@server.agent(extensions=[MCPExtension()])
async def mcp_enabled_agent(input: list[Message], context: Context):
    """Agent that exposes MCP tools via ACP"""

    # Access MCP tools through ACP context
    tools = context.mcp.available_tools()

    # Call MCP tool
    result = await context.mcp.call_tool("web_search", query="...")

    yield result
```
