---
name: workflow-state-manager
description: |
  Manages workflow state persistence and session recovery for sp.autonomous.
  Tracks phase progress, feature completion, and provides resume capability.
  Triggers: workflow state, session recovery, resume autonomous, progress tracking
version: 1.0.0
---

# Workflow State Manager

> **Ensures sp.autonomous can resume after interruption by persisting workflow state.**

---

## Overview

This skill manages the workflow state for the `/sp.autonomous` command, providing:
- **Phase tracking**: Current phase, completed phases, in-progress phases
- **Feature tracking**: For complex projects with multiple features
- **Session recovery**: Resume from interruption point
- **Progress logging**: Detailed step-by-step history
- **Artifact verification**: Check what work has been completed

---

## Core State File

**Location**: `.specify/workflow-state.json`

**Structure**:
```json
{
  "version": "2.0",
  "last_updated": "2026-01-22T10:30:00Z",
  "current_phase": 11,
  "project_type": "COMPLEX",
  "session_id": "session-20260122-103000",
  "phases_completed": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  "phases_in_progress": [11],
  "total_phases": 13,
  "complexity": "COMPLEX",
  "features": {
    "total": 3,
    "completed": ["F-01"],
    "current": "F-02",
    "pending": ["F-03"]
  },
  "artifacts": {
    "constitution": true,
    "spec": true,
    "plan": true,
    "tasks": true,
    "implementation_started": true,
    "tests_passing": false
  },
  "validation_status": {
    "last_validation_phase": 10,
    "last_validation_grade": "B",
    "validation_reports": [
      ".specify/validations/phase-10-report.md"
    ]
  },
  "resume_capability": {
    "can_resume": true,
    "resume_point": "Phase 11: Feature F-02 Implementation - Task 5 of 12",
    "resume_instructions": "Continue implementing F-02 tasks starting from T-F-02-005"
  }
}
```

---

## Progress Log File

**Location**: `.specify/workflow-progress.log`

**Format**: Timestamped chronological log of all workflow steps

```
[2026-01-22T10:00:00Z] SESSION_START session-20260122-100000
[2026-01-22T10:00:05Z] PHASE_START phase=1 name=INIT
[2026-01-22T10:00:30Z] PHASE_COMPLETE phase=1 grade=A
[2026-01-22T10:00:31Z] PHASE_START phase=2 name=ANALYZE_PROJECT
[2026-01-22T10:01:15Z] PHASE_COMPLETE phase=2 grade=B
[2026-01-22T10:01:16Z] PHASE_START phase=3 name=ANALYZE_REQUIREMENTS
[2026-01-22T10:02:00Z] PHASE_COMPLETE phase=3 grade=A
[2026-01-22T10:02:01Z] COMPLEXITY_DETECTED type=COMPLEX features=3
[2026-01-22T10:02:05Z] PHASE_START phase=7.5 name=FEATURE_BREAKDOWN
[2026-01-22T10:03:00Z] PHASE_COMPLETE phase=7.5 grade=A
[2026-01-22T10:03:05Z] FEATURE_START feature=F-01 name="User Authentication"
[2026-01-22T10:03:10Z] PHASE_START phase=8 feature=F-01 name=FEATURE_SPEC
[2026-01-22T10:04:00Z] PHASE_COMPLETE phase=8 feature=F-01 grade=B
[2026-01-22T10:04:05Z] PHASE_START phase=9 feature=F-01 name=FEATURE_PLAN
...
[2026-01-22T10:30:00Z] TASK_START task=T-F-02-005 name="Implement getTodos endpoint"
[2026-01-22T10:30:45Z] SESSION_INTERRUPT reason="User closed laptop"
```

---

## Workflow Functions

### 1. Initialize Workflow State

```typescript
function initializeWorkflowState(requirementsFile: string): WorkflowState {
  const state: WorkflowState = {
    version: "2.0",
    last_updated: new Date().toISOString(),
    current_phase: 0,
    project_type: "unknown",
    session_id: `session-${Date.now()}`,
    phases_completed: [],
    phases_in_progress: [],
    total_phases: 13,
    complexity: "SIMPLE",
    features: {
      total: 0,
      completed: [],
      current: null,
      pending: []
    },
    artifacts: {
      constitution: false,
      spec: false,
      plan: false,
      tasks: false,
      implementation_started: false,
      tests_passing: false
    },
    validation_status: {
      last_validation_phase: null,
      last_validation_grade: null,
      validation_reports: []
    },
    resume_capability: {
      can_resume: false,
      resume_point: null,
      resume_instructions: null
    }
  }

  writeFile('.specify/workflow-state.json', JSON.stringify(state, null, 2))
  logProgress('SESSION_START', { session_id: state.session_id })

  return state
}
```

### 2. Update Phase Progress

