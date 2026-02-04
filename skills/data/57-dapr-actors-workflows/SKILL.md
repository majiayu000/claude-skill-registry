---
sidebar_position: 20
title: "Finalize Your Dapr Skill"
description: "Complete your dapr-deployment skill with actor and workflow patterns, validate code generation, and document your Digital FTE component"
keywords: [dapr, skill finalization, actors, workflows, validation, digital fte, dapr-deployment, production skill]
chapter: 57
lesson: 20
duration_minutes: 20

skills:
  - name: "Skill Validation"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "Problem Solving"
    measurable_at_this_level: "Validates skill output against correctness criteria"
  - name: "Skill Documentation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Content Creation"
    measurable_at_this_level: "Documents skill capabilities and improvement history"
  - name: "Digital FTE Component Design"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Create"
    digcomp_area: "Problem Solving"
    measurable_at_this_level: "Packages skill as reusable Digital FTE component"

learning_objectives:
  - objective: "Validate that extended skill generates correct actor and workflow code"
    proficiency_level: "B1"
    bloom_level: "Evaluate"
    assessment_method: "Generated code passes type checking and runtime tests"
  - objective: "Document skill improvements and decision frameworks"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "SKILL.md contains comprehensive actor/workflow patterns"
  - objective: "Package skill as a Digital FTE component for reuse"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Skill directory structure follows conventions"

cognitive_load:
  new_concepts: 3
  assessment: "Within B1 limit - focuses on skill validation, documentation, and packaging"

differentiation:
  extension_for_advanced: "Add multi-app workflow patterns and namespaced actor configurations"
  remedial_for_struggling: "Focus on core actor and workflow validation only"
---

# Finalize Your Dapr Skill

You started Chapter 59 by extending your `dapr-deployment` skill with actor and workflow patterns. Over 19 lessons, you learned virtual actors with state management and turn-based concurrency, durable workflows with activities and retry policies, and production patterns like sagas, multi-app orchestration, and namespace isolation.

Each lesson added knowledge to your skill. Each "Reflect on Your Skill" section tested whether your skill captured that knowledge correctly. Now it is time to finalize: validate everything works, document what your skill knows, and package it as a production-ready Digital FTE component.

This matters because your skill is not just for learning. It is a sellable asset. A properly validated and documented skill can generate correct Dapr code for any team member, any project, any client. The twenty minutes you spend here transform accumulated knowledge into lasting organizational capability.

---

## The Skill Finalization Process

Skill finalization has three phases:

| Phase | Purpose | Output |
|-------|---------|--------|
| **Validation** | Confirm skill generates correct code | Test results showing pass/fail |
| **Documentation** | Record what skill knows and decisions it makes | Updated SKILL.md |
| **Packaging** | Structure skill for reuse and sharing | Clean directory with conventions |

Each phase builds on the previous. You cannot document what you have not validated. You cannot package what you have not documented.

---

## Phase 1: Validation

Your skill must generate correct code for both actors and workflows. Test it systematically.

### Test 1: Actor Code Generation

Ask your skill to generate a TaskActor with the patterns you learned:

```
Using my dapr-deployment skill, generate a TaskActor with:
1. State management using StateManager (get_state, set_state, try_get_state)
2. A deadline reminder that marks the task overdue after expiration
3. Turn-based concurrency guarantees
4. Proper lifecycle hooks (_on_activate, _on_deactivate)
```

**Validation criteria:**

- [ ] Uses `ActorInterface` with `@actormethod` decorators
- [ ] Uses `Actor` base class with `TaskActorInterface`
- [ ] Implements `_on_activate` with `try_get_state` for initialization
- [ ] Uses `register_reminder` (not timer) for deadline
- [ ] Implements `receive_reminder` callback
- [ ] State keys are consistent (e.g., `f"task_data_{self.id.id}"`)

**Example of correct output structure:**

