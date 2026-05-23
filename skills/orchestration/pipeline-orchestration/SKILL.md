---
activation_code: PIPELINE_ORCHESTRATION_V1
phase: 2
prerequisites:
  - PRD complete
  - Phase 2 checkpoint passed
outputs:
  - Pipeline status dashboard
  - Phase transition signals
  - Error recovery instructions
description: |
  Master orchestrator for the entire development pipeline from Phase 2-12.
  Activates via codeword [ACTIVATE:PIPELINE_ORCHESTRATION_V1] injected by hooks
  when user wants to start automated development.

  Activation trigger: [ACTIVATE:PIPELINE_ORCHESTRATION_V1]
---

# Pipeline Orchestration Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:PIPELINE_ORCHESTRATION_V1]
```

This occurs when:
- User says "begin automated development" or "start pipeline"
- Phase 2 is complete
- User wants full automation from Phase 5-11

# Pipeline Orchestrator Skill

## What This Skill Does

The **Pipeline Orchestrator** is the master controller for fully automated development from Phase 5 through Phase 11. It:

- **Monitors completion signals** from each phase
- **Automatically triggers** the next phase skill
- **Handles errors gracefully** with automatic recovery or human escalation
- **Preserves state** through checkpointing
- **Provides progress dashboard** with real-time status
- **Fully autonomous** from Phase 6 through deployment (no manual gates)

## When This Skill Activates

**Primary Trigger:** User completes Phase 2 (PRD creation, human validation, checkpoint passed)

**Activation Phrases:**
- "Begin automated development"
- "Start the pipeline"
- "Automate phases 5 through 11"
- "Run full development pipeline"
- "Phase 2 is complete, start automation"

**Prerequisites:**
- ✅ `.taskmaster/scripts/phase2-checkpoint.sh` passed
- ✅ `.taskmaster/tasks.json` exists and validated
- ✅ `.taskmaster/docs/phase2-signoff.md` exists
- ✅ Git repository clean state

## Pipeline Architecture

```
Phase 2 (Human) ────────────────────────┐
  ✅ Checkpoint Passed                   │ MANUAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ↓                        │
Phase 5: Task Decomposition             │ APPROVAL
  Skill: Task-Decomposer                │ (user approves tasks)
  Output: .signals/phase5-complete.json │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ↓                        │
Phase 6: Spec Generation                │
  Skill: Spec-Generator                 │
  Output: .signals/phase6-specs-created.json │
                ↓                        │
Phase 7: Implementation                 │
  Skill: TDD-Implementer                │ FULLY
  Output: .signals/phase7-complete.json │ AUTONOMOUS
                ↓                        │
Phase 9: Integration Testing            │
  Skill: Integration-Tester             │
  Output: .signals/phase9-complete.json │
                ↓                        │
Phase 10: E2E & Production Validation   │
  Skill: E2E-Prod-Validator             │
  Output: .signals/phase10-complete.json │
                ↓                        │
Phase 11: Deployment & Infrastructure   │
  Skill: Deployment-Orchestrator        │
  Includes: Docker build & health check  │
  Output: .signals/phase11-complete.json │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                ↓
        ✅ DEPLOYED TO PRODUCTION