```typescript
function updatePhaseProgress(
  phase: number,
  status: 'start' | 'complete' | 'fail',
  feature?: string,
  grade?: string
): void {
  const state = readWorkflowState()

  if (status === 'start') {
    state.current_phase = phase
    state.phases_in_progress.push(phase)
    logProgress('PHASE_START', { phase, feature })
  } else if (status === 'complete') {
    state.phases_completed.push(phase)
    state.phases_in_progress = state.phases_in_progress.filter(p => p !== phase)

    if (grade) {
      state.validation_status.last_validation_phase = phase
      state.validation_status.last_validation_grade = grade
    }

    logProgress('PHASE_COMPLETE', { phase, feature, grade })
  } else if (status === 'fail') {
    logProgress('PHASE_FAIL', { phase, feature, grade })
  }

  state.last_updated = new Date().toISOString()
  updateResumePoint(state)
  writeFile('.specify/workflow-state.json', JSON.stringify(state, null, 2))
}
```

### 3. Update Feature Progress

```typescript
function updateFeatureProgress(
  featureId: string,
  status: 'start' | 'complete'
): void {
  const state = readWorkflowState()

  if (status === 'start') {
    state.features.current = featureId
    logProgress('FEATURE_START', { feature: featureId })
  } else if (status === 'complete') {
    state.features.completed.push(featureId)
    state.features.pending = state.features.pending.filter(f => f !== featureId)

    // Move to next feature
    const nextFeature = state.features.pending[0] || null
    state.features.current = nextFeature

    logProgress('FEATURE_COMPLETE', { feature: featureId })
  }

  state.last_updated = new Date().toISOString()
  updateResumePoint(state)
  writeFile('.specify/workflow-state.json', JSON.stringify(state, null, 2))
}
```

### 4. Generate Resume Instructions

```typescript
function updateResumePoint(state: WorkflowState): void {
  // Determine resume point based on current state

  if (state.complexity === 'COMPLEX' && state.features.current) {
    const currentFeature = state.features.current
    const currentPhase = state.current_phase

    // Check task progress within feature
    const tasksFile = `.specify/features/${currentFeature}/tasks.md`
    const completedTasks = countCompletedTasks(tasksFile)
    const totalTasks = countTotalTasks(tasksFile)

    state.resume_capability = {
      can_resume: true,
      resume_point: `Phase ${currentPhase}: Feature ${currentFeature} - Task ${completedTasks} of ${totalTasks}`,
      resume_instructions: `Continue implementing ${currentFeature} starting from task ${completedTasks + 1}`
    }
  } else if (state.current_phase > 0) {
    const phaseNames = {
      1: 'INIT',
      2: 'ANALYZE_PROJECT',
      3: 'ANALYZE_REQUIREMENTS',
      4: 'GAP_ANALYSIS',
      5: 'GENERATE_SKILLS',
      7: 'CONSTITUTION',
      8: 'SPEC',
      9: 'PLAN',
      10: 'TASKS',
      11: 'IMPLEMENT',
      12: 'QA',
      13: 'DELIVER'
    }

    state.resume_capability = {
      can_resume: true,
      resume_point: `Phase ${state.current_phase}: ${phaseNames[state.current_phase]}`,
      resume_instructions: `Resume from phase ${state.current_phase}`
    }
  }
}
```

### 5. Detect Current State

```typescript
function detectCurrentState(): WorkflowState {
  /**
   * Detect workflow state from filesystem artifacts.
   * Used when workflow-state.json is missing or corrupted.
   */

  const state: WorkflowState = {
    version: "2.0",
    last_updated: new Date().toISOString(),
    current_phase: 0,
    project_type: "unknown",
    session_id: null,
    phases_completed: [],
    phases_in_progress: [],
    total_phases: 13,
    complexity: "SIMPLE",
    features: { total: 0, completed: [], current: null, pending: [] },
    artifacts: {
      constitution: false,
      spec: false,
      plan: false,
      tasks: false,
      implementation_started: false,
      tests_passing: false
    },
    validation_status: {
      last_validation_phase: null,
      last_validation_grade: null,
      validation_reports: []
    },
    resume_capability: {
      can_resume: false,
      resume_point: null,
      resume_instructions: null
    }
  }

  // Check phase artifacts
  if (fileExists('.specify') && fileExists('.claude')) {
    state.phases_completed.push(1)
    state.current_phase = 1
  }

  if (fileExists('.specify/project-analysis.json')) {
    state.phases_completed.push(2)
    state.current_phase = 2
  }

  if (fileExists('.specify/requirements-analysis.json')) {
    state.phases_completed.push(3)
    state.current_phase = 3
  }

  if (fileExists('.specify/feature-breakdown.json')) {
    state.complexity = 'COMPLEX'
    state.project_type = 'COMPLEX'

    // Load feature breakdown
    const breakdown = JSON.parse(readFile('.specify/feature-breakdown.json'))
    state.features.total = breakdown.total_features
    state.features.completed = breakdown.completed_features || []
    state.features.current = breakdown.current_feature
    state.features.pending = breakdown.features
      .filter(f => f.status !== 'complete')
      .map(f => f.id)
  }

  if (fileExists('.specify/constitution.md')) {
    state.phases_completed.push(7)
    state.current_phase = 7
    state.artifacts.constitution = true
  }

  if (fileExists('.specify/spec.md')) {
    state.artifacts.spec = true
    state.current_phase = 8
  }

  if (fileExists('.specify/plan.md')) {
    state.artifacts.plan = true
    state.current_phase = 9
  }

  if (fileExists('.specify/tasks.md')) {
    state.artifacts.tasks = true
    state.current_phase = 10
  }

  // Check if implementation started
  if (fileExists('src/') || fileExists('lib/')) {
    state.artifacts.implementation_started = true
    state.current_phase = 11
  }

  updateResumePoint(state)

  return state
}
```

