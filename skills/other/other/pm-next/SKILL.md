---
name: pm-next
description: Surface the single most valuable next coordination action by synthesizing task queue, inbox pressure, condition-based maintenance triggers, and active goals. The PM decision-making assistant. Triggers on "/pm-next", "what should I do next", "prioritize", "next action", "what's most important".
user-invocable: true
allowed-tools: Read, Write, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.
Read `ops/config.yaml` for all condition thresholds.
Read `ops/reminders.md` for standing directives.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: compute and present the single highest-value next action
- If "list": return top 5 next actions ranked
- If "sprint": focus on sprint-related next actions only
- If "maintenance": focus on vault maintenance only

**START NOW.**

---

## Philosophy

**The PM's scarcest resource is attention. /pm-next protects it.**

After a session with multiple teams deployed, multiple deliverables processed, and multiple decisions created, the queue of possible next actions is long. Running /pm-document when /pm-retrospect is more needed wastes coordination capacity. Deploying another implementation team when validation is overdue creates compounding debt.

/pm-next synthesizes all signals — the task queue, inbox pressure, maintenance condition triggers, active goal status, and sprint health trajectory — and returns one recommendation: the action that, if taken now, most improves the system's trajectory toward the target health score.

This is judgment, not scheduling. The recommendation requires explanation.

---

## Signal Sources

### Signal 1: Task Queue Pressure

```bash
# Check ops/tasks.md for pending tasks
cat ops/tasks.md
```

Tasks in the queue have been explicitly queued. If any task is overdue or blocking other tasks, it gets priority.

### Signal 2: Inbox Pressure

```bash
ls inbox/ 2>/dev/null | wc -l
```

Items in inbox/ represent sprint outputs or source material waiting for /pm-document processing. Each day an inbox item sits unprocessed, the decisions from that sprint are unavailable for linking and update. Inbox pressure compounds.

### Signal 3: Maintenance Condition Triggers

Read `ops/config.yaml` for thresholds, then check each condition:

```bash
# Pending observations count
rg "^status: pending" ops/observations/ --include="*.md" -l 2>/dev/null | wc -l

# Pending tensions count
rg "^status: pending" ops/tensions/ --include="*.md" -l 2>/dev/null | wc -l

# Stale issues count (open issues not reviewed in >14 days — approximate by count)
rg "^status: open" decisions/ --include="*.md" -l 2>/dev/null | wc -l

# Sprint gap (days since last sprint record) — check most recent sprint file
ls -t decisions/sprint-*.md 2>/dev/null | head -1
```

| Condition | Threshold | Trigger |
|-----------|-----------|---------|
| Pending observations | >10 | /pm-retrospect |
| Pending tensions | >5 | /pm-retrospect |
| Stale open issues | >14 days | /pm-update |
| Sprint gap | >7 days | /pm-document sprint output |
| Inbox items | >0 | /pm-document |

### Signal 4: Active Goals

```bash
cat self/goals.md
```

What are the current active threads? Is there a goal that's been in progress across multiple sessions without resolution? That priority degradation is a signal.

### Signal 5: Health Trajectory

```bash
cat ops/health/health-log.md 2>/dev/null | tail -20
```

Is health improving? Stalling? If health has stalled across 2+ sprints, the problem is usually structural — either the wrong teams are being deployed or validation is being skipped.

---

## Synthesis

After reading all signals, synthesize:

1. **Blocking tasks** — anything that blocks other work gets priority regardless of other signals
2. **Inbox pressure** — unprocessed sprint outputs create stale context; high priority
3. **Maintenance triggers** — condition violations degrade the system over time
4. **Active goals** — long-running goals that haven't progressed need attention
5. **Health trajectory** — if stalling, investigate root cause before deploying more teams

Rank by: Blocking > Inbox > Maintenance > Goals > Health Investigation

---

## Output Format

```
## Next Action Recommendation

### Recommended: [action name]
Command: [/pm-command or /teams:deploy-* command]
Reason: [2-3 sentences explaining why this is the highest-value action right now]

### Signals That Led Here
- Inbox: N items waiting (Sprint N output unprocessed)
- Observations: N pending (threshold: 10)
- Tensions: N pending (threshold: 5)
- Task queue: [N tasks / empty]
- Health: [last recorded] / trajectory: [improving/stalling]

### After This Action
Suggested sequence:
1. [current recommendation]
2. [next logical action]
3. [following action]

### What Would Change This Recommendation
- If [condition]: run [different action] instead
- If [condition]: [different priority]
```

---

## Hard Rules

- Never recommend more than one action at a time in the primary recommendation
- Always explain the reasoning — the PM must be able to disagree with good information
- If health is stalling and the reason is unclear, recommend investigation (/pm-retrospect or /pm-audit) before recommending more implementation
- Always note validation enforcement status if recent sprint work is in play
