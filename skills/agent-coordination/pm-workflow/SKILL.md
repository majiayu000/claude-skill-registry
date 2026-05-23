---
name: pm-workflow
description: Complete PM Coordinator workflow - task assignment, retrospective orchestration, PRD management, worker coordination. Use proactively when starting PM agent work.
category: coordination
user-invocable: true
---

# PM Coordinator Workflow

> Complete workflow for PM Coordinator. Load pm-router first, then this skill.

---

## Quick Start

<startup_workflow>

1. **Process Messages**: Check `.claude/session/messages/pm/msg-*.json`
2. **Sync State**: Read all agent state files + prd.json
3. **Make Decisions**: Assign tasks, trigger retrospectives
4. **Update & Exit**: Sync state files, send status, exit

</startup_workflow>

**Detailed synchronization patterns:** See [state-sync.md](state-sync.md)
**Task handoff between agents:** See [handoffs.md](handoffs.md)
**Phase-by-phase workflow:** See [phases.md](phases.md)
**Decision tables and message formats:** See [reference.md](reference.md)

---

## Startup Workflow

```
1. CHECK PENDING MESSAGES (MANDATORY - FIRST STEP)
   ├─ Use Glob to find messages: .claude/session/messages/pm/msg-*.json
   ├─ Read each message file (JSON fields: from, to, type, payload, timestamp)
   ├─ Process each message based on type
   ├─ Send acknowledgment to watchdog (REQUIRED)
   └─ Delete each message file after acknowledgment

2. READ PRD AND ALL AGENT STATE FILES
   ├─ Read prd.json for top 5 active tasks (PM-ONLY access)
   ├─ If < 5 tasks, read prd_backlog.json for full picture
   ├─ Read ALL agent state files:
   │  ├─ current-task-developer.json
   │  ├─ current-task-qa.json
   │  ├─ current-task-techartist.json
   │  └─ current-task-gamedesigner.json
   ├─ Update Worker Status Summary in current-task-pm.json
   └─ Update your lastSeen timestamp

3. CONSOLIDATE ALL AGENT INBOXES (MANDATORY)
   ├─ Use Glob to find ALL messages for each agent
   ├─ READ every message file
   ├─ DELETE each message after reading
   ├─ Send acknowledgment for each
   └─ Process consolidated information
      ├─ Correlate messages with PRD state
      ├─ Assess what each agent is doing/reporting
      ├─ Identify completed tasks, blockers, questions
      └─ Determine next actions

4. UPDATE STATE FILES AND PRD (ATOMIC)
   ├─ Update agent state files (if assigning/completing)
   ├─ Update prd.json with ALL decisions atomically
   └─ Update current-task-pm.json Worker Status Summary

5. SEND NEW MESSAGES (WAKE UP AGENTS)
   ├─ Task assignment → Send task_assign to worker
   ├─ QA needed → Send validation_request to qa
   ├─ Question response → Send question response
   └─ Retrospective → Send retrospective_initiate to all workers

6. SET PM-READY FLAG
   └─ Write to .claude/session/pm-ready.flag with timestamp

7. WAKE UP ASSIGNED AGENTS
   └─ Send wake_up message if agent has task but empty message queue

8. SEND STATUS_UPDATE TO WATCHDOG
   └─ Update: prd.json.agents.pm.status, lastSeen + send message

9. EXIT (watchdog will restart when needed)
```

---

## Decision Framework

Use this framework to determine the next action based on current state:

<thinking>
Step 1: Check current task status
Step 2: Identify applicable workflow phase
Step 3: Route to appropriate skill
Step 4: Update state and PRD
Step 5: CONTINUE to next phase if in post-completion workflow
</thinking>

