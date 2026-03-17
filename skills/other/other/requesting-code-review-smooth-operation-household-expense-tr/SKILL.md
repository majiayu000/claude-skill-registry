---
name: requesting-code-review
description: "Use when completing tasks or major features. Know when and how to request reviews. Provides git commit range to code-reviewer agent."
---

# Requesting Code Review

## Core Principle

**Request reviews at logical completion points with clear context.**

## Overview

Code review is most effective when requested at appropriate times with sufficient context. This skill defines when to request reviews and how to provide reviewers with what they need.

## When to Request Review

### Always Request Review:
- ✅ After completing individual planned tasks
- ✅ Upon finishing major features before merging
- ✅ Before merging to main/master branch
- ✅ When PR/MR is ready for human review

### Consider Requesting Review:
- ⚠️ After significant refactoring
- ⚠️ When implementing complex algorithms
- ⚠️ After fixing critical bugs
- ⚠️ When uncertain about approach

### Don't Request Review:
- ❌ Mid-task (wait until task complete)
- ❌ Work in progress (unless seeking early feedback)
- ❌ Trivial changes (typos, formatting)
- ❌ Before self-review complete

## Review Request Protocol

### Step 1: Complete Self-Review First

**MANDATORY:** Use `code-review` skill before requesting external review

```
I'm completing self-review using the code-review skill before requesting external review.

[Perform comprehensive self-review]

Self-review complete ✅
- All tests pass
- No obvious issues found
- Code quality verified

Now ready for external review.
```

### Step 2: Identify Commit Range

```bash
# Find first commit of your feature branch
git log --oneline --reverse origin/main..HEAD | head -1

# Find last commit
git log --oneline -1

# Example output:
abc1234 feat: add authentication (first commit)
def5678 test: add authentication tests (last commit)
```

### Step 3: Request Review from Code-Reviewer Agent

**Template:**
```
I'm requesting code review using the code-reviewer agent.

Commit range: abc1234..def5678
Feature: User authentication implementation

Context:
- Implemented JWT token authentication with Laravel Sanctum
- Added registration, login, logout endpoints
- Includes 15 tests covering auth flows
- API documentation generated

Please review for:
- Security vulnerabilities
- Performance issues
- Test coverage
- Code quality

Dispatching code-reviewer agent...
```

### Step 4: Deploy Code-Reviewer Agent

```
[Use Task tool to deploy code-reviewer agent]

Agent prompt:
You are a specialized code reviewer.

Review the changes in commit range abc1234..def5678.

Focus areas:
- Security (authentication implementation)
- Performance (database queries)
- Test coverage (15 new tests)
- Code quality (controller, service, model)

Provide detailed review with:
- Critical issues (must fix)
- Important issues (should fix)
- Minor issues (nice to have)
- Positive observations

Use the code-review skill for systematic review.
```

### Step 5: Process Review Results

```
Code Review Results Received:

Critical Issues (0):
[None found]

Important Issues (2):
1. [Issue description]
   - Impact: [Explanation]
   - Fix: [Recommendation]

2. [Issue description]
   - Impact: [Explanation]
   - Fix: [Recommendation]

Minor Issues (1):
1. [Issue description]
   - Suggestion: [Recommendation]

I'll address the important issues before proceeding.
```

## Review Request Formats

### Format 1: For Agent Review

```
Code Review Request

Commit Range: [first-commit]..[last-commit]
Branch: feature/authentication
Base: main

Changes:
- Added AuthController with 3 endpoints
- Created 15 authentication tests
- Updated API documentation
- Added Sanctum dependency

Files Changed: 12 files
Lines Added: +450
Lines Removed: -20

Focus Areas:
- Security: JWT implementation
- Performance: Database queries
- Tests: Coverage and quality

Requesting code-reviewer agent dispatch.
```

### Format 2: For Human Review (PR/MR)

```markdown
## Code Review Request

**Branch:** feature/authentication
**Commits:** abc1234..def5678 (8 commits)
**Changes:** Authentication system implementation

### What Changed
- Implemented JWT authentication with Laravel Sanctum
- Added user registration endpoint
- Added login/logout endpoints
- Protected routes with auth middleware
- 15 tests covering auth flows

### How to Review
1. Check out branch: `git checkout feature/authentication`
2. Run tests: `./scripts/safe-test.sh vendor/bin/paratest`
3. Test endpoints: See API docs at `/docs/api`

### Focus Areas
- **Security**: JWT implementation, password hashing
- **Performance**: Database queries (should be no N+1)
- **Tests**: Coverage of edge cases

### Self-Review Completed
- ✅ All tests pass (127 total, 15 new)
- ✅ No security issues found
- ✅ Performance verified
- ✅ Code quality checked

Ready for review.
```

