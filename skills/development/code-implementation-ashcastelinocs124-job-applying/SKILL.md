---
name: code-implementation-ashcastelinocs124-job-applying
description: 'Description: Deliver production-quality code for a requested task: plan
  → implement → verify → code review.'
---

# Code Implementation Skill
**Description:** Deliver production-quality code for a requested task: plan → implement → verify → code review.
**Usage:** /code-implementation "task description"

**Trigger this skill when:**
- User asks to implement/build/add code or a feature
- User requests a function/module/service to be written
- Bug fixes that require non-trivial coding (after root cause is known)

**Skip for:** Pure analysis, docs-only tasks, minor tweaks that don't need a plan

## Execution Workflow

### Phase 0: Architecture Context (if applicable)

**When invoked from /system-arch:**
- Review the approved architecture decision
- Extract specific implementation requirements:
  * Components to create/modify
  * Interface contracts and APIs
  * Data flow requirements
  * Success metrics from architecture plan
- Ensure test strategy aligns with architectural requirements
- Note any architectural constraints that affect implementation

### Phase 1: Understand & Bound
- Capture requirements and constraints (inputs/outputs, interfaces, performance, edge cases)
- Identify affected components/files
- Note non-functional needs (tests, types, logging, telemetry)

### Phase 2: Plan (checklist-driven)
Produce a concise plan before coding:
- Scope & assumptions
- Files to touch (including test files)
- Steps to implement (ordered)
- **Test cases required** (unit, integration, edge cases)
- Tests/verification commands
- Rollback notes

Use this template:
```markdown
## Implementation Plan
- Scope/assumptions: ...
- Files: [...]
- Test Files: [...] (MANDATORY: list all test files to create/modify)
- Test Cases Required:
  * Unit tests: [...]
  * Integration tests: [...]
  * Edge cases: [...]
- Steps:
  1) ...
  2) Write tests for [component] (BEFORE implementation)
  3) Implement [component]
  4) ...
- Tests/verify: `...`
- Rollback: ...
```
Only start coding after the plan is written. Keep the plan updated if scope changes.

**CRITICAL: Test-Driven Approach**
- Write test cases BEFORE implementing each component when possible
- Every new function/module MUST have corresponding tests
- Aim for >80% code coverage on new code

### Phase 3: Implement
- Follow the plan steps in order; keep changes minimal and focused
- Prefer existing patterns; match project style
- **Test-first workflow:**
  1. Write test case for a component/function
  2. Run test (expect it to fail - "red")
  3. Implement the component/function
  4. Run test again (expect it to pass - "green")
  5. Refactor if needed while keeping tests green
- Run `lsp_diagnostics` on changed files after each logical unit
- Ensure test files are created/updated for ALL new code

**Test Coverage Requirements:**
- [ ] Unit tests for all new functions/methods
- [ ] Integration tests for cross-component interactions
- [ ] Edge case tests (null, empty, boundary values)
- [ ] Error handling tests (exceptions, failures)

### Phase 4: Verify (COMPREHENSIVE)
- Run ALL planned tests/commands
- Check test coverage metrics (if available)
- Verify tests cover:
  * Happy path scenarios
  * Error conditions
  * Edge cases
  * Integration points
- If ANY failures occur, fix and re-run until ALL tests green
- Document test results in summary

### Phase 5: Code Review (MANDATORY)
- Invoke the **code-reviewer** agent (see AGENTS.md) after implementation & self-verification
- Address review findings; rerun verification if code changes

### Phase 6: Summarize
- Summarize changes, tests run, and status vs plan
- Call out any deviations or TODOs

### Phase 7: Explain (only if user asks)
- If the user requests an explanation of the new code, use the **Explain** skill (/explain) or the **tutor** agent to provide a concise walkthrough (what it does, how it works, key flows)

## Quality Guidelines

**ALWAYS:**
- Plan before you code; keep it short but specific
- Update the plan if the scope shifts
- Keep diffs tight; avoid drive-by refactors
- Add/maintain tests; keep `lsp_diagnostics` clean
- Use existing patterns and conventions
- Run code-reviewer agent before considering the task done

**NEVER:**
- Start coding without a plan
- Skip writing tests for new code
- Write implementation before tests (when TDD is feasible)
- Mark tests as TODO or skip tests
- Ignore failing tests or diagnostics
- Ship code with <80% test coverage
- Write tests after the fact without running them
- Introduce type suppressions (`# type: ignore`, `as any`, `@ts-ignore`)
- Mix unrelated refactors with the requested change

## Verification Checklist (tick before closing)
- [ ] Plan created with test cases identified
- [ ] Plan followed/updated throughout implementation
- [ ] Test files created/modified for ALL new code
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Edge case tests written and passing
- [ ] Error handling tests written and passing
- [ ] Test coverage >80% on new code (if measurable)
- [ ] All tests/commands executed and passing
- [ ] lsp_diagnostics clean on changed files
- [ ] code-reviewer agent run and feedback addressed
- [ ] Summary delivered to user with test results
