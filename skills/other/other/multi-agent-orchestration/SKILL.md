---
name: "Multi-Agent Orchestration"
description: "Coordinate multiple AI agents for complex tasks — decomposition, delegation, and synthesis"
applyTo: "**/*agent*,**/*orchestrat*,**/*multi*,**/*workflow*,**/*subagent*"
---

# Multi-Agent Orchestration Skill

> Decompose complex problems into agent-appropriate subtasks, delegate effectively, and synthesize results.

## ⚠️ Rapid Evolution Domain

Multi-agent patterns are evolving rapidly. This skill captures stable patterns while acknowledging the field is in flux.

**Refresh triggers:**
- New orchestration frameworks (LangGraph, AutoGen, CrewAI releases)
- Claude/GPT native multi-agent features
- VS Code Copilot agent architecture changes

**Last validated:** February 2026

---

## Core Concepts

### When to Use Multi-Agent

| Scenario | Single Agent | Multi-Agent |
|----------|--------------|-------------|
| Simple code edit | ✅ | ❌ Overkill |
| Multi-file refactor | ✅ (if capable model) | ⚠️ Consider |
| Research + implement | ⚠️ Long context | ✅ Decompose |
| Cross-domain task | ❌ Context overload | ✅ Specialists |
| Parallel independent work | ❌ Sequential | ✅ Parallel agents |

### Agent Roles

| Role | Responsibility | Example |
|------|---------------|---------|
| **Orchestrator** | Decompose, delegate, synthesize | Main chat session |
| **Specialist** | Deep expertise in one domain | Security reviewer agent |
| **Worker** | Execute well-defined subtask | "Find all usages of X" |
| **Critic** | Validate, review, improve | Code review agent |

---

## Decomposition Patterns

### 1. **Horizontal Decomposition** (Parallel)

Split task into independent subtasks that can run simultaneously.

```
┌─────────────────┐
│  Orchestrator   │
└───────┬─────────┘
        │ decompose
   ┌────┴────┬────────┐
   ▼         ▼        ▼
┌─────┐  ┌─────┐  ┌─────┐
│ A1  │  │ A2  │  │ A3  │   (parallel)
└──┬──┘  └──┬──┘  └──┬──┘
   └────────┼────────┘
            ▼
      synthesize
```

**When to use:**
- Tasks have no dependencies
- Results can be merged mechanically
- Time is critical

**Example:** "Search for security issues in auth, api, and database modules"

### 2. **Vertical Decomposition** (Pipeline)

Chain agents where each builds on previous output.

```
┌─────────────────┐
│  Orchestrator   │
└───────┬─────────┘
        ▼
    ┌───────┐
    │  A1   │ → research
    └───┬───┘
        ▼
    ┌───────┐
    │  A2   │ → analyze
    └───┬───┘
        ▼
    ┌───────┐
    │  A3   │ → implement
    └───────┘
```

**When to use:**
- Each step needs output from previous
- Context builds incrementally
- Quality gates between steps

**Example:** "Research best practices → Design API → Implement → Review"

### 3. **Hierarchical Decomposition** (Tree)

Orchestrator delegates to sub-orchestrators who manage workers.

```
┌─────────────────┐
│   Root Orch     │
└───────┬─────────┘
   ┌────┴────┐
   ▼         ▼
┌─────┐   ┌─────┐
│SubO1│   │SubO2│    (sub-orchestrators)
└──┬──┘   └──┬──┘
 ┌─┴─┐    ┌──┴──┐
 ▼   ▼    ▼     ▼
┌─┐ ┌─┐  ┌─┐   ┌─┐
│W│ │W│  │W│   │W│   (workers)
└─┘ └─┘  └─┘   └─┘
```

**When to use:**
- Very complex tasks
- Different domains within task
- Scale beyond single orchestrator's context

---

## Delegation Best Practices

### Crafting Agent Instructions

When delegating to a subagent, specify:

| Element | Purpose | Example |
|---------|---------|---------|
| **Context** | What they need to know | "Working on Alex VS Code extension" |
| **Scope** | Clear boundaries | "Only look in /src/services" |
| **Output** | Expected format | "Return JSON with findings" |
| **Constraints** | What NOT to do | "Don't modify files, only report" |

### Template for Subagent Prompt

