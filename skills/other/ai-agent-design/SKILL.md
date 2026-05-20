---
name: "AI Agent Design Skill"
description: "**Domain**: AI/ML Architecture"
---

# AI Agent Design Skill

> **Domain**: AI/ML Architecture
> **Inheritance**: inheritable
> **Version**: 1.0.0
> **Last Updated**: 2026-02-01

---

## Overview

Comprehensive patterns for designing AI agents—autonomous systems that use LLMs to reason, plan, and execute multi-step tasks. Covers single-agent architectures, multi-agent orchestration, tool use, memory systems, and production deployment patterns.

---

## Agent Architecture Fundamentals

### What Is an AI Agent?

```text
┌─────────────────────────────────────────────────────────────┐
│                      AI AGENT                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐    │
│  │ Perceive│ → │  Plan   │ → │   Act   │ → │  Learn  │    │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘    │
│       ↑                                          │         │
│       └──────────────────────────────────────────┘         │
│                    Feedback Loop                           │
└─────────────────────────────────────────────────────────────┘
```

**Core Components:**
- **Perception**: Receive and interpret inputs (user requests, environment state)
- **Planning**: Reason about goals, decompose tasks, select actions
- **Action**: Execute tools, API calls, or generate outputs
- **Learning**: Update memory, refine strategies based on outcomes

### Agent vs. Chatbot vs. Workflow

| Aspect | Chatbot | Workflow | Agent |
|--------|---------|----------|-------|
| Autonomy | Low | None | High |
| Planning | None | Predefined | Dynamic |
| Tool Use | Limited | Fixed sequence | Flexible |
| Memory | Session only | None | Persistent |
| Error Recovery | Retry/fail | Fail | Reason & adapt |

---

## Single-Agent Patterns

### ReAct Pattern (Reasoning + Acting)

The foundation of most modern agents:

```text
┌──────────────────────────────────────────┐
│              ReAct Loop                  │
├──────────────────────────────────────────┤
│  1. Thought: Reason about the task       │
│  2. Action: Choose and execute a tool    │
│  3. Observation: Process tool output     │
│  4. Repeat until task complete           │
└──────────────────────────────────────────┘
```

**Example Trace:**
```text
User: What's the weather in Seattle and should I bring an umbrella?

Thought: I need to check Seattle weather to answer this question.
Action: weather_api(location="Seattle, WA")
Observation: {"temp": 52, "condition": "rain", "precipitation": 80%}

Thought: It's raining with 80% precipitation chance. User should bring umbrella.
Action: respond("It's 52°F and raining in Seattle with 80% chance of
        precipitation. Yes, definitely bring an umbrella!")
```

### Plan-and-Execute Pattern

For complex, multi-step tasks:

```text
┌─────────────────────────────────────────────────────────────┐
│                   Plan-and-Execute                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐                                            │
│  │   Planner   │  Create high-level plan                    │
│  └──────┬──────┘                                            │
│         ↓                                                   │
│  ┌─────────────┐                                            │
│  │  Executor   │  Execute each step                         │
│  └──────┬──────┘                                            │
│         ↓                                                   │
│  ┌─────────────┐                                            │
│  │  Replanner  │  Adjust plan based on results              │
│  └─────────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```

**When to Use:**
- Tasks requiring multiple distinct phases
- When order of operations matters
- When partial failures need recovery

### Reflexion Pattern

Self-improvement through reflection:

```text
┌─────────────────────────────────────────────────────────────┐
│                     Reflexion                               │
├─────────────────────────────────────────────────────────────┤
│  1. Attempt task                                            │
│  2. Evaluate outcome (success/failure)                      │
│  3. Generate reflection on what went wrong                  │
│  4. Store reflection in memory                              │
│  5. Retry with reflection context                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Multi-Agent Patterns

### Supervisor Pattern

Central coordinator delegates to specialized agents:

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    ┌────────────┐                           │
│                    │ Supervisor │                           │
│                    └─────┬──────┘                           │
│            ┌─────────────┼─────────────┐                    │
│            ↓             ↓             ↓                    │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│     │ Research │  │  Writer  │  │ Reviewer │               │
│     │  Agent   │  │  Agent   │  │  Agent   │               │
│     └──────────┘  └──────────┘  └──────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Use Cases:**
- Content creation pipelines
- Research + analysis + reporting
- Code generation + review + testing

### Hierarchical Teams

Nested supervisor structure for complex organizations:

```text
┌─────────────────────────────────────────────────────────────┐
│                    Top Supervisor                           │
│            ┌─────────────┴─────────────┐                    │
│            ↓                           ↓                    │
│    ┌───────────────┐          ┌───────────────┐            │
│    │ Research Lead │          │ Writing Lead  │            │
│    └───────┬───────┘          └───────┬───────┘            │
│       ┌────┴────┐                ┌────┴────┐               │
│       ↓         ↓                ↓         ↓               │
│   ┌───────┐ ┌───────┐        ┌───────┐ ┌───────┐          │
│   │Web    │ │Paper  │        │Draft  │ │Edit   │          │
│   │Search │ │Review │        │Writer │ │Writer │          │
│   └───────┘ └───────┘        └───────┘ └───────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Debate/Adversarial Pattern

