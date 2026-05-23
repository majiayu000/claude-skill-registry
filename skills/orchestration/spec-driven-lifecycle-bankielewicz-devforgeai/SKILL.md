---
name: spec-driven-lifecycle
description: >
  Coordinates spec-driven development lifecycle from Epic -> Sprint -> Story ->
  Architecture -> Development -> QA -> Release with structural anti-skip enforcement.
  Manages story lifecycle across 11 workflow states, enforces 4 quality gates, and
  orchestrates skill invocation. Replaces spec-driven-lifecycle as the unified
  lifecycle coordinator. Use when starting sprints, managing story workflow progression,
  auditing deferrals, running sprint retrospectives, or coordinating multi-story releases.
  Always use this skill when /orchestrate, /create-sprint, or /audit-deferrals is invoked.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - Task
model: claude-opus-4-6
effort: High
---

# Spec-Driven Lifecycle

Coordinate the complete story lifecycle from Backlog through Released, enforcing quality gates at every transition and invoking specialized skills at the right time.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase State Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Fresh-context subagent execution** - Subagents run in isolated context without accumulated bias
2. **Binary CLI gates** - Compiled Rust in `src/commands/phase.rs`, cannot be forged by LLM
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - `.claude/hooks/phase-steps-registry.json` tracks every mandatory step

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002)

---

## Parameter Extraction

Extract parameters from conversation context. See `references/parameter-extraction.md` for the extraction algorithm.

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /orchestrate | Story identifier (STORY-NNN) |
| `**Operation:** plan-sprint` | /create-sprint | Sprint planning mode trigger |
| `**Command:** audit-deferrals` | /audit-deferrals | Audit deferrals mode trigger |
| `**Sprint Name:** {name}` | /create-sprint | Sprint name for planning |
| `**Selected Stories:** {ids}` | /create-sprint | Story IDs for sprint |
| `**Duration:** {days} days` | /create-sprint | Sprint duration |
| `**Start Date:** {date}` | /create-sprint | Sprint start date |
| `**Epic:** {id}` | /create-sprint | Epic linkage |
| `**Auto-Resume:** Enabled` | /orchestrate | Checkpoint resume flag |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init ${STORY_ID} --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${STORY_ID}` to get CURRENT_PHASE. |
| 2 | Invalid story ID | HALT. Must match STORY-XXX pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

**Iteration counter:** `iteration_count = 1`, `max_iterations = 5`. If resuming, read from phase-state.json.

**Note:** For Sprint Planning and Audit Deferrals modes, use a synthetic ID (e.g., `SPRINT-{name}` or `AUDIT-{timestamp}`) if no story ID is available.

---

## Mode Router [MANDATORY - AFTER Phase State Initialization]

Detect operating mode from conversation context markers. Mode determines which phases execute.

**Priority order:** Sprint > Audit > Story > Default (first match wins)

```
1. IF "**Operation:** plan-sprint" found in conversation:
   MODE = "sprint-planning"
   PHASE_SEQUENCE = [01, 03S, 08]
   Display: "Mode: Sprint Planning"

2. ELSE IF "**Command:** audit-deferrals" found in conversation:
   MODE = "audit-deferrals"
   PHASE_SEQUENCE = [01, 03A, 04A, 08]
   Display: "Mode: Audit Deferrals"

3. ELSE IF "**Story ID:** STORY-NNN" found in conversation:
   MODE = "story-management"
   PHASE_SEQUENCE = [01, 02, 03, 04, 05, 06, 07, 08]
   Display: "Mode: Story Management"

4. ELSE:
   MODE = "default"
   Read references/mode-detection.md for inference logic.
   IF inference fails:
     HALT with AskUserQuestion:
       Question: "Cannot determine operating mode. What would you like to do?"
       Header: "Mode"
       Options:
         - label: "Orchestrate a story"
           description: "Manage story lifecycle (dev -> QA -> release)"
         - label: "Plan a sprint"
           description: "Create a sprint with story selection"
         - label: "Audit deferrals"
           description: "Audit deferred work in completed stories"
       multiSelect: false
```

**See `references/mode-detection.md` for complete detection algorithm and edge cases.**

---

## Phase Orchestration Loop

```
FOR phase_id in PHASE_SEQUENCE:

    1. ENTRY GATE: devforgeai-validate phase-check ${STORY_ID} --from={prev} --to={phase_id}
       IF exit != 0: HALT

    2. LOAD: Read(file_path="phases/{phase_files[phase_id]}")

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-GATE triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${STORY_ID} --phase={phase_id} --subagent={name}

    5. EXIT GATE: devforgeai-validate phase-complete ${STORY_ID} --phase={phase_id} --checkpoint-passed
       IF exit != 0: HALT
```

### Story Management Mode Phases (01-08)

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 02 | Checkpoint Detection | `phases/phase-02-checkpoint.md` |
| 03 | Story Validation | `phases/phase-03-story-validation.md` |
| 04 | Skill Invocation | `phases/phase-04-skill-invocation.md` |
| 05 | Status Update | `phases/phase-05-status-update.md` |
| 06 | QA Retry Loop | `phases/phase-06-qa-retry.md` |
| 07 | Next Action | `phases/phase-07-next-action.md` |
| 08 | Finalization | `phases/phase-08-finalization.md` |

### Sprint Planning Mode Phases (01, 03S, 08)

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 03S | Sprint Planning | `phases/phase-03S-sprint-planning.md` |
| 08 | Finalization | `phases/phase-08-finalization.md` |

### Audit Deferrals Mode Phases (01, 03A, 04A, 08)

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 03A | Audit Deferrals | `phases/phase-03A-audit-deferrals.md` |
| 04A | Hook Integration | `phases/phase-04A-hook-integration.md` |
| 08 | Finalization | `phases/phase-08-finalization.md` |

### Sprint Retrospective Mode Phases (01, 03R, 08)

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 03R | Sprint Retrospective | `phases/phase-03R-retrospective.md` |
| 08 | Finalization | `phases/phase-08-finalization.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | (none) | N/A |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | (skills invoked: spec-driven-dev, spec-driven-qa, spec-driven-release) | BLOCKING |
| 05 | (none) | N/A |
| 06 | (none - delegates to skills) | N/A |
| 07 | (none) | N/A |
| 08 | (none) | N/A |
| 03S | sprint-planner | BLOCKING |
| 03A | deferral-validator | BLOCKING |
| 04A | (none) | N/A |
| 03R | technical-debt-analyzer | BLOCKING |

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion. See `references/troubleshooting.md`.

