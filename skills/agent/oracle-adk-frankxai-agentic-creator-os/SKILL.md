---
name: Oracle ADK Expert
description: Build production agentic applications on OCI using Oracle Agent Development Kit with multi-agent orchestration, function tools, and enterprise patterns
version: 1.0.0
---

# Oracle ADK Expert Skill

## Purpose
Master Oracle's Agent Development Kit (ADK) for building enterprise-grade agentic applications on OCI Generative AI Agents Service with code-first approach and advanced orchestration patterns.

## Platform Overview

### OCI Agent Development Kit (Released May 22, 2025)
Client-side library that simplifies building agentic applications on top of OCI Generative AI Agents Service.

**Key Value:** Code-first approach for embedding agents in applications (web apps, Slackbots, enterprise systems).

**Requirements:** Python 3.10 or later

## Core Capabilities

### 1. Multi-Turn Conversations
Build agents that maintain context across multiple interactions.

**Pattern:**
```python
from oci_adk import Agent

agent = Agent(
    name="customer_support",
    model="cohere.command-r-plus",
    system_prompt="You are a helpful customer support agent"
)

# Multi-turn conversation
conversation = agent.create_conversation()
response1 = conversation.send("I need help with my order")
response2 = conversation.send("It's order #12345")
# Agent remembers context from previous messages
```

### 2. Multi-Agent Orchestration

**Routing Pattern:**
```python
# Route requests to specialized agents
def orchestrator(user_query):
    if requires_technical_support(user_query):
        return technical_agent.handle(user_query)
    elif requires_billing(user_query):
        return billing_agent.handle(user_query)
    else:
        return general_agent.handle(user_query)
```

**Agent-as-a-Tool Pattern:**
```python
# One agent uses another agent as a tool
main_agent = Agent(
    name="supervisor",
    tools=[research_agent, analysis_agent, report_agent]
)

# Main agent orchestrates specialist agents
result = main_agent.execute("Research and analyze Q4 performance")
```

### 3. Deterministic Workflows
Build predictable, orchestrated workflows with explicit control flow.

```python
from oci_adk import Workflow, Step

workflow = Workflow([
    Step("validate_input", validation_agent),
    Step("process_request", processing_agent),
    Step("generate_response", response_agent)
])

result = workflow.execute(user_input)
```

### 4. Function Tools
Add custom capabilities to agents through function tools.

```python
from oci_adk import FunctionTool

@FunctionTool(
    name="get_customer_data",
    description="Retrieve customer information from CRM",
    parameters={
        "customer_id": {"type": "string", "required": True}
    }
)
def get_customer_data(customer_id: str):
    return crm_api.get_customer(customer_id)

agent = Agent(
    name="customer_agent",
    tools=[get_customer_data]
)
```

## Architectural Patterns

### Pattern 1: Hierarchical Orchestration
```
Supervisor Agent
    ├─→ Research Agent (gathers information)
    ├─→ Analysis Agent (processes data)
    └─→ Report Agent (generates output)
```

**Use Case:** Complex tasks requiring specialized subtask agents

**Implementation:**
```python
supervisor = Agent(
    name="supervisor",
    system_prompt="Coordinate specialist agents to complete complex tasks",
    tools=[research_tool, analysis_tool, report_tool]
)
```

### Pattern 2: Sequential Pipeline
```
Input → Agent 1 → Agent 2 → Agent 3 → Output
```

**Use Case:** Linear workflows with dependencies

**Implementation:**
```python
pipeline = AgentPipeline([
    ("extract", data_extraction_agent),
    ("transform", data_transformation_agent),
    ("load", data_loading_agent)
])

result = pipeline.execute(raw_data)
```

### Pattern 3: Parallel Processing
```
Coordinator
    ├──→ Agent A ──┐
    ├──→ Agent B ──┤→ Aggregator Agent
    └──→ Agent C ──┘
```

**Use Case:** Independent tasks that can run concurrently

**Implementation:**
```python
import asyncio

async def parallel_processing(task):
    results = await asyncio.gather(
        agent_a.execute_async(task),
        agent_b.execute_async(task),
        agent_c.execute_async(task)
    )
    return aggregator_agent.synthesize(results)
```

## Oracle-Specific Best Practices

### 1. Leverage OCI Services
```python
# Integrate with OCI services
from oci import object_storage, database

agent = Agent(
    name="data_agent",
    tools=[
        object_storage_tool,
        autonomous_db_tool,
        analytics_cloud_tool
    ]
)
```