| Current State     | Action                                    | Next State                 |
| ----------------- | ----------------------------------------- | -------------------------- |
| `null`            | `Skill("pm-organization-task-selection")` | `task_ready`               |
| `task_ready`      | Task with `pm-test-planner` sub-agent     | `test_plan_ready`          |
| `test_plan_ready` | Assign task, send message, exit           | `assigned`                 |
| `awaiting_qa`     | Wait for QA validation                    | (wait)                     |
| `passed` (QA)     | `Skill("pm-organization-task-selection")` | See [phases.md](phases.md) |
| `needs_fixes`     | Check attempts, reassign if < 3           | `assigned` or `blocked`    |

---

## Post-Completion Continuation Routing

```javascript
// Read current status
const status = prd.json.session.currentTask.status;

// Route based on status
switch (status) {
  case "prd_refinement":
    // Continue to Phase 4 (Cleanup)
    → Execute cleanup inline, then continue to skill research
  case "cleanup_completed":
    // Continue to Phase 5 (Skill Research)
    → Skill("pm-improvement-skill-research")
  case "skill_updates_applied":
    // Continue to Phase 6 (Task Selection)
    → Skill("pm-organization-task-selection")
  case "task_ready":
    // Continue to test planning
    → Skill("pm-planning-test-planning")
  case "test_plan_ready":
    // Final step: assign task, send message, THEN exit
    → Assign to worker, send message, EXIT
  case "assigned":
    // Normal flow - worker has task, wait for completion
    → EXIT (wait for worker messages)
  default:
    // Normal task flow
    → Follow standard decision framework
}
```

### Full Continuation Table

| Current Status                    | Next Skill                                           | Next Status                             |
| --------------------------------- | ---------------------------------------------------- | --------------------------------------- |
| `retrospective_synthesized`       | `Skill("pm-retrospective-playtest-session")` OR skip | `playtest_complete` or `prd_refinement` |
| `playtest_complete`               | `Skill("pm-organization-prd-reorganization")`        | `prd_refinement`                        |
| `prd_refinement`                  | Phase 4: Cleanup completed tasks                     | `cleanup_completed`                     |
| `cleanup_completed`               | `Skill("pm-improvement-skill-research")`             | `skill_research`                        |
| `skill_research`                  | `Skill("pm-organization-task-selection")`            | `task_ready`                            |
| `task_ready` (post-completion)    | `Skill("pm-planning-test-planning")`                 | `test_plan_ready`                       |
| `test_plan_ready` (post-complete) | Assign task, send message to worker                  | `assigned`                              |

---

## Post-Completion Phases

**⚠️ CRITICAL: After QA passes a task, complete ALL phases in order before selecting next task.**

```
completed (QA passed)
    ↓
Phase 2: PRD Reorganization (MANDATORY)
    ↓
Phase 3: Cleanup Completed Tasks (MANDATORY)
    ↓
Phase 4: Select Next Task (MANDATORY)
    ↓
task_ready → test_planning → assigned
```

## ⚠️ CRITICAL: Continuation After Each Phase

After completing each phase:

1. Set the new status in prd.json
2. **IMMEDIATELY continue to the next phase** (do NOT exit)
3. Only exit when reaching `assigned` status (worker has the task)

**Example flow:**

```
`passed` (QA)  → (continue)
→ prd_refinement → (continue) → cleanup_completed → (continue) → task_ready → (continue)
→ test_plan_ready → (continue) → assigned → NOW EXIT
```

---

## Task Assignment Priority

| Category        | Priority    | Examples                               |
| --------------- | ----------- | -------------------------------------- |
| `architectural` | 1 (Highest) | State stores, API design, core systems |
| `integration`   | 2           | API integration, third-party services  |
| `functional`    | 3           | Gameplay mechanics, features           |
| `visual`        | 4           | 3D models, materials, textures         |
| `shader`        | 4           | Shaders, visual effects                |
| `polish`        | 5 (Lowest)  | UI styling, visual refinement          |

---

## Exit Conditions

Only exit when:

- [ ] Sent messages and waiting for response
- [ ] All PRD items have `passes: true` → Output `<promise>RALPH_COMPLETE</promise>`
- [ ] `maxIterations` reached → Log status report
- [ ] `/cancel-ralph` invoked → Terminate gracefully