Multiple agents argue to reach better conclusions:

```text
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ┌──────────┐      Argue       ┌──────────┐               │
│   │ Agent A  │ ◄──────────────► │ Agent B  │               │
│   │ (Pro)    │                  │ (Con)    │               │
│   └────┬─────┘                  └────┬─────┘               │
│        │                             │                      │
│        └──────────┬──────────────────┘                      │
│                   ↓                                         │
│            ┌────────────┐                                   │
│            │   Judge    │  Synthesize best answer           │
│            └────────────┘                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Reduces hallucination through verification
- Explores multiple perspectives
- Better reasoning on complex questions

---

## Tool Use Patterns

### Tool Definition Best Practices

```json
{
  "name": "search_database",
  "description": "Search the product database. Returns matching products with prices. Use when user asks about product availability or pricing.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search terms (product name, category, or SKU)"
      },
      "max_results": {
        "type": "integer",
        "default": 10,
        "description": "Maximum results to return (1-100)"
      },
      "filters": {
        "type": "object",
        "properties": {
          "min_price": { "type": "number" },
          "max_price": { "type": "number" },
          "in_stock": { "type": "boolean" }
        }
      }
    },
    "required": ["query"]
  }
}
```

**Tool Design Principles:**
1. **Clear names**: Verb + noun (search_database, send_email)
2. **Rich descriptions**: Include when to use and what it returns
3. **Constrained parameters**: Enums, ranges, validation
4. **Sensible defaults**: Reduce required decisions
5. **Error handling**: Return structured errors, not exceptions

### Tool Selection Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Direct | LLM chooses from all tools | < 10 tools |
| Categorized | Group tools, select category first | 10-50 tools |
| Retrieval | Embed tool descriptions, retrieve relevant | 50+ tools |
| Routing | Specialized selector model | Production scale |

### Human-in-the-Loop Tools

```text
┌─────────────────────────────────────────────────────────────┐
│                Human-in-the-Loop Pattern                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Agent Action Request                                      │
│         │                                                   │
│         ↓                                                   │
│   ┌───────────────┐                                         │
│   │ Risk Check    │                                         │
│   └───────┬───────┘                                         │
│           │                                                 │
│     Low ──┴── High                                          │
│      │         │                                            │
│      ↓         ↓                                            │
│   Execute   ┌──────────┐                                    │
│   Directly  │ Human    │                                    │
│             │ Approval │                                    │
│             └────┬─────┘                                    │
│                  │                                          │
│          Approve/Reject/Modify                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**High-Risk Actions Requiring Approval:**
- Financial transactions
- Data deletion
- External communications
- Permission changes
- Irreversible operations

---

## Agent Memory Systems

### Memory Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Agent Memory                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Working Memory                          │   │
│  │  Current conversation + recent context (in prompt)   │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Short-Term Memory                       │   │
│  │  Session state, intermediate results (key-value)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Long-Term Memory                        │   │
│  │  Facts, preferences, history (vector DB + graph)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Memory Types

| Type | Storage | Retrieval | Use Case |
|------|---------|-----------|----------|
| Episodic | Vector DB | Semantic search | Past conversations, experiences |
| Semantic | Graph DB | Structured query | Facts, relationships, knowledge |
| Procedural | Code/prompts | Direct lookup | How to perform tasks |
| Working | Prompt context | Always present | Current task state |

### Memory Management Patterns

**Summarization**: Compress old conversations
```text
Full History → Summarize → Store Summary → Discard Full
```

**Forgetting**: Remove low-value memories
```text
Memories → Score by (recency × importance × access_count) → Prune lowest
```

**Consolidation**: Merge related memories
```text
Similar Memories → Cluster → Create consolidated memory → Archive originals
```

---

## Planning Strategies

### Task Decomposition

```text
Complex Task: "Build a marketing campaign for our new product"
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Research │   │ Content  │   │ Launch   │
        │  Phase   │   │  Phase   │   │  Phase   │
        └────┬─────┘   └────┬─────┘   └────┬─────┘
             │              │              │
      ┌──────┴──────┐  ┌───┴───┐     ┌───┴───┐
      ↓             ↓  ↓       ↓     ↓       ↓
   Analyze      Survey Create  Write Schedule Monitor
   Competitors  Users  Assets  Copy  Posts   Results
```

### Goal-Oriented Planning

```text
Current State: No marketing campaign
Goal State: Campaign live with 10K impressions
                    │
                    ↓
         ┌─────────────────────┐
         │ Gap Analysis        │
         │ What's missing?     │
         └──────────┬──────────┘
                    ↓
         ┌─────────────────────┐
         │ Action Generation   │
         │ What can close gap? │
         └──────────┬──────────┘
                    ↓
         ┌─────────────────────┐
         │ Action Selection    │
         │ Best next step?     │
         └─────────────────────┘
```

---

## Error Handling & Recovery

### Graceful Degradation