```

## Completion Signal System

Each phase skill generates a completion signal file when done:

### Phase 5 Signal
```json
{
  "phase": 5,
  "phase_name": "Task Decomposition",
  "status": "success",
  "completed_at": "2025-10-29T15:30:00Z",
  "duration_minutes": 12,
  "summary": {
    "tasks_analyzed": 18,
    "tasks_expanded": 8,
    "subtasks_generated": 34,
    "high_complexity_tasks": [3, 5, 7, 9, 12, 15, 18, 22]
  },
  "next_phase": 6,
  "trigger_next": true
}
```

### Phase 6 Signal
```json
{
  "phase": 6,
  "phase_name": "Spec Generation",
  "status": "success",
  "completed_at": "2025-10-29T16:45:00Z",
  "duration_minutes": 45,
  "summary": {
    "tasks_processed": 18,
    "proposals_created": 15,
    "tightly_coupled": 10,
    "loosely_coupled": 5,
    "batches_completed": 3
  },
  "next_phase": 7,
  "trigger_next": true
}
```

### Phase 7 Signal
```json
{
  "phase": 7,
  "phase_name": "Implementation",
  "status": "success",
  "completed_at": "2025-10-29T19:30:00Z",
  "duration_minutes": 165,
  "summary": {
    "subtasks_implemented": 34,
    "tests_written": 187,
    "tests_passing": 187,
    "code_coverage": {
      "line": 87,
      "branch": 76
    },
    "implementation_strategy": "worktree-isolation"
  },
  "next_phase": 9,
  "trigger_next": true
}
```

### Phase 9 Signal
```json
{
  "phase": 9,
  "phase_name": "Integration Testing",
  "status": "success",
  "completed_at": "2025-10-29T20:15:00Z",
  "duration_minutes": 45,
  "summary": {
    "integration_points_total": 12,
    "integration_points_tested": 12,
    "integration_tests_passing": 12,
    "coverage": "100%"
  },
  "next_phase": 10,
  "trigger_next": true
}
```

### Phase 10 Signal
```json
{
  "phase": 10,
  "phase_name": "E2E & Production Validation",
  "status": "success",
  "completed_at": "2025-10-29T21:30:00Z",
  "duration_minutes": 75,
  "summary": {
    "e2e_workflows_tested": 8,
    "e2e_tests_passing": 8,
    "production_readiness_score": 94,
    "blocking_issues": 0
  },
  "next_phase": 11,
  "trigger_next": true
}
```

### Phase 11 Signal
```json
{
  "phase": 11,
  "phase_name": "Deployment",
  "status": "success",
  "completed_at": "2025-10-29T23:00:00Z",
  "duration_minutes": 90,
  "summary": {
    "staging_deployed": true,
    "staging_validated": true,
    "production_deployed": true,
    "deployment_strategy": "canary",
    "rollback_tested": true
  },
  "next_phase": null,
  "trigger_next": false,
  "pipeline_complete": true
}
```

### Error Signal
```json
{
  "phase": 7,
  "phase_name": "Implementation",
  "status": "error",
  "failed_at": "2025-10-29T18:15:00Z",
  "error": {
    "type": "test_failure",
    "message": "5 tests failing in user authentication module",
    "recovery_attempted": true,
    "recovery_successful": false,
    "requires_human": true
  },
  "checkpoint": ".taskmaster/.checkpoints/phase7-checkpoint-5.json",
  "next_action": "Fix failing tests, then resume from checkpoint"
}
```

## Phase Transition Rules

### Phase 5 → Phase 6 Transition
```yaml
Triggers when:
  - ✅ .taskmaster/.signals/phase5-complete.json exists
  - ✅ status = "success"
  - ✅ trigger_next = true
  - ✅ All high-complexity tasks expanded

Action:
  - Load Phase 6 context
  - Activate Spec-Generator skill
  - Monitor for phase6-complete.json
```

### Phase 6 → Phase 7 Transition
```yaml
Triggers when:
  - ✅ .taskmaster/.signals/phase6-complete.json exists
  - ✅ status = "success"
  - ✅ trigger_next = true
  - ✅ All OpenSpec proposals created

Action:
  - Load Phase 7 context
  - Activate TDD-Implementer skill
  - Monitor for phase7-complete.json
```

### Phase 7 → Phase 9 Transition
```yaml
Triggers when:
  - ✅ .taskmaster/.signals/phase7-complete.json exists
  - ✅ status = "success"
  - ✅ trigger_next = true
  - ✅ All tests passing
  - ✅ Coverage ≥80% line, ≥70% branch

Action:
  - Load Phase 9 context
  - Activate Integration-Tester skill
  - Monitor for phase9-complete.json
```

### Phase 9 → Phase 10 Transition
```yaml
Triggers when:
  - ✅ .taskmaster/.signals/phase9-complete.json exists
  - ✅ status = "success"
  - ✅ trigger_next = true
  - ✅ 100% integration point coverage

Action:
  - Load Phase 10 context
  - Activate E2E-Prod-Validator skill
  - Monitor for phase10-complete.json
```

### Phase 10 → Phase 11 Transition (AUTOMATIC)
```yaml
Triggers when:
  - ✅ .taskmaster/.signals/phase10-complete.json exists
  - ✅ status = "success"
  - ✅ production_readiness_score ≥90%

Action:
  - Log Phase 10 summary
  - Automatically activate Deployment-Orchestrator skill
  - Pipeline proceeds to production deployment
```

## Error Handling Strategy

### Automatic Recovery (Skill Attempts First)

**Category 1: Dependency Issues**
```yaml
Error: "npm: command not found"
Recovery:
  - Detect package manager needed
  - Install via appropriate method
  - Retry operation
  - If success: Continue
  - If failure: Escalate to human
