---
name: subagent-driven-development
description: "Use when decomposing complex work. Dispatch fresh subagent per task, review between tasks. Flow: Load plan → Dispatch task → Review output → Apply feedback → Mark complete → Next task. No skipping reviews, no parallel dispatch."
---

# Subagent-Driven Development

## Core Principle

Each task gets a fresh subagent with focused instructions. Review output before proceeding. No shortcuts, no parallel work, no skipped reviews.

## When to Use This Skill

- Complex work that needs decomposition
- Multiple independent tasks
- When tasks require different skills
- When context needs to be fresh
- Quality matters more than speed
- Work benefits from systematic review

## The Iron Law

**NEVER SKIP THE REVIEW BETWEEN TASKS.**

Every subagent output must be reviewed before:
- Marking task complete
- Starting next task
- Dispatching another subagent

## Why Subagent-Driven Development?

**Benefits:**
✅ Fresh context per task (no baggage)
✅ Focused attention on one thing
✅ Catches errors between tasks
✅ Better quality control
✅ Clear task boundaries
✅ Easy to parallelize (when appropriate)

**Without subagents:**
❌ Context bloat over time
❌ Errors compound across tasks
❌ No checkpoints
❌ Harder to debug issues
❌ Mixed responsibilities

## The Subagent Flow

### Step 1: Load the Plan

```
📋 LOAD PLAN Phase

Before dispatching subagents, you need a clear plan.

Use writing-plans skill to create:
```markdown
# Feature: User Authentication

## Task 1: Database Migration
Create users table with authentication fields

## Task 2: User Model
Create User model with authentication methods

## Task 3: Authentication Controller
Implement login/logout endpoints

## Task 4: Tests
Write comprehensive auth tests

## Task 5: Integration
Connect auth to existing routes
```

Plan loaded ✅
Ready to dispatch first subagent
```

**Plan requirements:**
- Clear task boundaries
- Dependencies identified
- Each task is independent
- Acceptance criteria defined

### Step 2: Dispatch Subagent

```
🚀 DISPATCH Phase

Task: Database Migration
Dispatching subagent with focused instructions:

---
You are a database migration specialist.

Context:
- We're building user authentication
- Need users table
- Using Laravel framework

Task:
Create a migration for users table with:
- id (primary key)
- email (unique)
- password (hashed)
- remember_token
- email_verified_at
- timestamps

Success criteria:
- Migration follows Laravel conventions
- Includes all required fields
- Has proper indexes
- Includes rollback method

Constraints:
- Don't create the model yet (separate task)
- Don't run the migration
- Use Laravel migration syntax
---

Subagent dispatched ✅
Waiting for output...
```

**Dispatch best practices:**
- Give ONLY the context needed for this task
- Be specific about what NOT to do
- Define success criteria clearly
- Set constraints explicitly

### Step 3: Review Output

```
🔍 REVIEW Phase

Subagent completed task
Output received: database/migrations/2024_01_01_000000_create_users_table.php

Reviewing output:

✅ Checks:
- [x] Migration file created
- [x] All required fields present
- [x] Proper indexes (email)
- [x] Rollback method included
- [x] Follows Laravel conventions

⚠️ Issues found:
- Missing: unique constraint on email
- Issue: password field should be longer (255 chars)

Issues documented ✅
Ready for feedback
```

**Review checklist:**
- Does output meet success criteria?
- Are there quality issues?
- Does it integrate with existing code?
- Are there edge cases missed?
- Would you approve this in code review?

### Step 4: Apply Feedback

```
📝 FEEDBACK Phase

Dispatching feedback to same subagent:

---
Review complete. Two issues to fix:

1. Add unique constraint to email field:
   $table->string('email')->unique();

2. Increase password field length to 255:
   $table->string('password', 255);

Please update the migration accordingly.
---

Feedback sent ✅
Waiting for revised output...

---

Subagent returned updated migration
Re-reviewing...

✅ All issues fixed:
- [x] Email field has unique constraint
- [x] Password field is 255 characters
- [x] All other requirements met

Ready to accept ✅
```

**Feedback guidelines:**
- Be specific about what needs to change
- Explain why (helps learning)
- Reference success criteria
- Don't accept "good enough"