### 2. Enterprise Security
```python
# Use OCI IAM for authentication
from oci.config import from_file

config = from_file("~/.oci/config")

agent = Agent(
    name="secure_agent",
    oci_config=config,
    compartment_id="ocid1.compartment..."
)
```

### 3. Multi-Region Deployment
```python
# Deploy agents across OCI regions
regions = ["us-ashburn-1", "eu-frankfurt-1", "ap-tokyo-1"]

for region in regions:
    deploy_agent(
        agent=my_agent,
        region=region,
        config=regional_config[region]
    )
```

## Production Deployment

### Application Integration
```python
# Embed in FastAPI application
from fastapi import FastAPI
from oci_adk import Agent

app = FastAPI()
support_agent = Agent.load("customer_support_v2")

@app.post("/support/chat")
async def chat_endpoint(message: str, session_id: str):
    conversation = support_agent.get_conversation(session_id)
    response = await conversation.send_async(message)
    return {"reply": response.text}
```

### Slackbot Integration
```python
from slack_sdk import WebClient
from oci_adk import Agent

slack_client = WebClient(token=slack_token)
agent = Agent.load("slack_assistant")

@slack_app.event("message")
def handle_message(event):
    user_message = event["text"]
    response = agent.execute(user_message)
    slack_client.chat_postMessage(
        channel=event["channel"],
        text=response.text
    )
```

## Monitoring & Observability

### Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("oci_agent")

agent = Agent(
    name="monitored_agent",
    on_tool_call=lambda tool: logger.info(f"Calling tool: {tool}"),
    on_error=lambda error: logger.error(f"Agent error: {error}")
)
```

### Metrics Collection
```python
from oci.monitoring import MonitoringClient

def track_agent_metrics(agent_id, metrics):
    monitoring_client.post_metric_data(
        post_metric_data_details={
            "namespace": "agent_performance",
            "dimensions": {"agent_id": agent_id},
            "datapoints": metrics
        }
    )
```

## Cost Optimization

### Model Selection
```python
# Use appropriate models for tasks
simple_agent = Agent(
    model="cohere.command-light",  # Cheaper for simple tasks
)

complex_agent = Agent(
    model="cohere.command-r-plus",  # More capable for complex reasoning
)
```

### Caching Strategies
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_agent_call(prompt: str):
    return agent.execute(prompt)
```

## Testing

### Unit Testing Agents
```python
def test_customer_agent():
    agent = Agent.load("customer_support")
    response = agent.execute("What's your return policy?")
    assert "30 days" in response.text.lower()
```

### Integration Testing
```python
def test_agent_workflow():
    workflow = Workflow([
        Step("classify", classification_agent),
        Step("process", processing_agent)
    ])

    result = workflow.execute(test_input)
    assert result.status == "success"
```

## Oracle Enterprise Integration

### Fusion Applications
```python
# Integrate with Oracle Fusion
fusion_agent = Agent(
    name="fusion_assistant",
    tools=[
        fusion_hcm_tool,
        fusion_erp_tool,
        fusion_scm_tool
    ]
)
```

### Database Integration
```python
# Connect to Autonomous Database
from oci_adk.tools import SQLTool

db_tool = SQLTool(
    connection_string=autonomous_db_connection,
    allowed_tables=["customers", "orders", "products"]
)

agent = Agent(
    name="data_agent",
    tools=[db_tool]
)
```

## Decision Framework

**Use Oracle ADK when:**
- Building on OCI infrastructure
- Integrating with Oracle Fusion/Cloud applications
- Need enterprise-grade security and compliance
- Want code-first agent development
- Deploying multi-region applications

**Consider alternatives when:**
- Not on Oracle Cloud (use Claude SDK or AgentKit)
- Need visual builder interface (use AgentKit)
- Want framework-agnostic approach (use Agent Spec)

## Resources

**Documentation:**
- Official Docs: https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/adk/
- API Reference: https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/adk/api-reference/
- Tutorials: https://docs.public.content.oci.oraclecloud.com/en-us/iaas/Content/generative-ai-agents/add-tool-adk.htm

**Support:**
- OCI Documentation
- Oracle Support Portal
- Oracle Cloud Community

## Final Principles

1. **Code-First** - Leverage existing developer tooling and workflows
2. **Enterprise-Grade** - Built for production Oracle workloads
3. **OCI-Native** - Deep integration with Oracle Cloud services
4. **Multi-Agent** - Design for orchestration from the start
5. **Deterministic** - Explicit control flow for predictable behavior

---

*This skill enables you to build production-ready agentic applications on Oracle Cloud Infrastructure using ADK's code-first approach.*
