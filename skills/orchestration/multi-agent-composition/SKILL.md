---
name: multi-agent-composition
description: >
  This skill should be used when the user asks to "choose between skill and agent", "compose
  multi-agent system", "orchestrate agents", "manage agent context", "design component
  architecture", "should I use a skill or agent", "when to use hooks vs MCP", "build orchestrator
  workflow", needs decision frameworks for Claude Code components (skills, sub-agents, hooks, MCP
  servers, slash commands), context management patterns, or wants to build effective multi-component
  agentic systems with proper orchestration and anti-patterns guidance.
---

# Multi-Agent Composition

**Master Claude Code's components, patterns, and principles** to build effective agentic systems.

## When to Use This Knowledge

Use this knowledge when:

- **Learning Claude Code** - Understanding what each component does
- **Making architectural decisions** - Choosing Skills vs Sub-Agents vs MCP vs Slash Commands
- **Building custom solutions** - Creating specialized agents or orchestration systems
- **Scaling agentic workflows** - Moving from single agents to multi-agent orchestration
- **Debugging issues** - Understanding why components behave certain ways
- **Adding observability** - Implementing hooks for monitoring and control

## Quick Reference

### The Core 4 Framework

Every agent is built on these four elements:

1. **Context** - What information does the agent have?
2. **Model** - What capabilities does the model provide?
3. **Prompt** - What instruction are you giving?
4. **Tools** - What actions can the agent take?

> "Everything comes down to just four pieces. If you understand these, you will win."

### Component Overview

| Component | Trigger | Use When | Best For |
|-----------|---------|----------|----------|
| **Skills** | Agent-invoked | Repeat problems needing management | Domain-specific workflows |
| **Sub-Agents** | Tool-invoked | Parallelization & context isolation | Scale & batch operations |
| **MCP Servers** | As needed | External data/services | Integration with external systems |
| **Slash Commands** | Manual/tool | One-off tasks | Simple repeatable prompts |
| **Hooks** | Lifecycle events | Observability & control | Monitoring & blocking |

### Composition Hierarchy

```text
Skills (Top Layer)
  ├─→ Can use: Sub-Agents, Slash Commands, MCP Servers, Other Skills
  └─→ Purpose: Orchestrate primitives for repeatable workflows

Sub-Agents (Execution Layer)
  ├─→ Can use: Slash Commands, Skills
  └─→ Cannot nest other Sub-Agents

Slash Commands (Primitive Layer)
  └─→ The fundamental building block

MCP Servers (Integration Layer)
  └─→ Connect external systems
```

### Golden Rules

1. **Always start with prompts** - Master the primitive first
2. **"Parallel" = Sub-Agents** - Nothing else supports parallel execution
3. **External = MCP, Internal = Skills** - Clear separation of concerns
4. **One-off = Slash Command** - Don't over-engineer
5. **Repeat + Management = Skill** - Only scale when needed
6. **Don't convert all slash commands to skills** - Huge mistake
7. **Context, Model, Prompt, Tools** - Never forget the foundation

## Documentation Structure

This skill uses progressive disclosure. Start here, then navigate to specific topics as needed.

### Reference Documentation

**Architecture fundamentals** - What each component is and how they work

- **[architecture.md](reference/architecture.md)** - Component definitions, capabilities, restrictions
- **[core-4-framework.md](reference/core-4-framework.md)** - Deep dive into Context, Model, Prompt, Tools

### Implementation Patterns

**How to use components effectively** - Decision-making and implementation

- **[decision-framework.md](patterns/decision-framework.md)** - When to use Skills vs Sub-Agents vs MCP vs Slash Commands
- **[hooks-in-composition.md](patterns/hooks-in-composition.md)** - Implementing hooks for observability and control
- **[orchestrator-pattern.md](patterns/orchestrator-pattern.md)** - Multi-agent orchestration at scale
- **[context-management.md](patterns/context-management.md)** - Managing context across agents
- **[context-in-composition.md](patterns/context-in-composition.md)** - Context handling in multi-agent systems

### Anti-Patterns

#### Common mistakes to avoid

