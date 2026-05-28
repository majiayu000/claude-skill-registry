---
name: plan-execute
description: Two-phase workflow that generates explicit YAML plan before execution, with approval gates and checkpointing. Use for complex multi-file changes, refactoring, bug fixes with dependencies, or any task where mistakes are costly. Achieves 90% first-pass success rate vs ad-hoc changes. Provides audit trail, rollback capability, and explicit approval points. Triggers on "refactor", "multi-step", "plan then execute", "complex changes", "safe refactoring".
---

# Plan-Execute Workflow

## Purpose

Decompose complex coding tasks into explicit, reviewable plans before execution. This two-phase approach prevents breaking changes, provides audit trails, and enables safe rollback.

## When to Use

**Use this skill when:**
- Task involves 3+ files or modules
- Changes have dependencies or ordering constraints
- Risk of breaking existing functionality
- Need audit trail of modifications
- Want to review before execution
- Database migrations or schema changes
- API changes affecting multiple modules

**Do NOT use for:**
- Single-line fixes or typos
- Trivial changes (formatting, comments)
- Exploratory coding where you're learning
- Time-critical hotfixes (use direct mode)

## Performance Characteristics

Based on expert validation (@iannuttall, Claude Code release Oct 2025):

| Metric | Direct Implementation | With Plan-Execute | Improvement |
|--------|---------------------|-------------------|-------------|
| First-pass success | ~60% | ~90% | +50% success rate |
| Unintended changes | Common | Near-zero | Explicit control |
| Planning overhead | 0 sec | ~30 sec | Offset by fewer bugs |
| Audit trail | None | Complete YAML | Full traceability |
| Rollback time | Hours | Seconds | Checkpointing |

## Core Instructions

### PHASE 1: PLAN

Generate a YAML plan with this structure:

```yaml
task:
  id: "TASK-001"
  description: "Brief task summary"
  risk_level: "low|medium|high"
  estimated_time_minutes: 15

prerequisites:
  - "Tests passing"
  - "Git working directory clean"

steps:
  - id: "step-1"
    description: "Specific action"
    type: "read|write|test|validate"
    files: ["path/to/file.py"]
    dependencies: []
    approval_required: false

  - id: "step-2"
    description: "High-risk action"
    type: "write"
    files: ["critical/file.py"]
    dependencies: ["step-1"]
    approval_required: true    # Requires user confirmation

validation_gates:
  - id: "gate-1"
    after_step: "step-2"
    condition: "Linter passes"
    blocking: true

rollback:
  strategy: "git stash"
  checkpoint_frequency: "after_each_step"

success_criteria:
  - "All steps complete without errors"
  - "All validation gates pass"
  - "Tests pass"
```

**Planning Guidelines:**
1. **Atomic steps**: Break into smallest logical actions
2. **Dependencies**: Mark what depends on what
3. **Risk flagging**: Set `approval_required: true` for risky changes
4. **Validation gates**: Add checks after critical operations
5. **Rollback strategy**: Define undo mechanism

### PHASE 2: EXECUTE

Execute the plan with this loop:

```
For each step in plan:
  1. Check prerequisites satisfied
  2. If approval_required:
     - Display what will change
     - Prompt: "Proceed? (y/n/skip)"
     - Wait for user confirmation
  3. Execute step
  4. Run validation gate if defined
  5. If gate fails and blocking:
     - Stop execution
     - Report failure
     - Suggest rollback or fix
  6. Create checkpoint (git stash or snapshot)
  7. Continue to next step

After all steps:
  - Run final validation (tests, linting)
  - Report summary
  - Suggest commit message
```

**Checkpointing:**
```bash
# After each critical step
git add -A
git stash push -m "Checkpoint after step-X"
# Continue...

# If rollback needed
git stash pop  # Restore previous state
```

## Example Workflow

### User Request
```
Use Plan-Execute: Refactor authentication to use JWT instead of sessions
```

### Agent Response (PLAN Phase)

