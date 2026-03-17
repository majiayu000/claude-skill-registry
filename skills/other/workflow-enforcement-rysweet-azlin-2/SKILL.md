---
name: workflow-enforcement
version: 1.1.0
description: Workflow step compliance guidance with mandatory step reminders and visual progress tracking. Reminds Claude to complete all workflow steps before PR creation.
auto_activates:
  - "start workflow"
  - "beginning DEFAULT_WORKFLOW"
  - "Step 0: Workflow Preparation"
explicit_triggers:
  - /amplihack:workflow-enforcement
related_files:
  - .claude/workflow/DEFAULT_WORKFLOW.md
  - .claude/tools/amplihack/hooks/workflow_tracker.py
  - .claude/tools/amplihack/considerations.yaml
  - .claude/templates/workflow_state.yaml.template
implementation_status: specification
---

# Workflow Enforcement Skill

## Purpose

Guides Claude to complete all workflow steps by:

1. Reminding about step completion tracking (use TodoWrite or `.claude/runtime/workflow_state.yaml`)
2. Emphasizing mandatory steps (0, 10, 16-17) that must not be skipped
3. Providing visual progress indicator format
4. Defining expected blocking behavior at checkpoints

**Implementation Status**: This skill is currently a SPECIFICATION that guides Claude behavior. Actual blocking enforcement requires either:

- Claude self-compliance (current state)
- Future: Pre-commit hooks or CI checks (not yet implemented)

## The Problem (Issue #1607)

Agents routinely skip mandatory workflow steps, especially:

- **Step 0**: Workflow Preparation - Create todos for ALL steps (MANDATORY)
- **Step 10**: Pre-commit code review (MANDATORY)
- **Step 16**: PR review (MANDATORY)
- **Step 17**: Review feedback implementation (MANDATORY)

Root causes:

- **Completion Bias**: Agent considers "PR created" as completion instead of "PR merged after review"
- **Context Decay**: After heavy implementation, agent loses sight of remaining steps
- **Autonomy Misapplication**: Confuses "autonomous implementation" with "skip mandatory process"

## Philosophy Alignment and Honest Limitations

### The Irony

This skill was created because an agent skipped workflow steps while building a feature. The same cognitive patterns that cause step-skipping can also cause this skill to be ignored. We acknowledge this limitation directly.

### What This Skill CAN Do

- Provide clear guidance patterns for Claude to follow
- Define standard formats for progress tracking
- Establish checkpoints where Claude SHOULD pause and validate
- Integrate with power_steering for session-end verification
- Document the expected behavior for future agents

### What This Skill CANNOT Do

- Force Claude to read this skill (relies on auto-activation triggers)
- Prevent Claude from skipping steps if it "decides" to be autonomous
- Hard-block operations (no pre-commit hooks implemented yet)
- Catch workflow violations in real-time (only session-end checks exist)

### Philosophy Alignment

| Principle                  | How This Skill Aligns                                 |
| -------------------------- | ----------------------------------------------------- |
| **Ruthless Simplicity**    | Single YAML file for state; no complex infrastructure |
| **Zero-BS Implementation** | Honest about being guidance, not enforcement          |
| **Modular Design**         | Self-contained skill with clear integration points    |
| **Fail-Open**              | On errors, log and continue; never block users        |

**Self-Aware Note**: This skill is itself a brick that could be regenerated from its specification. It does not contain executable code - it is documentation that guides Claude's behavior through loaded context.

## How to Use This Skill

### Step-by-Step Instructions

#### At Workflow Start (Step 0)

1. **Initialize state tracking** (choose one):

   **Option A - TodoWrite (Recommended)**:

   ```
   Create TodoWrite entries for ALL 22 steps (0-21):
   - "Step 0: Workflow Preparation - Create todos for ALL steps"
   - "Step 1: Prepare the Workspace"
   - ...
   - "Step 21: Ensure PR is Mergeable - TASK COMPLETION"
   ```

   **Option B - YAML state file**:

   ```bash
   cp .claude/templates/workflow_state.yaml.template \
      .claude/runtime/workflow_state.yaml
   # Edit workflow_id, task_description, started_at
   ```

2. **Display initial progress**:

   ```
   WORKFLOW PROGRESS [0/22] [.......................] Step 0: Workflow Preparation
   Mandatory gates: Step 0 (Prep), Step 10 (Review), Step 16 (PR Review), Step 17 (Feedback)
   ```

3. **Verify initialization**: Confirm 22 todo items exist before proceeding.

#### At Each Step Completion

1. Mark step as `completed` in TodoWrite or YAML
2. Update `current_step` to next step number
3. Display progress indicator
4. If approaching mandatory step (10, 16, 17), display reminder

#### At Mandatory Checkpoints

**Before Step 15 (Open PR as Draft)**:

```
+------------------------------------------------------------------+
|  CHECKPOINT: Pre-PR Validation                                   |
+------------------------------------------------------------------+
|  [ ] Step 10: Pre-commit code review                            |
|      Status: ??? (check your TodoWrite/YAML state)              |
|                                                                  |
|  If Step 10 is NOT completed:                                    |
|  - STOP: Do not proceed to Step 15                              |
|  - ACTION: Invoke reviewer agent for code review                |
|  - ACTION: Invoke security agent for security review            |
|  - Then return here and verify completion                       |
+------------------------------------------------------------------+
```

**Before Step 21 (Ensure Mergeable)**:

```
+------------------------------------------------------------------+
|  CHECKPOINT: Final Validation                                    |
+------------------------------------------------------------------+
|  [ ] Step 10: Pre-commit code review                            |
|  [ ] Step 16: PR review                                         |
|  [ ] Step 17: Review feedback implementation                    |
|                                                                  |
|  ALL mandatory steps must be completed before Step 21.          |
|  Check your TodoWrite/YAML state for status.                    |
+------------------------------------------------------------------+
```

#### At Workflow End

1. Verify all steps completed (or explicitly skipped with documented reason)
2. Final progress: `[######################] 22/22 Steps Complete`
3. Delete `.claude/runtime/workflow_state.yaml` if used
4. Log completion to workflow_tracker.py

## Visual Progress Formats

### Standard Progress Bar

```
WORKFLOW: DEFAULT_WORKFLOW v1.1.0
PROGRESS: [##########............] 10/22 (45%)

Current: Step 10 - Pre-commit code review (MANDATORY)
Next: Step 11 - Incorporate Review Feedback
```

### Detailed Status Display

```
+======================================================================+
|                    DEFAULT WORKFLOW - Progress                        |
+======================================================================+
| Task: Add authentication feature                                     |
| Session: session_20251125_143022                                     |
| Started: 2025-11-25T14:30:22                                         |
+----------------------------------------------------------------------+
|  Progress: 10/22 steps (45%)                                         |
|  [##########............] 10/22                                       |
+----------------------------------------------------------------------+
|  COMPLETED (10):                                                     |
|    0, 1, 2, 3, 4, 5, 6, 7, 8, 9                                      |
|                                                                      |
|  CURRENT:                                                            |
|    >> Step 10: Pre-commit code review (MANDATORY) <<                 |
|                                                                      |
|  REMAINING (12):                                                     |
|    11, 12, 13, 14, 15, *16*, *17*, 18, 19, 20, 21                   |
|    (* = mandatory)                                                   |
+----------------------------------------------------------------------+
|  MANDATORY GATES:                                                    |
|    [X] Step 0  - Workflow Preparation      COMPLETED                 |
|    [ ] Step 10 - Pre-commit Review         IN PROGRESS               |
|    [ ] Step 16 - PR Review                 PENDING                   |
|    [ ] Step 17 - Feedback Implementation   PENDING                   |
+======================================================================+
```

### Compact Status (For Updates)

```
[10/22] Step 10 (MANDATORY) | Gates: 0[X] 10[>] 16[ ] 17[ ]
```

## State File Format

**Template Location**: `.claude/templates/workflow_state.yaml.template`
**Active State Location**: `.claude/runtime/workflow_state.yaml`

```yaml
workflow_id: "session_20251125_143022"
workflow_name: DEFAULT
task_description: "Add authentication feature"
started_at: "2025-11-25T14:30:22"
current_step: 10

steps:
  0: { status: completed, timestamp: "2025-11-25T14:30:22", mandatory: true }
  1: { status: completed, timestamp: "2025-11-25T14:31:05" }
  # ... steps 2-9 ...
  10: { status: in_progress, mandatory: true }
  # ... steps 11-15 ...
  16: { status: pending, mandatory: true }
  17: { status: pending, mandatory: true }
  # ... steps 18-21 ...

mandatory_steps: [0, 10, 16, 17]

checkpoints:
  before_step_15:
    required_steps: [10]
    error_message: "Cannot open PR without completing Step 10"
  before_step_21:
    required_steps: [10, 16, 17]
    error_message: "Cannot mark mergeable without all mandatory reviews"
```

## Integration with Power Steering

Power steering provides session-end verification through the `dev_workflow_complete` consideration in `considerations.yaml`.

### How It Works

1. **During Session**: This skill provides guidance; Claude should track steps in TodoWrite
2. **At Session End**: Power steering's `_check_dev_workflow_complete` analyzes the transcript
3. **Heuristics Used**:
   - Were architect, builder, reviewer agents invoked?
   - Were tests executed (Bash tool usage)?
   - Were git operations performed?
4. **Result**: Blocks session completion if workflow evidence is missing

### Integration Points

