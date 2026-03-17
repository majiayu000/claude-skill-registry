---
name: executing-plans
description: "Use when implementing a multi-step plan. Execute systematically with verification checkpoints to catch errors early."
---

# Executing Plans

## Core Principle

Execute plans systematically, one task at a time, with verification checkpoints. NEVER work through multiple tasks without verification.

## When to Use This Skill

- After completing `writing-plans` skill and getting user approval
- You have a written plan with TodoWrite entries
- Multi-step implementation work
- Any task where order matters

## The Iron Law

**Execute ONE task at a time. Verify EACH task before proceeding.**

Reasons:
- Catches errors early when they're cheap to fix
- Prevents cascading failures
- Maintains working state between steps
- Allows rollback to last known-good state
- Gives user visibility into progress

## Execution Protocol

### Step 1: Announce Start of Execution

**Template:**
```
I'm using the executing-plans skill to implement this systematically.

I'll work through each task one at a time, verifying as I go.
```

### Step 2: Mark Task as In Progress

**BEFORE starting ANY work:**
```
Marking Task 1 as in_progress.
```

Update TodoWrite status to `in_progress`.

**CRITICAL**: Only ONE task should ever be `in_progress` at a time.

### Step 3: Execute the Task

Follow the task's action items EXACTLY as written in the plan:
1. Read the plan task carefully
2. Execute each action step
3. Document any deviations or issues
4. If you encounter problems, STOP and report

### Step 4: Verify the Task

**MANDATORY after each task:**

1. Run the verification specified in the plan
2. Check the expected outcome
3. If verification fails:
   - DO NOT proceed to next task
   - Investigate the failure
   - Fix the issue
   - Re-verify
4. If verification passes:
   - Mark task as completed
   - Document the successful verification

**Template:**
```
Verifying Task 1:
- Running: [verification command]
- Expected: [expected outcome]
- Actual: [actual outcome]
- Status: ✅ PASS / ❌ FAIL
```

### Step 5: Mark Task as Completed

**ONLY after successful verification:**
```
Task 1 completed successfully. Moving to Task 2.
```

Update TodoWrite status to `completed`.

### Step 6: Repeat for Next Task

**Before moving on, explicitly state:**
```
Marking Task 2 as in_progress.
```

**NEVER start a new task without:**
1. Completing previous task
2. Verifying previous task
3. Marking previous task as completed
4. Marking new task as in_progress

### Step 7: Handle Failures

If a task fails verification:

**Template:**
```
❌ Task [X] verification FAILED

Expected: [what should have happened]
Actual: [what actually happened]

Issue: [description of problem]

I'm investigating before proceeding. Keeping Task [X] as in_progress.
```