### 6. Log Progress

```typescript
function logProgress(event: string, data: Record<string, any>): void {
  const timestamp = new Date().toISOString()
  const logEntry = `[${timestamp}] ${event} ${JSON.stringify(data)}\n`

  appendFile('.specify/workflow-progress.log', logEntry)
}
```

### 7. Generate Resume Report

```typescript
function generateResumeReport(): string {
  const state = readWorkflowState()

  let report = `
╔════════════════════════════════════════════════════════════════════════════╗
║                    WORKFLOW RESUME REPORT                                   ║
╠════════════════════════════════════════════════════════════════════════════╣

Project Type: ${state.complexity}
Current Phase: ${state.current_phase}
Phases Completed: ${state.phases_completed.join(', ')}

`

  if (state.complexity === 'COMPLEX') {
    report += `
Features:
  Total: ${state.features.total}
  Completed: ${state.features.completed.join(', ') || 'None'}
  Current: ${state.features.current || 'None'}
  Pending: ${state.features.pending.join(', ') || 'None'}

`
  }

  report += `
Artifacts:
  ✓ Constitution: ${state.artifacts.constitution ? 'YES' : 'NO'}
  ✓ Spec: ${state.artifacts.spec ? 'YES' : 'NO'}
  ✓ Plan: ${state.artifacts.plan ? 'YES' : 'NO'}
  ✓ Tasks: ${state.artifacts.tasks ? 'YES' : 'NO'}
  ✓ Implementation: ${state.artifacts.implementation_started ? 'STARTED' : 'NOT STARTED'}
  ✓ Tests Passing: ${state.artifacts.tests_passing ? 'YES' : 'NO'}

Resume Point:
  ${state.resume_capability.resume_point || 'N/A'}

Instructions:
  ${state.resume_capability.resume_instructions || 'Start from Phase 0'}

Last Updated: ${state.last_updated}
Last Validation: Phase ${state.validation_status.last_validation_phase || 'N/A'} - Grade ${state.validation_status.last_validation_grade || 'N/A'}

╚════════════════════════════════════════════════════════════════════════════╝
`

  return report
}
```

---

## Integration with sp.autonomous

### Phase 0: Check for Existing State

```bash
#!/bin/bash

echo "Checking for existing workflow state..."

if [ -f ".specify/workflow-state.json" ]; then
    echo "Found existing workflow state. Analyzing..."

    # Show resume report
    cat .specify/workflow-state.json | jq -r '.resume_capability.resume_point'

    # Ask user if they want to resume
    read -p "Resume from this point? (y/n): " RESUME

    if [ "$RESUME" = "y" ]; then
        RESUME_MODE=true
    else
        RESUME_MODE=false
        # Backup old state
        mv .specify/workflow-state.json .specify/workflow-state-$(date +%Y%m%d-%H%M%S).json.bak
    fi
else
    echo "No existing workflow state. Starting fresh."
    RESUME_MODE=false
fi
```

### After Each Phase: Update State

```typescript
// At the end of each phase execution

// Example: Phase 8 (SPEC) completes
updatePhaseProgress(8, 'complete', currentFeature, 'B')

// Example: Phase 11 (IMPLEMENT) starts
updatePhaseProgress(11, 'start', currentFeature)

// Example: Feature F-02 completes
updateFeatureProgress('F-02', 'complete')
```

### Session Interrupt Handler

