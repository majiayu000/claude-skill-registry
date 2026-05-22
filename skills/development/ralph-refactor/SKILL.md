---
name: ralph-refactor
description: Use this skill after a ralph-code phase has completed but before marking the task as complete in SCOPES.yml
---

Your job is to review the tests and the code that were written for this task, perform a security audit, and look for any needed rework.

**IMPORTANT**: Do NOT use superpowers:code-reviewer or superpowers:requesting-code-review for this skill. Follow the phases below directly.

## Phase 1: Code Quality Review

Analyze the completed code and look for needed refactors. Don't be overly critical or nit-pick, look for changes that are worth putting extra effort into.

**Code Smells**

1. Duplication - Repeated logic or similar code blocks
2. Long functions - Functions trying to do too much
3. Complex conditionals - Deeply nested ifs or complex boolean expressions
4. Magic numbers/strings - Hardcoded values without clear meaning
5. Poor naming - Unclear variable, function, or type names

**Design Issues**

1. Violation of project standards - Code doesn't follow established conventions
2. High coupling - Functions/modules with too many dependencies
3. Low cohesion - Functions doing unrelated things
4. Temporary hacks - Quick-fix code written just to make tests pass
5. Hard to test code - Indicates poor separation of concerns

## Phase 2: Security Audit

**CRITICAL**: Before marking any task as complete, you MUST invoke the security-review skill using the Skill tool:

```
Skill tool call:
  skill: "security-review"
```

Do NOT skip this step. Do NOT use superpowers:code-reviewer as a substitute.

The security review should cover:

1. **New code security** - Audit the code written for this task
2. **Integration security** - How the new code fits with existing code and potential attack vectors

If the security review identifies issues:

- Critical/High severity: MUST be fixed before completing the task
- Medium severity: Should be fixed, document if deferring with justification
- Low severity: Fix if trivial, otherwise note for future improvement

## When to Loop Back

**CRITICAL** If code quality OR security issues are found:

1. If the issue impacts function signatures or behavior, call the `ralph-test` skill to go back to the "Red" TDD phase
2. If the issue is implementation quality or security fix that doesn't change behavior, call the `ralph-code` skill to go back to the "Green" TDD phase
3. Do NOT update the status in SCOPES.yml - the called skill will handle status updates

## When to Complete

If NO issues are found (code is clean AND security audit passes):

1. Ensure there are no uncommitted workspace changes (all modified code should be committed)
2. Update the current task in the SCOPES.yml file to assign a status of "completed"
3. Commit the status update to VCS
4. Call the `ralph-pr` skill using the Skill tool with the same arguments that were passed to this skill

## Notes

- The refactor phase is about improving code quality without changing behavior - all tests should remain passing throughout
- Security is not optional - every task must pass security review before completion
- When in doubt about a security concern, err on the side of caution and fix it