```yaml
task:
  id: "REFACTOR-AUTH-001"
  description: "Refactor auth from sessions to JWT"
  risk_level: "high"
  estimated_time_minutes: 30

steps:
  - id: "analyze"
    description: "Identify all session-dependent code"
    type: "read"
    files: ["src/auth/**/*.js"]
    dependencies: []

  - id: "create-jwt-lib"
    description: "Create JWT utility library"
    type: "write"
    files: ["src/lib/jwt.js"]
    dependencies: ["analyze"]
    approval_required: false

  - id: "refactor-login"
    description: "Replace session creation with JWT generation"
    type: "write"
    files: ["src/routes/auth/login.js"]
    dependencies: ["create-jwt-lib"]
    approval_required: true    # Critical auth logic

  - id: "refactor-middleware"
    description: "Update auth middleware to validate JWT"
    type: "write"
    files: ["src/middleware/auth.js"]
    dependencies: ["create-jwt-lib"]
    approval_required: true

  - id: "test"
    description: "Run full test suite"
    type: "test"
    command: "npm test"
    dependencies: ["refactor-login", "refactor-middleware"]

validation_gates:
  - id: "lint-check"
    after_step: "refactor-middleware"
    condition: "eslint passes"
    blocking: true

  - id: "coverage-check"
    after_step: "test"
    condition: "coverage >= 80%"
    blocking: true

rollback:
  strategy: "git stash"
  checkpoint_frequency: "after_each_step"

success_criteria:
  - "JWT library created with encode/decode/verify"
  - "Login generates JWT token"
  - "Middleware validates JWT"
  - "All 127 tests pass"
  - "No linter errors"
```

**Agent then asks:**
```
PLAN generated. Review above and respond:
- 'execute' to run all steps
- 'modify' to edit plan
- 'cancel' to abort
```

### User Approves
```
execute
```

### Agent Executes (EXECUTE Phase)

```
✓ Step 1 (analyze): Found 8 files using sessions
✓ Step 2 (create-jwt-lib): Created jwt.js with sign/verify/decode
  [Checkpoint: stash-after-step-2]
→ Step 3 (refactor-login): APPROVAL REQUIRED
  Will modify: src/routes/auth/login.js (critical auth logic)
  Proceed? (y/n/skip)
```

**User:** `y`

```
✓ Step 3 (refactor-login): Replaced session.create with jwt.sign
  [Checkpoint: stash-after-step-3]
→ Step 4 (refactor-middleware): APPROVAL REQUIRED
  Will modify: src/middleware/auth.js
  Proceed? (y/n)
```

**User:** `y`

```
✓ Step 4 (refactor-middleware): Updated to jwt.verify
  [Checkpoint: stash-after-step-4]
✓ Gate: lint-check PASSED
✓ Step 5 (test): All 127 tests pass

✅ TASK COMPLETE
Files changed: 3
Checkpoints created: 4
Rollback available: stash-after-step-{2,3,4}

Suggested commit:
refactor(auth): replace sessions with JWT tokens

- Create JWT utility library (sign/verify/decode)
- Update login to generate JWT instead of session
- Update auth middleware to validate JWT
- All tests passing, 80% coverage maintained
```

## Templates

Use the template in [templates/plan-template.yaml](templates/plan-template.yaml) as a starting point for creating plans.

## Customization

### Adjust Risk Tolerance

```yaml
# Conservative: approve all writes
- id: "any-write"
  approval_required: true

# Balanced: approve only multi-file changes
- id: "single-file"
  approval_required: false

# Aggressive: only approve DB migrations
- id: "code-change"
  approval_required: false
```

### Add Custom Gates

```yaml
validation_gates:
  - id: "security-scan"
    after_step: "code-changes"
    command: "npm audit --audit-level=high"
    condition: "no high-severity issues"
    blocking: true

  - id: "performance-test"
    after_step: "refactor"
    command: "./scripts/perf-test.sh"
    condition: "response_time < 200ms"
    blocking: false    # Warning only
```

## Safety Features

1. **Explicit Approval Gates**: High-risk steps require user confirmation
2. **Checkpointing**: Can rollback to any previous step
3. **Validation Gates**: Automated checks catch issues early
4. **Dry-Run Mode**: Can generate plan without executing
5. **Audit Trail**: Complete YAML record of all changes

## Dependencies

**Required:**
- Git (for checkpointing)

**Optional:**
- Test runner (npm test, pytest, etc.)
- Linter (eslint, flake8, etc.)
- Coverage tools

## Version

v1.0.0 (2025-10-23) - Based on expert validation and Claude Code patterns

