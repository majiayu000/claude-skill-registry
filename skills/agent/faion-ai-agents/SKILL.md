---
name: faion-ai-agents
description: "AI agents: autonomous agents, multi-agent systems, LangChain, LlamaIndex, MCP."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# AI Agents Skill

**Communication: User's language. Code: English.**

## Purpose

Specializes in AI agent development and orchestration. Covers autonomous agents, multi-agent systems, frameworks, and MCP.

## Context Discovery

### Auto-Investigation

Check these project signals before asking questions:

| Signal | Where to Check | What to Look For |
|--------|----------------|------------------|
| **Dependencies** | package.json, requirements.txt | langchain, llamaindex, anthropic (MCP) |
| **Agent code** | Grep for "agent", "tool", "ReAct" | Existing agent implementations |
| **MCP config** | mcp.json, claude_desktop_config.json | MCP servers configuration |
| **Tools/functions** | Grep for "function", "tool_def" | Available agent tools |

### Discovery Questions

```yaml
question: "What type of agent are you building?"
header: "Agent Architecture"
multiSelect: false
options:
  - label: "Single autonomous agent"
    description: "One agent with tools (ReAct, plan-and-execute)"
  - label: "Multi-agent system"
    description: "Multiple agents collaborating/delegating"
  - label: "Agentic RAG"
    description: "Agent-driven document retrieval"
  - label: "MCP integration (Claude tools)"
    description: "Model Context Protocol for Claude Code"
```

```yaml
question: "Which agent framework?"
header: "Framework"
multiSelect: false
options:
  - label: "LangChain"
    description: "Most mature, extensive tooling"
  - label: "LlamaIndex"
    description: "Best for data/document agents"
  - label: "Custom implementation"
    description: "Direct API calls to LLM"
  - label: "Claude MCP (native)"
    description: "Claude-native tool protocol"
```

```yaml
question: "What tools/capabilities does the agent need?"
header: "Agent Capabilities"
multiSelect: true
options:
  - label: "Web search"
    description: "Search internet for information"
  - label: "Code execution"
    description: "Run Python/JS code safely"
  - label: "Database queries"
    description: "Query SQL/NoSQL databases"
  - label: "API calls"
    description: "Call external REST/GraphQL APIs"
  - label: "File operations"
    description: "Read/write files, search codebase"
```

## Scope

| Area | Coverage |
|------|----------|
| **Agent Patterns** | ReAct, plan-and-execute, reasoning-first |
| **Autonomous Agents** | Agent loops, memory, tool use |
| **Multi-Agent** | Coordination, communication, delegation |
| **Frameworks** | LangChain, LlamaIndex agent implementations |
| **MCP** | Model Context Protocol, Claude tools |
| **Governance** | EU AI Act compliance, safety |

## Quick Start

| Task | Files |
|------|-------|
| Basic agent | ai-agent-patterns.md → agent-patterns.md |
| Autonomous agent | autonomous-agents.md → agent-architectures.md |
| Multi-agent | multi-agent-basics.md → multi-agent-patterns.md |
| LangChain agents | langchain-agents-architectures.md |
| MCP integration | mcp-model-context-protocol.md → mcp-ecosystem-2026.md |

## Methodologies (26)

**Agent Fundamentals (4):**
- ai-agent-patterns: Core patterns, memory, planning
- agent-patterns: ReAct, chain-of-thought, reflection
- agent-architectures: System design, components
- autonomous-agents: Loops, decision-making, persistence

**Multi-Agent (4):**
- multi-agent-basics: Fundamentals, communication
- multi-agent-patterns: Delegation, collaboration
- multi-agent-design-patterns: Hierarchical, peer-to-peer

**LangChain (7):**
- langchain-basics: Setup, chains, components
- langchain-chains: LCEL, sequential, routing
- langchain-memory: Conversation, summary, entity
- langchain-workflows: Complex flows, branching
- langchain-agents-architectures: Agent types, tools
- langchain-agents-multi-agent: Multi-agent with LangChain
- langchain-patterns: Production patterns

**LlamaIndex (3):**
- llamaindex-basics: Data connectors, indexes
- llamaindex-indexes-queries: Query engines, retrievers
- llamaindex-agents-eval: Agent implementation, evaluation

**MCP & Tooling (4):**
- mcp-model-context-protocol: Protocol fundamentals
- model-context-protocol: Specification
- mcp-ecosystem: Available servers, tools
- mcp-ecosystem-2026: Latest developments

**Governance (2):**
- ai-governance-compliance: Frameworks, best practices
- eu-ai-act-compliance: Risk tiers, requirements
- eu-ai-act-compliance-2026: Latest updates

**Advanced (2):**
- agentic-rag: Agent-driven retrieval (duplicated in RAG)
- reasoning-first-architectures: Extended thinking patterns

## Agent Architectures

### ReAct Pattern

```
Input → Thought → Action → Observation → Thought → ... → Answer
```

### Plan-and-Execute

```
Input → Plan → Execute Step 1 → Execute Step 2 → ... → Synthesize
```

### Reasoning-First

```
Input → Extended Thinking → Plan → Execute → Answer
```

## Code Examples

### Basic ReAct Agent (LangChain)

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Math calculator"
    )
]

llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "What is 25 * 17?"})
```

### Multi-Agent System

```python
from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI

# Define specialized agents
researcher = ChatOpenAI(model="gpt-4o")
writer = ChatOpenAI(model="gpt-4o")

# Orchestrator delegates tasks
orchestrator = initialize_agent(
    tools=[
        Tool(name="research", func=research_agent),
        Tool(name="write", func=writer_agent)
    ],
    llm=ChatOpenAI(model="gpt-4o"),
    agent="zero-shot-react-description"
)

result = orchestrator.invoke("Research AI trends and write a summary")
```

### MCP Server Integration

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get weather data",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            }
        }
    }],
    messages=[{"role": "user", "content": "Weather in NYC?"}]
)
```

### LlamaIndex Agent

```python
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from llama_index.tools import QueryEngineTool

llm = OpenAI(model="gpt-4o")

tools = [
    QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="docs",
        description="Documentation search"
    )
]

agent = ReActAgent.from_tools(tools, llm=llm)
response = agent.chat("How do I use embeddings?")
```

## Multi-Agent Patterns

| Pattern | Use Case |
|---------|----------|
| **Hierarchical** | Manager delegates to specialists |
| **Peer-to-Peer** | Agents collaborate as equals |
| **Sequential** | Chain of agents, each refines |
| **Parallel** | Multiple agents work simultaneously |

## MCP Ecosystem (2026)

| Server | Purpose |
|---------|---------|
| **filesystem** | File operations |
| **postgres** | Database queries |
| **puppeteer** | Web automation |
| **github** | GitHub API access |
| **slack** | Slack integration |

## EU AI Act Compliance

| Risk Tier | Requirements |
|-----------|--------------|
| **Unacceptable** | Banned (social scoring, manipulation) |
| **High-risk** | Conformity assessment, documentation |
| **Limited-risk** | Transparency obligations |
| **Minimal-risk** | No obligations |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-llm-integration | Provides LLM APIs |
| faion-rag-engineer | Agentic RAG integration |
| faion-ml-ops | Agent evaluation |

---

*AI Agents v1.0 | 26 methodologies*