```

**Category 2: Test Failures**
```yaml
Error: "5 tests failing in authentication module"
Recovery:
  - Analyze test errors
  - Attempt automatic fixes (if safe):
    - Update test expectations
    - Fix obvious typos
    - Add missing mocks
  - If fixes succeed: Re-run tests
  - If still failing: Escalate to human with detailed report
```

**Category 3: Transient Failures**
```yaml
Error: "Network timeout", "Rate limit hit"
Recovery:
  - Wait exponentially (1min, 2min, 4min)
  - Retry operation up to 3 times
  - If success: Continue
  - If still failing: Escalate to human
```

### Human Escalation (Cannot Proceed)

**Category 1: Ambiguous Decisions**
```yaml
Scenario: "Two equally valid implementation approaches"
Action:
  - Pause pipeline
  - Present options with pros/cons
  - Wait for human decision
  - Resume with selected approach
```

**Category 2: Critical Errors**
```yaml
Scenario: "Git repository corrupted", "Database connection failed"
Action:
  - Save checkpoint immediately
  - Halt pipeline
  - Report error details
  - Provide recovery steps
  - Wait for human intervention
```

**Category 3: Unknown Errors**
```yaml
Scenario: "Unexpected error not covered by recovery rules"
Action:
  - Save checkpoint
  - Log full error trace
  - Halt pipeline
  - Report to human with context
```

## Checkpoint System

### Checkpoint Files
```
.taskmaster/.checkpoints/
├── phase5-checkpoint-1.json  (after complexity analysis)
├── phase5-checkpoint-2.json  (after task 5 expanded)
├── phase5-checkpoint-3.json  (after task 10 expanded)
├── phase6-checkpoint-1.json  (after batch 1 complete)
├── phase6-checkpoint-2.json  (after batch 2 complete)
├── phase7-checkpoint-1.json  (after task 3 implemented)
├── phase7-checkpoint-2.json  (after task 7 implemented)
└── ...
```

### Checkpoint Schema
```json
{
  "phase": 6,
  "checkpoint_number": 3,
  "created_at": "2025-10-29T16:20:00Z",
  "state": {
    "current_operation": "Creating OpenSpec proposal for task #9",
    "completed_operations": [
      "Analyzed coupling for batch 1 (tasks 1-5)",
      "Created 5 OpenSpec proposals",
      "Analyzed coupling for batch 2 (tasks 6-10)",
      "Created 3 OpenSpec proposals"
    ],
    "pending_operations": [
      "Create proposal for task #9",
      "Create proposal for task #10",
      "Start batch 3 (tasks 11-15)"
    ]
  },
  "resume_command": "Continue Phase 6 from checkpoint 3: task #9"
}
```

### Resume from Checkpoint
```bash
# If pipeline interrupted, resume with:
# "Resume pipeline from last checkpoint"

# Orchestrator will:
1. Find most recent checkpoint
2. Load saved state
3. Resume from exact point of interruption
4. Continue pipeline execution
```

## Progress Dashboard

While pipeline runs, orchestrator provides real-time updates:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATED DEVELOPMENT PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 2: Discovery                   ✅ COMPLETE
Phase 5: Task Decomposition          ✅ COMPLETE (12 min)
Phase 6: Spec Generation             ✅ COMPLETE (45 min)
Phase 7: Implementation              🔄 IN PROGRESS (87 min)
  └─ Task 15/18 complete
  └─ 127/187 tests passing
  └─ Coverage: 82% line, 74% branch
Phase 8: Code Review                 ⏸️  PENDING
Phase 9: Integration Testing         ⏸️  PENDING
Phase 10: E2E & Validation           ⏸️  PENDING
Phase 11: Deployment                 ⏸️  PENDING

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Elapsed Time: 144 minutes
Estimated Remaining: 156 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Usage Examples

### Example 1: Full Pipeline Automation

**User (after Phase 2 complete):**
```
I've completed Phase 2 and the checkpoint passed. Begin automated development pipeline.
```

**Orchestrator Response:**
```
✅ Phase 2 Checkpoint Verified
   - tasks.json: 18 tasks validated
   - PRD: Complete
   - Sign-off: Obtained

🚀 Starting Automated Development Pipeline

Phase 5: Task Decomposition
  → Activating Task-Decomposer skill...
  → Analyzing complexity for 18 tasks...
  → Expanding high-complexity tasks...
  ✅ Phase 5 Complete (12 minutes)
     - 8 tasks expanded into 34 subtasks
     - Signal: phase5-complete.json generated

