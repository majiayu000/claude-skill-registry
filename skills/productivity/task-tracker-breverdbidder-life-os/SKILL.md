---
name: task-tracker
description: >
  ADHD-optimized task state machine with abandonment detection and 
  interventions. Use when: (1) user initiates any task, (2) providing
  solutions to problems, (3) detecting context switches, (4) user says
  "done", "completed", "finished", (5) session ends with pending tasks,
  (6) >30 minutes since solution provided. Tracks complexity, clarity,
  domain (BUSINESS/MICHAEL/FAMILY/PERSONAL), and triggers interventions.
---

# Task Tracker - ADHD State Machine

## Overview

Systematic task tracking designed for ADHD patterns. Prevents task abandonment through proactive interventions while maintaining accountability without judgment.

## State Machine

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
┌──────────┐   ┌──────────────────┐   ┌─────────────┐         │
│ INITIATED│──▶│ SOLUTION_PROVIDED│──▶│ IN_PROGRESS │─────────┤
└──────────┘   └──────────────────┘   └─────────────┘         │
     │                  │                    │                 │
     │                  │                    ▼                 │
     │                  │              ┌───────────┐          │
     │                  │              │ COMPLETED │          │
     │                  │              └───────────┘          │
     │                  │                                      │
     │                  ├─────────────────┐                   │
     │                  │                 │                    │
     │                  ▼                 ▼                    │
     │           ┌───────────┐     ┌──────────┐               │
     └──────────▶│ ABANDONED │     │ BLOCKED  │               │
                 └───────────┘     └──────────┘               │
                        │                │                     │
                        ▼                ▼                     │
                 ┌───────────┐     ┌──────────┐               │
                 │  DEFERRED │◀────│ (Retry)  │───────────────┘
                 └───────────┘     └──────────┘
```

## State Definitions

| State | Trigger | Next Actions |
|-------|---------|--------------|
| INITIATED | Task request received | Assess complexity, provide solution |
| SOLUTION_PROVIDED | Solution given | Wait for execution signal |
| IN_PROGRESS | User confirms working | Monitor for completion |
| COMPLETED | User confirms done | Log success, update streak |
| ABANDONED | No response + context switch | Log pattern, intervention |
| BLOCKED | External dependency | Identify blocker, schedule retry |
| DEFERRED | Conscious postponement | Set reminder, capture reason |

## Task Metadata

Every task tracks:

```python
task = {
    "id": "task_20251219_001",
    "description": "Review Q4 insurance renewals",
    "state": "INITIATED",
    "domain": "BUSINESS",  # BUSINESS | MICHAEL | FAMILY | PERSONAL
    "complexity": 6,       # 1-10 scale
    "clarity": 8,          # 1-10 scale (how clear were instructions)
    "estimated_minutes": 45,
    "actual_minutes": None,
    "initiated_at": "2025-12-19T10:30:00Z",
    "solution_provided_at": None,
    "completed_at": None,
    "abandonment_count": 0,
    "intervention_level": 0
}
```

## Abandonment Detection Triggers

Monitor for these patterns:

1. **Context Switch** - New topic without closing current task
2. **Session End** - Chat ends with task in SOLUTION_PROVIDED or IN_PROGRESS
3. **Time Decay** - >30 minutes since solution with no update
4. **Topic Drift** - User asks unrelated question while task pending

### Detection Algorithm

```python
def check_abandonment(task, current_message, elapsed_minutes):
    if task["state"] not in ["SOLUTION_PROVIDED", "IN_PROGRESS"]:
        return False
    
    # Time-based trigger
    if elapsed_minutes > 30:
        return True
    
    # Context switch detection
    if not is_related_to_task(current_message, task):
        return True
    
    return False