```
**Task:** [One-sentence objective]

**Context:**
- Project: [name/type]
- Relevant files: [list]
- What's already done: [state]

**Scope:**
- DO: [specific actions]
- DON'T: [boundaries]

**Expected Output:**
[Format and content expectations]

**Success Criteria:**
[How you'll know it's done right]
```

---

## Synthesis Patterns

### Merging Agent Outputs

| Pattern | When | How |
|---------|------|-----|
| **Concatenate** | Independent results | Simple append |
| **Deduplicate** | Overlapping searches | Hash/compare |
| **Vote** | Multiple opinions | Majority wins |
| **Synthesize** | Diverse perspectives | LLM summary |
| **Validate** | Critical decisions | Critic agent reviews |

### Conflict Resolution

When agents disagree:

1. **Identify conflict type**
   - Factual (check sources)
   - Opinion (escalate to user)
   - Interpretation (provide both views)

2. **Resolution strategies**
   - Ask clarifying questions
   - Request evidence from agents
   - Escalate to more capable model
   - Present options to user

---

## VS Code Copilot Patterns

### Using `runSubagent` Effectively

The `runSubagent` tool enables orchestration within VS Code:

```typescript
// Good: Clear task with expected output
await runSubagent({
  prompt: `Search the codebase for all error handling patterns.
           Return a JSON array of: {file, line, pattern, quality}`,
  description: "Find error patterns"
});

// Bad: Vague delegation
await runSubagent({
  prompt: "Look for problems in the code",  // Too vague
  description: "Find issues"
});
```

### When to Use Subagent vs Direct

| Scenario | Approach |
|----------|----------|
| Simple search | Direct `grep_search` |
| Complex multi-step search | `runSubagent` |
| Single file edit | Direct `replace_string_in_file` |
| Multi-file coordinated change | Consider subagent for planning |
| Research + implementation | Subagent for research, direct for implementation |

---

## Common Anti-Patterns

### ❌ Over-Orchestration

**Problem:** Using multiple agents for simple tasks
**Symptom:** Slower, more expensive, no quality gain
**Fix:** Trust capable models for multi-step tasks up to complexity threshold

### ❌ Insufficient Context

**Problem:** Agents lack needed information
**Symptom:** Repeated clarification requests, wrong assumptions
**Fix:** Front-load context in delegation prompt

### ❌ No Synthesis Strategy

**Problem:** Raw agent outputs dumped on user
**Symptom:** User must manually integrate results
**Fix:** Plan synthesis before decomposition

### ❌ Circular Dependencies

**Problem:** Agent A needs B's output, B needs A's output
**Symptom:** Deadlock or infinite loops
**Fix:** Identify and break cycles in task graph

---

## Framework Landscape (2026)

| Framework | Strength | Use Case |
|-----------|----------|----------|
| **LangGraph** | State machines, cycles | Complex workflows |
| **AutoGen** | Conversation patterns | Research, debate |
| **CrewAI** | Role-based teams | Business processes |
| **VS Code Agents** | IDE integration | Code tasks |
| **Semantic Kernel** | .NET native | Enterprise C# |

---

## Alex-Specific Patterns

### Heir Orchestration

Master Alex can coordinate heirs for cross-platform tasks:

```
Master Alex (orchestrator)
├── VS Code Heir → code analysis
├── M365 Heir → document synthesis
└── Global Knowledge → pattern matching
```

### Skill Selection as Orchestration

When Alex runs Skill Selection Optimization (SSO), it's a form of self-orchestration:

1. Survey available skills (agents)
2. Match to task requirements
3. Load relevant skills
4. Execute with combined expertise

---

## Implementation Checklist

When designing multi-agent workflows:

- [ ] Can a single capable model handle this?
- [ ] Are subtasks truly independent (or pipelined)?
- [ ] Is context sufficient for each agent?
- [ ] Is output format clearly specified?
- [ ] Is synthesis strategy defined?
- [ ] Are failure modes handled?
- [ ] Is the orchestration overhead justified?

---

## Related Skills

- **skill-selection-optimization** — Pre-task skill loading
- **prompt-engineering** — Crafting effective agent prompts
- **appropriate-reliance** — Knowing when to trust agent output
- **root-cause-analysis** — Debugging multi-agent failures

---

*Multi-agent orchestration is powerful but not always necessary. Start simple, add agents when complexity demands it.*