Phase 6: Spec Generation
  → Activating Spec-Generator skill...
  → Analyzing coupling for batch 1 (tasks 1-5)...
  → Creating OpenSpec proposals...
  → Batch 1 complete (5 proposals)
  → Processing batch 2...
  [continues automatically...]
```

### Example 2: Error Recovery

**Orchestrator detects error:**
```
⚠️ Phase 7 Error Detected
   Error: 5 tests failing in user authentication module

🔄 Attempting Automatic Recovery
   → Analyzing test failures...
   → Identified: Missing mock for database connection
   → Adding mock configuration...
   → Re-running tests...
   ✅ Recovery Successful - All tests passing

Resuming Phase 7 Implementation...
```

### Example 3: Human Escalation

**Orchestrator encounters unknown error:**
```
🚨 Phase 7 Error - Human Intervention Required

Error Details:
  Phase: 7 (Implementation)
  Operation: Implementing task #12
  Error: Unable to resolve dependency conflict

Checkpoint Saved: .taskmaster/.checkpoints/phase7-checkpoint-7.json

Options:
A) Manually resolve the dependency conflict
B) Skip task #12 for now (resume later)
C) Abort pipeline

Please respond: A, B, or C
```

### Example 4: Phase 10 → Phase 11 Auto-Transition

**Orchestrator completes Phase 10:**
```
✅ Phase 10 Complete: E2E & Production Validation

Production Readiness Score: 94%

Summary:
  - All E2E tests passing (8/8 workflows)
  - Integration tests: 100% coverage
  - Test coverage: 87% line, 76% branch
  - Security scans: PASSED
  - No blocking issues

🚀 Auto-proceeding to Phase 11: Deployment

[ACTIVATE:DEPLOYMENT_ORCHESTRATOR_V1]
```

## Worktree Isolation Strategy

**ALL development must happen in isolated git worktrees - NO exceptions.**

### Worktree Management
- Each phase operates in its dedicated worktree: `phase-X-task-Y`
- Orchestrator automatically creates worktrees before activating skills
- Worktree boundaries are strictly enforced
- No cross-worktree contamination allowed

### Phase-Worktree Mapping
1. **Phase 5**: Creates `phase-5-task-1` worktree for task decomposition
2. **Phase 6**: Creates individual worktrees per task batch: `phase-6-task-N`
3. **Phase 7**: Each subtask gets isolated worktree: `phase-7-task-N`
4. **Phase 9**: Integration testing in `phase-9-task-1` worktree
5. **Phase 10**: E2E validation in `phase-10-task-1` worktree
6. **Phase 11**: Deployment from `phase-11-task-1` worktree

### Worktree Lifecycle
```bash
# Before each phase activation:
./lib/worktree-manager.sh create <phase> <task>
cd ./worktrees/phase-<phase>-task-<task>

# Phase execution with isolation enforcement
./hooks/worktree-enforcer.sh enforce

# After phase completion:
./lib/worktree-manager.sh merge phase-<phase>-task-<task>
./lib/worktree-manager.sh cleanup phase-<phase>-task-<task>
```

## Skill Coordination

The orchestrator manages these phase skills with strict worktree isolation:

1. **Task-Decomposer** (Phase 5) - Worktree: `phase-5-task-1`
2. **Spec-Generator** (Phase 6) - Worktrees: `phase-6-task-N` per batch
3. **TDD-Implementer** (Phase 7) - Worktrees: `phase-7-task-N` per subtask
4. **Integration-Tester** (Phase 9) - Worktree: `phase-9-task-1`
5. **E2E-Prod-Validator** (Phase 10) - Worktree: `phase-10-task-1`
6. **Deployment-Orchestrator** (Phase 11) - Worktree: `phase-11-task-1`

Each skill:
- Receives worktree context from orchestrator
- Validates worktree isolation before execution
- Executes its phase in dedicated worktree
- Generates completion signal when done
- Merges changes back to main branch
- Cleans up worktree after successful merge

## Success Criteria

Pipeline is successful when:
- ✅ All 12 phases complete without errors
- ✅ All tests passing (unit, integration, E2E)
- ✅ Production readiness score ≥90%
- ✅ GO decision from Phase 10
- ✅ Successfully deployed to production
- ✅ All validation gates passed

## See Also

- `/DEVELOPMENT_WORKFLOW.md` - Complete workflow documentation
- `/phase2-checkpoint.sh` - Phase 2 verification script
- `/.taskmaster/.signals/` - Completion signal files
- `/.taskmaster/.checkpoints/` - Pipeline checkpoints