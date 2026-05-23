---
name: subagent-teams
description: |
  Orchestrate complex tasks by delegating work to parallel subagent teams, preserving the main context window and preventing auto-compact.
  This skill should be used when users ask to apply subagent-teams, when performing complex multi-step tasks, when context window is getting large, or when independent subtasks can run in parallel.
---

# Subagent Teams

Maintain optimum Claude performance by delegating heavy work to subagent teams, minimizing auto-compact of the main context window.

## What This Skill Does

- Decomposes complex tasks into independent subtasks for parallel execution
- Delegates exploration, research, testing, and implementation to specialized subagents
- Keeps main orchestrator context lean (decision-making and synthesis only)
- Prevents auto-compact by isolating heavy work in separate context windows
- Selects optimal model per subtask (Opus for complex, Sonnet for moderate, Haiku for simple)

## What This Skill Does NOT Do

- Handle tasks with strict sequential dependencies (use normal flow)
- Replace the main orchestrator's decision-making role
- Work for single-step trivial tasks (no delegation needed)
- Manage persistent state across subagent sessions

---

## Before Implementation

Gather context to ensure successful delegation:

| Source | Gather |
|--------|--------|
| **User Request** | Full scope of the task, constraints, preferences |
| **Codebase** | Project structure, key files, existing patterns |
| **Skill References** | Delegation patterns from `references/` |
| **Task Complexity** | Number of independent subtasks, dependencies between them |

Only ask user for THEIR specific requirements (delegation strategy is in this skill).

---

## Core Principle: Context Isolation

```
WITHOUT subagent-teams:
  Main Context: [Explore + Search + Read + Analyze + Plan + Implement + Test]
  Result: Context fills → Auto-compact triggers → Quality degrades

WITH subagent-teams:
  Main Context: [Decompose → Delegate → Synthesize → Decide]
  Subagent 1: [Explore codebase] → returns summary
  Subagent 2: [Run tests] → returns pass/fail
  Subagent 3: [Implement feature] → returns code
  Result: Main context stays lean → No auto-compact → Consistent quality
```

---

## Workflow

### Phase 1: Task Decomposition

Analyze the user's request and break it into independent subtasks:

1. **Identify the full scope** of what needs to be done
2. **Map dependencies** — which tasks depend on others?
3. **Group independent tasks** — these can run in parallel
4. **Identify sequential gates** — tasks that must complete before others start

```
User Request
     │
     ▼
┌─────────────────────────┐
│ Dependency Analysis      │
│ - Independent tasks → parallel batch
│ - Dependent tasks → sequential order
│ - Gates → sync points  │
└─────────────────────────┘
     │
     ▼
[Parallel Batch 1] → [Gate] → [Parallel Batch 2] → [Gate] → [Final Synthesis]
```

### Phase 2: Team Assignment

For each subtask, select the optimal subagent configuration:

| Subtask Type | subagent_type | Model | Tools |
|--------------|---------------|-------|-------|
| Codebase exploration | `Explore` | haiku | Read, Grep, Glob |
| Architecture design | `Plan` | sonnet | All read tools |
| Multi-step implementation | `general-purpose` | sonnet/opus | All tools |
| Simple file search | `Explore` | haiku | Glob, Grep |
| Code review | `Explore` | sonnet | Read, Grep |
| Test execution | `general-purpose` | haiku | Bash, Read |

### Phase 3: Parallel Dispatch

Launch independent subagents in a **single message with multiple Task tool calls**:

```
# CORRECT: Single message, multiple tool calls (parallel)
Message contains:
  - Task tool call 1: Explore agent for codebase research
  - Task tool call 2: Explore agent for pattern analysis
  - Task tool call 3: General-purpose agent for test execution

# WRONG: Sequential messages (wastes time)
Message 1: Task tool call 1
[wait for result]
Message 2: Task tool call 2
[wait for result]
```

### Phase 4: Result Synthesis

After subagents return:

1. **Collect** all subagent outputs (compact summaries only enter main context)
2. **Analyze** findings for conflicts or gaps
3. **Synthesize** into unified action plan
4. **Execute** final decisions in main context (or delegate next batch)

### Phase 5: Sequential Gates (if needed)

When later tasks depend on earlier results:

1. Wait for Batch 1 subagents to complete
2. Synthesize Batch 1 results
3. Use synthesized results to inform Batch 2 prompts
4. Launch Batch 2 subagents in parallel
5. Repeat until task is complete

---

## Delegation Decision Matrix

| Condition | Action |
|-----------|--------|
| Task has 3+ independent subtasks | Use subagent-teams |
| Context window already large | Delegate ALL exploration |
| Task involves multiple file reads | Delegate to Explore agents |
| Task requires testing + implementation | Separate into different agents |
| Task is single-step and simple | Do NOT delegate (overhead not worth it) |
| Tasks have strict sequential dependency | Use sequential gates, not parallel |
| User explicitly requests subagent-teams | Always apply this skill |

---

## Subagent Prompt Engineering

Write clear, focused prompts for each subagent:

### Must Include
- **Specific goal**: What exactly to find/do/produce
- **Scope boundary**: What files/areas to focus on
- **Output format**: How to structure the response
- **Context**: Relevant information from earlier steps

### Must NOT Include
- Unnecessary background (wastes subagent context)
- Multiple unrelated tasks in one agent (breaks specialization)
- Vague instructions ("look around the codebase")

### Template
```
"[Action verb] [specific target] in [scope].
Focus on [key aspects].
Return: [structured output format].
Context: [relevant prior findings if any]."
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|-------------|------------------|
| Reading 10+ files in main context | Fills context → auto-compact | Delegate to Explore agent |
| Long grep/search chains in main | Each result adds to context | Single Explore agent does all searching |
| Explore AND implement in same session | Double context usage | Explore agents first, then implement |
| One mega-agent for everything | No specialization, bloated context | Multiple focused agents |
| Not using `run_in_background` | Blocks main session | Use background for long tasks |
| Asking subagent for info you already have | Wastes subagent context | Pass known context in prompt |

---

## Model Selection Strategy

| Task Complexity | Model | Cost | Use When |
|-----------------|-------|------|----------|
| Simple search/grep | `haiku` | Low | Finding files, simple patterns |
| Moderate analysis | `sonnet` | Medium | Code review, architecture design |
| Complex reasoning | `opus` | High | Multi-step implementation, critical decisions |
| Default (unspecified) | inherits | - | When unsure, let it inherit |

---

## Error Handling

| Scenario | Recovery |
|----------|----------|
| Subagent returns incomplete results | Re-launch with more specific prompt |
| Subagent times out | Check with `AgentOutputTool`, adjust scope |
| Conflicting results from agents | Synthesize manually, prioritize authoritative source |
| Too many parallel agents | Limit to 3-5 concurrent, batch the rest |
| Background agent still running | Use `AgentOutputTool` with `block=false` to check status |

---

## Output Checklist

Before completing a subagent-teams workflow, verify:

- [ ] All subtasks identified and categorized (independent vs dependent)
- [ ] Subagent types correctly matched to task types
- [ ] Independent tasks launched in parallel (single message)
- [ ] Sequential gates properly handled
- [ ] Results synthesized into coherent output
- [ ] Main context remains lean (no unnecessary file reads)
- [ ] Model selection optimized for cost/performance

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/delegation-patterns.md` | Complex task decomposition examples |
| `references/prompt-templates.md` | Subagent prompt engineering patterns |
| `references/context-management.md` | Context window optimization strategies |
