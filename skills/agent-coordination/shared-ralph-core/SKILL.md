---
name: ralph-core
description: Single source of truth for Ralph Orchestra - event-driven architecture, status values, exit conditions. Use when referencing core system behavior, status transitions, or Ralph-specific protocols.
category: core
tags: [orchestration, architecture, v2]
dependencies: [shared-ralph-event-protocol, shared-message-handling, shared-worker-protocol]
---

# Ralph Core Instructions

> "Single source of truth for all Ralph agents - reference, don't duplicate."

## When to Use This Skill

Use **when** you need to reference:
- Core system behavior or architecture
- Status value definitions
- Exit conditions
- Ralph-specific protocols

Use **proactively** for:
- Resolving ambiguities about status transitions
- Understanding file ownership rules
- Clarifying commit format requirements

---

## Quick Start

<examples>
Example 1: Check status value meaning
```
Q: What does "in_retrospective" status mean?
A: See "Status Values Reference" section below.
   - Used by: PM
   - passes: true
   - Meaning: Worker retrospective phase active
   - Who acts: Workers contribute, PM synthesizes
```

Example 2: Determine commit format
```
Q: How should I format my commit message?
A: Use Ralph commit format:
   [ralph] [{agent}] {task-id}: Brief description

   - Change 1
   - Change 2

   PRD: {task-id} | Agent: {agent} | Iteration: N
```

Example 3: Check file permissions
```
Q: Can I modify prd.json.items?
A: Only PM can modify task items. Workers can only
   modify their own agents.{agent} entry in prd.json.
```
</examples>

---

## Ralph Architecture (V2)

**Event-Driven with Actor Model + Event Sourcing:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACTOR SUPERVISOR (Watchdog)                   │
│                    - Monitors agents via named pipes            │
│                    - Auto-restart on crash ("let-it-crash")      │
│                    - Event log: .claude/session/eventlog.jsonl │
└─────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │    PM   │        │ Worker  │        │ Worker  │
    │ (pipes) │◄──────►│ (pipes) │◄──────►│ (pipes) │
    └─────────┘        └─────────┘        └─────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Single Source of Truth** | `prd.json` contains all status information |
| **Event Log** | `eventlog.jsonl` is append-only source of truth |
| **Named Pipes** | `ralph-{agent}-main` for message delivery |
| **Exit-After-Work** | Workers complete work, exit, watchdog restarts |

---

## Status Values Reference (Single Source of Truth)

### Task Status (`prd.json.items[{taskId}].status`)

| Status | Used By | passes | Meaning |
|--------|---------|--------|---------|
| `pending` | PM | false | Task not yet started |
| `assigned` | PM | false | Task assigned, waiting for worker |
| `in_progress` | Worker (self) | false | Worker actively working |
| `awaiting_qa` | PM | false | Worker finished, waiting for QA |
| `passed` | QA → PM | **true** | **QA PASSED** - triggers retrospective |
| `needs_fixes` | PM | false | QA found bugs, reassign to worker |
| `blocked` | PM | false | Max attempts, manual escalation |
| `in_retrospective` | PM | true | Worker retro phase active |
| `retrospective_synthesized` | PM | true | Retro complete, committed |
| `playtest_phase` | PM | true | Game Designer playtesting |
| `playtest_complete` | PM | true | Playtest reviewed |
| `prd_refinement` | PM | true | PRD reorganization |
| `task_ready` | PM | true | Acceptance criteria received |
| `skill_research` | PM | true | Improving agent skills |
| `completed` | PM | true | All phases complete, archived |

### Agent Status (`prd.json.agents.{agent}.status`)

| Status | Meaning | Who Sets |
|--------|---------|----------|
| `idle` | Available for work | Self/PM |
| `working` | Actively working | Self |
| `working_on_retrospective` | Contributing to retro | Self |
| `awaiting_pm` | Waiting for PM response | Self |
| `awaiting_gd` | Waiting for Game Designer | Self |
| `waiting` | General waiting state | Self |

