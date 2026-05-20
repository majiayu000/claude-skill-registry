---
name: dispatching-parallel-agents
description: "Use when multiple independent tasks can run simultaneously. Enables efficient parallel work execution with specialized agents."
---

# Dispatching Parallel Agents

## Core Principle

When tasks are independent and can run simultaneously, dispatch multiple agents in parallel rather than sequentially. This maximizes efficiency and reduces total time to completion.

## When to Use This Skill

- Multiple independent features to implement
- Separate bugs to fix that don't interact
- Different components that can be worked on simultaneously
- Code review and testing can happen in parallel
- Documentation and implementation don't block each other

## The Iron Law

**Only parallelize TRULY INDEPENDENT tasks.**

Dependent tasks MUST run sequentially, or you'll create conflicts and waste time.

## Identifying Parallelizable Work

### ✅ Good Candidates for Parallel Execution

- **Independent features**: Authentication and payment system
- **Separate components**: Frontend and backend work
- **Different skill domains**: Code review while writing docs
- **Non-overlapping files**: Different controllers, models, views
- **Isolated bug fixes**: Login bug and API bug

### ❌ Bad Candidates (Must Be Sequential)

- **Dependent features**: Database migration then seeder (seeder needs migration)
- **Same files**: Two changes to same controller
- **Build dependencies**: Tests need code to be written first
- **Data dependencies**: Need user model before user controller

## Dependency Analysis Checklist

Before parallelizing, ask:
- [ ] Do these tasks touch the same files?
- [ ] Does Task B need Task A's results?
- [ ] Will these tasks create merge conflicts?
- [ ] Are there shared resources (database, cache, files)?
- [ ] Can these tasks be independently tested?

**If ANY answer is YES → Do NOT parallelize**

## Parallel Agent Dispatch Protocol

### Step 1: Identify Independent Tasks

```
I'm analyzing which tasks can run in parallel.

Task List:
1. Implement authentication (AuthController, User model, routes)
2. Implement payment processing (PaymentController, Payment model, routes)
3. Create API documentation (swagger/openapi)
4. Set up email notifications (NotificationService)

Dependency Analysis:
- Authentication: touches auth files only ✅
- Payment: touches payment files only ✅
- API docs: reads code, doesn't modify ✅
- Email: touches notification files only ✅

All tasks are independent → Can parallelize ✅
```

### Step 2: Plan Agent Assignments

```
Parallel Agent Plan:

Agent 1: Authentication Implementation
- Files: AuthController, User model, routes/api.php (auth section)
- Skills: brainstorming, writing-plans, executing-plans, test-driven-development
- Estimated time: 60 minutes

Agent 2: Payment Processing Implementation
- Files: PaymentController, Payment model, routes/api.php (payment section)
- Skills: brainstorming, writing-plans, executing-plans, test-driven-development
- Estimated time: 90 minutes

Agent 3: API Documentation Generation
- Files: API docs (generated), PHPDoc comments
- Skills: API documentation generation
- Estimated time: 30 minutes

Agent 4: Email Notification Setup
- Files: NotificationService, email templates
- Skills: writing-plans, executing-plans
- Estimated time: 45 minutes

Expected total time: 90 minutes (longest agent)
Sequential time would be: 225 minutes (60+90+30+45)
Time saved: 135 minutes (60% reduction)
```

### Step 3: Dispatch Agents

**IMPORTANT**: Use Claude Code's parallel tool invocation

```
Dispatching 4 agents in parallel:

[Invoke all 4 Task tools simultaneously in a single message]
```

Example tool invocations:
```
Task 1: Implement authentication
Task 2: Implement payment processing
Task 3: Generate API documentation
Task 4: Set up email notifications
```

### Step 4: Monitor Progress

```
Parallel Agent Status:

Agent 1 (Auth): ✅ Completed in 58 minutes
Agent 2 (Payment): 🔄 In progress (Task 4 of 6)
Agent 3 (API Docs): ✅ Completed in 25 minutes
Agent 4 (Email): ✅ Completed in 42 minutes

Waiting for Agent 2 to complete...
```

### Step 5: Integrate Results

```
All agents completed. Integrating results:

Agent 1 (Auth):
- ✅ AuthController created with tests
- ✅ User model with authentication
- ✅ Routes added to api.php
- ✅ 12 tests, all passing

Agent 2 (Payment):
- ✅ PaymentController created with tests
- ✅ Payment model with Stripe integration
- ✅ Routes added to api.php
- ✅ 18 tests, all passing

Agent 3 (API Docs):
- ✅ OpenAPI documentation generated
- ✅ All endpoints documented
- ✅ Available at /docs/api

Agent 4 (Email):
- ✅ NotificationService created
- ✅ Email templates for auth events
- ✅ Queue configuration
- ✅ 5 tests, all passing

Integration Check:
- Merge conflicts? Checking...
- ✅ No conflicts (agents worked on independent files)
- ✅ All tests still pass after merge
- ✅ API docs include all endpoints
```

## Using Git Worktrees with Parallel Agents

For maximum isolation, combine with `git-worktrees` skill:

```bash
# Create worktrees for each agent
git worktree add -b feature/authentication ../myapp-auth main
git worktree add -b feature/payment ../myapp-payment main
git worktree add -b feature/email ../myapp-email main

# Dispatch agents to work in separate worktrees
# Agent 1 works in ../myapp-auth
# Agent 2 works in ../myapp-payment
# Agent 3 works in ../myapp-email

# After completion, merge one by one
git checkout main
git merge feature/authentication
git merge feature/payment
git merge feature/email

# Clean up worktrees
git worktree remove ../myapp-auth
git worktree remove ../myapp-payment
git worktree remove ../myapp-email
```

