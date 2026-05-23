---
name: plan-executor
description: Execute implementation plans created by /discover. Use this skill when working in a worktree with a --plan flag, when you need to execute tasks from a docs/plans/*.md file, or when implementing a multi-task feature systematically.
---

# Plan Executor

Execute implementation plans with two-stage review, verification, and batch checkpoints.

## When This Skill Applies

This skill automatically applies when:

- You're in a worktree created with `--plan` flag
- Your goal references a plan file at `docs/plans/...`
- You're executing a multi-task implementation

## Core Principles

1. **Evidence before claims** - Never claim completion without verification output
2. **Two-stage review** - Spec compliance first, then code quality
3. **Batch execution** - Execute 3 tasks, checkpoint, continue
4. **Fresh context per task** - For parallel execution, use separate subagents

---

## Execution Flow

### Phase 1: Load and Review Plan

```
1. Read the plan file completely
2. Extract all tasks with their:
   - Files to create/modify
   - Steps to follow
   - Verification commands
   - Dependencies
3. Create mental model of dependency graph
4. Identify independent vs dependent tasks
5. If concerns about the plan, raise with user BEFORE starting
```

### Phase 2: Execute Tasks

**For 1-3 tasks:** Execute sequentially yourself
**For 4+ independent tasks:** Consider parallel subagents

#### Per Task Execution

```
1. Mark task as in_progress (use TaskUpdate)
2. Follow each step exactly as written
3. Run verification commands, capture output
4. Perform two-stage review (see below)
5. Mark task as completed only with evidence
6. Commit the work
```

### Phase 3: Batch Checkpoints

After every 3 tasks (or all independent tasks):

```
Report to user:
- Tasks completed with evidence
- Issues encountered
- "Ready for feedback"

Wait for user confirmation before continuing.
```

### Phase 4: Dependent Tasks

After independent tasks complete:

1. Identify newly unblocked tasks
2. Execute next batch
3. Repeat until all tasks done

---

## Two-Stage Review

### Stage 1: Spec Compliance Review

**Question:** Does the code match the plan exactly?

```
Check:
- [ ] All required files created at exact paths
- [ ] All modifications match spec
- [ ] Nothing missing from requirements
- [ ] Nothing extra added (YAGNI)
- [ ] Tests cover specified behaviors
```

**If issues found:**

- Fix the gaps
- Re-review
- Don't proceed until spec-compliant

### Stage 2: Code Quality Review

**Question:** Is the implementation well-built?

```
Check:
- [ ] Code follows project patterns
- [ ] Tests are meaningful (not just coverage)
- [ ] No obvious bugs or edge cases missed
- [ ] Error handling appropriate
- [ ] No code smells
```

**If issues found:**

- Fix the issues
- Re-review
- Don't proceed until quality approved

---

## Verification Before Completion

### The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

### Required Evidence

| Claim            | Required Evidence                |
| ---------------- | -------------------------------- |
| "Tests pass"     | Actual test output: `X/Y pass`   |
| "Build succeeds" | Build output: `exit code 0`      |
| "Linter clean"   | Linter output: `0 errors`        |
| "Task complete"  | All verification commands output |

### Bad vs Good

```
❌ BAD: "The tests should pass now"
❌ BAD: "I believe this is working"
❌ BAD: "Task completed successfully"

✅ GOOD: "Tests pass (output: 12/12 pass, 0 failures)"
✅ GOOD: "Build succeeded (exit code 0, no errors)"
✅ GOOD: "Task complete. Evidence:
         - Tests: 12/12 pass
         - Lint: 0 errors
         - Build: success"
```

### When to Verify

- Before claiming any task is done
- Before moving to next task
- Before reporting to user
- Before committing

---

## Parallel Execution with Subagents

When you have 4+ independent tasks, use parallel subagents:

### Launching Subagents

```javascript
// Launch multiple Task tools in a SINGLE message
Task({
  description: 'Implement Task 1',
  prompt: `You are implementing Task 1 from the plan.

Task details:
${task1Content}

Requirements:
1. Follow each step exactly
2. Run all verification commands
3. Report actual output, not assumptions
4. Commit when complete

When done, report:
- Files created/modified
- Verification output (actual)
- Any issues encountered`,
  subagent_type: 'general-purpose',
});

// In the SAME message, launch Task 2, 3, etc.
```

### Collecting Results

After subagents complete:

1. Review each result
2. Verify the evidence provided
3. If subagent claimed success without evidence, re-verify yourself
4. Report consolidated results to user

### Don't Trust Blindly

```
❌ Subagent: "Task completed successfully"
   You: "Great, moving on"

✅ Subagent: "Task completed. Tests: 5/5 pass"
   You: [Verify the claim by running tests yourself if suspicious]
   You: "Confirmed, Task 1 complete with 5/5 tests passing"
```

---

## When to Stop and Ask

**STOP immediately when:**

- Verification fails repeatedly
- Plan has gaps or unclear instructions
- Dependencies aren't actually met
- You're unsure about an approach

**Don't:**

- Guess when confused
- Force through blockers
- Skip verification
- Proceed with failing tests

---

## Example Execution

```
Agent: I'm executing the plan at docs/plans/2026-02-01-webhooks.md

[Reads plan, extracts 5 tasks]

Task 1 (independent): WebhookConfig model
Task 2 (independent): WebhookDelivery service
Task 3 (independent): API endpoints
Task 4 (depends on 1,2): Integration
Task 5 (depends on 4): E2E tests

Starting with independent tasks 1-3...

---

Task 1: WebhookConfig model
[Following steps from plan]
1. Writing failing test...
2. Running: pnpm test packages/core --grep WebhookConfig
   Output: FAIL - WebhookConfig is not defined
3. Creating model...
4. Running: pnpm test packages/core --grep WebhookConfig
   Output: PASS - 3/3 tests pass

Spec compliance review:
✅ All files created at specified paths
✅ Model matches spec
✅ Tests cover required behaviors
✅ Nothing extra added

Code quality review:
✅ Follows project patterns
✅ Tests are meaningful
✅ No obvious issues

Task 1 complete.
Evidence: Tests pass (3/3), files created at packages/core/src/models/webhook-config.ts
[Commit: "feat: add WebhookConfig model"]

---

[Similar for Tasks 2, 3]

---

Batch checkpoint: Tasks 1-3 complete

Summary:
- Task 1: WebhookConfig model ✅ (3/3 tests)
- Task 2: WebhookDelivery service ✅ (5/5 tests)
- Task 3: API endpoints ✅ (4/4 tests)

All independent tasks verified and committed.

Ready for feedback. Should I proceed with Task 4 (Integration)?
```

---

## Integration with Workflow

```
/discover (main branch)
    │
    ├── Creates plan at docs/plans/YYYY-MM-DD-feature.md
    │
    └── Creates worktree with --plan flag
            │
            └── plan-executor (this skill)
                    │
                    ├── Execute tasks with verification
                    ├── Two-stage review
                    ├── Batch checkpoints
                    │
                    └── Complete with evidence
```

---

## Anti-Patterns

**Don't:**

- Claim completion without running verification
- Trust subagent "success" reports blindly
- Skip spec compliance review
- Move to next task with failing tests
- Guess when plan is unclear
- Add features not in the plan (YAGNI)

**Do:**

- Run every verification command
- Capture and report actual output
- Stop when blocked
- Ask for clarification when needed
- Follow the plan exactly
