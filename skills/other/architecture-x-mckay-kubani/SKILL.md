---
name: architecture
description: Kubani architecture principles, patterns, and design decisions. Use this skill when making architectural decisions or understanding the system design.
---

# Architecture Principles

This skill documents the core architecture principles and patterns used in Kubani. Reference this when making design decisions or understanding the system.

## Core Principles

### 1. Agentic-First Design

**Principle**: Lean on AI as much as possible.

- Agents should be autonomous and self-improving
- Prefer AI-driven solutions over hard-coded logic
- Enable agents to propose their own improvements via the learning system
- Design for continuous learning and adaptation

**Example**: Instead of hard-coding remediation steps, let the agent learn from successful remediations and propose new skills.

### 2. Single Source of Truth

**Principle**: One authoritative source for each type of data.

| Data Type | Source of Truth |
|-----------|-----------------|
| Configuration | `config_unified.py` + YAML files |
| Agent metadata | Registry service |
| Skill definitions | `skills/` directory → Registry |
| Learnings | Memory MCP (Qdrant + Neo4j) |
| Workflows | Temporal |

### 3. MCP-First Tool Integration

**Principle**: All external tool access goes through MCP servers.

```
Agent → MCP Client → MCP Server → External Service
```

Benefits:
- Standardized interfaces
- Consistent error handling
- Centralized metrics and logging
- Easy to add new capabilities

### 4. Registry-Centric Architecture

**Principle**: Everything is registered, discoverable, and synchronized.

```
Git (skills/) ←→ Registry ←→ Agents
                    ↑
                   UI
```

- Agents register on startup
- Skills sync from Git to Registry
- UI queries Registry for visibility
- Bidirectional sync keeps everything consistent

### 5. Hierarchical Configuration

**Principle**: Configuration cascades from general to specific.

```
config.default.yaml    (base)
    ↓
config.{env}.yaml      (environment)
    ↓
config.local.yaml      (local overrides)
    ↓
Environment variables  (runtime overrides)
```

## Architectural Patterns

### Federated Agent Pattern

Complex agents are composed of specialized sub-agents:

```
┌─────────────────────────────────────┐
│           Main Agent                │
│  ┌─────────┐ ┌─────────┐ ┌───────┐ │
│  │Explorer │ │Executor │ │Monitor│ │
│  └─────────┘ └─────────┘ └───────┘ │
└─────────────────────────────────────┘
```

- **Explorer**: Investigates and gathers information
- **Executor**: Takes actions based on decisions
- **Monitor**: Observes outcomes and triggers learning

### Temporal Workflow Pattern

Long-running operations use Temporal workflows:

```python
@workflow.defn
class RemediationWorkflow:
    @workflow.run
    async def run(self, input: RemediationInput) -> RemediationResult:
        # Investigate
        diagnosis = await workflow.execute_activity(
            investigate_pod,
            input.pod_name,
            start_to_close_timeout=timedelta(minutes=5),
        )
        
        # Decide
        action = await workflow.execute_activity(
            decide_action,
            diagnosis,
            start_to_close_timeout=timedelta(minutes=2),
        )
        
        # Execute
        result = await workflow.execute_activity(
            execute_remediation,
            action,
            start_to_close_timeout=timedelta(minutes=10),
        )
        
        return result
```

### Memory Layer Pattern

Three-tier memory architecture:

```
┌─────────────────────────────────────┐
│         Working Memory              │  ← Current context
│         (In-process)                │
├─────────────────────────────────────┤
│         Episodic Memory             │  ← Recent interactions
│         (Redis)                     │
├─────────────────────────────────────┤
│         Semantic Memory             │  ← Long-term knowledge
│         (Qdrant + Neo4j)            │
└─────────────────────────────────────┘
```

### Learning Loop Pattern

Continuous improvement through structured learning:

```
Execute → Critique → Reflect → Synthesize → Approve → Deploy
   ↑                                                    │
   └────────────────────────────────────────────────────┘
```

## Component Responsibilities

### Core Agents (`kubani/framework/`)

- Base agent classes and factories
- Unified configuration system
- MCP client integration
- Skill loading and management
- Learning system (Voyager)
- Memory systems

### Specialized Agents

