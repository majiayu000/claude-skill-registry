---
name: task-router
description: Automatically analyze tasks and route to optimal agent(s). Use when receiving complex requests to determine which agents to spawn.
---

# Task Router

<!-- Version: 1.1.0 | Last Updated: 2026-01-11 -->

Intelligent routing skill that analyzes user requests and determines optimal agent dispatch.

## Purpose

Reduce orchestrator cognitive load by automatically:
1. Inferring user intent (via `/infer-intent`)
2. Classifying task type and complexity
3. Identifying required agent(s)
4. Detecting parallelization opportunities
5. Recommending model tier per agent

## Integrated Workflow

```
User Request
     │
     ▼
┌─────────────────┐
│  /infer-intent  │ ← Step 0: Understand what user wants
└────────┬────────┘
         │ Intent Summary (YAML)
         ▼
┌─────────────────┐
│  /task-router   │ ← This skill: Route to agents
└────────┬────────┘
         │ Dispatch Plan
         ▼
    Execute Plan
```

## When to Use

- At the start of any non-trivial task
- When uncertain which agent(s) to spawn
- Before spawning multiple agents (to optimize parallelization)
- **Automatically invoked by /infer-intent for complex tasks**

## Routing Process

### Step 1: Task Classification

Classify the request into categories:

| Category | Signals | Primary Agent |
|----------|---------|---------------|
| **UI/Frontend** | component, styling, page, view, layout, responsive | Frontend Agent |
| **Backend/API** | server action, API, database, RLS, migration | Backend Agent |
| **Exploration** | where, how, find, trace, understand | Research Agent |
| **Documentation** | invariants, constraints, features, coupling | Doc Agent |
| **Testing** | test, verify, validate, check, QA | Test Agent |
| **Architecture** | design, refactor, structure, pattern | Architect Agent |
| **Security** | auth, permissions, RLS, vulnerability | Security Agent |
| **System** | optimize, improve, process, agent | Ops Agent |

### Step 2: Complexity Assessment

Score task complexity (1-10):

| Factor | Points |
|--------|--------|
| Touches 1 feature | +1 |
| Touches 2-3 features | +3 |
| Touches 4+ features | +5 |
| Database/schema changes | +2 |
| Auth/RLS involved | +2 |
| AI/context involved | +2 |
| Billing involved | +3 |
| New feature (not bugfix) | +1 |
| User workflow change | +2 |

**Complexity Levels**:
- 1-3: Simple (may not need agent)
- 4-6: Moderate (single agent)
- 7-9: Complex (multiple agents, sequential)
- 10+: Critical (multiple agents, Doc Agent required)

### Step 3: Parallelization Detection

Tasks can run in parallel when:
- [ ] No data dependencies between tasks
- [ ] Different domains (frontend vs backend)
- [ ] Independent bug fixes
- [ ] Research across different features

Tasks must be sequential when:
- [ ] API contract needed before frontend
- [ ] Schema needed before server actions
- [ ] Tests depend on implementation
- [ ] Security review before deployment

### Step 4: Model Recommendation

| Complexity | Agent Type | Recommended Model |
|------------|------------|-------------------|
| Simple | Research | `haiku` |
| Simple | Any other | `sonnet` |
| Moderate | Implementation | `sonnet` |
| Moderate | Review/Audit | `opus` |
| Complex | Any | `opus` |
| Critical | Any | `opus` |

## Output Format

```markdown
## Task Routing Analysis

### Classification
- **Primary Type**: [category]
- **Secondary Types**: [if multi-domain]
- **Complexity Score**: [N]/10 ([level])

### Agent Dispatch Plan

| Order | Agent | Model | Task |
|-------|-------|-------|------|
| 1 | [agent] | [model] | [specific task] |
| 2 | [agent] | [model] | [specific task] |

### Parallelization
- **Can Parallelize**: [Yes/No]
- **Parallel Groups**: [if yes, which agents can run together]
- **Dependencies**: [what must complete before what]

### Recommendation
[1-2 sentence summary of recommended approach]
```

## Quick Routing Table

| Request Pattern | Route To |
|-----------------|----------|
| "Add/create component..." | Frontend Agent |
| "Fix the button/card/modal..." | Frontend Agent |
| "Create server action..." | Backend Agent |
| "Add RLS policy..." | Backend Agent |
| "Where is X implemented?" | Research Agent |
| "How does Y work?" | Research Agent |
| "What are the invariants for..." | Doc Agent |
| "Test the..." | Test Agent |
| "Refactor/redesign..." | Architect Agent |
| "Review security of..." | Security Agent |
| "Optimize the system..." | Ops Agent |

## Integration

After routing, spawn agents using:
- `/spawn-frontend-agent`
- `/spawn-backend-agent`
- `/spawn-research-agent`
- `/spawn-doc-agent`
- `/spawn-test-agent`
- `/spawn-architect-agent`
- `/spawn-security-agent`
- `/spawn-ops-agent`

For parallel dispatch, use `/parallel-agents` with the routing analysis.

## Intent-Aware Routing

When `/infer-intent` provides an intent summary, use it to enhance routing:

### Using Intent Summary

If intent summary is available:

```yaml
# From /infer-intent
intent:
  primary: create
  secondary: [modify]
scope:
  level: cross-cutting
  domains: [frontend, backend]
complexity:
  score: 7
agents:
  primary: architect-agent
  supporting: [backend-agent, frontend-agent]
  parallel_possible: false
routing:
  recommended_flow: 2-gate
```

Map directly to dispatch plan:

```markdown
### Agent Dispatch Plan

| Order | Agent | Model | Task |
|-------|-------|-------|------|
| 1 | architect-agent | opus | Design system architecture |
| 2 | backend-agent | opus | Implement server-side |
| 2 | frontend-agent | sonnet | Implement UI (parallel with backend if disjoint) |
| 3 | test-agent | sonnet | Verify complete flow |
```

### Without Intent Summary

If no intent summary provided, run the full routing process (Steps 1-4 above).

## Quick Reference

See `.claude/agents/AGENT_INVENTORY.md` for:
- Complete agent profiles and capabilities
- Model selection guide
- Parallel agent patterns
- Decision tree for agent selection
- Cost optimization strategies

## Related Skills

| Skill | Purpose | When to Chain |
|-------|---------|---------------|
| `/infer-intent` | Understand user request | Before routing |
| `/parallel-dispatch` | Execute parallel agents | After routing identifies parallelization |
| `/doc-discovery` | Load feature context | For complexity >= 7 |
| `/plan-lint` | Validate plan | Before implementation