### Step 5: Mark Complete

```
✅ COMPLETION Phase

Task: Database Migration
Status: Complete

Checklist:
- [x] Output meets all success criteria
- [x] All feedback addressed
- [x] Code quality acceptable
- [x] No known issues
- [x] Ready for next task

Marking task complete in plan ✅

Updated plan:
- [x] Task 1: Database Migration ← COMPLETE
- [ ] Task 2: User Model ← NEXT
- [ ] Task 3: Authentication Controller
- [ ] Task 4: Tests
- [ ] Task 5: Integration
```

**Completion criteria:**
- All acceptance criteria met
- All feedback addressed
- No open issues
- You would approve in code review

### Step 6: Final Review

```
🎯 FINAL REVIEW Phase

After all tasks complete:

Review overall integration:
1. Do all pieces work together?
2. Is there consistency across tasks?
3. Are there gaps between tasks?
4. Is the original goal met?

Testing integration:
```bash
# Run database migration
php artisan migrate

# Test authentication flow
./scripts/safe-test.sh vendor/bin/paratest --filter=Authentication

# Manual testing
curl -X POST /api/login -d '{"email":"test@example.com","password":"secret"}'
```

Results:
- ✅ Migration runs successfully
- ✅ All auth tests pass
- ✅ Manual testing works
- ⚠️ Found: Missing rate limiting on login

Add new task for rate limiting:
- [ ] Task 6: Add rate limiting to auth endpoints

Final review complete ✅
```

## Subagent Patterns

### Pattern 1: Sequential Tasks

```
When tasks depend on each other:

Task 1: Create database schema
  ↓ (depends on)
Task 2: Create model
  ↓ (depends on)
Task 3: Create controller
  ↓ (depends on)
Task 4: Write tests

Flow:
1. Dispatch Task 1 → Review → Complete
2. Dispatch Task 2 → Review → Complete
3. Dispatch Task 3 → Review → Complete
4. Dispatch Task 4 → Review → Complete
5. Final review
```

### Pattern 2: Independent Tasks (with care)

```
When tasks are truly independent:

Task A: Update documentation
Task B: Fix bug #123
Task C: Add logging

These don't depend on each other, but:

⚠️ STILL REVIEW BETWEEN TASKS

Even independent tasks should be reviewed
before starting the next one.

Why?
- Catches issues early
- Prevents compounding errors
- Maintains quality

Flow:
1. Dispatch Task A → Review → Complete
2. Dispatch Task B → Review → Complete
3. Dispatch Task C → Review → Complete
4. Final review
```

### Pattern 3: Iterative Refinement

```
When task needs multiple iterations:

Task: Implement search feature

Iteration 1: Basic search
- Dispatch subagent
- Review: Works but slow
- Feedback: Add pagination

Iteration 2: Paginated search
- Update implementation
- Review: Better, but missing filters
- Feedback: Add filter support

Iteration 3: Filtered search
- Update implementation
- Review: Complete ✅
- Mark complete

Each iteration gets review before next
```

## Real-World Examples

### Example 1: API Endpoint Development

```
Feature: User Profile API

Plan:
1. Create ProfileController
2. Add validation rules
3. Implement CRUD methods
4. Add authentication middleware
5. Write tests

Execution:

Task 1: ProfileController
---
Dispatch:
"Create ProfileController with empty CRUD methods.
Don't implement logic yet, just method signatures."

Review:
✅ Controller created
✅ Methods have correct signatures
⚠️ Missing resource route registration

Feedback:
"Add route registration in routes/api.php"

Re-review:
✅ Routes added
Complete ✅
---

Task 2: Validation Rules
---
Dispatch:
"Create ProfileRequest with validation rules for:
- name (required, string, max:255)
- bio (optional, string, max:1000)
- avatar (optional, image, max:2MB)"

Review:
✅ Request created
✅ All validation rules present
✅ Custom error messages
Complete ✅
---

Task 3: CRUD Implementation
---
Dispatch:
"Implement ProfileController methods using ProfileRequest"

Review:
✅ All CRUD methods implemented
⚠️ Missing authorization checks

Feedback:
"Add policy to check user owns profile"

Re-review:
✅ Authorization added
Complete ✅
---

Task 4: Authentication Middleware
---
Dispatch:
"Add auth middleware to profile routes"

Review:
✅ Middleware added
✅ Tested with unauthenticated request
Complete ✅
---

Task 5: Tests
---
Dispatch:
"Write feature tests for profile CRUD operations"

Review:
✅ All CRUD operations tested
✅ Authentication tested
⚠️ Missing authorization tests

Feedback:
"Add test for user accessing another user's profile"

Re-review:
✅ Authorization test added
Complete ✅
---

Final Review:
- All tasks complete
- Integration tested
- No gaps found
Feature complete ✅
```