## Parallel Testing Strategy

When parallelizing implementation, parallel testing is critical:

```
Testing Strategy for Parallel Work:

Each agent MUST:
1. Use database-backup skill before tests
2. Use separate test databases (if possible)
3. Run tests in isolation
4. Report test results independently

Test Database Isolation:
- Agent 1: DB_DATABASE=testing_auth
- Agent 2: DB_DATABASE=testing_payment
- Agent 3: No database (docs only)
- Agent 4: DB_DATABASE=testing_email

After all agents complete:
- Run full integration test suite
- Verify no conflicts or regressions
```

## Examples

### Example 1: Microservices Development

```
Task: Create two independent microservices

Parallel Plan:
Agent 1: User Service
- CRUD operations for users
- Authentication
- Independent database

Agent 2: Order Service
- CRUD operations for orders
- Independent database
- No dependency on User Service yet

These are perfect for parallel work:
- Different codebases
- Different databases
- No shared code
- Can be tested independently

Dispatch agents in parallel → Save 50% time
```

### Example 2: Frontend + Backend Split

```
Task: Add user profile feature

Parallel Plan:
Agent 1: Backend API
- ProfileController with GET/PUT endpoints
- Profile model
- Validation
- Tests
Files: backend/app/Http/Controllers/ProfileController.php, etc.

Agent 2: Frontend UI
- Profile page component
- API integration
- Form validation
- Tests
Files: frontend/src/components/Profile.tsx, etc.

Independence check:
✅ Different directories (backend/ vs frontend/)
✅ Can work on API contract simultaneously
✅ Can test independently (mock API for frontend)

Dispatch agents in parallel → Complete in single timeframe
```

### Example 3: Bug Fixes

```
Task: Fix multiple unrelated bugs

Parallel Plan:
Agent 1: Login validation bug
Files: AuthController.php, LoginRequest.php
Tests: AuthenticationTest.php

Agent 2: API rate limiting bug
Files: RateLimitMiddleware.php
Tests: RateLimitTest.php

Agent 3: Email template bug
Files: WelcomeEmail.php, welcome.blade.php
Tests: EmailTest.php

Independence check:
✅ Different files
✅ No shared dependencies
✅ Can be tested independently

Dispatch 3 agents in parallel → 3x faster completion
```

## Red Flags (Don't Parallelize)

- ❌ Tasks touch same files
- ❌ Task B needs Task A's output
- ❌ Shared database without isolation
- ❌ Changes to same API endpoints
- ❌ Modifying same configuration files
- ❌ Creating same migrations
- ❌ Not enough information to ensure independence

## Common Rationalizations to Reject

- ❌ "They're probably independent" → KNOW they're independent
- ❌ "We can fix conflicts later" → Avoid conflicts by not parallelizing
- ❌ "Parallelizing will be faster" → Only if truly independent
- ❌ "Let's try and see" → Analyze dependencies first

## When Parallelization Goes Wrong

If you dispatch parallel agents and encounter issues:

```
❌ Parallel Agent Conflict Detected

Agent 1 and Agent 2 both modified: routes/api.php

Conflict:
Agent 1 added auth routes
Agent 2 added payment routes
Same file, merge conflict

Resolution:
1. Stop remaining agents
2. Manually merge changes
3. Re-run tests
4. Lesson: Should have split routes/api.php by concern first

Prevention:
- Better dependency analysis
- Split shared files first
- Use more granular tasks
```

## Integration with Skills

**Prerequisites:**
- `brainstorming` - Identify all work
- `writing-plans` - Break into tasks
- Dependency analysis

**Use with:**
- `git-worktrees` - Isolate work in separate directories
- `executing-plans` - Each agent executes its plan
- `code-review` - Parallel reviews possible

**After completion:**
- `code-review` - Review integrated result
- `verification-before-completion` - Full system test

## Parallel Agent Checklist

Before dispatching parallel agents:
- [ ] Tasks are truly independent (no shared files)
- [ ] No dependencies between tasks
- [ ] Each task can be tested independently
- [ ] Database isolation configured (if needed)
- [ ] Clear agent assignments and responsibilities
- [ ] Estimated time for each agent
- [ ] Plan for integrating results

During parallel execution:
- [ ] Monitor agent progress
- [ ] Watch for unexpected conflicts
- [ ] Ready to intervene if issues arise

After completion:
- [ ] Integrate results from all agents
- [ ] Check for merge conflicts
- [ ] Run full integration tests
- [ ] Verify nothing broken

## Authority

**This skill is based on:**
- Software engineering: Parallel development practices
- Efficiency: Reduce total completion time
- Resource utilization: Multiple AI agents available
- Professional teams: How large teams work in parallel

**Social Proof**: Large tech companies have hundreds of developers working in parallel on independent features.

## Your Commitment

Before dispatching parallel agents:
- [ ] I have analyzed dependencies thoroughly
- [ ] I am certain tasks are independent
- [ ] I have a plan for integration
- [ ] I will monitor progress
- [ ] I will not parallelize for the sake of speed

---

**Bottom Line**: Parallel agents are powerful when tasks are truly independent. Analyze dependencies first, dispatch in parallel, integrate carefully. When done right, you can achieve 50-75% time reduction.
