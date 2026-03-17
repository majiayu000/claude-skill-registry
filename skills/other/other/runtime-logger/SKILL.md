---
name: runtime-logger
description: Emit info-level logs to file during task execution, similar to logger.info() calls in code
---

# Runtime Activity Logger

Log key activities to `.claude/logs/activity.log` using bash as you work. This creates a trace of agent reasoning and actions analogous to info-level logging in deterministic code.

## Setup

Before starting any task, ensure the log directory exists:

```bash
mkdir -p .claude/logs
```

## Log Format

Use this consistent format for all log entries:

```bash
echo "[$(date -Iseconds)] [LEVEL] phase: message" >> .claude/logs/activity.log
```

### Log Levels

| Level | Use For |
|-------|---------|
| `INFO` | Normal operations, progress updates, decisions |
| `DEBUG` | Detailed technical information when troubleshooting |
| `WARN` | Unexpected situations that don't block progress |
| `ERROR` | Failures that affect task completion |

## When to Log

### Task Lifecycle
- **Task start**: Log the goal and planned approach
- **Task completion**: Log summary, outcome, and any artifacts created

### Tool Usage
- **Before significant tool use**: Log what tool and why
- **After tool use**: Log outcome (success/failure, key findings)

### Decision Points
- **Architectural choices**: Log reasoning for design decisions
- **Branch points**: Log why one approach was chosen over alternatives
- **Assumptions**: Log any assumptions being made

### Subagent Activity
- **Delegation**: Log task being delegated and to which subagent
- **Completion**: Log subagent results when they return

## Examples

### Starting a Task
```bash
echo "[$(date -Iseconds)] [INFO] start: Beginning refactoring task for payment module" >> .claude/logs/activity.log
echo "[$(date -Iseconds)] [INFO] planning: Will analyze current structure, identify patterns, then apply Strategy pattern" >> .claude/logs/activity.log
```

### Tool Usage
```bash
echo "[$(date -Iseconds)] [INFO] tool: Reading src/payments/processor.py to understand current implementation" >> .claude/logs/activity.log
echo "[$(date -Iseconds)] [INFO] tool-result: Found 3 payment types with duplicated validation logic" >> .claude/logs/activity.log
```

### Decision Points
```bash
echo "[$(date -Iseconds)] [INFO] decision: Using Strategy pattern - cleaner than inheritance for 3 payment types" >> .claude/logs/activity.log
echo "[$(date -Iseconds)] [INFO] decision: Keeping backward compatibility by wrapping legacy interface" >> .claude/logs/activity.log
```

### Subagent Delegation
```bash
echo "[$(date -Iseconds)] [INFO] delegate: Spawning test-writer subagent for unit test coverage" >> .claude/logs/activity.log
echo "[$(date -Iseconds)] [INFO] delegate-complete: test-writer created 12 unit tests, all passing" >> .claude/logs/activity.log
```

### Warnings and Errors
```bash
echo "[$(date -Iseconds)] [WARN] Found deprecated API usage in line 142, will need migration" >> .claude/logs/activity.log
echo "[$(date -Iseconds)] [ERROR] Build failed: missing dependency 'stripe-sdk', attempting to resolve" >> .claude/logs/activity.log
```

### Task Completion
```bash
echo "[$(date -Iseconds)] [INFO] complete: Refactoring finished - 3 files modified, 12 tests added" >> .claude/logs/activity.log
echo "[$(date -Iseconds)] [INFO] artifacts: Created src/payments/strategies/*.py, updated tests/test_payments.py" >> .claude/logs/activity.log
```

## Log File Management

### Viewing Logs in Real-Time
```bash
tail -f .claude/logs/activity.log
```

### Rotating Logs
For long-running projects, consider date-based log files:
```bash
echo "[$(date -Iseconds)] [INFO] message" >> .claude/logs/activity-$(date +%Y-%m-%d).log
```

## Integration with Subagents

Subagents inherit access to bash and should follow the same logging conventions. When delegating tasks, instruct subagents to:

1. Log their start and completion
2. Use the same log file path
3. Prefix messages with their agent name for traceability

Example subagent log entry:
```bash
echo "[$(date -Iseconds)] [INFO] [test-writer] start: Generating unit tests for PaymentStrategy classes" >> .claude/logs/activity.log
```
