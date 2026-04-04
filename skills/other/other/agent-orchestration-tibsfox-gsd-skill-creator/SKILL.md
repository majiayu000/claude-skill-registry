---
name: agent-orchestration
description: Provides best practices for AI agent orchestration including MCP servers, A2A protocol, multi-agent coordination, and swarm architectures. Use when designing agent systems, configuring MCP servers, setting up agent teams, or when user mentions 'MCP', 'A2A', 'agent orchestration', 'multi-agent', 'swarm', 'agent team', 'LangGraph', 'CrewAI', 'AutoGen'.
---

# Agent Orchestration

Best practices for designing, deploying, and coordinating AI agent systems using MCP servers, A2A protocol, and multi-agent patterns.

## Agent Orchestration Patterns

Orchestration determines how agents are coordinated, who makes decisions, and how work flows between them.

| Pattern | Description | Best For | Drawback |
|---------|------------|----------|----------|
| **Centralized** | Single orchestrator dispatches tasks to worker agents | Predictable workflows, clear task boundaries | Orchestrator is a bottleneck and single point of failure |
| **Hierarchical** | Manager agents delegate to specialist sub-agents | Complex multi-domain tasks | Deep hierarchies add latency and lose context |
| **Peer-to-peer** | Agents communicate directly, no central coordinator | Collaborative reasoning, brainstorming | Hard to debug, potential infinite loops |
| **Pipeline** | Agents process sequentially, output feeds next agent | Data transformation, multi-stage analysis | Slow for parallelizable work, rigid ordering |
| **Blackboard** | Shared state space that agents read from and write to | Problems requiring incremental refinement | Contention on shared state, ordering issues |
| **Auction/Market** | Agents bid on tasks based on capability and capacity | Dynamic workload distribution | Overhead of bidding, suboptimal for simple tasks |
| **Swarm** | Many lightweight agents with simple rules, emergent behavior | Exploration, search, large-scale parallel tasks | Unpredictable outcomes, hard to steer |

### Choosing the Right Pattern

```
Is the workflow predictable and linear?
  YES --> Pipeline or Centralized
  NO  --> Does it require specialized domain expertise?
            YES --> Hierarchical (domain managers + specialists)
            NO  --> Do agents need to collaborate on shared output?
                      YES --> Blackboard or Peer-to-peer
                      NO  --> Is the workload dynamic and variable?
                                YES --> Auction/Market
                                NO  --> Centralized (default safe choice)
```

## MCP (Model Context Protocol) for DevOps

MCP provides a standardized way for AI agents to interact with external tools, services, and data sources. Each MCP server exposes capabilities that agents can discover and invoke.

### MCP Architecture

```
Agent (Claude, GPT, etc.)
  |
  +--> MCP Client (built into agent runtime)
         |
         +--> MCP Server: GitHub     (repos, PRs, issues)
         +--> MCP Server: Kubernetes (pods, deployments, services)
         +--> MCP Server: Database   (queries, schema inspection)
         +--> MCP Server: Monitoring (metrics, alerts, dashboards)
         +--> MCP Server: Cloud      (AWS/GCP/Azure resources)
```

