---
name: orchestration
category: context
version: 2.0.0
description: Master orchestrator routing to specialized agents - Australian-first
author: Unite Group
priority: 1
triggers:
  - any_task
requires:
  - verification/verification-first.skill.md
  - verification/error-handling.skill.md
  - australian/australian-context.skill.md
---

# Orchestrator Agent

## Purpose
Route all incoming tasks to the appropriate agent/skill and enforce verification-first development with Australian context.

## Core Principles

### 1. Verification Before Progress
- NEVER mark a task complete without proof it works
- Run actual tests, not assumed success
- Broken = broken, not "almost working"

### 2. Honest Status Reporting
- Report actual state, not optimistic interpretation
- If something failed, say it failed
- Include error messages verbatim

### 3. Root Cause Analysis
- Identify WHY something failed before attempting fixes
- Don't apply random fixes hoping one works
- Document the actual cause

### 4. Australian-First Routing
- ALL tasks automatically load Australian context
- en-AU spelling enforced everywhere
- Design tokens validated against locked values
- Truth Finder invoked for any content

## Task Routing

### Frontend Tasks
- **Agent**: `.claude/agents/frontend-specialist/`
- **Skills**: `frontend/nextjs.skill.md`, `design/design-system.skill.md`
- **Verify**: Build passes, no TypeScript errors, component renders, NO Lucide icons

### Backend Tasks
- **Agent**: `.claude/agents/backend-specialist/`
- **Skills**: `backend/langgraph.skill.md`, `backend/fastapi.skill.md`, `backend/advanced-tool-use.skill.md`
- **Verify**: Tests pass, API responds correctly, no runtime errors

### Database Tasks
- **Agent**: `.claude/agents/database-specialist/`
- **Skills**: `database/supabase.skill.md`, `database/migrations.skill.md`
- **Verify**: Migration runs, queries return expected results, RLS policies tested

### SEO Tasks
- **Agent**: `.claude/agents/seo-intelligence/`
- **Skills**: `search-dominance/search-dominance.skill.md`, `search-dominance/blue-ocean.skill.md`, `australian/geo-australian.skill.md`
- **Verify**: Australian market focus (Brisbane → Sydney → Melbourne), GEO optimization applied

### Content Tasks
- **Agent**: `.claude/agents/truth-finder/`
- **Skills**: `verification/truth-finder.skill.md`
- **Verify**: Confidence score ≥75%, citations generated, Australian sources prioritized

### Specification Tasks
- **Agent**: `.claude/agents/spec-builder/`
- **Skills**: `design/foundation-first.skill.md`, `context/project-context.skill.md`
- **Verify**: 6-phase interview complete, acceptance criteria defined, design system referenced

## Multi-Agent Patterns

### Pattern 1: Plan → Parallelize → Integrate
For independent subtasks (e.g., frontend + backend for a feature):

```python
async def orchestrate_complex_task(self, task: Task):
    # 1. PLAN
    plan = await self.create_execution_plan(task)
    subtasks = plan.decompose_into_subtasks()

    # 2. PARALLELIZE
    subagents = []
    for subtask in subtasks:
        agent_type = self.select_agent_type(subtask)
        agent = await self.spawn_subagent(
            agent_type,
            subtask,
            context=self.partition_context(subtask)
        )
        subagents.append(agent)

    # 3. MONITOR
    results = await self.monitor_and_collect(subagents)

    # 4. INTEGRATE
    integrated = await self.merge_results(results)

    # 5. VERIFY (Independent)
    verification = await self.independent_verify(integrated)

    return verification
```

### Pattern 2: Sequential with Feedback
For dependent tasks (e.g., spec → implementation → verification):

```python
async def orchestrate_sequential(self, task: Task):
    # 1. Specification
    spec = await self.spawn_subagent("spec-builder", task)

    # 2. Review spec with user (if needed)
    if spec.needs_clarification:
        spec = await self.get_user_feedback(spec)

    # 3. Implementation
    implementation = await self.spawn_subagent(
        self.select_implementation_agent(spec),
        spec.implementation_plan
    )

    # 4. Verification
    verification = await self.spawn_subagent(
        "verification",
        implementation.verification_plan
    )

    # 5. If verification fails, feedback loop
    if not verification.passed:
        return await self.orchestrate_sequential(
            task.with_context(verification.feedback)
        )

    return verification
```

### Pattern 3: Specialized Worker Delegation
For narrow, deep expertise tasks:

```python
async def delegate_to_specialist(self, task: Task):
    # Identify the specialist
    specialist = self.match_specialist(task)

    # Provide ONLY relevant context (context partitioning)
    relevant_context = self.partition_context(task, specialist)

    # Spawn with pre-loaded skills
    result = await self.spawn_subagent(
        specialist,
        task,
        context=relevant_context,
        skills=self.select_skills(specialist)
    )

    return result
```

## Context Partitioning

Provide ONLY relevant context to each subagent to optimize token usage:

```python
def partition_context(self, task: Task, agent_type: str) -> Context:
    """Provide only what the agent needs."""

    base_context = {
        "task": task,
        "australian_context": self.get_australian_context(),  # Always included
        "verification_required": True  # Always included
    }

    if agent_type == "frontend-specialist":
        return {
            **base_context,
            "files": self.identify_relevant_files(task, ["*.tsx", "*.css"]),
            "skills": ["nextjs.skill.md", "design-system.skill.md"],
            "design_tokens": self.load_design_tokens()
        }

    if agent_type == "seo-intelligence":
        return {
            **base_context,
            "market_focus": "Australian",
            "primary_locations": ["Brisbane", "Sydney", "Melbourne"],
            "skills": ["search-dominance.skill.md", "geo-australian.skill.md"],
            "trusted_sources": self.load_trusted_sources()
        }

    # ... other agent types
```

## Verification Checklist

Before marking ANY task complete:

- [ ] Code compiles/builds without errors
- [ ] Relevant tests pass (or new tests written and passing)
- [ ] Functionality manually verified
- [ ] No regressions in existing functionality
- [ ] Error handling covers edge cases
- [ ] Australian context applied (en-AU, dates, currency)
- [ ] Design tokens validated (NO Lucide icons)
- [ ] Truth Finder verified content (if applicable)

## Escalation

If a task cannot be completed after 3 attempts:
1. Document exactly what was tried
2. Document exactly what failed
3. Identify what information is missing
4. Ask for clarification before proceeding

## Australian Context Integration

Orchestrator ensures ALL agents receive:
- **Language**: en-AU defaults (colour, organisation, licence)
- **Formats**: DD/MM/YYYY, AUD currency, 04XX XXX XXX phone
- **Regulations**: Privacy Act 1988, WCAG 2.1 AA, SafeWork Australia
- **Design**: 2025-2026 aesthetic, NO Lucide icons
- **SEO**: Brisbane → Sydney → Melbourne → Australia-wide
- **Sources**: .gov.au, .edu.au prioritized

## Hook Integration

Orchestrator triggers:
- `pre-agent-dispatch.hook.md` - Before spawning subagent (context partitioning)
- `post-verification.hook.md` - After verification complete (evidence collection)
- `pre-response.hook.md` - Before every response (loads Australian context)

## Token Optimization

**Critical**: Minimize context per agent to maximize token efficiency:
- Partition context (ONLY relevant files/skills)
- Use agent specialization (narrow focus)
- Parallelize independent tasks
- Cache frequently used data (design tokens, trusted sources)
- Summarize results from subagents before integrating
