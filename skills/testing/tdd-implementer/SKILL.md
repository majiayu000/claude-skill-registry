---
activation_code: TDD_IMPLEMENTER_V1
phase: 7
prerequisites:
  - OpenSpec proposals
  - Test strategy
outputs:
  - Implementation files
  - Test files
  - .signals/phase3-complete.json
description: |
  Guides TDD implementation following RED-GREEN-REFACTOR cycle.
  Activates via codeword [ACTIVATE:TDD_IMPLEMENTER_V1] injected by hooks
  when entering Phase 3 implementation.
  
  Activation trigger: [ACTIVATE:TDD_IMPLEMENTER_V1]
---

# TDD Implementer Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:TDD_IMPLEMENTER_V1]
```

This occurs when:
- Phase 6 is complete (specs and test strategy ready)
- User begins implementation
- Tests need to be written first

## Anti-Mock Directive

**CRITICAL**: NO MOCK IMPLEMENTATIONS IN OPERATIONAL CODE
- Do NOT create simulated services or fake deployments
- Do NOT return hardcoded success responses
- If cannot implement, raise NotImplementedError
- Mock code allowed ONLY in test files

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in dedicated worktrees per subtask `phase-3-task-N`:

```bash
# For each subtask implementation:
./lib/worktree-manager.sh create 3 <subtask_number>
cd ./worktrees/phase-3-task-<subtask_number>

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# TDD implementation with strict isolation
```

### Implementation Isolation Strategy
1. **One worktree per subtask**: Each subtask gets completely isolated environment
2. **TDD cycle isolation**: RED-GREEN-REFACTOR happens within worktree boundaries
3. **NO MOCKS**: Real implementations only, fail if cannot implement
3. **Test contamination prevention**: Tests don't interfere across subtasks
4. **Sequential merge**: Subtasks merged in dependency order
5. **Integration validation**: Each merge tested in isolation before next subtask

# TDD Implementer Skill

## What This Skill Does

Automates Phase 7: Test-Driven Development implementation in isolated worktrees

- **RED-GREEN-REFACTOR cycle** (tests first, always) per worktree
- **Mandatory coverage gates** (80% line, 70% branch) validated per subtask
- **Worktree-based isolation** (one subtask per worktree)
- **Status updates** (TaskMaster & OpenSpec) from isolated environments
- **Completion signal** → triggers Phase 8
- **NEW**: Complete task isolation prevents implementation conflicts
- **NEW**: Safe parallel development through worktree boundaries

## Execution Flow

```
Stage 1: Load Phase 2 Results
Stage 2: Determine Implementation Strategy
         - Sequential (tightly coupled)
         - Parallel (loosely coupled)
Stage 3: Implement Tasks (TDD Cycle)
         RED: Write failing tests
         GREEN: Implement code
         REFACTOR: Clean up
         VALIDATE: Check coverage
Stage 4: Update Status
Stage 5: Generate Summary
Stage 6: Create Signal → Phase 8
```

## TDD Cycle (Per Task)

### RED Phase: Write Failing Tests FIRST

```bash
# 1. Create test files
tests/unit/[component].test.js
tests/integration/[component]-integration.test.js

# 2. Write comprehensive tests
- Unit tests (60%)
- Integration tests (30%)
- E2E tests (10%)
- Edge cases
- Error cases

# 3. Run tests (MUST FAIL)
npm test
# ❌ All new tests fail (proves they're valid)

# 4. Commit failing tests
git commit -m "Add failing tests for [feature] (RED)"
```

### GREEN Phase: Implement Minimum Code

```bash
# 1. Apply OpenSpec
/openspec:apply [proposal-name]

# 2. Write MINIMUM code to pass tests
# Run tests continuously
npm test -- --watch

# 3. Verify all tests pass
npm test
# ✅ All tests pass

# 4. Commit implementation
git commit -m "Implement [feature] (GREEN)"
```

### REFACTOR Phase: Improve Quality

```bash
# 1. Clean up code
- Remove duplication
- Improve naming
- Extract functions
- Add comments

# 2. Run tests after EVERY change
npm test

# 3. Tests must stay GREEN
# ✅ All tests still pass