```python
from dapr.actor import ActorInterface, actormethod, Actor, ActorId
from dapr.actor.runtime.context import ActorRuntimeContext
from datetime import datetime, timedelta

class TaskActorInterface(ActorInterface):
    @actormethod(name="GetTask")
    async def get_task(self) -> dict: ...

    @actormethod(name="UpdateStatus")
    async def update_status(self, status: str) -> None: ...

    @actormethod(name="SetDeadlineReminder")
    async def set_deadline_reminder(self, seconds: int) -> None: ...

class TaskActor(Actor, TaskActorInterface):
    def __init__(self, ctx: ActorRuntimeContext, actor_id: ActorId):
        super().__init__(ctx, actor_id)
        self._state_key = f"task_data_{actor_id.id}"

    async def _on_activate(self) -> None:
        found, _ = await self._state_manager.try_get_state(self._state_key)
        if not found:
            await self._state_manager.set_state(self._state_key, {
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            })

    async def set_deadline_reminder(self, seconds: int) -> None:
        await self.register_reminder(
            reminder_name="deadline",
            state=b'{}',
            due_time=timedelta(seconds=seconds),
            period=timedelta(seconds=0)
        )

    async def receive_reminder(self, name: str, state: bytes,
                               due_time: timedelta, period: timedelta) -> None:
        if name == "deadline":
            await self.update_status("overdue")
```

If your skill generates code missing any criteria, note the gap for documentation.

### Test 2: Workflow Code Generation

Ask your skill to generate a TaskProcessingWorkflow:

```
Using my dapr-deployment skill, generate a TaskProcessingWorkflow with:
1. Three chained activities: validate_task, assign_task, notify_assignee
2. Retry policy on assign_task (3 attempts, exponential backoff)
3. WorkflowRuntime setup with FastAPI lifespan
4. Proper determinism (no datetime.now() in workflow code)
```

**Validation criteria:**

- [ ] Uses `yield ctx.call_activity()` pattern (not async/await)
- [ ] Dataclass inputs and outputs for type safety
- [ ] `RetryPolicy` with `max_attempts`, `initial_interval`, `backoff_coefficient`
- [ ] Activities can use `datetime.now()` (non-deterministic operations)
- [ ] Workflow uses `ctx.current_utc_datetime` if time is needed
- [ ] `WorkflowRuntime` with `register_workflow` and `register_activity`
- [ ] `lifespan` context manager calling `start()` and `shutdown()`

**Example of correct output structure:**

```python
import dapr.ext.workflow as wf
from dataclasses import dataclass
from datetime import timedelta
from contextlib import asynccontextmanager
from fastapi import FastAPI

@dataclass
class TaskOrder:
    task_id: str
    title: str
    assignee: str

@dataclass
class TaskResult:
    task_id: str
    status: str

def task_processing_workflow(ctx: wf.DaprWorkflowContext, order: TaskOrder):
    # Step 1: Validate
    validation = yield ctx.call_activity(validate_task, input=order)
    if not validation["valid"]:
        return TaskResult(order.task_id, "rejected")

    # Step 2: Assign with retry
    yield ctx.call_activity(
        assign_task,
        input=order,
        retry_policy=wf.RetryPolicy(
            max_attempts=3,
            initial_interval=timedelta(seconds=1),
            backoff_coefficient=2.0
        )
    )

    # Step 3: Notify
    yield ctx.call_activity(notify_assignee, input=order)

    return TaskResult(order.task_id, "completed")

def validate_task(ctx, order: TaskOrder) -> dict:
    from datetime import datetime
    return {"valid": True, "validated_at": datetime.utcnow().isoformat()}

# ... more activities ...

workflow_runtime = wf.WorkflowRuntime()
workflow_runtime.register_workflow(task_processing_workflow)
workflow_runtime.register_activity(validate_task)
workflow_runtime.register_activity(assign_task)
workflow_runtime.register_activity(notify_assignee)

@asynccontextmanager
async def lifespan(app: FastAPI):
    workflow_runtime.start()
    yield
    workflow_runtime.shutdown()
```

### Test 3: Decision Framework

Ask your skill to explain when to use actors vs workflows:

```
Using my dapr-deployment skill, explain when I should use a Dapr actor vs a Dapr workflow for:
1. A chat agent maintaining conversation history
2. An order processing pipeline
3. A notification scheduler
```

**Validation criteria:**

- [ ] Recommends actor for chat agent (stateful entity with identity, turn-based concurrency)
- [ ] Recommends workflow for order processing (multi-step, compensation, durable)
- [ ] Discusses both options for notification scheduler with tradeoffs
- [ ] References the decision table from the skill

**Example of correct reasoning:**

| Use Case | Recommendation | Rationale |
|----------|----------------|-----------|
| Chat agent | **Actor** | Each user is a stateful entity needing isolated state and turn-based concurrency |
| Order processing | **Workflow** | Multi-step process requiring durability, retry, and compensation (saga) |
| Notification scheduler | **Depends** | Actor reminder if tied to entity; workflow if orchestrating multiple notifications |

