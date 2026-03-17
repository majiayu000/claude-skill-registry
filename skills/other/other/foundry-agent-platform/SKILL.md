---
name: "foundry-agent-platform"
description: "Microsoft Foundry agent deployment, orchestration, and cloud-native AI service patterns"
---

# Foundry Agent Platform Skill

> Deploy, orchestrate, and manage AI agents on Microsoft Foundry — the unified Azure PaaS for enterprise AI.

## Rapid Evolution Domain

Foundry is in active preview (February 2026). SDK versions change frequently.

**Refresh triggers:**
- `azure-ai-projects` SDK version bump (currently 2.0.0b3)
- Foundry portal feature releases
- Hosted Agents GA
- Memory API changes

**Last validated:** February 2026

---

## Platform Overview

Microsoft Foundry (formerly Azure AI Foundry) unifies model hosting, agent orchestration, tool management, observability, and multi-channel publishing.

| Concept | Description |
|---------|-------------|
| **Portal** | https://ai.azure.com |
| **Endpoint** | `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| **MCP Server** | https://mcp.ai.azure.com (cloud-hosted, Entra ID) |
| **VS Code Extension** | `TeamsDevApp.vscode-ai-foundry` |
| **Key Distinction** | Infrastructure platform (backend), not a surface |

### Foundry vs Other Platforms

| Aspect | VS Code Extension | M365 Copilot | Foundry |
|--------|------------------|-------------|---------|
| **Type** | IDE plugin | Declarative agent | Cloud PaaS |
| **Runtime** | Desktop app | M365 cloud | Azure managed |
| **Users** | Single developer | Single user | Multi-user |
| **Availability** | When IDE open | When M365 open | Always-on (24/7) |
| **Memory** | File-based synapses | OneDrive | Platform-managed |
| **Tools** | MCP (manual config) | Web/SP/Graph | 1,400+ catalog |
| **Agents** | `.agent.md` files | Single agent | Multi-agent fleet |
| **Observability** | Manual | None | Full OpenTelemetry |

---

## Four SDK Types

This is the most common source of confusion. Foundry has **four distinct SDK types**, each with different endpoints and use cases:

| SDK | Endpoint | When to Use |
|-----|----------|-------------|
| **Foundry SDK** | `.services.ai.azure.com/api/projects/` | Agent management, evaluations, deployments |
| **OpenAI SDK** | `.openai.azure.com/openai/v1` | Chat completions, embeddings (OpenAI-compatible) |
| **Foundry Tools SDKs** | Service-specific | Speech, Vision, Language, Search, etc. |
| **Agent Framework** | Framework-specific | Multi-agent orchestration (cloud-agnostic) |

### SDK Packages

| Language | Foundry SDK | OpenAI SDK |
|----------|-------------|------------|
| Python | `azure-ai-projects>=2.0.0b3` (use `--pre`) | `openai` |
| C# | `Azure.AI.Projects` (preview) | `Azure.AI.OpenAI` |
| JS/TS | `@azure/ai-projects` (beta) | `openai` |
| Java | `com.azure:azure-ai-projects` (preview) | — |

> **Breaking Change**: Python 2.x is **incompatible** with 1.x. The 2.x uses `.services.ai.azure.com` endpoints.

---

## Agent Service Patterns

### Create Agent

```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

client = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential()
)

agent = client.agents.create_agent(
    model="gpt-4.1-mini",
    name="my-agent",
    instructions="System prompt here."
)
```

### Versioned Agents

```python
from azure.ai.projects.models import PromptAgentDefinition

definition = PromptAgentDefinition(
    model="gpt-4.1-mini",
    instructions="System prompt",
    tools=[bing_tool, file_search_tool]
)

version = client.agents.create_agent_version(
    agent_id=agent.id,
    definition=definition
)
```

### Conversations (Multi-Turn)

```python
conversation = client.agents.create_conversation(agent_id=agent.id)

client.agents.create_message(
    conversation_id=conversation.id,
    role="user",
    content="Hello"
)