| Agent | Pattern | Responsibility |
|-------|---------|----------------|
| k8s-monitor | Syndicate (multi-agent) | Kubernetes monitoring and remediation |
| news-monitor | Syndicate (multi-agent) | News aggregation and digest generation |
| learning-agent | Syndicate (multi-agent) | Continuous learning orchestration |
| **Nexus** | **Single agentic loop** | **Conversational PI agent** |

### Nexus Entity Workflow Pattern

Nexus is architecturally distinct from syndicates — it uses a single Strands Agent in a long-running Temporal entity workflow:

```
UI (WebSocket) → Nexus Gateway (FastAPI) → Temporal Signal
    → Orchestrator Workflow → run_agent_turn Activity
        → Strands Agent (think → act → observe loop)
            → Core Tools (read/write/edit/bash)
            → MCP Tools (memory, skills, fetch)
            → Custom Tools (web_search)
        → Response via Redis PubSub → Gateway → UI
```

Key characteristics:
- **Entity workflow**: Receives messages via signals, uses continue-as-new after 100 iterations
- **Direct env vars**: Uses environment variables, not the kubani config system
- **Strands Agent SDK**: Single agent with tool access, not multi-agent orchestration
- **Location**: `kubani/nexus/orchestrator/` (worker, activities, workflow) and `kubani/nexus/gateway/`

See the `nexus` skill for full development details.

### MCP Servers

| Server | Responsibility |
|--------|----------------|
| Temporal MCP | Workflow management |
| Qdrant MCP | Vector operations |
| Memory MCP | Unified memory interface |
| Discord MCP | Discord messaging |
| Kubernetes MCP | Cluster operations |

### Registry

- Agent metadata storage
- Skill catalog
- Model registry
- Health status tracking

### UI

- Agent monitoring dashboard
- Skill browser
- Learning visualization
- Deployment management

## Design Decisions

### Why Temporal?

- Durable execution (survives crashes)
- Built-in retry and timeout handling
- Workflow versioning
- Visibility into execution state
- Supports long-running operations

### Why MCP?

- Standard protocol for tool integration
- Language-agnostic (can use any MCP server)
- Consistent interface for AI agents
- Growing ecosystem of servers

### Why Qdrant + Neo4j?

- **Qdrant**: Fast vector similarity search for semantic matching
- **Neo4j**: Relationship tracking for knowledge graphs
- Combined: Rich memory with both semantic and relational queries

### Why pydantic-settings?

- Type-safe configuration
- Environment variable support
- Validation at load time
- IDE autocomplete
- Easy testing with overrides

## Anti-Patterns to Avoid

### ❌ Hard-coded Logic

```python
# Bad: Hard-coded remediation
if error == "OOMKilled":
    increase_memory()
```

```python
# Good: Skill-driven remediation
skill = await skill_library.find_skill(error_type=error)
await skill.execute(context)
```

### ❌ Direct Service Access

```python
# Bad: Direct Qdrant access
from qdrant_client import QdrantClient
client = QdrantClient(url="...")
```

```python
# Good: MCP client access
from kubani.framework.mcp import get_mcp_client
client = get_mcp_client()
await client.qdrant.search_vectors(...)
```

### ❌ Scattered Configuration

```python
# Bad: Configuration in multiple places
QDRANT_URL = os.getenv("QDRANT_URL", "localhost:6333")
```

```python
# Good: Unified configuration
from kubani.framework.config import get_config
config = get_config()
url = config.memory.qdrant_url
```

### ❌ Monolithic Agents

```python
# Bad: One agent does everything
class SuperAgent:
    def investigate(self): ...
    def decide(self): ...
    def execute(self): ...
    def monitor(self): ...
    def learn(self): ...
```

```python
# Good: Federated agents
class InvestigatorAgent: ...
class ExecutorAgent: ...
class MonitorAgent: ...
```

## When to Deviate

These principles are guidelines, not rules. Deviate when:

1. **Performance requires it**: Direct access may be needed for hot paths
2. **Simplicity wins**: Don't over-engineer simple cases
3. **Prototyping**: Quick experiments can skip patterns
4. **External constraints**: Third-party integrations may require different approaches

Document deviations and plan to refactor when appropriate.
