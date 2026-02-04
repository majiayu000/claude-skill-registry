---
name: agent-orchestration
description: |
  Coordinate parallel agent execution with context handoff. Use when:
  (1) task has parallelizable subtasks, (2) need to explore multiple areas,
  (3) research and implementation can happen concurrently. Updates AGENTS.md
  with status and results.
category: development
user-invocable: true
---

# Agent Orchestration

Coordinates parallel agent execution with context handoff via documentation.

## Trigger Conditions

Invoke when:
- Task has independent subtasks
- Need to explore multiple code areas
- Research and implementation can run in parallel
- Complex task benefits from divide-and-conquer

Also invoke explicitly with:
- `/agent-orchestration [task]`
- "coordinate agents"
- "run in parallel"

## Procedure

### Step 1: Analyze Task

Break down the task into subtasks:

**Questions to ask:**
- Can subtasks run independently?
- Do subtasks have dependencies?
- What context does each agent need?
- How will results be combined?

### Step 2: Classify Parallelization Pattern

| Pattern | Description | Example |
|---------|-------------|---------|
| **Independent** | No dependencies | Explore 3 code areas |
| **Fan-out/Fan-in** | Parallel then combine | Research multiple approaches, then decide |
| **Pipeline** | Sequential handoff | Research → Plan → Implement |
| **Hybrid** | Mix of above | Research (parallel) → Plan → Implement (parallel) |

### Step 3: Create Agent Specifications

For each agent, define:

```markdown
## Agent: {{agent_id}}

**Task:** {{specific_task}}
**Type:** Explore | Research | Implement | Review
**Dependencies:** {{none | agent_ids}}
**Expected output:** {{files | summary | decision}}
**Context:** {{what this agent needs to know}}
```

### Step 4: Update AGENTS.md

Before launching:

```markdown
# Agent Coordination

## Current Task

Implement user authentication with OAuth support

## Active Agents

| ID | Task | Status | Started | Output |
|----|------|--------|---------|--------|
| a1 | Research OAuth providers | running | 14:30 | - |
| a2 | Explore existing auth code | running | 14:30 | - |
| a3 | Review security requirements | running | 14:30 | - |

## Dependencies

a1 ─┐
a2 ─┼─> a4 (implementation)
a3 ─┘
```

### Step 5: Launch Agents

**Independent agents (launch in parallel):**

```
Launch agents a1, a2, a3 in parallel:

Agent a1: "Research OAuth providers (Google, GitHub, Microsoft). Compare features, security, implementation complexity. Output to RESEARCH.md"

Agent a2: "Explore existing auth code in src/auth/. Document current patterns, identify extension points. Output findings to AGENTS.md"

Agent a3: "Review security requirements in docs/security.md. List authentication requirements and constraints."
```

**Dependent agents (wait for predecessors):**

```
Wait for a1, a2, a3 to complete.

Agent a4: "Using research from a1, patterns from a2, and requirements from a3, implement OAuth authentication. Follow TDD workflow."
```

### Step 6: Collect Results

Update AGENTS.md with results:

```markdown
## Completed Agents

### Agent a1: Research OAuth providers

**Status:** complete
**Duration:** 15 min

**Results:**
Recommended Google OAuth for:
- Widest user base
- Best documentation
- Simplest implementation

**Files modified:**
- RESEARCH.md (OAuth findings section)

### Agent a2: Explore existing auth code

**Status:** complete
**Duration:** 12 min

**Results:**
Found extension points in:
- src/auth/middleware.ts (add OAuth check)
- src/auth/providers/ (add Google provider)

**Files modified:**
- None (exploration only)
```

### Step 7: Context Handoff

Document what each agent discovered for the next phase:

```markdown
## Context Handoff

### From a1 to a4

**Discovered:** Google OAuth is best choice. Use @google-cloud/oauth2 library.

**Next steps:** Implement Google OAuth provider in src/auth/providers/google.ts

### From a2 to a4

**Discovered:** Existing auth middleware at src/auth/middleware.ts can be extended. Pattern: each provider exports `authenticate()` and `getUser()` functions.

**Next steps:** Follow existing pattern when adding Google provider.
```

## Parallelization Patterns

### Pattern 1: Independent Exploration

Good for: Understanding codebase, initial research

```
┌─ Agent a1: Explore frontend ────┐
├─ Agent a2: Explore backend ─────┼─> Synthesize
└─ Agent a3: Explore infrastructure ─┘
```

### Pattern 2: Research Then Decide

Good for: Evaluating options before implementation

```
┌─ Agent a1: Research option A ───┐
├─ Agent a2: Research option B ───┼─> Decision Agent
└─ Agent a3: Research option C ───┘
```

### Pattern 3: Parallel Implementation

Good for: Independent features or components

```
┌─ Agent a1: Implement feature A ─┐
├─ Agent a2: Implement feature B ─┼─> Integration
└─ Agent a3: Implement feature C ─┘
```

### Pattern 4: Pipeline

Good for: Sequential transformation

```
Research Agent ─> Design Agent ─> Implementation Agent ─> Review Agent
```

## Agent Types

| Type | Purpose | Tools |
|------|---------|-------|
| **Explore** | Find files, understand structure | Glob, Grep, Read |
| **Research** | Gather information, compare options | WebSearch, WebFetch, Read |
| **Implement** | Write code, make changes | Edit, Write, Bash |
| **Review** | Check quality, security, tests | Read, Grep, Bash |

## Skill Chaining

### With TDD

Implementation agents should follow TDD:
1. Write failing test
2. Implement to pass
3. Refactor

### With doc-maintenance

After all agents complete:
1. Update PLAN.md with completed tasks
2. Add discovered work to backlog

### With research-to-plan

Research agents output feeds into planning:
1. Research agents gather information
2. research-to-plan converts to executable plan

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "I'll do it sequentially" | Wastes time on independent tasks | Parallelize |
| "Context is in my head" | Other agents can't read minds | Document in AGENTS.md |
| "Results are obvious" | Future reference needs explicit record | Write it down |
| "Dependencies are clear" | Implicit dependencies cause bugs | Document explicitly |

## Example Session

```
/agent-orchestration "Add OAuth authentication"

Analyzing task...

Identified subtasks:
1. Research OAuth providers (independent)
2. Explore existing auth code (independent)
3. Review security requirements (independent)
4. Implement OAuth (depends on 1, 2, 3)
5. Write tests (depends on 4)

Parallelization plan:

Phase 1 (parallel):
  - a1: Research providers
  - a2: Explore auth code
  - a3: Review requirements

Phase 2 (sequential):
  - a4: Implementation (after phase 1)
  - a5: Tests (after a4)

Launch phase 1? [y/n]
```

## Notes

- Maximum 5 parallel agents recommended
- Each agent should have clear, bounded scope
- Use AGENTS.md for all context handoff
- Prefer explicit over implicit dependencies
- Document agent outputs even if "obvious"

## References

For detailed guidance, see:
- [context-handoff.md](references/context-handoff.md) - Agent communication patterns
- [parallel-patterns.md](references/parallel-patterns.md) - When to parallelize
