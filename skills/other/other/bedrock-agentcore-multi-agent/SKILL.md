---
name: bedrock-agentcore-multi-agent
description: Amazon Bedrock AgentCore multi-agent orchestration with Agent-to-Agent (A2A) protocol. Supervisor-worker patterns, agent collaboration, and hierarchical delegation. Use when building multi-agent systems, orchestrating specialized agents, or implementing complex workflows.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Amazon Bedrock AgentCore Multi-Agent

## Overview

Build sophisticated multi-agent systems using AgentCore's Agent-to-Agent (A2A) protocol. Implement supervisor-worker patterns where a routing agent delegates to specialized domain experts, maintaining context across the agent hierarchy.

**Purpose**: Orchestrate multiple AI agents for complex, multi-domain tasks

**Pattern**: Workflow-based (3 orchestration patterns)

**Key Principles** (validated by AWS December 2025):
1. **Supervisor-Worker Architecture** - Routing agent delegates to specialists
2. **A2A Protocol** - Standard communication between agents
3. **Context Preservation** - Conversation history shared across agents
4. **Failure Isolation** - Single agent failure doesn't crash system
5. **Modular Design** - Each agent focused on specific domain
6. **Framework Interoperability** - Works across different agent frameworks

**Quality Targets**:
- Routing accuracy: ≥ 95%
- Context preservation: 100%
- Failure isolation: Complete
- Latency overhead: < 200ms per hop

---

## When to Use

Use bedrock-agentcore-multi-agent when:

- Task requires multiple specialized domains
- Single agent becomes too complex
- Need different models for different tasks
- Want fault-isolated agent architecture
- Building enterprise customer service
- Implementing complex workflows

**When NOT to Use**:
- Simple single-domain tasks
- Cost-sensitive applications (multi-hop adds cost)
- Low-latency requirements (< 1s total)

---

## Prerequisites

### Required
- Multiple AgentCore agents deployed
- Supervisor agent with routing capability
- A2A protocol enabled
- IAM permissions for cross-agent calls

### Recommended
- Clear domain boundaries defined
- Handoff prompts tested
- Fallback strategies documented

---

## Architecture Patterns

### Pattern 1: Hub-and-Spoke (Supervisor)

```
                    ┌─────────────────┐
                    │   User Query    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Supervisor    │
                    │    (Router)     │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │   Orders    │   │   Returns   │   │   Support   │
    │   Agent     │   │   Agent     │   │   Agent     │
    └─────────────┘   └─────────────┘   └─────────────┘
```

### Pattern 2: Sequential Pipeline

```
    ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
    │ Intake  │ ──▶ │ Analyze │ ──▶ │ Resolve │ ──▶ │  Close  │
    │ Agent   │     │ Agent   │     │ Agent   │     │ Agent   │
    └─────────┘     └─────────┘     └─────────┘     └─────────┘
```

### Pattern 3: Hierarchical

```
                    ┌─────────────────┐
                    │   Executive     │
                    │   Supervisor    │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
    │   Sales     │   │   Support   │   │   Billing   │
    │ Supervisor  │   │ Supervisor  │   │ Supervisor  │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                 │                 │
     ┌─────┴─────┐     ┌─────┴─────┐     ┌─────┴─────┐
     │           │     │           │     │           │
     ▼           ▼     ▼           ▼     ▼           ▼
   ┌───┐       ┌───┐ ┌───┐       ┌───┐ ┌───┐       ┌───┐
   │B2B│       │B2C│ │L1 │       │L2 │ │Pay│       │Inv│
   └───┘       └───┘ └───┘       └───┘ └───┘       └───┘
```

---

## Operations

### Operation 1: Create Supervisor Agent

**Time**: 15-30 minutes
**Automation**: 80%
**Purpose**: Build the routing/orchestration agent