# 4. Commit refactoring
git commit -m "Refactor [feature] (REFACTOR)"
```

### VALIDATE Phase: Check Coverage

```bash
# 1. Run coverage report
npm run coverage

# 2. Check thresholds (BLOCKING)
Line coverage:     >= 80%  ✓
Branch coverage:   >= 70%  ✓
Critical paths:    = 100%  ✓

# 3. If insufficient → Back to RED
# Write more tests, repeat cycle

# 4. Run all validation
npm test                 # All tests
npm test:integration     # Integration
npm test:regression      # No breaks
npm run lint            # No errors

# 5. Mark complete ONLY if all pass
task-master set-task-status --id=[id] --status=done
openspec archive [proposal-name] --yes
```

### VERIFY Phase: Security and Compliance

After VALIDATE passes, run security verification before marking complete.

#### Security Scanning (SAST)

**Python Projects:**
```bash
# Bandit - Python security linter
bandit -r src/ -f json -o .reports/bandit-report.json
# CRITICAL/HIGH findings = BLOCKING

# Safety - Dependency vulnerability scanner
safety check --json -r requirements.txt > .reports/safety-report.json
# Known vulnerabilities = BLOCKING

# pip-audit - Alternative dependency scanner
pip-audit --json > .reports/pip-audit-report.json
```

**JavaScript/Node Projects:**
```bash
# npm audit - Dependency vulnerabilities
npm audit --json > .reports/npm-audit-report.json
# CRITICAL/HIGH vulnerabilities = BLOCKING

# ESLint security plugin
npx eslint --plugin security src/ --format json > .reports/eslint-security.json
```

**Multi-Language (if available):**
```bash
# Semgrep - Semantic code analysis
semgrep --config auto --json src/ > .reports/semgrep-report.json

# Trivy - Container/dependency scanning
trivy fs --format json --output .reports/trivy-report.json .
```

#### Compliance Checks

```bash
# 1. Hardcoded Secrets Detection
# Check for passwords, API keys, tokens in code
# Look for patterns: password=, api_key=, secret=, token=
# CRITICAL finding if detected

# 2. License Header Verification
# All source files should have copyright/license headers
# WARNING if missing (not blocking)

# 3. Documentation Existence
# Public functions should have docstrings/JSDoc
# WARNING if missing (not blocking)
```

#### VERIFY Phase Pass/Fail Criteria

| Finding Severity | Action |
|------------------|--------|
| CRITICAL | **BLOCKING** - Must fix before proceeding |
| HIGH | **BLOCKING** - Must fix before proceeding |
| MEDIUM | Warning - Document and acknowledge |
| LOW | Informational - Log for review |

#### VERIFY Phase Output

Generate `.reports/security-verification.json`:
```json
{
  "task_id": "T-XXX-N.3",
  "timestamp": "ISO8601",
  "passed": true,
  "summary": {
    "critical": 0,
    "high": 0,
    "medium": 2,
    "low": 5
  },
  "tools_run": ["bandit", "safety", "semgrep"],
  "acknowledged_findings": []
}
```

**If VERIFY fails:** Fix security issues, re-run from GREEN phase.

## Implementation Strategies

### Strategy A: Sequential (Tightly Coupled)

**Use when:** Tasks share code, must implement together

```bash
# For each task in order:
# 1. Load task
task-master show [id]
openspec show [proposal-name]

# 2. Run TDD cycle
# [RED → GREEN → REFACTOR → VALIDATE]

# 3. Mark complete
task-master set-task-status --id=[id] --status=done
openspec archive [proposal-name] --yes

# 4. Move to next task
```

**Time:** 45-90 min per task

### Strategy B: Parallel (Loosely Coupled)

**Use when:** Tasks independent, can run simultaneously

```bash
# Setup: Create git worktrees
git worktree add ../project-task-[id] -b feature/task-[id]

# Launch Claude Code per worktree
# Each runs TDD cycle independently

# Merge when all complete
git merge feature/task-[id]
```

**Time:** 3-4x faster (30-45 min total vs sequential)

## Parallel Subagent Execution

For maximum implementation speed, use parallel Claude Code subagents with worktrees:

### Step 1: Analyze Dependencies

```bash
# Identify independent subtasks that can run in parallel
# Group by master task or by loose coupling analysis
jq '.tasks[] | select(.subtasks != null) | {id, subtasks: [.subtasks[].id]}' \
  .taskmaster/tasks/tasks.json