```
considerations.yaml
==================
- id: dev_workflow_complete
  category: Workflow Process Adherence
  question: Was full DEFAULT_WORKFLOW followed?
  severity: blocker
  checker: _check_dev_workflow_complete
  applicable_session_types: ["DEVELOPMENT"]
```

**Current Limitation**: Power steering checks for evidence of workflow (agent usage, test runs) but does NOT read `workflow_state.yaml`. This is a future enhancement opportunity.

### Proposed Enhancement (Not Yet Implemented)

```python
# In power_steering_checker.py (future)
def _check_dev_workflow_complete(self, transcript, session_id):
    # Check for workflow_state.yaml
    state_file = Path(".claude/runtime/workflow_state.yaml")
    if state_file.exists():
        state = yaml.safe_load(state_file.read_text())
        mandatory = state.get("mandatory_steps", [0, 10, 16, 17])
        steps = state.get("steps", {})

        for step_num in mandatory:
            step = steps.get(step_num, {})
            if step.get("status") != "completed":
                return False  # Mandatory step incomplete

        return True  # All mandatory steps completed

    # Fall back to heuristic analysis
    return self._check_workflow_heuristics(transcript)
```

## Integration with TodoWrite

When using TodoWrite, ensure step numbers match workflow tracking:

```python
TodoWrite(todos=[
    {"content": "Step 0: Workflow Preparation - Create todos for ALL steps", "status": "completed", "activeForm": "Creating step todos"},
    {"content": "Step 10: Pre-commit code review - MANDATORY", "status": "in_progress", "activeForm": "Reviewing code"},
    {"content": "Step 16: PR review - MANDATORY", "status": "pending", "activeForm": "Reviewing PR"},
    {"content": "Step 17: Implement review feedback - MANDATORY", "status": "pending", "activeForm": "Implementing feedback"},
])
```

**Key Point**: TodoWrite is the primary tracking mechanism. YAML state file is optional for additional persistence and structured validation.

## Blocking Behavior (Self-Compliance Pattern)

When mandatory steps are skipped, Claude SHOULD display and follow this pattern:

```
+======================================================================+
|                    WORKFLOW ENFORCEMENT: BLOCKED                      |
+======================================================================+
|                                                                      |
|  Cannot proceed to Step 15 (Open PR as Draft).                       |
|                                                                      |
|  MISSING MANDATORY STEP:                                             |
|    Step 10: Pre-commit code review                                   |
|                                                                      |
|  WHY THIS MATTERS:                                                   |
|    - Code review catches bugs before they reach CI                   |
|    - Philosophy compliance ensures quality                           |
|    - Issue #1607 identified this as a recurring problem              |
|                                                                      |
|  ACTION REQUIRED:                                                    |
|    1. Invoke reviewer agent for comprehensive code review            |
|    2. Invoke security agent for security review                      |
|    3. Mark Step 10 as completed in TodoWrite                         |
|    4. Then proceed to Step 15                                        |
|                                                                      |
+======================================================================+
```

## Error Recovery

If state file is missing or corrupt:

1. Check TodoWrite for current step information
2. Reconstruct state from conversation context
3. If unrecoverable, prompt user to confirm current step
4. Always fail-open: continue with warning rather than blocking

## Future Work: Path to Hard Enforcement

### Phase 1: Current State (Guidance Only)

- Skill provides documentation and patterns
- Claude self-compliance determines effectiveness
- Power steering provides session-end warnings

### Phase 2: Enhanced Power Steering (Planned)

- Power steering reads workflow_state.yaml
- Real-time validation at checkpoint steps
- More granular `dev_workflow_complete` checks

### Phase 3: Pre-Commit Integration (Future)

```bash
# .pre-commit-config.yaml (future)
- repo: local
  hooks:
    - id: workflow-validation
      name: Validate workflow completion
      entry: python .claude/tools/amplihack/validate_workflow.py
      language: system
      pass_filenames: false
```

### Phase 4: CI Gate (Future)

```yaml
# .github/workflows/ci.yml (future)
- name: Validate Workflow Compliance
  run: |
    python -c "
    from pathlib import Path
    import yaml
    state = yaml.safe_load(Path('.claude/runtime/workflow_state.yaml').read_text())
    mandatory = state.get('mandatory_steps', [0, 10, 16, 17])
    for step in mandatory:
        if state['steps'].get(step, {}).get('status') != 'completed':
            print(f'FAIL: Mandatory step {step} not completed')
            exit(1)
    print('PASS: All mandatory workflow steps completed')
    "
```

## Related Components

- **DEFAULT_WORKFLOW.md**: Canonical workflow definition with Step 0 guidance
- **templates/workflow_state.yaml.template**: Template for structured state tracking
- **workflow_tracker.py**: Historical logging (JSONL format)
- **power_steering_checker.py**: Session-end enforcement (transcript-based)
- **considerations.yaml**: `dev_workflow_complete` consideration definition
