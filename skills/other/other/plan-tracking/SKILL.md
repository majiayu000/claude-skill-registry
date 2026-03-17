---
name: plan-tracking
description: Guidelines for working with plan files. Claude should use this skill when the user provides a plan file (e.g., *-plan.md) to ensure task completion is tracked in the plan file itself, not just internally.
---

# Plan File Tracking Guidelines

When working from a plan file (markdown file with task checkboxes), follow these guidelines to ensure proper tracking.

## Core Rule

**The plan file is the source of truth for task completion status.**

Use the `plan-file-management` skill's subcommands to read and update plan files:
- **Find next task**: `plan-file-management` → `get-next-task`
- **Mark task complete**: `plan-file-management` → `mark-task-complete`

See the `plan-file-management` skill for invocation details.

Do NOT rely on internal tracking (like TodoWrite) as a substitute for updating the actual plan file.

## ⚠️ Verifying Observable and Evidence (CRITICAL - READ THIS)

**THIS IS THE MOST IMPORTANT SECTION OF THIS SKILL.**

**A task is NOT complete until the Observable outcome is actually observed and the Evidence is actually collected.**

If a task has these fields:
- **Observable**: What should be true after the task is complete
- **Evidence**: How to verify the observable

Then **tests** must verify the Evidence - not the agent manually running commands and checking output.

This applies to all test types:
- JUnit/unit tests
- Integration tests
- Component tests
- Shell test scripts

Example task:
```
- [ ] **Task 1.3: POST /orders endpoint creates order and returns 201**
  - Observable: Endpoint accepts order JSON, persists to database, returns 201 with order ID
  - Evidence: Integration test POSTs valid order, asserts 201 response, asserts order exists in database
```

The test must contain assertions that verify the Evidence:
```java
@Test
void createOrder_returnsCreatedWithOrderId() {
    var response = restTemplate.postForEntity("/orders", validOrderRequest, OrderResponse.class);

    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
    assertThat(response.getBody().getId()).isNotNull();

    // Verify persisted to database
    var saved = orderRepository.findById(response.getBody().getId());
    assertThat(saved).isPresent();
    assertThat(saved.get().getCustomerId()).isEqualTo(validOrderRequest.getCustomerId());
}
```

WRONG: Agent writes the endpoint code, assumes it works because the code looks right
RIGHT: Tests contain assertions for the Evidence criteria; tests pass = Evidence verified

**Tests are the source of truth for verification, not the agent's judgment.**

## Migration Planning

When creating migration or upgrade plans for existing codebases:
1. Before describing any file/directory creation tasks, verify whether the target already exists using Glob or Read
2. Use precise language: "Transform" or "Convert" for existing items, "Create" only for genuinely new items
3. Include a "Current State" section in plans that documents what exists before transformation

## Review Plans for Technical Correctness

Before implementing a task from the plan, review its implementation details for technical flaws:

- Apply fundamental engineering principles (e.g., uniqueness constraints belong at database level, not application level)
- If the plan specifies a flawed approach, fix it before proceeding
- Do not blindly follow implementation details that violate best practices

## Workflow

For each task in the plan:

1. Get the next task using `plan-file-management` → `get-next-task`
2. **Review for technical correctness** before implementing
3. Implement the task (write test, implement code, verify)
4. **Verify Observable and Evidence criteria** - tests must pass that verify the Evidence (see critical section above)
5. **Mark task complete* using `plan-file-management` → `mark-task-complete`
6. Continue to the next task

## Continue Without Stopping

When implementing a documented plan:
- Continue through all phases without stopping for confirmation
- Only pause if blocked, uncertain about requirements, or encountering errors
- The plan itself serves as the user's approval to proceed
- Summarize progress periodically but don't ask "should I continue?"

## Why This Matters

- The plan file is visible to the user and persists across sessions
- Internal tracking (TodoWrite) is ephemeral and not visible in the codebase
- Commits should include both the implementation AND the updated plan
- Other developers can see progress by looking at the plan file

## Common Mistake

BAD:
```
Complete task 1.1
Update internal TodoWrite
Complete task 1.2
Update internal TodoWrite
... (plan file never updated)
```

GOOD:
```
Complete task 1.1
Use plan-file-management → mark-task-complete for thread 1, task 1
Complete task 1.2
Use plan-file-management → mark-task-complete for thread 1, task 2
```

## When to Apply

Apply this guideline when:
- User provides a plan file path (e.g., `*-plan.md`, `*-tasks.md`)
- User says "follow the plan" or "implement from the plan"
- Working with any markdown file containing `- [ ]` task checkboxes

## Commit Guidelines

When committing completed tasks:
1. Stage the implementation changes
2. Stage the updated plan file (with checkbox marked)
3. Commit together so the commit reflects both the work done and the progress tracked

## Commit Verification for Plan Files

Before running `git commit`, always:
1. Run `git status` from the **repository root** (not a subdirectory)
2. Verify the plan file appears in "Changes to be committed"
3. If the plan file is not staged, explicitly add it: `git add path/to/plan.md`

When committing from a subdirectory:
- Use absolute paths or navigate to repo root first
- Example: `git add /path/to/plan.md` or `cd /repo/root && git add .`
