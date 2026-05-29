---
sidebar_position: 0
title: "Extend Your Dapr Skill"
description: "Extend your existing Dapr skill with actor and workflow patterns using official documentation"
keywords: [dapr, actors, workflows, skill extension, virtual actors, durable execution, python sdk]
chapter: 57
lesson: 0
duration_minutes: 25

skills:
  - name: "Skill Extension"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Problem Solving"
    measurable_at_this_level: "Extends existing skill with new capabilities from official docs"
  - name: "Actor Pattern Recognition"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Identifies when to use actors vs workflows"
  - name: "Documentation Research"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Uses /fetching-library-docs to retrieve SDK documentation"

learning_objectives:
  - objective: "Write a LEARNING-SPEC.md that defines goals for actor and workflow extension"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Review of specification document"
  - objective: "Extend existing skill with actor interface patterns from official docs"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill generates valid actor code"
  - objective: "Add WorkflowRuntime setup patterns to skill knowledge base"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill generates valid workflow code"

cognitive_load:
  new_concepts: 2
  assessment: "Within B1 limit - focuses on skill extension workflow, not new technical depth"

differentiation:
  extension_for_advanced: "Extend skill to handle multi-app workflows and namespaced actors"
  remedial_for_struggling: "Focus only on actor patterns, add workflows in later iteration"
---

# Extend Your Dapr Skill

In Chapter 53, you built a `dapr-deployment` skill that understands sidecar architecture, state management, pub/sub, and service invocation. That skill can generate code for stateless microservices. But your AI agents need more.

Consider a chat agent that maintains conversation history for thousands of concurrent users. Each user needs isolated state, and you want state to persist even when pods restart. Or consider an order processing workflow that must survive failures, retry automatically, and rollback gracefully if payment fails.

These patterns require two advanced Dapr building blocks: **Actors** for stateful entities with identity, and **Workflows** for durable orchestration. Your current skill does not know these patterns.

This lesson extends your Dapr skill with actor and workflow capabilities. You will write a specification defining what your skill should learn, fetch official documentation using `/fetching-library-docs`, and update your skill with production-ready patterns. By the end, your skill will generate actor interfaces, workflow definitions, and runtime setup code grounded in official Dapr documentation rather than memory.

---

## Why Skill-First for Actors and Workflows

The traditional approach would be: read about actors, try some code, maybe build something, and later codify what you learned. The problem? By "later," you have forgotten the nuances, and your skill ends up with hallucinated patterns.

The Skill-First approach inverts this:

1. **Specification**: Define what your skill should know BEFORE learning
2. **Research**: Fetch official documentation as the authoritative source
3. **Extension**: Add patterns grounded in verified documentation
4. **Validation**: Test that your skill generates correct code

This ensures your skill contains accurate, production-ready patterns from day one. Every lesson in this chapter will test and improve this skill, so the investment compounds.

---

## Step 1: Clone Skills-Lab Fresh

Start with a clean environment. Your skills-lab may have accumulated state from previous chapters.

```bash
# Navigate to your workspace
cd ~/workspace

# Remove existing skills-lab if present
rm -rf skills-lab

# Clone fresh
git clone https://github.com/your-username/skills-lab.git
cd skills-lab
```

**Why fresh clone?** Skills accumulate context. If your previous skill had errors, they propagate. A fresh clone ensures you start from known-good state.

Verify your existing Dapr skill exists:

```bash
ls -la .claude/skills/
```

**Expected output:**
```
drwxr-xr-x  5 user  staff  160 Dec 29 10:00 .
drwxr-xr-x  3 user  staff   96 Dec 29 10:00 ..
drwxr-xr-x  4 user  staff  128 Dec 29 10:00 dapr-deployment
```

If `dapr-deployment` does not exist, you need to complete Chapter 53 first. This lesson assumes you have the base skill from that chapter.

---

## Step 2: Write LEARNING-SPEC.md

Before extending your skill, write a specification that defines exactly what it should learn. This prevents scope creep and ensures focused improvement.

Create `LEARNING-SPEC.md` in your skill directory:

```bash
touch .claude/skills/dapr-deployment/LEARNING-SPEC.md
```

Write the specification:

```markdown
# LEARNING-SPEC: Dapr Actors & Workflows Extension

## Intent

Extend the dapr-deployment skill to generate code for:
1. Virtual actors with state management, timers, and reminders
2. Durable workflows with activities, retry policies, and external events

## Current Skill Capabilities (from Ch53)

- Dapr sidecar architecture
- Service invocation with app-id
- State management with DaprClient
- Pub/sub messaging with CloudEvents
- Secrets retrieval from Kubernetes stores
- Kubernetes deployment with Dapr annotations

## New Capabilities to Add

### Actors

1. **Actor Interface Definition**
   - ABC base class pattern
   - @actormethod decorator with name parameter
   - Async method signatures

2. **Actor Implementation**
   - Extending Actor and interface classes
   - _on_activate and _on_deactivate lifecycle hooks
   - StateManager for persistent state (get_state, set_state, try_get_state)

3. **Actor Registration**
   - DaprActor(app) FastAPI extension
   - register_actor on startup
   - ActorRuntimeConfig for idle timeout

4. **Actor Invocation**
   - ActorProxy.create pattern
   - DaprClient.invoke_actor alternative

5. **Timers and Reminders**
   - register_timer (non-persistent)
   - register_reminder (persistent, survives restart)
   - receive_reminder callback

### Workflows

1. **Workflow Definition**
   - @wfr.workflow decorator
   - DaprWorkflowContext for orchestration
   - yield ctx.call_activity pattern

2. **Activity Definition**
   - @wfr.activity decorator
   - WorkflowActivityContext
   - Non-deterministic code allowed

3. **WorkflowRuntime Setup**
   - WorkflowRuntime() initialization
   - register_workflow and register_activity
   - FastAPI lifespan integration (start/shutdown)

4. **Workflow Client**
   - DaprWorkflowClient for management
   - schedule_new_workflow
   - get_workflow_state
   - raise_workflow_event
   - terminate_workflow

5. **Determinism Rules**
   - Use ctx.current_utc_datetime (not datetime.now())
   - No random, no direct HTTP calls in workflows
   - Activities handle non-deterministic operations

## Success Criteria

- [ ] Skill generates valid actor interface with @actormethod decorators
- [ ] Skill generates actor implementation with StateManager patterns
- [ ] Skill generates DaprActor registration code for FastAPI
- [ ] Skill generates workflow with 3+ chained activities
- [ ] Skill generates WorkflowRuntime setup with lifespan
- [ ] Skill explains when to use actors vs workflows
- [ ] Generated code passes type checking (mypy)

## Verification Prompts

Test the extended skill with these prompts:

1. "Using my dapr-deployment skill, generate a TaskActor that stores task state and has a deadline reminder."

2. "Using my dapr-deployment skill, generate a TaskProcessingWorkflow with validate, assign, and notify activities."

3. "When should I use a Dapr actor vs a Dapr workflow for stateful AI agents?"
```

This specification serves two purposes:
1. **Guides your research** - You know exactly what patterns to look for in the docs
2. **Defines done** - Clear criteria to validate your skill extension

---

## Step 3: Fetch Official Documentation

Now use `/fetching-library-docs` to retrieve the official Dapr Python SDK documentation. This ensures your skill is grounded in authoritative sources, not AI memory.

### Fetch Actor Documentation

```
/fetching-library-docs dapr-ext-fastapi actors
```

**What you're retrieving:**
- `dapr.actor.ActorInterface` - Base class for interfaces
- `dapr.actor.actormethod` - Decorator for actor methods
- `dapr.actor.Actor` - Base class for implementations
- `dapr.ext.fastapi.DaprActor` - FastAPI integration
- `dapr.actor.ActorProxy` - Client-side invocation

Review the output and note:
- The exact import paths
- Required method signatures
- Pattern for StateManager access
- Timer and reminder APIs

### Fetch Workflow Documentation

```
/fetching-library-docs dapr-ext-workflow
```

**What you're retrieving:**
- `dapr.ext.workflow.WorkflowRuntime` - Runtime management
- `dapr.ext.workflow.DaprWorkflowContext` - Orchestration context
- `dapr.ext.workflow.DaprWorkflowClient` - Client operations
- Activity definition patterns
- Retry policy configuration

Review the output and note:
- The yield-based execution model
- Activity registration patterns
- External event handling
- Determinism requirements

---

## Step 4: Update Your Skill with Actor Patterns

Open your skill file and add the actor knowledge section:

```bash
# Open your skill for editing
code .claude/skills/dapr-deployment/SKILL.md
```

Add this section to your skill (after the existing content):

```markdown
## Actors (Chapter 59)

### When to Use Actors

Use Dapr actors when you have:
- Stateful entities with identity (ChatActor per user, TaskActor per task)
- Need for turn-based concurrency (no race conditions)
- Timers or reminders on entities
- Virtual actor pattern (on-demand activation, garbage collection)

### Actor Interface Pattern

```python
from dapr.actor import ActorInterface, actormethod

