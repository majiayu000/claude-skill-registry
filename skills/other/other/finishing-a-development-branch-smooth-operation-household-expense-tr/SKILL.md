---
name: finishing-a-development-branch
description: "Use when ready to merge feature branch. Complete checklist before creating PR/MR. Ensures professional quality and prevents embarrassing mistakes."
---

# Finishing a Development Branch

## Core Principle

Before creating a Pull/Merge Request, complete a comprehensive checklist to ensure professional quality work.

## When to Use This Skill

- Feature is implemented and tested
- Ready to create PR/MR
- About to merge branch to main/develop
- User says "it's done, let's merge"
- Before marking work as complete

## The Iron Law

**NEVER create a PR/MR without completing the finish checklist.**

Incomplete PRs waste reviewer time and damage your reputation.

## Complete Finish Checklist

### 1. Code Completion

- [ ] All planned features implemented
- [ ] All requirements met
- [ ] No TODO comments remaining
- [ ] No commented-out code
- [ ] No debugging statements (console.log, dd(), var_dump())
- [ ] No temporary/experimental code

### 2. Testing

- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Edge cases tested
- [ ] Error cases tested
- [ ] Test coverage adequate (>80%)
- [ ] Database backup before tests (used `./scripts/safe-test.sh`)
- [ ] Integration tests pass
- [ ] No skipped or pending tests

### 3. Code Quality

- [ ] No linter errors
- [ ] Code formatted consistently
- [ ] No compiler warnings
- [ ] DRY principle followed (no duplication)
- [ ] Functions are single-purpose
- [ ] Meaningful variable names
- [ ] Complex logic has comments
- [ ] No magic numbers

### 4. Security

- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation comprehensive
- [ ] Authentication/authorization correct
- [ ] No hardcoded secrets
- [ ] Sensitive data not logged
- [ ] CSRF protection enabled

### 5. Performance

- [ ] No N+1 query problems
- [ ] Appropriate database indexes
- [ ] Efficient algorithms used
- [ ] No memory leaks
- [ ] Large datasets paginated
- [ ] Caching used where appropriate

### 6. Documentation

- [ ] PHPDoc/JSDoc comments on public methods
- [ ] Complex logic explained
- [ ] API endpoints documented
- [ ] README updated (if needed)
- [ ] CHANGELOG updated
- [ ] .env.example updated (new variables)
- [ ] Migration instructions (if applicable)

### 7. Git Hygiene

- [ ] All changes committed
- [ ] Commit messages follow convention
- [ ] Branch up to date with base branch
- [ ] No merge conflicts
- [ ] No unintended file changes
- [ ] .gitignore correct (no secrets committed)
- [ ] Sensible commit history (consider squashing if messy)

### 8. Integration

- [ ] No existing functionality broken
- [ ] API contracts maintained (backwards compatible)
- [ ] Database migrations reversible
- [ ] No conflicts with other features
- [ ] Works with other branches (if known)

### 9. CI/CD

- [ ] CI pipeline passes (if configured)
- [ ] Build succeeds
- [ ] Deployment script works (if applicable)
- [ ] Environment variables documented

### 10. Review Preparation

- [ ] PR/MR title is descriptive
- [ ] PR/MR description complete
- [ ] Screenshots/videos (if UI changes)
- [ ] Test plan included
- [ ] Breaking changes noted
- [ ] Related issues linked

## Pre-PR/MR Protocol

### Step 1: Final Self-Review

```
I'm using the finishing-a-development-branch skill before creating PR.

Running through complete checklist...

Code Completion:
✅ All features implemented
✅ No TODO comments
✅ No debugging code

Testing:
✅ Running final test suite with backup
✅ All 127 tests pass
✅ Coverage: 87%

[... complete all sections ...]

Ready to create PR ✅
```

### Step 2: Update Branch with Latest Changes