**Actions to take:**
1. Keep task as `in_progress` (don't mark completed)
2. Investigate the root cause
3. Fix the issue
4. Re-verify
5. Only mark completed after successful verification

**If issue is blocking:**
```
This issue is blocking progress. I need to resolve it before continuing.

Options:
1. [Fix approach 1]
2. [Fix approach 2]

Which approach would you prefer?
```

### Step 8: Report Progress Regularly

For long-running plans, provide status updates:

**Template:**
```
Progress Update:
✅ Task 1: [Name] - Completed
✅ Task 2: [Name] - Completed
🔄 Task 3: [Name] - In Progress
⏳ Task 4: [Name] - Pending
⏳ Task 5: [Name] - Pending

Currently working on: [Current task description]
```

## Critical Safety Checks

### Before ANY Database Operation

**MANDATORY**: Use `database-backup` skill

```
Before proceeding with Task [X] (database operation), I'm using the database-backup skill.
```

### Before Running Tests

**MANDATORY**: Use database safety wrapper

```
Running tests with safety wrapper: ./scripts/safe-test.sh [test command]
```

### Before Git Operations

1. Verify clean working directory
2. Ensure you're on correct branch
3. Pull latest changes if needed

## Red Flags (Execution is Going Wrong)

- ❌ Multiple tasks marked as `in_progress` → Only ONE at a time
- ❌ Skipping verification → NEVER skip verification
- ❌ Marking tasks completed without verification → Verification is mandatory
- ❌ "I'll test everything at the end" → Test each task immediately
- ❌ Deviating from plan without user approval → Stick to the plan
- ❌ Moving to next task despite failed verification → Fix failures first

## Common Rationalizations to Reject

- ❌ "I'll verify later" → Verify NOW
- ❌ "These tasks are related, I'll do them together" → One at a time
- ❌ "Verification is too slow" → Verification SAVES time
- ❌ "I know it works" → Prove it with verification
- ❌ "I'll batch the todos" → Update todos immediately

## When Plans Change

If you discover issues during execution:

**Template:**
```
During Task [X], I discovered [issue/new information].

This affects the plan:
- [Impact 1]
- [Impact 2]

I recommend [adjustment to plan].

Should I:
1. Continue with original plan
2. Adjust plan as suggested
3. Stop and re-plan
```

**NEVER silently deviate from the plan.**

## Integration with Other Skills

**Before executing-plans**: Use `writing-plans` skill
**During execution**: Use `database-backup`, `test-driven-development` as needed
**After execution**: Use `code-review` and `verification-before-completion` skills

## Example Execution

### Starting a Plan

```
I'm using the executing-plans skill to implement user authentication.

Plan has 6 tasks. I'll execute them one at a time with verification.

Marking Task 1 as in_progress: Install and Configure Sanctum
```

### Executing Task 1

```
Task 1: Install and Configure Sanctum

Actions:
1. Running: composer require laravel/sanctum
   ✅ Package installed

2. Publishing config: php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
   ✅ Config published

3. Database backup (MANDATORY before migration)
   I'm using the database-backup skill.
   ✅ Backup created: backups/database_2025-01-06_14-30-00.sql

4. Running migration: php artisan migrate
   ✅ Migrations completed

5. Adding Sanctum middleware to app/Http/Kernel.php
   ✅ Middleware added

Verifying Task 1:
- Running: php artisan route:list | grep sanctum
- Expected: Sanctum routes should be visible
- Actual: Found sanctum routes in output
- Status: ✅ PASS

Task 1 completed successfully.
```

### Moving to Task 2

```
Marking Task 2 as in_progress: Create Authentication Controller

Task 2: Create Authentication Controller

Actions:
1. Creating app/Http/Controllers/AuthController.php
   ✅ File created

2. Implementing register() method with validation
   ✅ Method added

3. Implementing login() method with token generation
   ✅ Method added

4. Implementing logout() method with token revocation
   ✅ Method added

Verifying Task 2:
- Running: cat app/Http/Controllers/AuthController.php | grep "public function"
- Expected: Should see register, login, logout methods
- Actual: All three methods present
- Status: ✅ PASS

Task 2 completed successfully.
```

### Handling a Failure

```
Marking Task 5 as in_progress: Run Tests with Database Backup

Task 5: Run Tests with Database Backup

Actions:
1. Using database-backup skill
   ✅ Backup created: backups/database_2025-01-06_14-45-00.sql

2. Running: ./scripts/safe-test.sh vendor/bin/paratest --filter=AuthenticationTest
   ❌ Test failed

Verifying Task 5:
- Running: vendor/bin/paratest --filter=AuthenticationTest
- Expected: All authentication tests pass
- Actual: 2 failures in login test
- Status: ❌ FAIL

Error output:
```
Failed asserting that 401 matches expected 200.
Expected token in response, got error message.
```

Issue: Login endpoint returning 401 instead of 200. Appears to be credentials validation issue.

Investigating AuthController login method...

Found issue: Missing password verification.

Fixing: Added Hash::check() for password validation.

Re-running verification:
- Running: ./scripts/safe-test.sh vendor/bin/paratest --filter=AuthenticationTest
- Status: ✅ PASS - All tests now passing

Task 5 completed successfully (after fix).
```

### Progress Update

```
Progress Update - User Authentication Implementation:
✅ Task 1: Install and Configure Sanctum - Completed
✅ Task 2: Create Authentication Controller - Completed
✅ Task 3: Add API Routes - Completed
✅ Task 4: Create Authentication Tests - Completed
✅ Task 5: Run Tests with Database Backup - Completed (fixed login validation)
🔄 Task 6: Update API Documentation - In Progress

Currently working on: Generating OpenAPI documentation for auth endpoints
```

### Completing the Plan

```
Task 6: Update API Documentation

Actions:
1. Adding PHPDoc comments to AuthController methods
   ✅ Comments added

2. Generating OpenAPI docs: php artisan scramble:generate
   ✅ Documentation generated

3. Verifying endpoints in /docs/api
   ✅ Auth endpoints visible

Verifying Task 6:
- Running: curl http://localhost/docs/api | grep "auth"
- Expected: Should see register, login, logout endpoints
- Actual: All three endpoints present in documentation
- Status: ✅ PASS

Task 6 completed successfully.

---

All 6 tasks completed successfully! ✅

Summary:
✅ Sanctum installed and configured
✅ Authentication controller created
✅ API routes exposed
✅ Tests created and passing
✅ API documentation generated

Ready for code-review skill.
```

## Task Completion Checklist

Before marking a task as completed:
- [ ] All actions in the task are executed
- [ ] Verification step has been run
- [ ] Verification has PASSED
- [ ] Any files created/modified are correct
- [ ] No errors or warnings
- [ ] TodoWrite status updated

## Authority

**This skill is based on**:
- Software engineering best practice: Incremental development with verification
- Test-driven development: Verify each step
- Agile methodology: Working software at all times
- Empirical evidence: Verified incremental progress has 90% success rate vs 40% for unverified batch work

**Social Proof**: Professional developers verify each step. No one writes 1000 lines without running tests.

## Your Commitment

Before using this skill, confirm:
- [ ] I will execute ONE task at a time
- [ ] I will VERIFY each task before moving on
- [ ] I will NEVER mark tasks completed without verification
- [ ] I will UPDATE TodoWrite status immediately
- [ ] I will REPORT failures and stop if blocked

---

**Bottom Line**: Slow and steady wins. One task, one verification, one completion at a time. Batch work leads to batch failures.
