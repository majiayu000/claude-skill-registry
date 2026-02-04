---
name: thinking-tools
description: Structured thinking patterns for agent self-reflection. Includes think-about-collected-information (validate research), think-about-task-adherence (stay on track), and think-about-whether-you-are-done (completion validation).
version: 1.0.0
model: sonnet
invoked_by: agent
user_invocable: false
tools: [Read, Glob, Grep]
best_practices:
  - Use think-about-collected-information after research/exploration phases
  - Use think-about-task-adherence before making code changes
  - Use think-about-whether-you-are-done before declaring completion
  - Be honest in self-assessment, don't skip steps to appear fast
  - Document gaps found during reflection
error_handling: graceful
streaming: supported
---

<identity>
Structured Thinking Framework - Self-reflection patterns for quality agent work.
</identity>

<capabilities>
- Validating completeness of collected information
- Ensuring adherence to the original task
- Confirming work is truly complete before stopping
- Identifying gaps in understanding or implementation
- Preventing scope creep and tangential work
</capabilities>

<instructions>

## Overview

This skill provides three structured thinking patterns that agents should use at key points during task execution. These patterns help maintain quality and prevent common mistakes like incomplete research, task drift, and premature completion.

## Thinking Pattern 1: Think About Collected Information

**When to Use**: After completing a non-trivial sequence of searching steps like:

- Reading multiple files
- Searching for symbols or patterns
- Exploring directory structures
- Gathering requirements

**Self-Assessment Questions**:

```markdown
## Information Completeness Check

1. **Sufficiency**: Do I have enough information to proceed?
   - [ ] I understand the relevant code structure
   - [ ] I know the dependencies and relationships
   - [ ] I have identified all affected components

2. **Relevance**: Is all collected information relevant?
   - [ ] Information directly relates to the task
   - [ ] No tangential exploration
   - [ ] Focused on actionable insights

3. **Gaps**: What am I missing?
   - [ ] Are there files I should read but haven't?
   - [ ] Are there patterns I should search for?
   - [ ] Do I need to understand related systems?

4. **Confidence**: How confident am I in my understanding?
   - [ ] High: Ready to proceed
   - [ ] Medium: Minor clarification needed
   - [ ] Low: More research required

**Decision**: [Proceed / Gather More Information / Ask User]
```

**Example Reflection**:

```
I've read the authentication module (auth.ts) and the user model (user.ts).
I understand how login works but I haven't checked:
- How session tokens are managed
- Where logout is implemented
- What the error handling pattern is

Decision: Read session.ts and error-handler.ts before proceeding.
```

## Thinking Pattern 2: Think About Task Adherence

**When to Use**: BEFORE making any code changes (insert, replace, delete). This is critical to ensure you're still solving the original problem.

**Self-Assessment Questions**:

```markdown
## Task Adherence Check

1. **Original Task**: What was I asked to do?
   - Restate the original request clearly
   - Identify the core goal

2. **Current Action**: What am I about to do?
   - Describe the planned change
   - Explain how it relates to the goal

3. **Alignment Check**:
   - [ ] This action directly addresses the original task
   - [ ] I am not adding unrequested features
   - [ ] I am not "improving" code that wasn't asked about
   - [ ] The scope is appropriate for the request

4. **Scope Creep Warning Signs**:
   - Am I refactoring code that works?
   - Am I adding "nice to have" features?
   - Am I fixing unrelated issues I noticed?
   - Have I drifted from the original ask?

**Decision**: [Proceed / Refocus / Ask User for Clarification]
```

**Example Reflection**:

```
Original Task: "Fix the login timeout error"

I'm about to:
1. Fix the timeout by increasing the limit (directly addresses task)
2. Also refactor the error messages (NOT requested)
3. Also add retry logic (NOT requested)

Decision: Only implement #1. The other changes are scope creep.
If user wants those improvements, they can request them separately.
```

## Thinking Pattern 3: Think About Whether You Are Done

**When to Use**: When you believe you have completed the task. This prevents premature completion and ensures quality.

**Self-Assessment Questions**:

```markdown
## Completion Validation Check

1. **Requirements Met**:
   - [ ] All explicit requirements addressed
   - [ ] All implicit requirements considered
   - [ ] Edge cases handled

2. **Quality Checks**:
   - [ ] Code compiles/runs without errors
   - [ ] Tests pass (or new tests written)
   - [ ] No regressions introduced
   - [ ] Follows project conventions

3. **Documentation**:
   - [ ] Code is self-documenting or commented where needed
   - [ ] README updated if needed
   - [ ] Breaking changes documented

4. **Verification Steps Taken**:
   - [ ] Ran relevant tests
   - [ ] Tested manually if applicable
   - [ ] Checked for lint/type errors

5. **Loose Ends**:
   - Any TODOs introduced?
   - Any known limitations?
   - Any follow-up work needed?

**Decision**: [Complete / Additional Work Needed / Partial Completion]
```

**Example Reflection**:

```
Task: "Add user email validation"

Requirements Check:
- [x] Email format validation added
- [x] Error message shows for invalid email
- [ ] Did NOT check: what about empty email?

Quality Check:
- [x] TypeScript compiles
- [ ] Tests: No tests written yet!

Decision: NOT complete. Need to:
1. Handle empty email case
2. Write unit tests for validation
```

## Integration Guidelines

### Workflow Integration

```
[Research Phase]
    |
    v
Think About Collected Information
    |
    v
[Planning Phase]
    |
    v
Think About Task Adherence (before each change)
    |
    v
[Implementation Phase]
    |
    v
Think About Whether You Are Done
    |
    v
[Completion or Iterate]
```

### When NOT to Use

- Simple, trivial tasks (fix typo, rename variable)
- When user explicitly asks to skip validation
- Quick answers that don't involve code changes

### Logging Reflections

For important tasks, log reflections to memory:

```markdown
## Task: [description]

## Reflection Log

### Information Gathering

- Files read: [list]
- Gaps identified: [list]
- Decision: [proceed/gather more]

### Task Adherence Check

- Original task: [description]
- Planned changes: [list]
- Scope assessment: [in-scope/adjusted]

### Completion Check

- Requirements: [met/partial/not met]
- Tests: [passed/failed/not run]
- Final status: [complete/needs work]
```

</instructions>

<examples>
<usage_example>
**Scenario**: Agent is asked to "fix the broken search feature"

**Phase 1 - After Research**:

```
Think About Collected Information:
- Read search.ts, index.ts, searchUtils.ts
- Found the bug: incorrect regex pattern
- Checked: test file exists (search.test.ts)
- Gap: Haven't checked if there are related search files
Decision: Quick grep for "search" to ensure completeness...
Found search-config.ts which is relevant. Reading now.
```

**Phase 2 - Before Coding**:

```
Think About Task Adherence:
- Original: "fix the broken search feature"
- Planned: Fix regex pattern in searchUtils.ts line 45
- Scope check: This directly fixes the bug. NOT adding new search features.
Decision: Proceed with targeted fix.
```

**Phase 3 - After Implementation**:

```
Think About Whether You Are Done:
- [x] Bug fixed (regex corrected)
- [x] Existing tests still pass
- [ ] No new test for this specific case
Decision: Add regression test, then complete.
```

</usage_example>
</examples>

<integration>
**Related Skills**:
- `verification-before-completion` - Complements completion validation
- `tdd` - Test-driven development integrates with completion checks
- `sequential-thinking` - Structured problem decomposition
</integration>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
