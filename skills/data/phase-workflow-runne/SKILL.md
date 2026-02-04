---
name: phase-workflow-runner
description: Runs a complete phase workflow: audit existing work, fill gaps, run tests, verify acceptance criteria, and report readiness for next phase. Use when user asks to run or complete a project phase.
---

# Phase Workflow Runner

This skill executes a deterministic, repeatable phase workflow.

## Core Principles
- Never overwrite existing working code
- Never redo completed tasks
- Always audit before action
- Tests define correctness
- Phase completion requires verification

## Workflow Steps (MANDATORY)

### 1. Phase Audit
- Inspect project structure
- Read relevant spec and tasks files
- Identify:
  - Completed items
  - Missing files
  - Failing or absent tests
  - Partial implementations

Produce a concise audit report before proceeding.

### 2. Gap Filling
Only after audit:
- Create missing source files
- Create missing test files (RED)
- Implement minimal code to pass tests (GREEN)
- Refactor if required

Rules:
- Do not modify completed, passing code
- Do not remove existing functionality

### 3. Execution & Verification
- Run full test suite
- Perform manual smoke checks if CLI/project requires
- Verify acceptance criteria from spec.md

### 4. Documentation Update
- Update tasks.md checkboxes
- Mark checkpoints complete
- Add short completion summary

### 5. Completion Gate
If all criteria pass:
- Declare phase COMPLETE
- Ask user:
  “Phase X complete. Proceed to Phase X+1?”

If not:
- Report blockers and stop

## Safety Rules
- Never hallucinate missing work
- Never assume tests exist
- Never skip audit
- Never continue if tests fail

## Output Format
Always output:
1. Audit Summary
2. Actions Taken
3. Test Results
4. Acceptance Criteria Status
5. Next Step Recommendation
