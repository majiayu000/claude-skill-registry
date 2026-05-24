---
name: proceed
description: Execute an implementation plan with surgical precision. Use after a planning phase (plan-now or similar) has produced a step-by-step strategy and identified critical files. Focuses on precise code changes with verification at each step.
---
# Proceed Command

Execute the provided implementation plan with surgical precision.

CRITICAL: This is an EXECUTION task. Implement changes exactly as specified in the plan.

## Process

1. **Review the Plan**: Analyze the provided implementation plan and critical files. Understand the architectural decisions and sequence of operations before writing any code.

2. **Execute Surgically**:
   - Implement changes step-by-step as outlined in the plan.
   - Use `ast-grep` (preferred) or the Edit tool for code transformations.
   - Follow the **Find -> Transform -> Verify** workflow.
   - Complete each task in the plan sequentially. Batch independent operations where possible, but never batch dependent ones.

3. **Verify After Each Step**:
   - After each file modification, use `difft` to inspect changes and ensure no unintended modifications.
   - If the project has build/lint/test commands available, run them to catch regressions early.
   - If verification fails, debug and fix before proceeding to the next step.

4. **Finalize**:
   - Run available build/lint/test commands for final verification.
   - VCS operations (commits, branch management) only if the user explicitly requests them or the plan specifies them.

## Required Output

End your response with:

### Implementation Summary

- [File path] - [Status: e.g., "Implemented & Verified"]
- [File path] - [Status: e.g., "Updated & Tested"]

### Verification Results

- Build: [pass/fail/not available]
- Lint: [pass/fail/not available]
- Tests: [pass/fail/not available]

Remember: Execute the plan precisely. Follow existing patterns. Verify every change.