```bash
# Ensure branch is up to date
git checkout main
git pull origin main

git checkout feature/authentication
git merge main

# Or use rebase for cleaner history
git rebase main

# Resolve any conflicts
[if conflicts, resolve them]

# Run tests again after merge/rebase
./scripts/safe-test.sh vendor/bin/paratest
```

### Step 3: Clean Up Commits (Optional)

If commit history is messy:

```bash
# Interactive rebase to squash/reword commits
git rebase -i main

# Squash all commits into one (if appropriate)
# Or clean up commit messages
# Or split large commits

# Force push after rebase (ONLY on feature branches)
git push --force-with-lease origin feature/authentication
```

### Step 4: Write PR/MR Description

**Template:**

```markdown
## What

Brief description of what this PR does

## Why

Why is this change needed? What problem does it solve?

## Changes

- Bullet point list of major changes
- Added X
- Modified Y
- Removed Z

## Testing

How to test these changes:
1. Step 1
2. Step 2
3. Expected result

Test results:
- All tests pass (X tests)
- Manual testing completed
- No regressions detected

## Screenshots/Videos

(If applicable, add screenshots or video demonstrating changes)

## Breaking Changes

(If any, list them with migration instructions)

## Checklist

- [ ] Tests pass
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Reviewed own code

Closes #123
```

**Example:**

```markdown
## What

Implements JWT token-based authentication for API using Laravel Sanctum

## Why

Needed stateless authentication to support mobile app. Session-based auth doesn't work well for mobile clients.

## Changes

- Added Laravel Sanctum package
- Created AuthController with register/login/logout endpoints
- Added auth:sanctum middleware to protected routes
- Implemented token generation and revocation
- Added 15 tests covering auth flows
- Updated API documentation

## Testing

How to test:
1. POST /api/register with email/password
2. Receive token in response
3. Use token in Authorization header for protected routes
4. POST /api/logout to revoke token

Test results:
- All 127 tests pass (added 15 new auth tests)
- Manual testing completed with Postman
- Tested token expiration
- Tested invalid credentials
- Tested protected route access

## API Endpoints

New endpoints:
- POST /api/register - User registration
- POST /api/login - User login (returns token)
- POST /api/logout - Token revocation (protected)

Protected endpoints now require:
```
Authorization: Bearer {token}
```

## Breaking Changes

None. Existing endpoints unchanged. New auth is opt-in for protected routes.

## Migration Instructions

1. Run migrations: `php artisan migrate`
2. Publish Sanctum config (optional): `php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"`
3. Add `SANCTUM_STATEFUL_DOMAINS` to .env (for SPA, optional)

## Rollback Plan

If issues occur:
```bash
php artisan migrate:rollback --step=2
composer remove laravel/sanctum
```

## Checklist

- [x] All tests pass
- [x] API documentation updated
- [x] README updated with auth setup
- [x] CHANGELOG updated
- [x] .env.example includes Sanctum variables
- [x] No merge conflicts
- [x] Self-reviewed code
- [x] Database migrations reversible

Closes #45
```

### Step 5: Create PR/MR

**GitHub:**
```bash
# Using GitHub CLI
gh pr create \
  --title "feat(auth): Add JWT token authentication" \
  --body-file pr-description.md \
  --base main \
  --head feature/authentication

# Or interactively
gh pr create
```

**GitLab:**
```bash
# Using GitLab CLI
glab mr create \
  --title "feat(auth): Add JWT token authentication" \
  --description "$(cat pr-description.md)" \
  --source-branch feature/authentication \
  --target-branch main

# Or interactively
glab mr create
```

### Step 6: Post-PR Actions

After creating PR:

```
PR created: #156

Post-PR checklist:
- [ ] Link to related issues
- [ ] Request reviewers
- [ ] Add labels (feature, enhancement, etc.)
- [ ] Assign to milestone (if applicable)
- [ ] Add to project board (if applicable)
- [ ] Notify team in chat/email