- **[common-mistakes.md](anti-patterns/common-mistakes.md)** - Converting all slash commands to
  skills, using skills for one-offs, context explosion, and more

### Examples

#### Real-world case studies and progression paths

- **[progression-example.md](examples/progression-example.md)** - Evolution from prompt → sub-agent → skill (work tree manager example)
- **[case-studies.md](examples/case-studies.md)** - Scout-builder patterns, orchestration workflows, multi-agent systems

### Workflows

#### Visual guides and decision trees

- **[decision-tree.md](workflows/decision-tree.md)** - Decision trees, mindmaps, and visual guides for choosing components

## Getting Started

### If you're new to Claude Code

1. Start with **[reference/architecture.md](reference/architecture.md)** to understand components
2. Read **[reference/core-4-framework.md](reference/core-4-framework.md)** to grasp the foundation
3. Use **[patterns/decision-framework.md](patterns/decision-framework.md)** to make your first architectural choice
4. Check **[anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md)** to avoid pitfalls

### If you're making an architectural decision

1. Open **[patterns/decision-framework.md](patterns/decision-framework.md)**
2. Follow the decision tree to identify the right component
3. Review the specific component in **[reference/architecture.md](reference/architecture.md)**
4. Check **[examples/](examples/)** for similar use cases

### If you're adding observability

1. Read **[patterns/hooks-in-composition.md](patterns/hooks-in-composition.md)** to understand available hooks and implementation
2. Use isolated scripts pattern (UV, bun, or shell)

### If you're scaling to multi-agent orchestration

1. Ensure you've mastered custom agents first
2. Read **[patterns/orchestrator-pattern.md](patterns/orchestrator-pattern.md)**
3. Study **[examples/case-studies.md](examples/case-studies.md)**
4. Review **[patterns/context-management.md](patterns/context-management.md)**

## Key Principles from the Field

### Prompts Are the Primitive

> "Do not give away the prompt. The prompt is the fundamental unit of knowledge work and of programming. If you don't know how to build and manage prompts, you will lose."

**Everything is prompts in the end.** Master slash commands before skills. Have a strong bias toward slash commands.

### Skills Are Compositional, Not Replacements

> "It is very clear this does not replace any existing feature or capability. It is a higher compositional level."

Skills orchestrate other components; they don't replace them. Don't convert all your
slash commands to skills—that's a huge mistake.

### Observability is Everything

> "When it comes to agentic coding, observability is everything. How well you can observe, iterate, and improve your agentic system is going to be a massive differentiating factor."

If you can't measure it, you can't improve it. If you can't measure it, you can't scale it.

### Context Window Protection

> "200k context window is plenty. You're just stuffing a single agent with too much work. Don't force your agent to context switch."

Create focused agents with single purposes. Delete them when done. Treat agents as temporary, deletable resources.

### The Agentic Engineering Progression

```text
Level 1: Base agents       → Use agents out of the box
Level 2: Better agents     → Customize prompts and workflows
Level 3: More agents       → Run multiple agents
Level 4: Custom agents     → Build specialized solutions
Level 5: Orchestration     → Manage fleets of agents
```

## Source Attribution

This knowledge synthesizes:

- Video presentations by Claude Code engineering team
- Official Claude Code documentation (docs.claude.com)
- Hands-on experimentation and validation
- Multi-agent orchestration patterns from the field

## Quick Navigation

**Need to understand what a component is?** → [reference/architecture.md](reference/architecture.md)

**Need to choose the right component?** → [patterns/decision-framework.md](patterns/decision-framework.md)

**Need to implement hooks?** → [patterns/hooks-in-composition.md](patterns/hooks-in-composition.md)

**Need to scale to multiple agents?** → [patterns/orchestrator-pattern.md](patterns/orchestrator-pattern.md)

**Need to see real examples?** → [examples/](examples/)

**Need visual guides?** → [workflows/decision-tree.md](workflows/decision-tree.md)

**Want to avoid mistakes?** → [anti-patterns/common-mistakes.md](anti-patterns/common-mistakes.md)

---

**Remember:** Context, Model, Prompt, Tools. Master these four, and you master Claude Code.