Record any gaps in decision framework reasoning.

---

## Phase 2: Documentation

Update your skill with what you learned and validated. Open your skill file:

```bash
code .claude/skills/dapr-deployment/SKILL.md
```

### Document Capabilities

Add or update this section at the end of your skill:

```markdown
## Capabilities Summary (Chapter 59)

This skill now knows:

### Actors
- Actor interface definition with `@actormethod` decorators
- Actor implementation with `StateManager` for persistent state
- Lifecycle hooks: `_on_activate`, `_on_deactivate`
- Timers (non-persistent) vs Reminders (persistent, survives restart)
- Actor registration with `DaprActor(app)` and `register_actor`
- Actor invocation with `ActorProxy.create`
- Actor-to-actor communication patterns
- Event-driven actors with pub/sub integration
- Observability with Zipkin/Jaeger tracing

### Workflows
- Workflow definition with `yield ctx.call_activity()` pattern
- Activity definitions (can be non-deterministic)
- `WorkflowRuntime` setup with FastAPI lifespan
- Workflow management: start, query, raise events, terminate
- Patterns: chaining, fan-out/fan-in, saga, monitor
- Determinism rules (what's safe in workflows vs activities)
- External events with `wait_for_external_event`
- Retry policies with exponential backoff

### Production Patterns
- Actors vs workflows decision framework
- Multi-app workflows with `app_id` parameter
- Namespaced actors for multi-tenant isolation
- State encryption and mTLS security
- Combined actor + workflow architectures
```

### Document Decision Frameworks

Add the decision trees your skill uses:

```markdown
## Decision Frameworks

### When to Use Actors vs Workflows

```
Question: Does the entity need identity and isolated state?
├── Yes → Consider Actor
│   └── Question: Does it need timers or reminders on the entity?
│       ├── Yes → Actor (with reminders for durable scheduling)
│       └── No → Actor may still be best for turn-based concurrency
└── No → Consider Workflow
    └── Question: Is this a multi-step process?
        ├── Yes → Workflow (with activities for each step)
        └── No → Neither (simple service method)

Question: Does the process need to survive failures?
├── Yes → Workflow (durable execution)
└── No → Actor method or service call

Question: Does the process need compensation/rollback?
├── Yes → Workflow with saga pattern
└── No → Either could work
```

### When to Use Timers vs Reminders

```
Question: Must the scheduled work survive pod restart?
├── Yes → Reminder (persistent)
└── No → Timer (non-persistent, lower resource cost)

Question: Is this a one-time or recurring schedule?
├── One-time → Either (set period=0 for reminders)
└── Recurring → Reminder (reliable recurrence)
```
```

### Document Known Limitations

Honesty about what your skill does NOT know:

```markdown
## Known Limitations

This skill does NOT currently know:
- Actor reentrancy configuration (advanced concurrency control)
- Workflow versioning strategies (for updating running workflows)
- Custom serialization for complex state types
- Placement service affinity hints
- State store encryption configuration details

For these patterns, consult official Dapr documentation or extend this skill.
```

---

## Phase 3: Packaging

Structure your skill for reuse and sharing.

### Verify Directory Structure

Your skill directory should follow conventions:

```
.claude/skills/dapr-deployment/
├── SKILL.md              # Main skill document (updated)
├── LEARNING-SPEC.md      # What skill learned (from L00)
├── references/
│   ├── actors.md         # Actor API reference
│   └── workflows.md      # Workflow API reference
└── examples/
    ├── task-actor.py     # Complete TaskActor example
    └── task-workflow.py  # Complete TaskProcessingWorkflow example
```

### Create Validation Checklist

Add a checklist for future validation:

```bash
touch .claude/skills/dapr-deployment/VALIDATION-CHECKLIST.md
```

```markdown
# Dapr Deployment Skill Validation Checklist

Run these tests before considering the skill production-ready:

## Actor Validation
- [ ] Generate TaskActor with state management
- [ ] Verify @actormethod decorator names match interface
- [ ] Verify StateManager patterns (try_get_state for init)
- [ ] Verify reminder registration (not timer for persistent scheduling)
- [ ] Verify receive_reminder callback exists

## Workflow Validation
- [ ] Generate workflow with 3+ chained activities
- [ ] Verify yield ctx.call_activity pattern (not await)
- [ ] Verify retry policy syntax
- [ ] Verify activities can use datetime.now()
- [ ] Verify workflow does NOT use datetime.now()
- [ ] Verify WorkflowRuntime lifespan integration

## Decision Framework Validation
- [ ] Actor recommendation for stateful entities
- [ ] Workflow recommendation for orchestration
- [ ] Correct timer vs reminder guidance
- [ ] Combined architecture reasoning

## Generated Code Quality
- [ ] Imports are correct and complete
- [ ] Type hints present throughout
- [ ] No hallucinated APIs
- [ ] Code matches official Dapr Python SDK

Last validated: [DATE]
Validated by: [NAME]
```