Monitoring:
- Watch for CI/CD results
- Address reviewer comments promptly
- Keep branch up to date if base changes
```

## Common PR/MR Mistakes to Avoid

### ❌ Incomplete PRs

```
Bad PR:
Title: "Update"
Description: "Fixed stuff"
Changes: 50 files modified, no explanation
```

**Why bad**: Reviewers have no context, can't review effectively

**Fix**: Complete title, thorough description, explain changes

### ❌ Huge PRs

```
Bad PR:
Title: "Add authentication, payment, and notification systems"
Changes: 150 files, 5000 lines
```

**Why bad**: Too large to review effectively, high chance of bugs

**Fix**: Split into multiple smaller PRs

**Good size**: < 400 lines of actual code changes

### ❌ PRs with Failing Tests

```
Bad PR:
- Tests: 5 passing, 3 failing
- CI: ❌ Failed
- Description: "Tests will pass after merge"
```

**Why bad**: Breaks the build, unprofessional

**Fix**: Make tests pass BEFORE creating PR

### ❌ PRs with Merge Conflicts

```
Bad PR:
- Status: Has merge conflicts with main
- Comment: "Can someone resolve the conflicts?"
```

**Why bad**: PR author should resolve conflicts

**Fix**: Merge main into your branch, resolve conflicts, test, push

### ❌ PRs without Context

```
Bad PR:
Title: "Fix bug"
Description: (empty)
Changes: Modified 3 files
```

**Why bad**: Reviewers don't know what bug or how it was fixed

**Fix**: Explain the bug, root cause, and solution

## Handling PR Feedback

### When Reviewer Requests Changes

```
Reviewer comment:
"This AuthController method is 100 lines. Can you split it?"

Good response:
"Good catch! I'll refactor this into:
- validateCredentials() method
- generateToken() method
- logAuthEvent() method

Will push update today."

[Make changes, push, notify reviewer]
"Updated! AuthController methods now < 30 lines each."
```

### When You Disagree with Feedback

```
Reviewer comment:
"Use bcrypt instead of argon2"

Your response (if you disagree):
"I chose argon2 because:
1. More secure (2015 Password Hashing Competition winner)
2. Better resistance to GPU attacks
3. Laravel default since 5.8

However, happy to switch to bcrypt if there's a specific concern. What do you think?"

[Discuss, reach consensus, implement agreed solution]
```

## Integration with Skills

**Prerequisites:**
- `code-review` - Self-review before PR
- `verification-before-completion` - Final checks
- `executing-plans` - Implementation complete

**Use with:**
- `git-workflow` - Commit conventions
- `database-backup` - Test before PR
- `systematic-debugging` - If issues found

**After PR created:**
- Monitor CI/CD results
- Address reviewer feedback
- Merge after approval

## Red Flags (Not Ready for PR)

- ❌ Tests don't pass
- ❌ Contains TODO comments
- ❌ Has merge conflicts
- ❌ No description
- ❌ Includes debugging code
- ❌ Secrets committed
- ❌ CI/CD fails
- ❌ No new tests for new features

## Common Rationalizations to Reject

- ❌ "I'll fix it after merge" → Fix BEFORE merge
- ❌ "The reviewer will catch issues" → Catch them yourself first
- ❌ "It's just a small change" → Small changes still need quality
- ❌ "I'm in a hurry" → Rushing creates bugs
- ❌ "Tests will pass in production" → Tests must pass now

## Authority

**This skill is based on:**
- Professional software development practices
- Code review best practices
- Industry standard: All major companies require thorough PR process
- Git workflow conventions
- Team collaboration efficiency

**Social Proof**: Google, Facebook, Microsoft all have rigorous PR processes.

## Your Commitment

Before creating PR/MR:
- [ ] I will complete the entire finish checklist
- [ ] I will ensure all tests pass
- [ ] I will write a thorough PR description
- [ ] I will review my own code first
- [ ] I will address all red flags

---

**Bottom Line**: Your PR represents you. Make it professional, complete, and easy to review. Reviewers' time is valuable - respect it by submitting quality work.