**Supervisor Agent Code**:
```python
# supervisor_agent.py
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
import boto3
import json

app = BedrockAgentCoreApp()
client = boto3.client('bedrock-agentcore')

# Define collaborator agents
COLLABORATORS = {
    'orders': {
        'arn': 'arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/orders-agent',
        'description': 'Handles order status, tracking, and modifications',
        'triggers': ['order', 'tracking', 'delivery', 'shipment', 'status']
    },
    'returns': {
        'arn': 'arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/returns-agent',
        'description': 'Processes returns, refunds, and exchanges',
        'triggers': ['return', 'refund', 'exchange', 'damaged', 'wrong item']
    },
    'support': {
        'arn': 'arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/support-agent',
        'description': 'Technical support and product questions',
        'triggers': ['help', 'problem', 'issue', 'how to', 'broken', 'not working']
    },
    'billing': {
        'arn': 'arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/billing-agent',
        'description': 'Payment issues, invoices, and account billing',
        'triggers': ['payment', 'charge', 'invoice', 'bill', 'subscription']
    }
}

# Routing agent
router = Agent(
    model="anthropic.claude-sonnet-4-20250514-v1:0",
    system_prompt=f"""You are a customer service supervisor. Your job is to:
1. Understand the customer's intent
2. Route to the appropriate specialist
3. Handle escalations and complex multi-domain issues

Available specialists:
{json.dumps({k: v['description'] for k, v in COLLABORATORS.items()}, indent=2)}

Respond with JSON:
{{"route": "orders|returns|support|billing|self", "reason": "...", "context": "..."}}

Use "self" only for greetings or if truly unclear.
"""
)

@app.entrypoint
def invoke(payload):
    user_message = payload.get('prompt', '')
    session_id = payload.get('session_id', 'default')
    conversation_history = payload.get('history', [])

    # Step 1: Route the request
    routing_prompt = f"""
Customer message: {user_message}

Previous context: {json.dumps(conversation_history[-3:]) if conversation_history else 'None'}

Determine the appropriate specialist and respond with routing JSON.
"""

    routing_response = router(routing_prompt)

    try:
        routing = json.loads(routing_response.message)
    except json.JSONDecodeError:
        # Fallback to keyword matching
        routing = keyword_route(user_message)

    route = routing.get('route', 'self')

    # Step 2: Handle routing
    if route == 'self':
        # Handle directly
        return {
            'response': "Hello! I'm here to help. What can I assist you with today?",
            'routed_to': None
        }

    # Step 3: Delegate to specialist
    collaborator = COLLABORATORS.get(route)
    if not collaborator:
        return {'response': "I apologize, let me connect you with support.", 'routed_to': 'support'}

    # Invoke collaborator with context
    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=collaborator['arn'],
            runtimeSessionId=f"{session_id}-{route}",
            payload={
                'prompt': user_message,
                'context': routing.get('context', ''),
                'supervisor_notes': routing.get('reason', ''),
                'history': conversation_history
            }
        )

        return {
            'response': response['payload'].get('response', ''),
            'routed_to': route,
            'routing_reason': routing.get('reason', '')
        }

    except Exception as e:
        # Fallback: handle ourselves or escalate
        app.logger.error(f"Collaborator failed: {e}")
        return {
            'response': "I apologize for the inconvenience. Let me help you directly.",
            'routed_to': None,
            'error': str(e)
        }

def keyword_route(message):
    """Fallback keyword-based routing"""
    message_lower = message.lower()

    for route, config in COLLABORATORS.items():
        if any(trigger in message_lower for trigger in config['triggers']):
            return {'route': route, 'reason': 'keyword_match'}

    return {'route': 'self', 'reason': 'no_match'}

if __name__ == "__main__":
    app.run()
```

---

### Operation 2: Create Specialist Agents

**Time**: 10-20 minutes per agent
**Automation**: 85%
**Purpose**: Build domain-specific worker agents

**Orders Agent**:
```python
# orders_agent.py
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()

# Orders specialist
agent = Agent(
    model="anthropic.claude-sonnet-4-20250514-v1:0",
    system_prompt="""You are an orders specialist. You handle:
- Order status inquiries
- Delivery tracking
- Order modifications
- Shipping questions

You have access to these tools:
- get_order_status(order_id) - Get order details
- track_shipment(tracking_number) - Track delivery
- modify_order(order_id, changes) - Update order

Be helpful, accurate, and efficient. If a request is outside your domain
(returns, billing, technical support), indicate that clearly.
"""
)

@app.entrypoint
def invoke(payload):
    user_message = payload.get('prompt', '')
    context = payload.get('context', '')
    supervisor_notes = payload.get('supervisor_notes', '')
    history = payload.get('history', [])

    # Build context-aware prompt
    prompt = user_message
    if context:
        prompt = f"Context from supervisor: {context}\n\nCustomer request: {user_message}"

    result = agent(prompt)

    # Check if we need to hand back to supervisor
    needs_handoff = check_domain_boundary(result.message)

    return {
        'response': result.message,
        'needs_handoff': needs_handoff,
        'handoff_reason': needs_handoff if needs_handoff else None
    }

def check_domain_boundary(response):
    """Check if response indicates need for different specialist"""
    handoff_indicators = [
        ('return', 'returns'),
        ('refund', 'returns'),
        ('billing', 'billing'),
        ('payment', 'billing'),
        ('technical', 'support')
    ]

    response_lower = response.lower()
    for indicator, domain in handoff_indicators:
        if f"need to contact {indicator}" in response_lower or \
           f"transfer to {indicator}" in response_lower:
            return domain

    return None

if __name__ == "__main__":
    app.run()
```