### Tag Your Skill Version

If using version control for your skills:

```bash
cd .claude/skills/dapr-deployment
git add .
git commit -m "feat: finalize dapr-deployment skill with Ch59 patterns"
git tag v2.0.0  # Major version for significant capability addition
```

---

## Your Production-Ready Digital FTE Component

Your `dapr-deployment` skill is now a production-ready Digital FTE component. Here is what it provides:

| Capability | Business Value |
|------------|----------------|
| **Actor Code Generation** | Any team member can generate correct actor code for stateful services |
| **Workflow Code Generation** | Durable orchestration patterns available without deep Dapr expertise |
| **Decision Frameworks** | Consistent architectural decisions across projects |
| **Validated Patterns** | Patterns tested against official SDK, reducing bugs |
| **Documented Limitations** | Clear boundaries prevent misuse |

This skill can now be:
- **Shared** with teammates who need Dapr capabilities
- **Composed** with other skills for larger agent architectures
- **Monetized** as part of a consulting offering or SaaS product

You built this skill through structured learning: specification first, official documentation research, progressive enhancement through lessons, and systematic validation at the end.

---

## Reflect on Your Skill Journey

Look back at Chapter 59:

**L00**: You wrote LEARNING-SPEC.md defining what your skill should learn. That specification guided everything.

**L01-L08**: You learned actor patterns. Each lesson added knowledge: actor model, interfaces, state management, timers, reminders, communication, events, observability.

**L09-L14**: You learned workflow patterns. Each lesson added knowledge: durable execution, determinism, authoring, managing, chaining, fan-out, saga, monitor.

**L15-L18**: You learned production patterns. Each lesson added knowledge: combining actors with workflows, multi-app orchestration, namespaced isolation, security.

**L19**: You built a complete system integrating everything. The capstone validated your accumulated knowledge.

**L20**: You finalized the skill, validating that it captures all this knowledge correctly.

This is the Skill-First pattern in action. You did not just learn Dapr actors and workflows. You built a reusable asset that encodes that knowledge for future use.

---

## Try With AI

Now practice skill validation and refinement with AI collaboration.

### Prompt 1: Gap Analysis

```
I've finalized my dapr-deployment skill for Chapter 59.
Review my skill's actor patterns against the official Dapr Python SDK documentation.

Identify any gaps:
1. Patterns that are missing or incomplete
2. API signatures that may be outdated
3. Best practices from docs not captured in skill

Use /fetching-library-docs for dapr-ext-fastapi to get current documentation.
```

**What you're learning:** Using AI to audit your skill against authoritative sources. Your skill may have gaps you did not notice during lesson-by-lesson building. A systematic review catches them.

### Prompt 2: Edge Case Testing

```
Test my dapr-deployment skill with edge cases:

1. "Generate an actor that needs to call another actor and handle timeout."
2. "Generate a workflow with fan-out to 100 items but only 10 should run in parallel."
3. "Generate a workflow that waits for approval but the approver might be a different service."

For each, evaluate whether my skill generates correct, production-ready code.
```

**What you're learning:** Pushing your skill beyond the standard patterns to see where it breaks. Edge cases reveal whether your skill truly understands the patterns or just memorized examples.

### Prompt 3: Skill Portfolio Integration

```
I have these skills in my portfolio:
- dapr-deployment (actors, workflows, state, pub/sub)
- fastapi-agent-api (REST endpoints, Pydantic models)
- helm-chart-architect (Kubernetes deployments)

Design how these skills should compose for building a complete AI agent platform.
What's the interface between them? What shared conventions do they need?
```

**What you're learning:** Skills are not isolated. They compose into larger capabilities. Understanding composition patterns prepares you for building complete Digital FTEs that use multiple skills together.

**Safety Note:** When finalizing skills, always validate against official documentation before marking production-ready. Skills built from AI memory may contain subtle errors that compound over time. Use `/fetching-library-docs` to verify patterns against authoritative sources.