```bash
# Add to sp.autonomous command

trap 'on_interrupt' INT TERM

function on_interrupt() {
    echo ""
    echo "Session interrupted. Saving state..."

    # Log interrupt
    echo "[$(date -Iseconds)] SESSION_INTERRUPT reason=\"User stopped process\"" >> .specify/workflow-progress.log

    # Generate resume report
    echo ""
    echo "Workflow state saved. To resume:"
    echo "  /sp.autonomous [requirements-file]"
    echo ""
    echo "Resume report:"
    cat .specify/workflow-state.json | jq -r '.resume_capability'

    exit 0
}
```

---

## Resume Workflow

### Step 1: Load State

```typescript
function resumeWorkflow(requirementsFile: string): void {
  let state: WorkflowState

  if (fileExists('.specify/workflow-state.json')) {
    state = JSON.parse(readFile('.specify/workflow-state.json'))
    console.log('Resuming from saved state')
  } else {
    console.log('No saved state. Detecting from artifacts...')
    state = detectCurrentState()
  }

  // Display resume report
  console.log(generateResumeReport())

  // Continue from resume point
  continueFromPhase(state.current_phase, state)
}
```

### Step 2: Validate Resume Point

```typescript
function validateResumePoint(state: WorkflowState): boolean {
  /**
   * Verify that artifacts match the claimed phase.
   * Prevents resuming from invalid state.
   */

  const requiredArtifacts = {
    7: ['.specify/constitution.md'],
    8: ['.specify/spec.md'],
    9: ['.specify/plan.md'],
    10: ['.specify/tasks.md'],
    11: ['src/']
  }

  const phase = state.current_phase
  const required = requiredArtifacts[phase] || []

  for (const artifact of required) {
    if (!fileExists(artifact)) {
      console.error(`Missing artifact: ${artifact}`)
      console.error(`Cannot resume from phase ${phase}`)
      return false
    }
  }

  return true
}
```

### Step 3: Continue Execution

```typescript
function continueFromPhase(phase: number, state: WorkflowState): void {
  if (!validateResumePoint(state)) {
    console.log('Resuming from detected safe point instead')
    phase = findSafeResumePhase(state)
  }

  console.log(`Continuing from Phase ${phase}`)

  // Execute workflow starting from this phase
  switch (phase) {
    case 0:
    case 1:
      executePhase1()
      break
    case 2:
      executePhase2()
      break
    // ... continue
    case 11:
      if (state.complexity === 'COMPLEX') {
        const currentFeature = state.features.current
        resumeFeatureImplementation(currentFeature, state)
      } else {
        executePhase11()
      }
      break
  }
}
```

---

## Best Practices

### 1. Update State Frequently

```typescript
// Update after EVERY significant step
updatePhaseProgress(phase, 'start')
// ... do work ...
updatePhaseProgress(phase, 'complete', null, grade)
```

### 2. Log Everything

```typescript
// Log all important events
logProgress('TASK_START', { task: 'T-F-02-005' })
logProgress('SKILL_LOADED', { skill: 'api-patterns' })
logProgress('TEST_PASS', { test: 'user.test.ts' })
logProgress('VALIDATION_COMPLETE', { phase: 11, grade: 'B' })
```

### 3. Validate Before Resume

```typescript
// Always validate state before resuming
if (!validateResumePoint(state)) {
  // Fall back to safe resume point
  state = detectCurrentState()
}
```

### 4. Backup State Periodically

```bash
# Backup workflow state every 5 phases
if [ $((PHASE % 5)) -eq 0 ]; then
    cp .specify/workflow-state.json .specify/workflow-state-backup.json
fi
```

---

## Anti-Patterns

### ❌ Don't Skip State Updates

```typescript
// BAD: Completing phase without updating state
executePhase8()
// State not updated!

// GOOD
executePhase8()
updatePhaseProgress(8, 'complete', null, 'B')
```

### ❌ Don't Assume State is Accurate

```typescript
// BAD: Blindly trust workflow-state.json
const state = JSON.parse(readFile('.specify/workflow-state.json'))
continueFromPhase(state.current_phase)

// GOOD: Validate first
const state = JSON.parse(readFile('.specify/workflow-state.json'))
if (validateResumePoint(state)) {
  continueFromPhase(state.current_phase)
} else {
  state = detectCurrentState()
  continueFromPhase(state.current_phase)
}
```

### ❌ Don't Forget to Handle Interrupts

```bash
# BAD: No interrupt handler
/sp.autonomous requirements.md
# User closes laptop - state not saved

# GOOD: Trap signals
trap 'on_interrupt' INT TERM
/sp.autonomous requirements.md
```

---

## Validation Checklist

- [ ] workflow-state.json updated after each phase
- [ ] Progress logged to workflow-progress.log
- [ ] Resume point updated correctly
- [ ] Feature progress tracked (for COMPLEX projects)
- [ ] Artifacts verified before resume
- [ ] Interrupt handler installed
- [ ] Resume report generated on interrupt
- [ ] State backup created periodically
