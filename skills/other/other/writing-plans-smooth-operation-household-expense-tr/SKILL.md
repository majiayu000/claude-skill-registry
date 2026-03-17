---
name: writing-plans
description: "Use after brainstorming, before implementation. Breaks work into discrete, actionable tasks with clear verification points."
---

# Writing Plans

## Core Principle

After brainstorming and getting user approval, break the work into a detailed, step-by-step plan BEFORE coding.

## When to Use This Skill

- After completing `brainstorming` skill and getting user approval
- User explicitly asks for an implementation plan
- Task has 3+ distinct steps
- Work involves multiple files or systems
- Dependencies between tasks exist

## The Iron Law

**NEVER start implementation without a written plan for non-trivial work.**

A plan:
- Forces you to think through the full scope
- Identifies dependencies and potential issues early
- Gives the user visibility into your approach
- Provides checkpoints to verify progress
- Prevents "I forgot to do X" mistakes

## Plan Writing Protocol

### Step 1: Announce the Planning Phase

**Template:**
```
Great! Now let me create a detailed implementation plan.

I'm using the writing-plans skill to break this down into discrete tasks.
```

### Step 2: Break Down into Tasks

Each task should be:
- **Discrete**: Can be completed independently
- **Actionable**: Clear what to do
- **Verifiable**: Clear how to verify it's done
- **Appropriately sized**: 5-30 minutes of work

**Task Format:**
```
## Task [Number]: [Clear, action-oriented name]

**Purpose**: What this accomplishes
**Actions**:
- [Specific step 1]
- [Specific step 2]
**Files affected**: [List of files]
**Verification**: How to confirm this works
**Dependencies**: Requires Task X to be completed first
```

### Step 3: Identify Dependencies

Make dependencies explicit:
```
Task 2 depends on Task 1 (needs database schema)
Task 5 depends on Tasks 2, 3, 4 (needs all API endpoints)
```

This prevents:
- Starting tasks out of order
- Discovering blocking issues mid-implementation
- Inefficient back-and-forth

### Step 4: Add Verification Checkpoints

For each task, specify:
- **How to verify**: What test/check confirms success
- **Expected outcome**: What should happen
- **Rollback**: How to undo if it fails

**Example:**
```
**Verification**:
- Run `php artisan test --filter=AuthenticationTest`
- Expected: All tests pass
- If fails: Rollback migration with `php artisan migrate:rollback`
```

### Step 5: Create TodoWrite Entries

**MANDATORY**: Convert plan to TodoWrite todos

**Never work through plans mentally**. Always create explicit todos:
```
I'm creating todos for each task in the plan.
```

Each plan task becomes ONE todo item:
- Use the task name as the `content`
- Provide `activeForm` (present continuous)
- Start with status: `pending`

### Step 6: Estimate Complexity

For each task, indicate:
- **Simple**: Straightforward, low risk
- **Moderate**: Some complexity, medium risk
- **Complex**: High complexity, needs extra care

This helps users understand time investment.

### Step 7: Get User Approval

**Template:**
```
Here's my implementation plan with [X] tasks.

Does this plan make sense? Any tasks I should add, remove, or change?
```

Wait for approval before moving to `executing-plans` skill.

## Plan Template

```markdown
# Implementation Plan: [Feature Name]

## Overview
**Goal**: [What we're building]
**Approach**: [Brief summary of chosen approach from brainstorming]
**Estimated tasks**: [Number]
**Estimated time**: [Rough estimate]

## Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Tasks

### Task 1: [Name]
**Purpose**: [What this accomplishes]
**Complexity**: Simple/Moderate/Complex
**Actions**:
1. [Specific step]
2. [Specific step]
**Files affected**:
- `path/to/file1.php`
- `path/to/file2.php`
**Verification**: [How to verify]
**Dependencies**: None

### Task 2: [Name]
**Purpose**: [What this accomplishes]
**Complexity**: Simple/Moderate/Complex
**Actions**:
1. [Specific step]
2. [Specific step]
**Files affected**:
- `path/to/file3.php`
**Verification**: [How to verify]
**Dependencies**: Task 1

[Continue for all tasks...]

## Risk Assessment
**Potential issues**:
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Rollback Plan
If something goes wrong:
1. [Rollback step 1]
2. [Rollback step 2]

## Success Criteria
When complete, we should have:
- [ ] [Criteria 1]
- [ ] [Criteria 2]
- [ ] All tests passing
- [ ] Documentation updated
```

## Red Flags (Plan is Inadequate)

- ❌ Vague tasks: "Set up authentication" → Too broad
- ❌ No verification: Can't tell if task succeeded
- ❌ Missing dependencies: Tasks in wrong order
- ❌ No file paths: Unclear what needs changing
- ❌ No rollback: Can't undo if it fails
- ❌ Only 1-2 tasks: Probably not detailed enough