```

### Step 2: Create Worktrees

```bash
# Create one worktree per parallel subagent
./lib/worktree-manager.sh create 3 1  # phase-3-task-1
./lib/worktree-manager.sh create 3 2  # phase-3-task-2
./lib/worktree-manager.sh create 3 3  # phase-3-task-3
# ... continue for each parallel implementation slot
```

### Step 3: Launch Parallel Subagents

Use Claude Code's Task tool to implement tasks in parallel:

```
Launch 5 parallel subagents for TDD implementation:

Subagent 1 (worktree: phase-3-task-1):
  - Implement subtasks 1.1, 1.2, 1.3
  - Follow RED → GREEN → REFACTOR cycle
  - Validate 80% coverage before marking complete
  - Commit to feature/task-1 branch

Subagent 2 (worktree: phase-3-task-2):
  - Implement subtasks 2.1, 2.2, 2.3
  - Independent code paths (no conflicts)
  - Commit to feature/task-2 branch

Subagent 3 (worktree: phase-3-task-3):
  - Implement subtasks 3.1, 3.2
  - Commit to feature/task-3 branch

[Continue for remaining subagents...]
```

### Step 4: Sequential Merge

After all subagents complete:
```bash
# Merge in dependency order (not random)
git checkout main

# Merge independent branches first
git merge feature/task-1 --no-ff -m "Implement task 1 subtasks"
git merge feature/task-2 --no-ff -m "Implement task 2 subtasks"
git merge feature/task-3 --no-ff -m "Implement task 3 subtasks"

# Run integration tests after each merge
npm test:integration

# Clean up worktrees
./lib/worktree-manager.sh cleanup
```

### Conflict Prevention

- Each subagent works in isolated worktree
- Assign subtasks by directory/module to minimize conflicts
- Run linting and tests before merge
- Use `--no-ff` to preserve merge history

### Performance Comparison

| Method | 20 Subtasks | Speed |
|--------|-------------|-------|
| Sequential | 15-30 hours | 1x |
| 4 Parallel Subagents | 4-8 hours | 4x |
| 8 Parallel Subagents | 2-4 hours | 6-8x |

**Note:** Diminishing returns above 8 subagents due to merge overhead

## Time Estimates (Sequential)

| Tasks | Sequential | Parallel |
|-------|-----------|----------|
| 5     | 4-7 hours | 1-2 hours |
| 10    | 7-15 hours| 2-4 hours |
| 20    | 15-30 hours| 4-8 hours |

## Mandatory Gates

**Before marking task complete:**

- ✅ All tests pass (100%)
- ✅ Line coverage ≥ 80%
- ✅ Branch coverage ≥ 70%
- ✅ Critical paths = 100%
- ✅ Integration tests pass
- ✅ Regression tests pass
- ✅ No lint errors
- ✅ No type errors

**If ANY gate fails:** Back to RED phase

## Completion Signal

```json
{
  "phase": 7,
  "status": "success",
  "summary": {
    "tasks_implemented": N,
    "tests_written": M,
    "coverage_achieved": {
      "line": 85,
      "branch": 78
    }
  },
  "next_phase": 8,
  "trigger_next": true
}
```

## Output Files

```
src/
└── [implementation code]

tests/
├── unit/
├── integration/
└── e2e/

.taskmaster/
├── phase7-summary.md
└── .signals/phase7-complete.json
```

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 8.**

When Phase 7 is complete (all tasks implemented with tests passing), you MUST:

1. Output the completion signal:
   ```
   ✅ PHASE 7 COMPLETE
   [SIGNAL:PHASE7_COMPLETE]
   ```

2. **IMMEDIATELY** proceed to Phase 8 by outputting:
   ```
   [ACTIVATE:CODE_REVIEW_GATE_V1]
   ```

3. Begin code review gate without waiting for user input.

**The pipeline is fully autonomous. Do not ask "Would you like to proceed?" - just proceed.**

## See Also

- Pipeline Orchestrator (triggers this)
- Spec Generator (Phase 6, provides input)
- Test Strategy Generator (provides test guidance)
- Code Review Gate (Phase 8, triggered by signal)