class TaskActorInterface(ActorInterface):
    @actormethod(name="get_task")
    async def get_task(self) -> dict: ...

    @actormethod(name="update_status")
    async def update_status(self, status: str) -> None: ...

    @actormethod(name="set_deadline_reminder")
    async def set_deadline_reminder(self, seconds: int) -> None: ...
```

### Actor Implementation Pattern

```python
from dapr.actor import Actor
from dapr.actor.runtime.context import ActorRuntimeContext
from datetime import datetime, timedelta

class TaskActor(Actor, TaskActorInterface):
    def __init__(self, ctx: ActorRuntimeContext, actor_id: str):
        super().__init__(ctx, actor_id)
        self._state_manager = ctx.state_manager

    async def _on_activate(self) -> None:
        """Initialize state on activation."""
        found, state = await self._state_manager.try_get_state("task_data")
        if not found:
            await self._state_manager.set_state("task_data", {
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            })

    async def _on_deactivate(self) -> None:
        """Cleanup on deactivation."""
        pass

    async def get_task(self) -> dict:
        state = await self._state_manager.get_state("task_data")
        return {"id": self.id.id, **state}

    async def update_status(self, status: str) -> None:
        state = await self._state_manager.get_state("task_data")
        state["status"] = status
        state["updated_at"] = datetime.utcnow().isoformat()
        await self._state_manager.set_state("task_data", state)

    async def set_deadline_reminder(self, seconds: int) -> None:
        await self.register_reminder(
            reminder_name="deadline",
            state=b'{}',
            due_time=timedelta(seconds=seconds),
            period=timedelta(seconds=0)  # One-time
        )

    async def receive_reminder(self, name: str, state: bytes,
                               due_time: timedelta, period: timedelta) -> None:
        if name == "deadline":
            await self.update_status("overdue")
```

### Actor Registration Pattern

```python
from fastapi import FastAPI
from dapr.ext.fastapi import DaprActor
from dapr.actor.runtime.config import ActorRuntimeConfig
from dapr.actor.runtime.runtime import ActorRuntime

app = FastAPI()
dapr_actor = DaprActor(app)

# Configure runtime
config = ActorRuntimeConfig()
config.update_actor_idle_timeout(timedelta(minutes=10))
ActorRuntime.set_actor_config(config)

@app.on_event("startup")
async def startup():
    await dapr_actor.register_actor(TaskActor)
```

### Actor Invocation Pattern

```python
from dapr.actor import ActorProxy, ActorId

# Type-safe proxy
proxy = ActorProxy.create("TaskActor", ActorId("task-123"), TaskActorInterface)
task = await proxy.get_task()
await proxy.update_status("in_progress")
```
```

---

## Step 5: Update Your Skill with Workflow Patterns

Continue adding the workflow knowledge section:

```markdown
## Workflows (Chapter 59)

### When to Use Workflows

Use Dapr workflows when you have:
- Long-running orchestration (hours, days)
- Multi-step processes requiring durability
- Compensation/rollback requirements (saga pattern)
- Parallel task execution (fan-out/fan-in)

### Workflow Definition Pattern

```python
import dapr.ext.workflow as wf
from dataclasses import dataclass

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
    """Orchestrate task processing with activities."""

    # Step 1: Validate
    validation = yield ctx.call_activity(validate_task, input=order)
    if not validation["valid"]:
        return TaskResult(order.task_id, "rejected")

    # Step 2: Assign with retry
    assignment = yield ctx.call_activity(
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
```

### Activity Definition Pattern

```python
def validate_task(ctx, order: TaskOrder) -> dict:
    """Activities CAN be non-deterministic."""
    # Can call external APIs, use datetime.now(), etc.
    return {"valid": True, "validated_at": datetime.now().isoformat()}

def assign_task(ctx, order: TaskOrder) -> dict:
    return {"assigned": True, "assignee": order.assignee}

def notify_assignee(ctx, order: TaskOrder) -> None:
    # Can call notification service
    pass
```

### WorkflowRuntime Setup Pattern

```python
from dapr.ext.workflow import WorkflowRuntime, DaprWorkflowClient
from contextlib import asynccontextmanager

wfr = WorkflowRuntime()

# Register workflows and activities
wfr.register_workflow(task_processing_workflow)
wfr.register_activity(validate_task)
wfr.register_activity(assign_task)
wfr.register_activity(notify_assignee)

@asynccontextmanager
async def lifespan(app: FastAPI):
    wfr.start()
    yield
    wfr.shutdown()

app = FastAPI(lifespan=lifespan)

# Client for management
client = DaprWorkflowClient()
```

### Workflow Management Pattern

```python
# Start workflow
instance_id = client.schedule_new_workflow(
    workflow=task_processing_workflow,
    input=TaskOrder("task-123", "Review PR", "alice@example.com")
)

# Query status
state = client.get_workflow_state(instance_id)
print(f"Status: {state.runtime_status}")

# Raise external event
client.raise_workflow_event(
    instance_id=instance_id,
    event_name="approval_received",
    data={"approved": True}
)
```

### Determinism Rules (CRITICAL)

Workflows MUST be deterministic for replay to work.

**DO NOT use in workflows:**
```python
# WRONG - Non-deterministic
import random
value = random.randint(1, 100)

from datetime import datetime
now = datetime.utcnow()  # Use ctx.current_utc_datetime instead

import httpx
response = httpx.get(url)  # Use activity instead
```

**DO use:**
```python
# CORRECT - Deterministic
now = ctx.current_utc_datetime

result = yield ctx.call_activity(make_api_call, input=url)
```

### Actors vs Workflows Decision

| Use Case | Actors | Workflows |
|----------|--------|-----------|
| Stateful entity with identity | Yes | No |
| Long-running orchestration | No | Yes |
| Turn-based concurrency | Yes | No |
| Multi-step business process | No | Yes |
| Timers/reminders on entity | Yes | No |
| Compensation/rollback | No | Yes |
| Chat sessions | Yes | No |
| Order processing | No | Yes |
```

---

## Step 6: Verify Your Extended Skill

Test your skill against the success criteria from your LEARNING-SPEC.md.

### Test 1: Actor Generation

```
Using my dapr-deployment skill, generate a TaskActor that stores task state and has a deadline reminder.
```

**Expected:** Your skill should generate code matching the patterns you added, with proper imports, StateManager usage, and reminder registration.

### Test 2: Workflow Generation

```
Using my dapr-deployment skill, generate a TaskProcessingWorkflow with validate, assign, and notify activities.
```

**Expected:** Your skill should generate a workflow with yield-based activity calls, proper dataclass inputs/outputs, and WorkflowRuntime setup.

### Test 3: Decision Framework

```
When should I use a Dapr actor vs a Dapr workflow for my AI chat agent that needs conversation history and also needs to process multi-step reasoning chains?
```

**Expected:** Your skill should recommend actors for conversation state (per-user identity, turn-based concurrency) and workflows for multi-step reasoning (durable execution, retry on failure).

---

## What You Have Built

You now have an extended `dapr-deployment` skill that:

1. **Knows actor patterns** - Interface definition, implementation with StateManager, registration with DaprActor, invocation with ActorProxy, timers and reminders
2. **Knows workflow patterns** - Workflow definition with yield, activity definition, WorkflowRuntime setup, client management operations
3. **Understands determinism** - What code is safe in workflows vs what must be in activities
4. **Can decide** - When to use actors (entity state) vs workflows (orchestration)

This skill will be tested and improved throughout Chapter 59. Each lesson teaches a concept, and the "Reflect on Your Skill" section validates that your skill captured it correctly.

---

## Try With AI

Now practice extending skills with AI collaboration. These prompts help you explore actor and workflow patterns beyond what we covered.

### Prompt 1: Advanced Actor Patterns

```
Using /fetching-library-docs, fetch the Dapr actors documentation for Python.
I want to understand:
1. How actor reentrancy works
2. How to configure actor garbage collection timeout
3. How actors communicate with each other via ActorProxy

Summarize the key patterns I should add to my dapr-deployment skill.
```

**What you're learning:** Using AI to research official documentation and extract patterns for skill extension. The AI helps you identify what's important without hallucinating implementation details.

### Prompt 2: Workflow Patterns Discovery

```
Help me extend my dapr-deployment skill with workflow patterns.
Using /fetching-library-docs for dapr-ext-workflow, find:
1. The fan-out/fan-in pattern (when_all)
2. The saga pattern with compensation
3. The monitor pattern with continue_as_new

Show me the code patterns I should add to my skill.
```

**What you're learning:** Collaborative pattern discovery where AI fetches documentation and you decide what patterns are worth adding to your skill. This is bidirectional learning: AI knows the docs, you know your use cases.

### Prompt 3: Skill Validation

```
I extended my dapr-deployment skill with actor and workflow patterns.
Test it by asking:
"Generate a ChatActor that maintains conversation history with a 5-minute idle reminder."

Review the generated code against official Dapr Python SDK patterns.
What's correct? What needs improvement?
```

**What you're learning:** Using AI to validate your skill's output against authoritative sources. This catches errors before they propagate to production code.

**Safety Note:** When extending skills, always ground patterns in official documentation retrieved via `/fetching-library-docs`. Patterns from AI memory may be outdated or incorrect. Your skill is only as good as its sources.