## Common Rationalizations to Reject

- ❌ "I'll figure it out as I go" → Plan first, code second
- ❌ "The plan is in my head" → Write it down
- ❌ "Plans take too long" → Planning SAVES time
- ❌ "I'll just start and see what happens" → Recipe for failure
- ❌ "It's a simple feature" → Simple features still need plans

## Integration with Other Skills

**Before writing-plans**: Use `brainstorming` skill
**After writing-plans**: Use `executing-plans` skill
**During execution**: Use `database-backup` skill for database tasks
**After completion**: Use `code-review` and `verification-before-completion` skills

## Examples

### Example 1: Add User Authentication

```markdown
# Implementation Plan: User Authentication with Laravel Sanctum

## Overview
**Goal**: Add token-based authentication to API
**Approach**: Laravel Sanctum with email/password login
**Estimated tasks**: 6
**Estimated time**: 60-90 minutes

## Prerequisites
- [ ] Laravel project is set up
- [ ] Database is configured and backed up
- [ ] Paratest is installed

## Tasks

### Task 1: Install and Configure Sanctum
**Purpose**: Add Sanctum package to project
**Complexity**: Simple
**Actions**:
1. Run `composer require laravel/sanctum`
2. Publish configuration: `php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"`
3. Run migration: `php artisan migrate` (with backup!)
4. Add Sanctum middleware to `app/Http/Kernel.php`
**Files affected**:
- `composer.json`
- `config/sanctum.php`
- `app/Http/Kernel.php`
**Verification**:
- `php artisan route:list` shows Sanctum routes
- No errors during migration
**Dependencies**: None

### Task 2: Create Authentication Controller
**Purpose**: Handle login/logout/register endpoints
**Complexity**: Moderate
**Actions**:
1. Create `app/Http/Controllers/AuthController.php`
2. Implement `register()` method with validation
3. Implement `login()` method with token generation
4. Implement `logout()` method with token revocation
**Files affected**:
- `app/Http/Controllers/AuthController.php` (new)
**Verification**: Controller file exists with all methods
**Dependencies**: Task 1

### Task 3: Add API Routes
**Purpose**: Expose authentication endpoints
**Complexity**: Simple
**Actions**:
1. Add routes to `routes/api.php`:
   - POST /register
   - POST /login
   - POST /logout (protected)
**Files affected**:
- `routes/api.php`
**Verification**: `php artisan route:list` shows new routes
**Dependencies**: Task 2