### Status Transition Rules

1. **Only PM** can set task status (except `in_progress` by workers)
2. **Only QA** can set `passed` status (PM then transitions)
3. **Only PM** can transition to `completed`
4. `blocked` is **terminal** - requires manual intervention
5. All `awaiting_*` statuses have **10-minute watchdog timeout**

---

## Task Status Flow

### Core Flow (Implementation)

```
pending → assigned → in_progress → awaiting_qa → passed
                                        ↓
                                   needs_fixes
                                        ↓
                                   blocked (after max attempts)
```

### Post-Validation Phases

```
passed → in_retrospective → retrospective_synthesized → playtest_phase
       → playtest_complete → prd_refinement → task_ready
       → skill_research → completed
```

---

## File Ownership (Single-Writer Principle)

| File | Primary Owner | Other Agents |
|------|---------------|--------------|
| `prd.json` | PM (all fields) | Workers: own `agents.{role}.*` only |
| `eventlog.jsonl` | Watchdog (append-only) | All: read-only |
| `agent-status.json` | Watchdog (auto) | All: read-only |

### Concurrency Rules

1. **Read-modify-write atomically** - Use temp file pattern
2. **Only update fields you own** - Never overwrite another agent's data
3. **Append-only for logs** - Never delete or reorder entries
4. **Retry on conflict** - If write fails, re-read and retry once

---

## Commit Format (Universal)

```
[ralph] [{AGENT}] {PRD_ID}: Brief description

- Change 1
- Change 2

PRD: {PRD_ID} | Agent: {AGENT} | Iteration: {N}
```

### Universal Commit Rule

**CRITICAL: Every agent MUST commit their file changes.**

**When to Commit:**
- After any file modifications (source, configs, PRD, docs, session)
- Before sending completion messages
- After any skill file updates
- After any documentation changes

**No Commit Exceptions:**
- Heartbeat updates (`prd.json.agents.{agent}.lastSeen`)
- Temporary/pending message files

---

## Exit Conditions

**Only these allow agents to exit:**

| Condition | Description |
|-----------|-------------|
| `completed` | All PRD items have `passes: true` |
| `terminated` | `/cancel-ralph` invoked |
| `max_iterations_reached` | Iteration limit hit |

**Workers MUST check** and exit when any condition is met.

---

## Heartbeat Protocol

**Agents MUST emit heartbeat markers during long operations:**

```
[HEARTBEAT] Agent: {AGENT_TYPE} | Status: working | Task: {TASK_ID}
```

Emit:
- Every 30 seconds during long-running operations
- When starting a new phase of work
- When waiting for external processes (builds, tests)

---

## Configuration

Configurable via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `RALPH_IDLE_TIMEOUT` | 60s | No output before restart |
| `RALPH_HEARTBEAT_INTERVAL` | 30s | Heartbeat frequency |
| `RALPH_STALE_THRESHOLD` | 90s | Agent considered stale |
| `RALPH_MAX_ITERATIONS` | 200 | Maximum loop iterations |
| `RALPH_CONTEXT_THRESHOLD` | 70% | Context usage triggering reset |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-event-protocol` | V2 event-driven messaging |
| `shared-message-handling` | V2 message delivery via named pipes |
| `shared-worker-protocol` | Worker exit patterns, message sending |
| `shared-context-management` | Context window auto-reset |
| `shared-file-permissions` | File read/write permissions |
| `shared-atomic-updates` | File update atomicity |
| `shared-process-lifecycle` | Process lifecycle, cleanup |
| `docs/powershell/v2-architecture.md` | 🆕 V2 infrastructure: Event Sourcing, Actor Model, CQRS |
| `.claude/scripts/v2-architecture/` | 🆕 Core V2 modules (concurrency, serialization, metrics, eventlog) |