### Example 2: Bug Fix Workflow

```
Bug: User search returns incorrect results

Plan:
1. Write failing test that reproduces bug
2. Debug to find root cause
3. Implement fix
4. Verify fix with test
5. Check for regressions

Execution:

Task 1: Failing Test
---
Dispatch:
"Write test that demonstrates search bug:
- Create 3 users: Alice, Bob, Charlie
- Search for 'Alice'
- Assert only Alice returned
- Bug: Currently returns all users"

Review:
✅ Test written
✅ Test fails (demonstrates bug)
Complete ✅
---

Task 2: Debug Root Cause
---
Dispatch:
"Debug why search returns all users.
Use root-cause-tracing skill.
Don't fix yet, just identify cause."

Review:
✅ Root cause identified: Missing WHERE clause
✅ Traced to User::search() method
✅ Issue: $query variable shadowed
Complete ✅
---

Task 3: Implement Fix
---
Dispatch:
"Fix the bug in User::search() method:
- Add proper WHERE clause
- Use correct $query variable
- Don't break existing functionality"

Review:
✅ Fix implemented
✅ Test now passes
✅ Code is clean
Complete ✅
---

Task 4: Verify Fix
---
Dispatch:
"Run full test suite to verify fix"

Review:
✅ Original test passes
✅ All other tests pass
✅ No regressions
Complete ✅
---

Task 5: Check Regressions
---
Dispatch:
"Manually test related features:
- User list
- User filter
- Admin search"

Review:
✅ All related features work
✅ No side effects
Complete ✅
---

Final Review:
- Bug fixed
- Tests pass
- No regressions
Bug fix complete ✅
```

### Example 3: Refactoring Workflow

```
Refactor: Extract authentication logic to service

Plan:
1. Write tests for existing behavior (safety net)
2. Create AuthService
3. Move logic to service
4. Update controllers to use service
5. Run tests (should still pass)
6. Cleanup old code

Execution:

Task 1: Safety Tests
---
Dispatch:
"Write tests for current authentication behavior:
- Login succeeds with correct credentials
- Login fails with wrong credentials
- Logout invalidates token
- Token refresh works"

Review:
✅ All current behaviors tested
✅ All tests pass (baseline)
Complete ✅
---

Task 2: Create Service
---
Dispatch:
"Create AuthService with empty methods:
- login($credentials)
- logout($user)
- refresh($token)
Don't implement yet, just structure"

Review:
✅ Service created
✅ Method signatures correct
✅ Dependency injection setup
Complete ✅
---

Task 3: Move Login Logic
---
Dispatch:
"Move login logic from AuthController to AuthService.login()
Keep controller thin, just calling service"

Review:
✅ Logic moved to service
✅ Controller simplified
⚠️ Tests fail (need to update)

Feedback:
"Tests failing is expected. We'll fix in next task."

Complete ✅
---

Task 4: Update Tests
---
Dispatch:
"Update tests to work with new AuthService structure"

Review:
✅ Tests updated
✅ All tests pass again
Complete ✅
---

Task 5: Move Remaining Logic
---
Dispatch:
"Move logout and refresh logic to AuthService"

Review:
✅ All auth logic in service
✅ Tests still pass
✅ Controllers are thin
Complete ✅
---

Task 6: Cleanup
---
Dispatch:
"Remove unused code from AuthController"

Review:
✅ Dead code removed
✅ Imports cleaned up
✅ Tests still pass
Complete ✅
---

Final Review:
- All logic extracted to service
- All tests pass
- Code is cleaner
Refactor complete ✅
```

