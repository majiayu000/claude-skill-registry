---
name: implementing-plans
description: >-
  This skill should be used when the user asks to "implement the plan",
  "execute the plan", "start implementation", "build the feature",
  "make the changes", or invokes the rpikit:implement command. Provides
  methodology for disciplined execution with checkpoint validation and
  progress tracking.
---

# Implementation Phase

Execute the implementation plan for: **$ARGUMENTS**

## Purpose

Implementation executes an approved plan with discipline and verification.
The goal is not just working code, but verified, documented progress that
matches the plan. Implementation follows the plan strictly, verifying each
step before proceeding.

## Process

### 1. Verify Plan Exists

Look for plan at: `docs/plans/YYYY-MM-DD-$ARGUMENTS-plan.md`

(Search for files matching `*-$ARGUMENTS-plan.md` pattern)

**If plan exists:**

- Read the plan document
- Check if plan is marked approved
- Proceed based on stakes level

**If no plan exists:**

- Check stakes level of the requested work
- Apply enforcement based on stakes

### 2. Apply Stakes-Based Enforcement

**High Stakes** (architectural, security-sensitive, hard to rollback):

```text
Cannot proceed without an approved plan.

High-stakes implementations require:
1. Research phase (rpikit:researching-codebase skill)
2. Approved plan (rpikit:writing-plans skill)

Invoke the Skill tool with skill "rpikit:writing-plans" to create a plan first.
```

Stop and do not proceed.

**Medium Stakes** (multiple files, moderate impact):

```text
Warning: No approved plan found for '$ARGUMENTS'.

Medium-stakes changes benefit from planning.
```

Use AskUserQuestion with options:

- "Create a plan first" (recommended)
- "Proceed with caution"
- "Cancel"

**Low Stakes** (isolated, easy rollback):

```text
Note: Consider rpikit:researching-codebase and rpikit:writing-plans skills for better results.
Proceeding with implementation...
```

Proceed with inline planning.

### 3. Offer Worktree Isolation

Before making changes, offer to create an isolated worktree.

**First, check if already in an additional worktree:**

```bash
# Check if .git is a file (indicates additional worktree, not main repo)
test -f .git
```

Run this command via the Bash tool:

- Exit code 0 (success): `.git` is a file → this is an additional worktree → skip the prompt and proceed to progress tracking
- Exit code 1 (failure): `.git` is a directory → this is the main repository → continue with the worktree offer below

**If not in a worktree, offer based on stakes level:**

**High Stakes:**

Use AskUserQuestion with options:

- "Use worktree (Recommended)" - Create isolated workspace for safer changes
- "Continue in current directory" - Proceed without isolation

**Medium Stakes:**

Use AskUserQuestion with options:

- "Use worktree" - Create isolated workspace
- "Continue in current directory" - Proceed without isolation

**Low Stakes:**

Brief mention only:

```text
Tip: For isolation, you can use the git-worktrees skill.
Proceeding in current directory...
```

Skip the prompt and continue.

**If user chooses worktree:**

Invoke Skill tool with skill: "rpikit:git-worktrees"

After worktree is created:

1. Implementation continues in the new worktree directory
2. The finishing-work skill handles cleanup when done

### 4. Initialize Progress Tracking

Convert plan steps to TodoWrite todos:

Read each step from the plan and create corresponding todos:

- Use step descriptions as todo content
- Mark all as pending initially
- This provides visible progress tracking

### 5. Execute Steps in Order

For each step in the plan:

1. **Mark in_progress** - Update TodoWrite
2. **Locate target files** - If file path is unclear or missing, use file-finder:

   ```text
   Task tool with subagent_type: "file-finder"
   Prompt: "Find [what the step describes]. Need to [action from plan]"
   ```

3. **Read target files** - Always read before modifying
4. **Make the change** - Follow plan specification exactly
5. **Run verification** - Execute the verify criteria
6. **Confirm success** - Only proceed if verification passes
7. **Mark completed** - Update TodoWrite immediately
8. **Update plan** - Mark step complete in plan document

### 6. Checkpoint After Phases

After completing each phase:

Summarize progress:

```text
Phase [N] complete:
- Step N.1: [description]
- Step N.2: [description]
- Step N.3: [description]

Verifications: All passed
```

Use AskUserQuestion:

- "Continue to Phase [N+1]"
- "Review changes so far"
- "Pause implementation"

### 7. Handle Failures

When verification fails:

1. **Stop** - Do not proceed to next step
2. **Report** - Explain what failed and why
3. **Diagnose** - Investigate the cause. If the error involves external
   libraries or unfamiliar issues, use web-researcher:

   ```text
   Task tool with subagent_type: "web-researcher"
   Prompt: "[error message or issue] in [library/context]"
   ```

4. **Propose fix** - Suggest correction based on diagnosis

If fix requires plan changes:

```text
Verification failed for Step [X.Y]: [description]

The planned approach doesn't work because: [reason]

Proposed adjustment: [new approach]
```

Use AskUserQuestion:

- "Approve adjustment and continue"
- "Return to planning"
- "Cancel implementation"

### 8. Complete Implementation

When all steps are done:

1. Mark all todos complete
2. Update plan document status section
3. Run final verification (full test suite if applicable)
4. Run code review:

   ```text
   Task tool with subagent_type: "code-reviewer"
   Prompt: "Review implementation changes for: $ARGUMENTS"
   ```

   If verdict is REQUEST CHANGES (soft gate):

   Use AskUserQuestion:

   - "Address findings first" (recommended)
   - "Proceed anyway"
   - "Cancel implementation"

   If user chooses "Proceed anyway", continue to security review.

5. Run security review:

   ```text
   Task tool with subagent_type: "security-reviewer"
   Prompt: "Review implementation changes for: $ARGUMENTS"
   ```

   If verdict is FAIL, stop and address findings before completing.

6. Summarize results

```text
Implementation complete for '$ARGUMENTS'.

Summary:
- Steps completed: [N]
- Phases completed: [M]
- Files changed: [list]
- Tests: [pass/fail status]

Plan updated: docs/plans/YYYY-MM-DD-$ARGUMENTS-plan.md

All success criteria met.
```

## Core Principles

### Follow the Plan

The plan is the contract. Deviations require explicit approval:

- Execute steps in order
- Use specified files and approaches
- Meet verification criteria before proceeding
- Document any necessary deviations

### Verify Before Claiming Done

Never claim completion without evidence:

- Run the verification for each step
- Confirm tests pass
- Check that changes match expectations
- Document verification results

### Track Progress Visibly

Use TodoWrite to show real-time progress:

- Create todos from plan steps
- Mark in_progress when starting
- Mark completed only after verification
- Update plan document with status

## Progress Documentation

### TodoWrite Format

Maintain real-time visibility:

```text
[completed] Step 1.1: Add validation function
[completed] Step 1.2: Update API endpoint
[in_progress] Step 2.1: Add unit tests
[pending] Step 2.2: Update integration tests
```

### Plan Document Updates

Update the plan file as implementation progresses:

```markdown
#### Step 1.1: Add validation function

- **Status**: Complete
- **Verified**: Unit tests pass
- **Notes**: Used existing regex pattern from validatePhone()
```

## Test-Driven Execution

When plan includes test steps, follow TDD:

1. **Red** - Write failing test first
2. **Green** - Write minimal code to pass
3. **Refactor** - Improve without breaking

Mark test steps complete only when tests pass.

## Deviation Handling

If implementation reveals the plan needs changes:

1. Stop current step
2. Document the issue
3. If additional files are needed, use file-finder to locate them:

   ```text
   Task tool with subagent_type: "file-finder"
   Prompt: "Find files related to [issue discovered]. Need to [proposed change]"
   ```

4. Propose plan modification with updated file references
5. Get approval before continuing

Never deviate silently from the approved plan.

## Verification Techniques

### Code Verification

For code changes, verify by:

- **Syntax check**: Code compiles/parses without errors
- **Type check**: TypeScript/type annotations pass
- **Lint check**: No new linting errors
- **Unit tests**: Related tests pass

### Behavior Verification

For functionality, verify by:

- **Manual test**: Exercise the feature
- **Integration test**: Run relevant integration tests
- **API test**: Hit endpoints and verify responses
- **UI check**: Visual verification if applicable

### Regression Verification

Ensure no breakage:

- **Full test suite**: Run all tests
- **Build**: Project builds successfully
- **Smoke test**: Core functionality works

## Anti-Patterns to Avoid

### Skipping Verification

**Wrong**: Marking done without running verification
**Right**: Always run verification, document results

### Proceeding After Failure

**Wrong**: Moving to next step when current step failed
**Right**: Stop, diagnose, fix, re-verify

### Deviating Silently

**Wrong**: Changing approach without updating plan
**Right**: Request approval for plan changes

### Batch Completion

**Wrong**: Marking multiple steps done at once
**Right**: Mark complete immediately after each verification

### Ignoring Stakes

**Wrong**: Rushing high-stakes changes
**Right**: Respect enforcement based on stakes level

## Quality Checklist

During implementation:

- [ ] Always read files before modifying
- [ ] Run verification after each step
- [ ] Mark todos complete immediately (no batching)
- [ ] Update plan document with status
- [ ] Get approval at phase checkpoints
- [ ] Document any deviations

At completion:

- [ ] All plan steps marked done
- [ ] All verifications passed
- [ ] Code review completed (code-reviewer agent)
- [ ] Security review completed (security-reviewer agent)
- [ ] Plan document updated with completion status
- [ ] Final summary provided