---

## Workflow States

Stories progress through **11 sequential states:**

```
Backlog -> Architecture -> Ready for Dev -> In Development -> Dev Complete ->
QA In Progress -> [QA Approved | QA Failed] -> Releasing -> Released
```

**See `references/workflow-states.md` for complete state definitions.**
**See `references/state-transitions.md` for valid transitions, prerequisites, and quality gate requirements.**

---

## Quality Gate Enforcement

**Four gates block workflow progression** when requirements not met:

| Gate | Transition | Key Requirements |
|------|-----------|-----------------|
| Gate 1: Context Validation | Architecture -> Ready for Dev | 6 context files present and valid |
| Gate 2: Test Passing | Dev Complete -> QA In Progress | All tests pass, coverage 95%/85%/80% |
| Gate 3: QA Approval | QA Approved -> Releasing | All ACs verified, no unresolved deferrals |
| Gate 4: Release Readiness | Releasing -> Released | Smoke tests pass, rollback plan documented |

**See `references/quality-gates.md` for complete gate requirements and enforcement logic.**

---

## State Persistence

**Location:** `devforgeai/workflows/${STORY_ID}-phase-state.json`

---

## Workflow Completion Validation

```
Story Management mode:
  IF completed_count < 8: HALT "WORKFLOW INCOMPLETE - {completed_count}/8 phases"
  IF completed_count == 8: "All 8 phases completed - Workflow validation passed"

Sprint Planning mode:
  IF completed_count < 3: HALT "WORKFLOW INCOMPLETE - {completed_count}/3 phases"

Audit Deferrals mode:
  IF completed_count < 4: HALT "WORKFLOW INCOMPLETE - {completed_count}/4 phases"
```

IF iteration_count >= 4: Display "Approaching limit"
IF iteration_count >= max_iterations: HALT "Maximum iterations reached"

---

## Success Criteria

### Story Management Mode
- Story progresses through appropriate workflow states
- Skills invoked at correct transition points
- Quality gates enforced at every transition
- Status history updated with complete timeline
- Story status reflects actual completion state

### Sprint Planning Mode
- Sprint file created in devforgeai/specs/Sprints/
- Stories updated to "Ready for Dev" status
- Capacity validated within 20-40 point range

### Audit Deferrals Mode
- All QA Approved and Released stories scanned
- Deferrals categorized (resolvable, valid, invalid)
- Audit report generated and saved
- Hooks invoked if eligible

---

## Reference Files

### Phase Execution (phases/ directory)

| File | Phase | Mode |
|------|-------|------|
| phase-01-preflight.md | Pre-Flight Validation | All |
| phase-02-checkpoint.md | Checkpoint Detection | Story |
| phase-03-story-validation.md | Story Validation | Story |
| phase-03S-sprint-planning.md | Sprint Planning | Sprint |
| phase-03A-audit-deferrals.md | Audit Deferrals | Audit |
| phase-03R-retrospective.md | Sprint Retrospective | Retro |
| phase-04-skill-invocation.md | Skill Invocation | Story |
| phase-04A-hook-integration.md | Hook Integration | Audit |
| phase-05-status-update.md | Status Update | Story |
| phase-06-qa-retry.md | QA Retry Loop | Story |
| phase-07-next-action.md | Next Action | Story |
| phase-08-finalization.md | Finalization | All |

### Supporting References (references/ directory)

| File | Purpose |
|------|---------|
| parameter-extraction.md | Parameter extraction algorithm |
| mode-detection.md | Mode detection logic and context markers |
| workflow-states.md | 11 state definitions |
| state-transitions.md | Valid transitions and rules |
| quality-gates.md | 4 gate requirements and enforcement |
| story-management.md | Story lifecycle procedures |
| subagent-registry.md | Subagent coordination patterns |
| troubleshooting.md | Common issues and solutions |
| error-handling-patterns.md | Error recovery patterns |
| deferred-tracking.md | Technical debt tracking and analysis |
| user-input-guidance.md | AskUserQuestion templates and patterns |

### Asset Templates (assets/templates/ directory)

| File | Purpose |
|------|---------|
| sprint-template.md | Sprint document template |
| story-template.md | Story document template |
| technical-debt-register-template.md | Debt register template |

---

## Common Issues

**Top 5 issues and quick solutions:**

1. **Mode detection fails** - Check context markers match expected format (see `references/mode-detection.md`)
2. **Checkpoint not detected** - Verify Status History format in story file (see `references/workflow-states.md`)
3. **Quality gate blocks** - Review gate requirements for the specific transition (see `references/quality-gates.md`)
4. **QA retry exceeds 3** - Address root cause, consider splitting story (see phase-06-qa-retry.md)
5. **Sprint capacity exceeded** - Remove lower-priority stories or adjust capacity (see phase-03S-sprint-planning.md)

**See `references/troubleshooting.md` for comprehensive troubleshooting guide.**
