---
name: openai-agents
description: >-
  You are an expert in the OpenAI Agents SDK (formerly Swarm), the official
  framework for building multi-agent systems. You help developers create
  agents with tool calling, guardrails, agent handoffs, streaming, tracing,
  and MCP integration — building production-grade AI agents that coordinate,
  delegate tasks, and execute tools with built-in safety controls.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: AI & Machine Learning
  tags:
    - openai
    - agents
    - tools
    - guardrails
    - handoff
    - multi-agent
    - python
---

# OpenAI Agents SDK — Build Production AI Agents

You are an expert in the OpenAI Agents SDK (formerly Swarm), the official framework for building multi-agent systems. You help developers create agents with tool calling, guardrails, agent handoffs, streaming, tracing, and MCP integration — building production-grade AI agents that coordinate, delegate tasks, and execute tools with built-in safety controls.

## Core Capabilities

### Agent Definition

```python
# agents/customer_support.py — Multi-agent customer support system
from agents import Agent, Runner, function_tool, GuardrailFunctionOutput, InputGuardrail
from pydantic import BaseModel

class OrderInfo(BaseModel):
    order_id: str
    status: str
    total: float
    items: list[str]

@function_tool
async def lookup_order(order_id: str) -> OrderInfo:
    """Look up an order by ID.

    Args:
        order_id: The order identifier (e.g., ORD-12345)
    """
    order = await db.orders.find_by_id(order_id)
    return OrderInfo(
        order_id=order.id,
        status=order.status,
        total=order.total,
        items=[item.name for item in order.items],
    )

@function_tool
async def initiate_refund(order_id: str, reason: str) -> str:
    """Initiate a refund for an order.

    Args:
        order_id: The order to refund
        reason: Reason for the refund
    """
    result = await payments.refund(order_id, reason)
    return f"Refund initiated: ${result.amount}. Reference: {result.reference_id}"

@function_tool
async def escalate_to_human(summary: str) -> str:
    """Escalate to a human agent when the issue is too complex.

    Args:
        summary: Brief summary of the issue for the human agent
    """
    ticket = await support.create_ticket(summary, priority="high")
    return f"Escalated to human agent. Ticket: {ticket.id}"

# Triage agent — routes to the right specialist
triage_agent = Agent(
    name="Triage",
    instructions="""You are a customer support triage agent.
    Determine the customer's issue and hand off to the appropriate specialist:
    - Order issues → Order Specialist
    - Billing/refund → Billing Specialist
    - Technical problems → escalate to human""",
    handoffs=["order_specialist", "billing_specialist"],
    tools=[escalate_to_human],
)

# Specialist agents
order_specialist = Agent(
    name="Order Specialist",
    instructions="You handle order-related inquiries. Look up orders, provide status updates, and help with modifications.",
    tools=[lookup_order],
    handoffs=["billing_specialist"],       # Can hand off to billing if needed
)

billing_specialist = Agent(
    name="Billing Specialist",
    instructions="You handle billing and refund requests. Verify orders before processing refunds. Maximum refund without approval: $500.",
    tools=[lookup_order, initiate_refund],
)
```

### Guardrails

```python
# Input guardrail — runs before the agent processes the message
class ContentCheck(BaseModel):
    is_appropriate: bool
    reasoning: str

async def content_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    """Check if user input is appropriate before processing."""
    result = await Runner.run(
        Agent(
            name="Content Checker",
            instructions="Check if the input is a legitimate customer support request. Flag inappropriate content.",
            output_type=ContentCheck,
        ),
        input,
        context=ctx,
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_appropriate,
    )

triage_agent = Agent(
    name="Triage",
    instructions="...",
    input_guardrails=[InputGuardrail(guardrail_function=content_guardrail)],
    handoffs=["order_specialist", "billing_specialist"],
)
```

### Running Agents

```python
from agents import Runner

# Single turn
result = await Runner.run(
    triage_agent,
    "I want a refund for order ORD-12345, the product arrived damaged",
)
print(result.final_output)
# Agent flow: Triage → Billing Specialist → lookup_order → initiate_refund

# Streaming
async for event in Runner.run_streamed(triage_agent, user_message):
    if event.type == "raw_response_event":
        if hasattr(event.data, "delta"):
            print(event.data.delta, end="")
    elif event.type == "agent_updated_stream_event":
        print(f"\n[Handed off to: {event.new_agent.name}]")
    elif event.type == "tool_call_event":
        print(f"\n[Calling tool: {event.tool_name}]")

# With MCP servers
from agents.mcp import MCPServerStdio

async with MCPServerStdio(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", "/data"]) as mcp:
    agent = Agent(
        name="File Assistant",
        instructions="Help users manage files",
        mcp_servers=[mcp],
    )
    result = await Runner.run(agent, "List all Python files in /data")
```

## Installation

```bash
pip install openai-agents
```

## Best Practices

1. **Triage + specialists** — Use a triage agent for routing; specialist agents for domain-specific tasks
2. **Guardrails** — Add input/output guardrails for content filtering, PII detection, policy enforcement
3. **Handoffs** — Use handoffs for agent delegation; cheaper than one mega-agent with all tools
4. **Structured output** — Use `output_type` with Pydantic models for typed, validated agent responses
5. **Tool design** — Make tools focused (one action each); clear docstrings help the agent use them correctly
6. **Tracing** — Enable tracing for debugging agent decisions, tool calls, and handoff chains
7. **MCP integration** — Connect MCP servers for file access, database queries, API calls without custom tools
8. **Streaming** — Use `run_streamed` for real-time output; show tool calls and handoffs to users for transparency