**Returns Agent**:
```python
# returns_agent.py
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()

agent = Agent(
    model="anthropic.claude-3-haiku-20240307-v1:0",  # Faster model for simple tasks
    system_prompt="""You are a returns specialist. You handle:
- Return requests
- Refund processing
- Exchanges
- Damaged item claims

Tools available:
- initiate_return(order_id, reason) - Start return process
- check_return_eligibility(order_id) - Verify return policy
- process_refund(order_id) - Issue refund
- create_exchange(order_id, new_item) - Process exchange

Be empathetic and solution-oriented. Follow return policy strictly.
"""
)

@app.entrypoint
def invoke(payload):
    result = agent(payload.get('prompt', ''))
    return {'response': result.message}

if __name__ == "__main__":
    app.run()
```

---

### Operation 3: Configure A2A Protocol

**Time**: 10-15 minutes
**Automation**: 90%
**Purpose**: Enable secure agent-to-agent communication

**Enable A2A for Agents**:
```python
import boto3

control = boto3.client('bedrock-agentcore-control')

# Configure supervisor to call collaborators
response = control.update_agent_runtime(
    agentRuntimeId='supervisor-agent',
    collaborationConfig={
        'enabled': True,
        'collaborators': [
            {
                'agentRuntimeArn': 'arn:...:agent-runtime/orders-agent',
                'alias': 'orders',
                'description': 'Order management specialist'
            },
            {
                'agentRuntimeArn': 'arn:...:agent-runtime/returns-agent',
                'alias': 'returns',
                'description': 'Returns and refunds specialist'
            },
            {
                'agentRuntimeArn': 'arn:...:agent-runtime/support-agent',
                'alias': 'support',
                'description': 'Technical support specialist'
            },
            {
                'agentRuntimeArn': 'arn:...:agent-runtime/billing-agent',
                'alias': 'billing',
                'description': 'Billing and payments specialist'
            }
        ],
        'routingMode': 'SUPERVISOR_WITH_ROUTING',
        'contextSharing': {
            'shareConversationHistory': True,
            'maxHistoryTurns': 10
        }
    }
)
```

**IAM Policy for A2A**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": [
        "arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/orders-agent",
        "arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/returns-agent",
        "arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/support-agent",
        "arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/billing-agent"
      ],
      "Condition": {
        "StringEquals": {
          "bedrock-agentcore:CallerAgentRuntimeArn": "arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/supervisor-agent"
        }
      }
    }
  ]
}
```

---

### Operation 4: Implement Handoff Patterns

**Time**: 15-30 minutes
**Automation**: 70%
**Purpose**: Handle smooth transitions between agents

**Context-Preserving Handoff**:
```python
class AgentHandoff:
    """Manages handoffs between agents"""

    def __init__(self, client, supervisor_arn):
        self.client = client
        self.supervisor_arn = supervisor_arn
        self.context_store = {}

    def initiate_handoff(self, from_agent, to_agent, session_id, context):
        """Hand off from one agent to another"""

        # Store context for receiving agent
        handoff_context = {
            'from_agent': from_agent,
            'reason': context.get('reason', ''),
            'summary': context.get('summary', ''),
            'customer_sentiment': context.get('sentiment', 'neutral'),
            'conversation_history': context.get('history', []),
            'pending_actions': context.get('pending_actions', [])
        }

        self.context_store[session_id] = handoff_context

        # Notify receiving agent
        response = self.client.invoke_agent_runtime(
            agentRuntimeArn=to_agent,
            runtimeSessionId=session_id,
            payload={
                'type': 'HANDOFF_RECEIVE',
                'context': handoff_context,
                'prompt': f"Customer transferred from {from_agent}. Context: {handoff_context['summary']}"
            }
        )

        return response

    def escalate_to_supervisor(self, agent_arn, session_id, reason):
        """Escalate back to supervisor"""

        return self.client.invoke_agent_runtime(
            agentRuntimeArn=self.supervisor_arn,
            runtimeSessionId=session_id,
            payload={
                'type': 'ESCALATION',
                'from_agent': agent_arn,
                'reason': reason,
                'needs_human': reason.get('needs_human', False)
            }
        )
```

**Multi-Turn Handoff Example**:
```python
# Conversation flow with handoffs

# Turn 1: User -> Supervisor
# "I want to return an order and also change my payment method"

# Supervisor detects multi-domain request
# Routes to returns first (primary intent)

# Turn 2: Returns Agent handles return
# Initiates return process

# Turn 3: Returns Agent hands off to Billing
# With context: "Return initiated for order #123, customer also needs payment update"

# Turn 4: Billing Agent receives handoff
# "I see you've started a return. Let me help you update your payment method."
# Handles payment update