run = client.agents.create_run(
    conversation_id=conversation.id,
    agent_id=agent.id
)
```

### Key Concepts

| Concept | Meaning |
|---------|---------|
| **Agent** | Stateless definition (model + instructions + tools) |
| **Conversation** | Stateful multi-turn context |
| **Run** | Single execution within a conversation |
| **Version** | Immutable snapshot of agent definition |

---

## Tool Categories

| Tool | Use Case | Setup |
|------|----------|-------|
| **Bing Grounding** | Real-time web search | Bing Search resource |
| **File Search** | RAG over documents (vector stores) | Upload files → vector store |
| **Code Interpreter** | Python sandbox execution | Automatic |
| **SharePoint** | Enterprise document grounding | SP site + permissions |
| **OpenAPI** | Any REST API via spec | Provide spec + auth |
| **MCP Servers** | Remote Model Context Protocol | Server URL + auth |
| **A2A** | Agent-to-Agent communication | Target URL + auth |

### File Search Setup

```python
vector_store = client.agents.create_vector_store(name="knowledge")
client.agents.upload_file_and_poll(
    vector_store_id=vector_store.id,
    file_path="skills.pdf"
)
file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
```

---

## Memory & Foundry IQ

| Feature | Description |
|---------|-------------|
| **Memory** | Cross-session context retention, per-user, automatic |
| **Foundry IQ** | Enterprise knowledge base with citations + web grounding |
| **Priority Chain** | Instructions → IQ → File Search → Tool results → Training data |

Memory is the cloud-native equivalent of Alex's synapse architecture — automatic, persistent, cross-surface.

---

## Hosted Agents (Preview)

Containerized agents on managed infrastructure:

```bash
pip install azure-ai-agentserver-agentframework
agentserver run --interactive   # local test
agentserver run                 # container mode (port 8080)
azd deploy                      # deploy to Foundry
```

Supports any framework: LangGraph, MS Agent Framework, Semantic Kernel, custom.

---

## Observability Stack

```
Agent → OpenTelemetry → Application Insights → Agent Dashboard
```

```python
from azure.ai.agentserver import setup_observability
setup_observability(vs_code_extension_port=4319)  # local dev
```

### Built-in Evaluators

Relevance, Groundedness, Coherence, Safety, F1, BLEU, ROUGE

---

## Publishing Channels

One agent, many surfaces:

| Channel | Transport |
|---------|-----------|
| **M365 Copilot** | Teams manifest + Entra app |
| **Teams** | Bot Framework |
| **BizChat** | Via M365 publish |
| **Web Preview** | Auto-generated URL |
| **REST API** | Standard HTTP |
| **Container** | Docker (Hosted Agent) |

---

## Realtime API (Voice)

| Transport | Latency | Use Case |
|-----------|---------|----------|
| **WebRTC** | ~100ms | Browser voice |
| **WebSocket** | ~200ms | Server-side |
| **SIP** | Varies | Telephony |

Models: `gpt-realtime` (GA), `gpt-realtime-mini` (GA). Supports MCP tools during voice sessions, semantic VAD, image input. 30-min session limit, PCM16 mono 24kHz.

---

## Authentication

```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()  # Keyless (recommended)
client = AIProjectClient(endpoint=endpoint, credential=credential)
```

| RBAC Role | Scope |
|-----------|-------|
| Azure AI User | Least privilege — call agents, use models |
| Azure AI Owner | Create/manage agents, deploy models |
| Contributor | Create Foundry projects and resources |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Instead |
|-------------|-------------|---------|
| Using Python SDK 1.x with 2.x docs | Incompatible APIs, wrong endpoints | Always install `--pre` for 2.x |
| Treating Foundry as "just another heir" | It's a backend, not a surface | Design as shared infrastructure |
| Hardcoding API keys | Security risk, doesn't scale | Use `DefaultAzureCredential` |
| One giant agent | Context overload, poor routing | Multi-agent with orchestrator |
| Skipping evaluation | No quality baseline | Run evaluators before shipping |
| Ignoring cost | Pay-per-use can surprise | Use efficient models (4.1-mini) for most agents |

---

## Decision Checklist

When designing a Foundry-based agent:

- [ ] Which SDK type? (Foundry SDK for agents, OpenAI SDK for completions)
- [ ] Which model tier? (Premium for orchestrator, efficient for specialists)
- [ ] Agent Service or Hosted Agent? (Start with Agent Service; migrate later)
- [ ] What tools? (Bing, File Search, Code Interpreter, MCP, OpenAPI)
- [ ] Memory strategy? (Foundry Memory, File Search, or hybrid)
- [ ] Publishing targets? (API first, then Teams, then Web, then Voice)
- [ ] Evaluation plan? (Which evaluators, what dataset, what baseline)
- [ ] Auth model? (Entra ID keyless via DefaultAzureCredential)

---

## Synapses

- [.github/skills/ai-agent-design/SKILL.md] (Critical, Implements, Bidirectional) - "Foundry is the runtime for agent design patterns"
- [.github/skills/multi-agent-orchestration/SKILL.md] (Critical, Implements, Bidirectional) - "Foundry Agent Service enables multi-agent orchestration at scale"
- [.github/skills/azure-architecture-patterns/SKILL.md] (High, Extends, Bidirectional) - "Foundry is an Azure PaaS that follows WAF principles"
- [.github/skills/mcp-development/SKILL.md] (High, Complements, Bidirectional) - "Foundry supports MCP servers as agent tools"
- [.github/skills/enterprise-integration/SKILL.md] (High, Enables, Forward) - "Foundry provides enterprise-grade agent deployment"
- [.github/instructions/meditation.instructions.md] (Medium, Created-During, Forward) - "Skill created during platform expansion meditation"

---

*Microsoft Foundry Agent Platform — cloud-native agent deployment for the Alex ecosystem*