## Subagent Best Practices

### Practice 1: Fresh Context

```
✅ GOOD:
Each subagent gets only what it needs:
- Current task description
- Relevant context
- Success criteria
- Constraints

❌ BAD:
Dumping entire project history:
- All previous tasks
- All discussions
- All decisions
- Everything ever
```

### Practice 2: Clear Boundaries

```
✅ GOOD:
"Task: Create user migration
Don't: Create model, controller, or tests"

❌ BAD:
"Task: Do the user stuff"
```

### Practice 3: Explicit Success Criteria

```
✅ GOOD:
Success criteria:
- [ ] Migration file created
- [ ] All fields included
- [ ] Indexes defined
- [ ] Rollback method works

❌ BAD:
"Make it good"
```

### Practice 4: One Task at a Time

```
✅ GOOD:
Task 1: Create migration
→ Review → Complete
Task 2: Create model
→ Review → Complete

❌ BAD:
Task 1: Create migration and model and controller
→ Too much in one task
```

## Anti-Patterns to Avoid

### ❌ Skipping Reviews

```
BAD:
Task 1 → Complete (no review)
Task 2 → Complete (no review)
Task 3 → Complete (no review)
Final: Everything is broken

GOOD:
Task 1 → Review → Fix issues → Complete
Task 2 → Review → Fix issues → Complete
Task 3 → Review → Fix issues → Complete
Final: Everything works
```

### ❌ Parallel Dispatch Without Plan

```
BAD:
Dispatch 5 subagents at once for different tasks
→ Conflicts
→ Inconsistencies
→ Wasted work

GOOD:
Dispatch one at a time
→ Review each
→ Learn from each
→ Adapt plan if needed
```

### ❌ Vague Instructions

```
BAD:
"Fix the auth system"
→ Subagent doesn't know where to start

GOOD:
"Add password reset functionality:
1. Create password_resets table
2. Add reset token generation
3. Create reset form
4. Send reset email
5. Implement token validation"
```

### ❌ Accepting "Good Enough"

```
BAD:
Review: "This mostly works, ship it"
→ Technical debt
→ Future bugs

GOOD:
Review: "This works but has issues:
1. Missing error handling
2. No validation
Please fix before marking complete"
```

## Integration with Skills

**Required:**
- `writing-plans` - Create clear task plan first
- `executing-plans` - Follow plan systematically
- `code-review` - Review subagent output

**Use with:**
- `verification-before-completion` - Final checks
- `git-workflow` - Commit after each task
- `test-driven-development` - Each task can be TDD

**Enables:**
- `dispatching-parallel-agents` - When tasks are independent
- `systematic-debugging` - Each task easier to debug

## Checklist

Before dispatching subagent:
- [ ] Task clearly defined
- [ ] Success criteria explicit
- [ ] Context provided (minimal)
- [ ] Constraints stated

After subagent completes:
- [ ] Output reviewed thoroughly
- [ ] Issues documented
- [ ] Feedback provided if needed
- [ ] Acceptance criteria met
- [ ] Ready to mark complete

Before final completion:
- [ ] All tasks complete
- [ ] Integration tested
- [ ] No gaps between tasks
- [ ] Original goal achieved

## Authority

**This skill is based on:**
- Divide-and-conquer problem-solving methodology
- Code review best practices (pull request workflow)
- Quality gates in software development
- Systematic review processes from manufacturing (Toyota)

**Research**: Studies show reviewed work has 40-60% fewer defects than unreviewed work.

**Social Proof**: All professional development teams use review checkpoints.

## Your Commitment

When using subagents:
- [ ] I will review every task output
- [ ] I will not skip reviews to save time
- [ ] I will provide clear feedback
- [ ] I will not accept "good enough"
- [ ] I will dispatch one task at a time (unless truly independent)
- [ ] I will maintain quality standards
- [ ] I will do final integration review

---

**Bottom Line**: Fresh subagent per task. Review between tasks. No shortcuts. Quality over speed. Each checkpoint prevents downstream errors from compounding.