## Severity Levels (From Code-Reviewer)

### Critical Issues
**Definition:** Must fix immediately, blocks merge

**Examples:**
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Tests failing

**Action:** Fix before any further work

### Important Issues
**Definition:** Should fix before merging

**Examples:**
- Performance problems (N+1 queries)
- Missing error handling
- Incomplete test coverage
- Code quality issues

**Action:** Resolve before merge, document if deferring

### Minor Issues
**Definition:** Nice to have, can defer

**Examples:**
- Naming improvements
- Additional comments
- Refactoring opportunities
- Style inconsistencies

**Action:** Fix if quick, otherwise create follow-up issue

## Examples

### Example 1: Task Completion Review

```
Task Complete: User Registration Endpoint

I'm requesting code review before marking task complete.

Commit: abc1234
Changes:
- Added POST /api/register endpoint
- Validation for email/password
- Returns JWT token on success
- 5 tests added

Self-review complete ✅

Requesting code-reviewer agent for commit abc1234.
```

### Example 2: Feature Complete Review

```
Feature Complete: Authentication System

I'm requesting comprehensive code review before creating PR.

Commit range: abc1234..def5678 (8 commits)

Changes summary:
- Registration endpoint
- Login endpoint
- Logout endpoint
- Protected route middleware
- 15 tests
- API documentation

Self-review complete ✅

Critical focus areas:
- Security: JWT implementation
- Performance: Database queries
- Tests: Edge case coverage

Requesting code-reviewer agent for full feature review.
```

### Example 3: Pre-Merge Review

```
Ready for Merge: Authentication Feature

Final code review before merging to main.

Branch: feature/authentication
Commits: abc1234..def5678
Base: main (up to date)

All previous review feedback addressed:
✅ Added rate limiting
✅ Fixed N+1 query
✅ Added missing test cases

Final check requested before merge.

Requesting code-reviewer agent for final review.
```

## Common Mistakes

### Mistake 1: No Self-Review First

```
❌ Bad: Requesting review without self-review
"Please review my code" [without checking yourself first]

✅ Good: Self-review then request
"I've completed self-review (all tests pass, no issues found).
Requesting code review for commit range abc1234..def5678"
```

### Mistake 2: Vague Request

```
❌ Bad: No context
"Please review"

✅ Good: Clear context
"Please review authentication implementation (commits abc1234..def5678).
Focus on security and performance. 15 new tests added."
```

### Mistake 3: Wrong Timing

```
❌ Bad: Mid-implementation
"I'm halfway through, can you review what I have so far?"

✅ Good: At completion
"Implementation complete, all tests passing. Ready for review."
```

### Mistake 4: No Commit Range

```
❌ Bad: Unclear what to review
"Review the authentication feature"

✅ Good: Specific commits
"Review commits abc1234..def5678 (authentication feature)"
```

## Integration with Other Skills

**Prerequisites:**
- `code-review` - Self-review BEFORE requesting external review
- `verification-before-completion` - Verify all tests pass

**Use with:**
- `receiving-code-review` - Process feedback received
- `finishing-a-development-branch` - After review approved

**Agents:**
- Deploy `code-reviewer` agent for automated review

## Review Request Checklist

Before requesting review:
- [ ] Self-review completed using `code-review` skill
- [ ] All tests pass
- [ ] No debugging code left in
- [ ] Commit messages clear
- [ ] Branch up to date with base
- [ ] Commit range identified
- [ ] Context provided (what changed, why, how to test)

## Authority

**This skill is based on:**
- Professional code review practices
- Industry standard: Reviews at logical completion points
- Efficient reviewer time usage
- Clear communication best practices

**Social Proof**: All professional development teams use structured code review processes.

## Your Commitment

When requesting reviews:
- [ ] I will complete self-review first
- [ ] I will provide clear commit ranges
- [ ] I will give sufficient context
- [ ] I will request at appropriate times
- [ ] I will not waste reviewer time

---

**Bottom Line**: Request reviews at completion points with clear context. Self-review first, then provide commit range and focus areas to reviewer.
