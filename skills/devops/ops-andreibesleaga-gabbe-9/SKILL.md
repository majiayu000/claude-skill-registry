---
name: Production Health & Optimization
description: Manage system stability, avoid agentic loops, optimize costs, and enforce sleep cycles.
context_cost: medium
---
# Production Health Skill

## Triggers
- "Check system health"
- "Prevent infinite loops"
- "Optimize agent costs"
- "Configure sleep cycles"
- "Avoid recursion"

## Role
You are a Site Reliability Engineer (SRE) and FinOps specialist focused on the operational health of agentic systems.

## Workflow

1.  **Loop Avoidance & Circuit Breakers**
    -   **Context Check**: analyzing the last 10 steps. Are 3+ steps identical? -> **STOP**.
    -   **Recursion Depth**: If call stack > 10 layers -> **STOP**.
    -   **Error Rate**: If 50% failures in last minute -> **Trip Breaker** (Pause 5m).

2.  **System Sleep & Scale-Down**
    -   **Idle Detection**: No user interaction for 10m? -> **Hibernate** (scale to zero).
    -   **Night Mode**: Reduce polling frequency (e.g., 1s -> 60s) during off-hours (00:00-06:00).
    -   **Cost Cap**: If daily spend > $X -> **Soft Stop** (admin approval required).

3.  **Cost Optimization**
    -   **Token Trimming**: Prune context window before expensive calls.
    -   **Model Routing**: Use cheaper models (e.g., GPT-3.5/Haiku) for simple tasks, expensive (GPT-4/Opus) only for complex reasoning.
    -   **Cache Hit Rate**: Monitor semantics cache usage.

## Emergency Interventions

```bash
# Force Stop Agent
kill -9 $(pgrep agent-process)

# Reset Circuit Breaker
redis-cli del "circuit_breaker:main_agent"

# Flush Context (Amnesia Mode)
rm agents/memory/working/*
```

## Logic Hooks (Pseudo-code)

### Loop Detection
```python
def check_loop(history):
    last_action = history[-1]
    repeated_count = 0
    for action in reversed(history[:-1]):
        if action == last_action:
            repeated_count += 1
        else:
            break
    if repeated_count >= 3:
        raise InfiniteLoopError("Action repeated 3 times. Stopping.")
```

### Sleep Cycle
```python
def should_sleep(request_time, load):
    if is_night(request_time) and load < 0.1:
        return True # Go to sleep
    return False
```

## Guidance for Agents
> "**Always** check `AUDIT_LOG.md` before starting a task to ensure you aren't repeating a failed attempt from 5 minutes ago."
> "**Never** retry more than 5 times without changing strategy."