```text
┌─────────────────────────────────────────────────────────────┐
│              Error Recovery Ladder                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Level 1: Retry                                             │
│     └── Same action, maybe with backoff                     │
│                                                             │
│  Level 2: Rephrase                                          │
│     └── Reformulate the action (different query)            │
│                                                             │
│  Level 3: Alternative                                       │
│     └── Use different tool for same goal                    │
│                                                             │
│  Level 4: Partial                                           │
│     └── Return partial results, note limitations            │
│                                                             │
│  Level 5: Escalate                                          │
│     └── Ask human for help                                  │
│                                                             │
│  Level 6: Abort                                             │
│     └── Cannot complete, explain why                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Loop Detection

Agents can get stuck. Detect and break loops:

```python
def detect_loop(action_history, window=5, threshold=0.8):
    """Detect if agent is repeating similar actions."""
    if len(action_history) < window * 2:
        return False

    recent = action_history[-window:]
    previous = action_history[-window*2:-window]

    # Compare action patterns
    similarity = calculate_similarity(recent, previous)
    return similarity > threshold
```

**Recovery Actions:**
- Inject reflection prompt: "You seem to be repeating. What's different now?"
- Force tool change: Exclude recently used tools
- Replan: Discard current plan, start fresh
- Escalate: Ask user for clarification

---

## Production Considerations

### Observability

**What to Log:**
- Every LLM call (prompt, completion, tokens, latency)
- Tool calls (name, parameters, result, duration)
- State transitions (plan changes, memory updates)
- Errors and recovery attempts

**Trace Structure:**
```text
Trace: user_request_abc123
├── parse_intent (50ms)
├── plan_generation (200ms)
├── step_1_research
│   ├── tool_call: search_web (150ms)
│   └── tool_call: summarize (100ms)
├── step_2_write
│   └── llm_call: generate_draft (300ms)
└── step_3_review
    └── llm_call: critique (200ms)
```

### Cost Control

| Strategy | Implementation |
|----------|----------------|
| Token budgets | Set max tokens per task |
| Step limits | Maximum N actions per request |
| Tiered models | GPT-4 for planning, GPT-3.5 for execution |
| Caching | Cache tool results, LLM responses |
| Early termination | Stop when "good enough" |

### Safety Guardrails

```text
┌─────────────────────────────────────────────────────────────┐
│                  Safety Layer                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Input Validation                                           │
│  ├── Prompt injection detection                             │
│  ├── PII/sensitive data filtering                           │
│  └── Request rate limiting                                  │
│                                                             │
│  Action Validation                                          │
│  ├── Tool parameter sanitization                            │
│  ├── Scope/permission checks                                │
│  └── Dangerous action blocking                              │
│                                                             │
│  Output Validation                                          │
│  ├── Content policy compliance                              │
│  ├── Hallucination detection                                │
│  └── Sensitive data redaction                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Framework Comparison

| Framework | Strengths | Best For |
|-----------|-----------|----------|
| LangChain | Comprehensive, many integrations | Rapid prototyping |
| LangGraph | Stateful, graph-based flows | Complex multi-agent |
| AutoGen | Multi-agent conversations | Research, code gen |
| CrewAI | Role-based teams | Business workflows |
| Semantic Kernel | Enterprise, .NET/Python | Microsoft stack |
| Agents SDK (OpenAI) | Simple, hosted | Quick single-agent |

---

## Anti-Patterns

### ❌ Over-Autonomous Agent

**Problem**: Agent makes too many decisions without checkpoints
**Solution**: Add approval gates for significant actions

### ❌ Unbounded Loops

**Problem**: No termination conditions
**Solution**: Set max iterations, cost limits, time bounds

### ❌ Tool Explosion

**Problem**: Too many tools confuse the agent
**Solution**: Curate tools, use retrieval for large toolsets

### ❌ Memory Bloat

**Problem**: Accumulating context without pruning
**Solution**: Summarize, forget, consolidate

### ❌ Monolithic Agent

**Problem**: One agent does everything
**Solution**: Decompose into specialized sub-agents

---

## Activation Triggers

- "agent", "autonomous", "multi-agent"
- "tool use", "function calling"
- "ReAct", "plan and execute"
- "agent memory", "agent planning"
- "orchestration", "supervisor agent"
- "LangChain", "LangGraph", "AutoGen", "CrewAI"

---

## Quick Reference

### Agent Design Checklist

- [ ] Define clear agent persona and capabilities
- [ ] Design minimal, well-described tool set
- [ ] Implement appropriate memory architecture
- [ ] Add human-in-the-loop for high-risk actions
- [ ] Set up observability (logging, tracing)
- [ ] Configure safety guardrails
- [ ] Test with adversarial inputs
- [ ] Plan for cost control and scaling

### When to Use Agents

✅ **Good Fit:**
- Open-ended research tasks
- Multi-step workflows with decisions
- Tasks requiring tool orchestration
- Personalized, context-aware interactions

❌ **Poor Fit:**
- Simple Q&A (use RAG)
- Deterministic workflows (use code)
- High-stakes with no human oversight
- Real-time, latency-critical applications

---

*AI Agent Design skill — Building autonomous, reliable AI systems*