### MCP Server Configuration for DevOps Tools

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "kubernetes": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-kubernetes"],
      "env": {
        "KUBECONFIG": "${HOME}/.kube/config"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://readonly:${DB_PASSWORD}@db.internal:5432/production"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/opt/configs",
        "/var/log/apps"
      ]
    },
    "prometheus": {
      "command": "python",
      "args": ["-m", "mcp_prometheus"],
      "env": {
        "PROMETHEUS_URL": "http://prometheus.internal:9090"
      }
    }
  }
}
```

### MCP Server Security Rules

| Rule | Rationale |
|------|-----------|
| Use read-only credentials where possible | Agents should observe before acting; limit blast radius |
| Scope tokens to minimum required permissions | A GitHub token for reading PRs should not have admin access |
| Run MCP servers in isolated environments | Prevent lateral movement if an MCP server is compromised |
| Log all MCP tool invocations | Audit trail for agent actions, required for compliance |
| Set rate limits on MCP server endpoints | Prevent runaway agents from overwhelming external services |
| Validate agent inputs before execution | MCP servers must sanitize and validate all parameters |

### Custom MCP Server Example

```typescript
// mcp-server-deploy.ts -- Custom MCP server for deployment operations
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "deploy-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "get_deployment_status",
    description: "Get current deployment status for a service",
    inputSchema: {
      type: "object",
      properties: {
        service: { type: "string" },
        environment: { type: "string", enum: ["staging", "production"] },
      },
      required: ["service", "environment"],
    },
  }],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  if (name === "get_deployment_status") {
    const status = await queryDeploymentSystem(args.service, args.environment);
    return { content: [{ type: "text", text: JSON.stringify(status, null, 2) }] };
  }
  throw new Error(`Unknown tool: ${name}`);
});