### Task 4: Create Authentication Tests
**Purpose**: Ensure auth works correctly
**Complexity**: Moderate
**Actions**:
1. Create `tests/Feature/AuthenticationTest.php`
2. Test registration with valid data
3. Test registration with invalid data
4. Test login with correct credentials
5. Test login with wrong credentials
6. Test logout functionality
7. Test protected route access
**Files affected**:
- `tests/Feature/AuthenticationTest.php` (new)
**Verification**: Tests exist (don't run yet)
**Dependencies**: Task 3

### Task 5: Run Tests with Database Backup
**Purpose**: Verify implementation works
**Complexity**: Simple
**Actions**:
1. Use database-backup skill (MANDATORY)
2. Run `./scripts/safe-test.sh vendor/bin/paratest --filter=AuthenticationTest`
3. Verify all tests pass
**Files affected**: None
**Verification**: All authentication tests pass
**Dependencies**: Task 4, database-backup skill

### Task 6: Update API Documentation
**Purpose**: Document new endpoints
**Complexity**: Simple
**Actions**:
1. Add PHPDoc comments to AuthController methods
2. Generate OpenAPI docs: `php artisan scramble:generate`
3. Verify endpoints appear in `/docs/api`
**Files affected**:
- `app/Http/Controllers/AuthController.php`
- API documentation (auto-generated)
**Verification**: Can see auth endpoints in API docs
**Dependencies**: Task 5

## Risk Assessment
**Potential issues**:
- **Database migration fails**: Ensure database is backed up (Task 1)
- **Tests fail**: Common issue is missing .env.testing config
- **Token not generated**: Check Sanctum middleware is in Kernel.php

## Rollback Plan
If something goes wrong:
1. Rollback database: `php artisan migrate:rollback`
2. Remove Sanctum package: `composer remove laravel/sanctum`
3. Restore from backup if needed
4. Delete created files

## Success Criteria
When complete, we should have:
- [ ] Users can register via POST /register
- [ ] Users can login and receive token via POST /login
- [ ] Users can logout via POST /logout
- [ ] Protected routes require valid token
- [ ] All authentication tests pass
- [ ] API documentation includes auth endpoints
```

### Example 2: Add Database Activity Logging

```markdown
# Implementation Plan: User Activity Logging

## Overview
**Goal**: Track user actions in activity_logs table
**Approach**: Database table with observer pattern
**Estimated tasks**: 5
**Estimated time**: 45-60 minutes

## Prerequisites
- [ ] Database is backed up (MANDATORY)
- [ ] User model exists

## Tasks

### Task 1: Create Migration for Activity Logs
**Purpose**: Add activity_logs table
**Complexity**: Simple
**Actions**:
1. Backup database (MANDATORY - use database-backup skill)
2. Create migration: `php artisan make:migration create_activity_logs_table`
3. Add columns: id, user_id, action, description, ip_address, user_agent, timestamps
4. Add indexes on user_id and created_at
5. Run migration: `php artisan migrate`
**Files affected**:
- `database/migrations/[timestamp]_create_activity_logs_table.php` (new)
**Verification**:
- Table exists: `php artisan db:show --table=activity_logs`
- Has correct columns and indexes
**Dependencies**: None (but requires database-backup skill FIRST)

### Task 2: Create ActivityLog Model
**Purpose**: Eloquent model for activity_logs
**Complexity**: Simple
**Actions**:
1. Create `app/Models/ActivityLog.php`
2. Define fillable fields
3. Add relationship to User model
4. Add cast for created_at (immutable)
**Files affected**:
- `app/Models/ActivityLog.php` (new)
**Verification**: Model file exists with proper structure
**Dependencies**: Task 1

### Task 3: Create Activity Logger Service
**Purpose**: Centralized logging logic
**Complexity**: Moderate
**Actions**:
1. Create `app/Services/ActivityLogger.php`
2. Implement `log()` method that captures:
   - User ID (from auth)
   - Action name
   - Description
   - IP address (from request)
   - User agent (from request)
3. Add helper function for easy access
**Files affected**:
- `app/Services/ActivityLogger.php` (new)
**Verification**: Service class exists with log() method
**Dependencies**: Task 2

### Task 4: Add Logging to Auth Controller
**Purpose**: Log authentication events
**Complexity**: Simple
**Actions**:
1. Update `app/Http/Controllers/AuthController.php`
2. Log "user.registered" on registration
3. Log "user.logged_in" on successful login
4. Log "user.logged_out" on logout
**Files affected**:
- `app/Http/Controllers/AuthController.php`
**Verification**: Code review - logging calls added
**Dependencies**: Task 3

### Task 5: Create Tests and Verify
**Purpose**: Ensure logging works
**Complexity**: Moderate
**Actions**:
1. Create `tests/Feature/ActivityLogTest.php`
2. Test that registration creates log entry
3. Test that login creates log entry
4. Test that logout creates log entry
5. Test that log contains correct data (IP, user agent)
6. Backup database (MANDATORY)
7. Run tests: `./scripts/safe-test.sh vendor/bin/paratest --filter=ActivityLogTest`
**Files affected**:
- `tests/Feature/ActivityLogTest.php` (new)
**Verification**: All activity log tests pass
**Dependencies**: Task 4, database-backup skill

## Risk Assessment
**Potential issues**:
- **Migration fails**: Database backup ensures we can rollback
- **Logs get too large**: Add cleanup task (30 days retention)
- **Performance impact**: Indexes on user_id and created_at mitigate this

## Rollback Plan
If something goes wrong:
1. Rollback migration: `php artisan migrate:rollback`
2. Remove logging calls from AuthController
3. Delete ActivityLogger service
4. Delete ActivityLog model

## Success Criteria
When complete, we should have:
- [ ] activity_logs table exists with proper schema
- [ ] ActivityLog model and ActivityLogger service created
- [ ] User registration/login/logout creates log entries
- [ ] Logs contain user_id, action, IP, user agent, timestamp
- [ ] All tests pass
- [ ] No performance degradation
```

## Authority

**This skill is based on**:
- Software engineering best practice: Design before implementation
- Agile methodology: Break work into small, verifiable increments
- Empirical evidence: Planned work is 3-5x more likely to succeed
- Professional experience: Plans prevent forgotten requirements

**Social Proof**: Professional developers ALWAYS plan before coding. No exceptions.

## Your Commitment

Before using this skill, confirm:
- [ ] I will ALWAYS create a written plan for non-trivial work
- [ ] I will BREAK DOWN work into discrete, verifiable tasks
- [ ] I will CREATE TodoWrite entries for all tasks
- [ ] I will GET USER APPROVAL before executing the plan

---

**Bottom Line**: Plans don't take extra time - they reveal the time required. Write the plan, then execute it systematically.