```

## Intervention Protocol

### Level 1: Gentle Check (0-30 minutes)
```
📌 Quick check: [task description] - still on it?
```

### Level 2: Pattern Observation (30-60 minutes)
```
🔄 I notice [task] from earlier. This is pattern #[N] this week.
Continue or consciously defer?
```

### Level 3: Direct Accountability (>60 minutes)
```
⚠️ ACCOUNTABILITY: [task] started [time] ago.
Current status? Be honest - no judgment, just facts.
```

## ADHD Intervention Strategies

When abandonment detected, apply these techniques:

### Micro-Commitment
Break to smallest possible action:
```
Just step 1? [tiny specific action] That's it.
Nothing else required right now.
```

### Body Doubling
Create virtual co-working presence:
```
Let's do this together. You: [specific action]
Me: ⏱️ Waiting... (I'll check back in 5 minutes)
```

### Chunking
Focus tunnel vision:
```
Step 1 only. Confirm when done.
Don't think about step 2 yet.
```

### Energy Matching
Align with daily patterns:
```
It's [time] - your [peak/dip] period.
[Suggest appropriate task complexity]
```

## Workflow: Task Creation

**Trigger:** Any request that implies work to be done

1. Extract task description from message
2. Assess complexity (1-10) based on:
   - Number of steps
   - External dependencies
   - Decision-making required
   - Time estimate
3. Assess clarity (1-10) based on:
   - Specificity of request
   - Known vs unknown elements
   - Ambiguity level
4. Assign domain (BUSINESS/MICHAEL/FAMILY/PERSONAL)
5. Set state to INITIATED
6. Provide solution → state to SOLUTION_PROVIDED

## Workflow: State Transitions

### INITIATED → SOLUTION_PROVIDED
```python
# After providing solution
task["state"] = "SOLUTION_PROVIDED"
task["solution_provided_at"] = now()
```

### SOLUTION_PROVIDED → IN_PROGRESS
**Trigger:** User says "working on it", "starting now", "doing this"
```python
task["state"] = "IN_PROGRESS"
```

### IN_PROGRESS → COMPLETED
**Trigger:** User says "done", "finished", "completed"
```python
task["state"] = "COMPLETED"
task["completed_at"] = now()
task["actual_minutes"] = elapsed_time()
update_streak()
```

### Any → ABANDONED
**Trigger:** Abandonment detection + no response to intervention
```python
task["state"] = "ABANDONED"
task["abandonment_count"] += 1
log_pattern()
```

### Any → BLOCKED
**Trigger:** User identifies external dependency
```python
task["state"] = "BLOCKED"
task["blocker"] = identified_dependency
schedule_retry()
```

### Any → DEFERRED
**Trigger:** Conscious postponement with reason
```python
task["state"] = "DEFERRED"
task["defer_reason"] = reason
task["defer_until"] = scheduled_time
```

## Streak Tracking

Maintain completion streak for motivation:

```python
streak = {
    "current": 5,  # Days with at least 1 completion
    "longest": 12,
    "total_completions": 47,
    "abandonment_rate": 0.23  # 23% tasks abandoned
}

# On completion
"✅ Done. Streak: 5 days. Total: 47 tasks."

# On first task of day
"Day 6 starts now. Keep the streak alive."
```

## Domain-Specific Behavior

### BUSINESS (Everest Capital)
- Higher urgency weighting
- Deadline awareness
- Revenue impact assessment

### MICHAEL (D1 Swimming)
- Connect to swim schedule
- Nutrition/training alignment
- Recruiting deadlines

### FAMILY (Orthodox Observance)
- Shabbat/holiday awareness
- No work pressure evenings
- Family event priority

### PERSONAL (Health/Learning)
- Energy level consideration
- Learning capture integration
- Health metric correlation

## LangGraph Integration

### State Schema
```python
class TaskState(TypedDict):
    task_id: str
    description: str
    state: str
    domain: str
    complexity: int
    clarity: int
    elapsed_minutes: int
    intervention_level: int
    streak_current: int
```

### Nodes
- `create_task` - Initialize from user message
- `provide_solution` - Generate response, update state
- `check_abandonment` - Periodic abandonment check
- `intervene` - Apply intervention strategy
- `complete_task` - Log completion, update streak

## Scripts

- `scripts/task_state_machine.py` - State transition logic
- `scripts/abandonment_detector.py` - Pattern detection
- `scripts/streak_calculator.py` - Streak maintenance

## References

- `references/intervention_templates.md` - Full intervention scripts
- `references/adhd_patterns.md` - Common patterns and responses