await server.connect(new StdioServerTransport());
```

## A2A (Agent-to-Agent) Protocol

A2A is Google's open protocol for agent interoperability. It enables agents built on different frameworks to discover each other, negotiate capabilities, and exchange tasks.

### A2A Core Concepts

| Concept | Description |
|---------|-------------|
| **Agent Card** | JSON metadata describing an agent's capabilities, endpoint, and auth |
| **Task** | A unit of work sent from one agent to another |
| **Message** | Communication within a task (text, files, structured data) |
| **Artifact** | Output produced by an agent (files, data, results) |
| **Push Notification** | Server-sent updates for long-running tasks |

### A2A Agent Card

```json
{
  "name": "DevOps Deployment Agent",
  "description": "Handles deployments, rollbacks, and release management",
  "url": "https://agents.internal/deploy",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "authentication": {
    "schemes": ["bearer"],
    "credentials": "oauth2_token"
  },
  "defaultInputModes": ["text/plain", "application/json"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "skills": [
    {
      "id": "deploy-service",
      "name": "Deploy Service",
      "description": "Deploy a service to staging or production",
      "tags": ["deployment", "release"],
      "examples": [
        "Deploy payment-api v2.3.1 to staging",
        "Roll back auth-service in production to previous version"
      ]
    },
    {
      "id": "deployment-status",
      "name": "Check Deployment Status",
      "description": "Get current deployment status and history",
      "tags": ["monitoring", "status"]
    }
  ]
}
```

### A2A Task Message Exchange

```json
{
  "jsonrpc": "2.0",
  "method": "tasks/send",
  "id": "req-001",
  "params": {
    "id": "task-deploy-2025-001",
    "message": {
      "role": "user",
      "parts": [
        {
          "type": "text",
          "text": "Deploy payment-api v2.3.1 to staging environment"
        },
        {
          "type": "data",
          "mimeType": "application/json",
          "data": {
            "service": "payment-api",
            "version": "v2.3.1",
            "environment": "staging",
            "strategy": "canary",
            "canary_percentage": 10,
            "rollback_on_error": true
          }
        }
      ]
    }
  }
}
```

### A2A Task Response

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "id": "task-deploy-2025-001",
    "status": {
      "state": "completed",
      "message": {
        "role": "agent",
        "parts": [{ "type": "text", "text": "Deployed payment-api v2.3.1 to staging, canary at 10%." }]
      }
    },
    "artifacts": [{
      "name": "deployment-report",
      "parts": [{
        "type": "data",
        "mimeType": "application/json",
        "data": {
          "deployment_id": "deploy-abc123",
          "status": "healthy",
          "canary_metrics": { "error_rate": 0.001, "p99_latency_ms": 245 }
        }
      }]
    }]
  }
}
```

## Agent Team Configuration

Agent teams assign distinct roles to specialized agents that collaborate on complex tasks.

### Claude Code Agent Team Configuration

```yaml
# agent-team.yaml -- DevOps agent team using Claude Code
team:
  name: devops-ops-team
  coordination: centralized

agents:
  - role: orchestrator
    model: claude-sonnet-4-20250514
    system_prompt: "Receive requests, delegate to specialists, synthesize results. Never act directly."
    tools: [dispatch_to_agent, check_agent_status, aggregate_results]

  - role: code-reviewer
    model: claude-sonnet-4-20250514
    system_prompt: "Review code for security, reliability, team standards. Actionable feedback with line refs."
    tools: [github_pr_read, github_pr_comment, run_static_analysis]

  - role: deployment-agent
    model: claude-sonnet-4-20250514
    system_prompt: "Handle deployments. Verify pre-conditions, canary for prod, confirm health checks."
    tools: [kubernetes_apply, deployment_status, rollback_deployment, run_smoke_tests]

  - role: incident-responder
    model: claude-sonnet-4-20250514
    system_prompt: "Gather metrics, correlate with changes, propose mitigations. No prod changes without approval."
    tools: [query_prometheus, query_logs, get_recent_deployments, create_incident_report]

workflows:
  deploy_request:
    - { agent: code-reviewer, action: review_changes, gate: approval_required }
    - { agent: deployment-agent, action: deploy_to_staging }
    - { agent: deployment-agent, action: run_smoke_tests, gate: tests_must_pass }
    - { agent: deployment-agent, action: deploy_to_production }
    - { agent: orchestrator, action: notify_team }
```

## Swarm Architecture Comparison

Swarm architectures use multiple lightweight agents that coordinate through simple rules or shared state.

| Framework | Architecture | Coordination | State Management | Best For |
|-----------|-------------|-------------|-----------------|----------|
| **LangGraph** | Graph-based DAG | Explicit edges between nodes | Shared state object passed through graph | Complex workflows with conditional branching |
| **CrewAI** | Role-based crew | Sequential or parallel task execution | Shared memory + per-agent memory | Task-oriented teams with clear role separation |
| **AutoGen** | Conversational | Agent-to-agent messaging | Conversation history as shared context | Multi-turn collaborative reasoning |
| **OpenAI Agents SDK** | Handoff-based | Agent-to-agent handoffs with context transfer | Thread-level state with tool results | Production agent systems with tool use |
| **Claude Code** | Orchestrator + sub-agents | Parent spawns child agents via Task tool | File system + context passing | Developer tooling and code generation |

### LangGraph: Conditional Workflow

```python
# langgraph_deploy_workflow.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class DeployState(TypedDict):
    service: str
    version: str
    review_result: str       # "approved" | "rejected"
    staging_healthy: bool

def review_code(state: DeployState) -> DeployState:
    result = code_review_agent.invoke(f"Review {state['service']} {state['version']}")
    state["review_result"] = result.approval_status
    return state

def deploy_staging(state: DeployState) -> DeployState:
    result = deploy_agent.invoke(f"Deploy {state['service']} {state['version']} to staging")
    state["staging_healthy"] = result.healthy
    return state

def should_deploy(state: DeployState) -> Literal["deploy_staging", "end"]:
    return "deploy_staging" if state["review_result"] == "approved" else "end"

# Build: review --> (approved?) --> staging --> (healthy?) --> production
workflow = StateGraph(DeployState)
workflow.add_node("review", review_code)
workflow.add_node("deploy_staging", deploy_staging)
workflow.set_entry_point("review")
workflow.add_conditional_edges("review", should_deploy)
workflow.add_edge("deploy_staging", END)
graph = workflow.compile()
```

### OpenAI Agents SDK: Handoff Pattern

```python
# openai_agents_deploy.py
from agents import Agent, handoff, Runner

code_reviewer = Agent(
    name="Code Reviewer",
    instructions="""Review code changes for security and reliability.
    If approved, hand off to Deployer. If rejected, explain why.""",
    handoffs=["deployer"],
)

deployer = Agent(
    name="Deployer",
    instructions="""Deploy the approved changes. Use canary strategy
    for production. Hand off to Monitor after deployment.""",
    handoffs=["monitor"],
    tools=[deploy_to_staging, deploy_to_production, run_smoke_tests],
)

monitor = Agent(
    name="Monitor",
    instructions="""Monitor the deployment for 15 minutes. Check error
    rates, latency, and resource usage. Report any anomalies.""",
    tools=[query_metrics, check_error_rate, check_latency],
)

# Run the pipeline
result = Runner.run(
    code_reviewer,
    input="Deploy payment-api v2.3.1 -- changes include rate limiting middleware",
)
```

## Agent Communication Patterns

### Message Types

| Message Type | Purpose | Example |
|-------------|---------|---------|
| **Task Request** | Ask an agent to perform work | "Deploy service X to staging" |
| **Status Update** | Report progress on ongoing work | "Deployment at 50%, canary healthy" |
| **Result** | Deliver completed work output | "Deployment complete, all health checks pass" |
| **Query** | Ask for information without action | "What is the current error rate for service X?" |
| **Escalation** | Report a problem requiring higher authority | "Canary error rate exceeds 5%, requesting rollback approval" |
| **Handoff** | Transfer responsibility to another agent | "Code review complete, handing off to deployment agent" |

### Communication Topology

```
Centralized (Star):          Peer-to-peer (Mesh):
                              A --- B
    B   C                     |\ /|
     \ /                      | X |
      A  (orchestrator)       |/ \|
     / \                      C --- D
    D   E

Pipeline (Chain):            Hierarchical (Tree):
A --> B --> C --> D                A
                                /   \
                               B     C
                              / \     \
                             D   E     F
```

### Shared State Protocol

```python
# agent_state.py -- Thread-safe shared state (Blackboard pattern)
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

class SharedAgentState:
    """Shared state space for multi-agent coordination."""

    def __init__(self):
        self._state: dict[str, Any] = {}
        self._lock = threading.RLock()

    def write(self, key: str, value: Any, agent_id: str) -> None:
        with self._lock:
            self._state[key] = {
                "value": value, "updated_by": agent_id,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }

    def read(self, key: str) -> Any | None:
        with self._lock:
            entry = self._state.get(key)
            return entry["value"] if entry else None
```

## State Management Across Agents

### State Strategies by Pattern

| Strategy | Mechanism | Consistency | Scalability |
|----------|----------|-------------|-------------|
| **Pass-through** | State object passed as function argument | Strong (single owner) | Low (deep copying overhead) |
| **Shared memory** | In-process shared dict with locking | Strong (with locks) | Low (single process) |
| **Message queue** | Redis Streams, Kafka, RabbitMQ | Eventual | High |
| **Database** | PostgreSQL, DynamoDB | Strong or eventual (configurable) | High |
| **File system** | JSON/YAML files in shared volume | Weak (race conditions) | Low |
| **Event sourcing** | Append-only log of state changes | Strong (replayable) | High |

### State Persistence for Long-Running Agents

```yaml
# agent-state-config.yaml
state_management:
  backend: redis
  connection: "redis://state.internal:6379/0"
  key_prefix: "agent-state:"
  persistence:
    snapshot_interval: 60s
    snapshot_backend: s3
  isolation:
    strategy: namespace           # {team}:{workflow}:{run_id}
  recovery:
    on_agent_crash: restore_from_snapshot
    on_state_corruption: replay_from_event_log
```

## Multi-Agent Coordination Example

End-to-end example: an incident response pipeline with four coordinating agents using parallel data gathering and sequential analysis.

```python
# incident_response_team.py
import asyncio
from dataclasses import dataclass

@dataclass
class IncidentContext:
    alert_id: str
    service: str
    severity: str
    metrics: dict | None = None
    recent_deploys: list | None = None
    root_cause: str | None = None
    mitigation: str | None = None

async def run_incident_response(alert_id: str, service: str, severity: str):
    ctx = IncidentContext(alert_id=alert_id, service=service, severity=severity)

    # Phase 1: Parallel data gathering (metrics + deploy history agents)
    ctx.metrics, ctx.recent_deploys = await asyncio.gather(
        gather_metrics_agent(ctx),
        gather_deploys_agent(ctx),
    )

    # Phase 2: Sequential analysis (needs data from phase 1)
    ctx.root_cause = await analyze_root_cause_agent(ctx)

    # Phase 3: Mitigation (needs root cause from phase 2)
    ctx.mitigation = await execute_mitigation_agent(ctx)

    # Phase 4: Documentation agent generates postmortem from full context
    return ctx
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Giving agents unrestricted production access | Single hallucinated command can cause outage | Use read-only access by default; require approval gates for writes |
| No audit trail for agent actions | Cannot determine what an agent did or why | Log all tool invocations, decisions, and state changes |
| Agents calling agents in unbounded loops | Infinite recursion, cost explosion, no convergence | Set max iteration limits, timeout budgets, and cycle detection |
| Single mega-agent instead of specialized team | Context window overflow, poor at every task | Split into focused agents with clear responsibilities |
| Shared state without concurrency control | Race conditions, lost updates, inconsistent state | Use locking, versioned writes, or event sourcing |
| No fallback when an agent fails | Entire pipeline stops on one agent error | Implement retries, circuit breakers, and graceful degradation |
| Hardcoding agent dependencies | Cannot swap implementations or scale independently | Use discovery (A2A Agent Cards) or dependency injection |
| Trusting agent output without validation | Hallucinated data propagates through the pipeline | Validate outputs against schemas; add human checkpoints for critical actions |
| Running all agents on the most expensive model | Unnecessary cost for simple tasks | Match model capability to task complexity (small model for routing, large for analysis) |
| No resource budgets per agent | One runaway agent consumes all API quota or compute | Set per-agent token limits, rate limits, and cost ceilings |
| Synchronous-only communication | Pipeline blocked waiting for slow agents | Use async messaging with status callbacks for long-running tasks |
| Ignoring agent context window limits | Agents receive truncated context and make poor decisions | Summarize and filter context before passing between agents |

## Agent Orchestration Readiness Checklist

### Infrastructure

- [ ] MCP servers deployed for required external tools (GitHub, K8s, monitoring)
- [ ] MCP server credentials scoped to minimum required permissions
- [ ] Agent communication channel established (A2A, message queue, or direct)
- [ ] State management backend selected and configured (Redis, DB, or file)
- [ ] Logging and audit trail capturing all agent actions
- [ ] Rate limiting configured per agent and per MCP server

### Agent Design

- [ ] Each agent has a single, well-defined responsibility
- [ ] Agent system prompts include boundaries (what NOT to do)
- [ ] Model selection matches task complexity (not all tasks need the largest model)
- [ ] Input/output schemas defined for agent communication
- [ ] Error handling and retry logic implemented per agent
- [ ] Maximum iteration and token budgets set per agent

### Coordination

- [ ] Orchestration pattern selected and documented (centralized, hierarchical, etc.)
- [ ] Task routing logic tested with representative workloads
- [ ] Handoff protocols defined between agent pairs
- [ ] Shared state access patterns documented with concurrency controls
- [ ] Timeout and circuit breaker thresholds configured
- [ ] Escalation paths defined (agent to agent, agent to human)

### Safety and Governance

- [ ] Human-in-the-loop gates for destructive actions (deploy, delete, rollback)
- [ ] Agent outputs validated against schemas before downstream consumption
- [ ] Cost monitoring and alerting configured per agent team
- [ ] Kill switch available to halt all agent activity immediately
- [ ] Regular review of agent decision logs for quality and drift
- [ ] Incident response plan covers agent-caused failures