# Turn 5: Billing -> Supervisor
# "Both requests handled. Return initiated, payment updated."
```

---

### Operation 5: Multi-Agent Monitoring

**Time**: 15-20 minutes
**Automation**: 85%
**Purpose**: Monitor the multi-agent system

**Trace Multi-Agent Calls**:
```python
import boto3
import json

cloudwatch = boto3.client('cloudwatch')
logs = boto3.client('logs')

# CloudWatch Metrics for Multi-Agent
cloudwatch.put_metric_data(
    Namespace='AgentCore/MultiAgent',
    MetricData=[
        {
            'MetricName': 'RoutingDecisions',
            'Dimensions': [
                {'Name': 'SupervisorAgent', 'Value': 'customer-service-supervisor'},
                {'Name': 'TargetAgent', 'Value': 'orders-agent'}
            ],
            'Value': 1,
            'Unit': 'Count'
        },
        {
            'MetricName': 'HandoffLatency',
            'Dimensions': [
                {'Name': 'FromAgent', 'Value': 'returns-agent'},
                {'Name': 'ToAgent', 'Value': 'billing-agent'}
            ],
            'Value': 150,  # milliseconds
            'Unit': 'Milliseconds'
        }
    ]
)

# Log Insights Query for Multi-Agent Traces
query = '''
fields @timestamp, @message
| filter @message like /agent-runtime/
| parse @message '"agentRuntimeArn":"*"' as agent
| parse @message '"runtimeSessionId":"*"' as session
| stats count() by agent, session
| sort count desc
'''
```

**Dashboard for Multi-Agent System**:
```python
dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "title": "Routing Distribution",
                "metrics": [
                    ["AgentCore/MultiAgent", "RoutingDecisions", "TargetAgent", "orders-agent"],
                    [".", ".", ".", "returns-agent"],
                    [".", ".", ".", "support-agent"],
                    [".", ".", ".", "billing-agent"]
                ],
                "period": 3600,
                "stat": "Sum",
                "view": "pie"
            }
        },
        {
            "type": "metric",
            "properties": {
                "title": "Handoff Latency",
                "metrics": [
                    ["AgentCore/MultiAgent", "HandoffLatency"]
                ],
                "period": 300,
                "stat": "p99"
            }
        },
        {
            "type": "metric",
            "properties": {
                "title": "Escalation Rate",
                "metrics": [
                    ["AgentCore/MultiAgent", "Escalations", "Reason", "out_of_scope"],
                    [".", ".", ".", "customer_request"],
                    [".", ".", ".", "agent_failure"]
                ],
                "period": 3600,
                "stat": "Sum"
            }
        }
    ]
}

cloudwatch.put_dashboard(
    DashboardName='MultiAgentOrchestration',
    DashboardBody=json.dumps(dashboard_body)
)
```

---

## Best Practices

### 1. Clear Domain Boundaries
```python
# Good: Clear separation
DOMAINS = {
    'orders': ['status', 'tracking', 'modify', 'cancel'],
    'returns': ['return', 'refund', 'exchange', 'damaged'],
    'billing': ['payment', 'invoice', 'subscription']
}

# Bad: Overlapping domains
# 'orders': ['status', 'refund']  # Refund overlaps with returns
```

### 2. Graceful Degradation
```python
async def invoke_with_fallback(primary_agent, fallback_agent, payload):
    """Try primary, fall back to backup"""
    try:
        return await invoke_agent(primary_agent, payload)
    except Exception:
        return await invoke_agent(fallback_agent, payload)
```

### 3. Context Compression
```python
def compress_history(history, max_turns=10):
    """Keep relevant context, compress old turns"""
    if len(history) <= max_turns:
        return history

    # Keep first turn (initial context) and recent turns
    return [history[0]] + history[-(max_turns-1):]
```

---

## Related Skills

- **bedrock-agentcore**: Core platform features
- **bedrock-agentcore-deployment**: Deploy multi-agent systems
- **bedrock-agentcore-evaluations**: Test multi-agent workflows
- **end-to-end-orchestrator**: Workflow orchestration patterns

---

## References

- `references/routing-strategies.md` - Advanced routing patterns
- `references/context-management.md` - Cross-agent context handling
- `references/failure-handling.md` - Error recovery patterns

---

## Sources

- [Agent-to-Agent Protocol](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [Multi-Agent Collaboration](https://aws.amazon.com/blogs/machine-learning/build-an-intelligent-multi-agent-business-expert-using-amazon-bedrock/)
- [Best Practices Part 2](https://aws.amazon.com/blogs/machine-learning/best-practices-for-building-robust-generative-ai-applications-with-amazon-bedrock-agents-part-2/)
