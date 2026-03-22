---
name: a2a-dev-patterns
description: Apply A2A cross-cutting development patterns — orchestration topologies, idempotency, observability, agent registries, versioning, and production deployment. Use when architecting multi-agent systems or solving cross-cutting concerns.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Development Patterns

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the latest protocol details
2. Web-search `a2a protocol best practices multi-agent architecture` for community patterns
3. Web-search `site:github.com a2aproject A2A samples patterns` for reference architectures
4. Web-search `multi-agent system design patterns` for general multi-agent architecture guidance

## Conceptual Architecture

### Orchestration Topologies

#### Hub-and-Spoke (Orchestrator)
A central coordinator agent delegates subtasks to specialist agents:
```
                    ┌→ Research Agent
Coordinator Agent ──┼→ Analysis Agent
                    └→ Writing Agent
```
- **Pros**: Centralized control, clear task routing, easy to monitor
- **Cons**: Single point of failure, coordinator bottleneck
- **Use when**: Well-defined subtask decomposition, need for aggregation

#### Peer-to-Peer (Mesh)
Agents discover and communicate directly with each other:
```
Agent A ←→ Agent B
  ↕           ↕
Agent C ←→ Agent D
```
- **Pros**: No single point of failure, flexible
- **Cons**: Complex routing, harder to monitor, potential loops
- **Use when**: Agents are loosely coupled, dynamic discovery needed

#### Pipeline (Chain)
Tasks flow through a sequence of agents:
```
Input → Agent A → Agent B → Agent C → Output
```
- **Pros**: Simple flow, easy to reason about, composable
- **Cons**: Sequential latency, failure in one stage blocks all
- **Use when**: Clear transformation stages, ETL-like workflows

#### Hierarchical (Tree)
Manager agents delegate to team agents, which may further delegate:
```
CEO Agent
├── Marketing Manager Agent
│   ├── Content Agent
│   └── SEO Agent
└── Engineering Manager Agent
    ├── Frontend Agent
    └── Backend Agent
```
- **Pros**: Natural decomposition, scoped authority, scalable
- **Cons**: Deep hierarchies add latency, complex coordination
- **Use when**: Large organizations of agents, domain separation

### Idempotency

Design A2A interactions to be idempotent:
- Use deterministic task IDs (hash of input + context) when possible
- Handle duplicate `message/send` requests gracefully
- Store task results for replay on retry
- Use request IDs for deduplication at the transport level

### Observability

Multi-agent systems need deep observability:

**Distributed tracing:**
- Propagate trace IDs through A2A task metadata
- Log entry/exit for each agent in the chain
- Use OpenTelemetry or similar for cross-agent tracing

**Metrics:**
- Task latency per agent
- Task success/failure rates
- Message volume and throughput
- Active task count per agent
- Error code distribution

**Logging:**
- Log all JSON-RPC requests/responses (with sensitive data redacted)
- Include task IDs and request IDs in all log entries
- Log state transitions with timestamps

### Agent Registries

For systems with many agents:
- **Centralized registry** — Agents register their Agent Cards; clients query by skill/tag
- **DNS-based discovery** — Agent Cards at well-known URLs
- **Service mesh** — Use infrastructure-level service discovery

### Versioning

A2A agents evolve over time:
- **Agent Card version** — Update when skills or capabilities change
- **Skill versioning** — Individual skills can be versioned
- **Protocol version** — Track which A2A spec version you implement
- **Breaking changes** — Update the Agent Card URL or version for breaking changes
- **Backward compatibility** — Support old and new message formats during transitions

### Security Patterns

- **Zero trust** — Authenticate every agent-to-agent call
- **Least privilege** — Agents only get access to the skills they need
- **Audit trail** — Log all cross-agent interactions for compliance
- **Secret management** — Use vaults for API keys and credentials, never hardcode

### Production Deployment

- **Health checks** — Implement `/health` endpoints alongside the A2A endpoint
- **Graceful shutdown** — Complete or cancel in-flight tasks before stopping
- **Scaling** — A2A servers are stateless per-request; task store handles state
- **Load balancing** — Standard HTTP load balancing works for A2A endpoints
- **Rate limiting** — Protect agents from being overwhelmed by requests
- **Circuit breakers** — Stop calling failing agents, use fallbacks

### Error Recovery Patterns

- **Retry with backoff** — Transient failures, exponential backoff
- **Fallback agents** — If primary agent fails, try an alternative
- **Dead letter queue** — Store failed tasks for later analysis/replay
- **Compensation** — If a multi-step workflow fails midway, undo completed steps
- **Timeout escalation** — If a task is stuck, escalate to a human or different agent

### Best Practices

- Start simple — hub-and-spoke before mesh
- Design for failure — every agent call can fail
- Make agents stateless where possible — state lives in the task store
- Use structured DataParts for inter-agent data, not serialized text
- Monitor everything — you can't debug what you can't see
- Version your Agent Cards and document changes
- Test the full topology, not just individual agents
- Set SLOs for agent response times and success rates

Fetch the latest A2A specification and community patterns before implementing multi-agent architectures.
