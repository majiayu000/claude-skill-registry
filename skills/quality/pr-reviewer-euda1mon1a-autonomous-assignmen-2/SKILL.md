---
name: pr-reviewer
description: Pull request review expertise with focus on context, quality gates, and team standards. Use when reviewing PRs, validating changes before merge, or generating PR descriptions. Works with gh CLI for GitHub integration.
model_tier: opus
parallel_hints:
  can_parallel_with:
    - code-review
    - security-audit
  must_serialize_with:
    - database-migration
  preferred_batch_size: 3
---

# PR Reviewer Skill

Comprehensive pull request review skill that validates changes against project standards, runs quality gates, and provides structured feedback for merge decisions.

## When This Skill Activates

- Reviewing open pull requests
- Creating PR descriptions
- Validating changes before merge
- Checking CI/CD status
- Generating review summaries
- Approving or requesting changes

## PR Review Workflow

### Step 1: Gather Context

```bash
# Get PR details
gh pr view <PR_NUMBER> --json title,body,author,state,reviews,files,commits

# View the diff
gh pr diff <PR_NUMBER>

# Check CI status
gh pr checks <PR_NUMBER>

# Get commits
gh pr view <PR_NUMBER> --json commits

# List changed files
gh pr diff <PR_NUMBER> --name-only
```

### Step 2: Understand the Change

Questions to answer:
- What problem does this PR solve?
- What is the approach taken?
- What are the key changes?
- What might break?
- What tests were added?

### Step 3: Run Quality Gates

```bash
cd /home/user/Autonomous-Assignment-Program-Manager/backend

# Fetch and checkout PR
git fetch origin pull/<PR_NUMBER>/head:pr-<PR_NUMBER>
git checkout pr-<PR_NUMBER>

# Run quality checks
pytest --tb=short -q
ruff check app/ tests/
black --check app/ tests/
mypy app/ --python-version 3.11

# Check test coverage
pytest --cov=app --cov-fail-under=70
```

### Step 4: Review Categories

#### A. Code Quality
- [ ] Code follows layered architecture
- [ ] Type hints on all functions
- [ ] Docstrings on public APIs
- [ ] No magic numbers/hardcoded values
- [ ] DRY principle followed
- [ ] Appropriate error handling

#### B. Testing
- [ ] Tests added for new code
- [ ] Tests cover edge cases
- [ ] Tests are readable and maintainable
- [ ] Coverage >= 70%
- [ ] No flaky tests

#### C. Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Auth checks in place
- [ ] No sensitive data in logs/errors
- [ ] SQL injection prevention

#### D. Architecture
- [ ] Follows project patterns
- [ ] Database changes have migrations
- [ ] Async/await used correctly
- [ ] Pydantic schemas for I/O
- [ ] No circular dependencies

#### E. Documentation
- [ ] PR description is clear
- [ ] Complex logic commented
- [ ] API docs updated if needed
- [ ] CHANGELOG updated for features
- [ ] **Code/comment consistency** - verify comments match actual behavior
- [ ] **Seed data alignment** - filter values match canonical data sources

## Review Decision Matrix

| Gate | Pass | Block |
|------|------|-------|
| Tests | All pass | Any failure |
| Linting | 0 errors | Any error |
| Types | 0 errors | Critical types missing |
| Security | No issues | Any vulnerability |
| Coverage | >= 70% | < 60% |
| Architecture | Follows patterns | Major violation |

## PR Feedback Format

### Inline Comments

Use GitHub's suggestion format for fixes:

````markdown
```suggestion
def calculate_hours(assignments: list[Assignment]) -> float:
    """Calculate total hours from assignments."""
    return sum(a.hours for a in assignments)
```
````

### Review Summary

```markdown
## Review Summary

**Decision:** APPROVE / REQUEST CHANGES / COMMENT

### What This PR Does
[One sentence summary]

### Quality Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| Tests | :white_check_mark: | 47 passed |
| Linting | :white_check_mark: | 0 errors |
| Types | :white_check_mark: | 100% coverage |
| Security | :white_check_mark: | bandit clear |
| Coverage | :yellow_circle: | 72% (target 80%) |

### Changes Reviewed
- `app/services/new_feature.py` - New service implementation
- `tests/test_new_feature.py` - Test coverage

### Feedback

#### Required Changes (Blocking)
1. [file:line] - Description of issue
   - Impact: [what could go wrong]
   - Suggestion: [how to fix]

#### Suggestions (Non-blocking)
1. [file:line] - Description
   - Recommendation: [improvement]

#### Questions
1. [Question about the approach]

### Testing Notes
Tested locally:
- [x] Unit tests pass
- [x] Integration tests pass
- [ ] Manual testing [describe if done]

### Merge Checklist
- [ ] All conversations resolved
- [ ] CI checks passing
- [ ] Required reviews obtained
- [ ] Documentation updated
```

## PR Description Template

When creating PRs:

```markdown
## Summary
[1-3 bullet points describing the change]

## Motivation
[Why this change is needed]

## Changes
- [List key changes]

## Testing
- [How was this tested?]

## Test Plan
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing done

## Screenshots
[If applicable]

## Checklist
- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

## Related Issues
Closes #[issue number]
```

## GitHub CLI Commands

```bash
# List open PRs
gh pr list

# View specific PR
gh pr view <number>

# Check PR status
gh pr checks <number>

# Review PR
gh pr review <number> --approve -b "Looks good!"
gh pr review <number> --request-changes -b "See comments"
gh pr review <number> --comment -b "Questions inline"

# Add comment
gh pr comment <number> --body "Comment text"

# Merge PR
gh pr merge <number> --squash --delete-branch

# Get PR diff
gh pr diff <number>

# Create PR
gh pr create --title "Title" --body "Description"
```

## Automated PR Checks

### Pre-Review Automation

```bash
#!/bin/bash
# scripts/pr-review-prep.sh

PR_NUMBER=$1

# Fetch PR
git fetch origin pull/${PR_NUMBER}/head:pr-${PR_NUMBER}
git checkout pr-${PR_NUMBER}

# Run quality checks
echo "=== Running Tests ==="
pytest --tb=short -q

echo "=== Running Linting ==="
ruff check app/ tests/

echo "=== Running Type Check ==="
mypy app/ --python-version 3.11

echo "=== Coverage Report ==="
pytest --cov=app --cov-report=term-missing --cov-fail-under=70

echo "=== Security Scan ==="
bandit -r app/ -ll

echo "=== PR Review Prep Complete ==="
```

## Common Review Patterns

### Missing Tests

```markdown
This new functionality needs test coverage.

**Files needing tests:**
- `app/services/new_service.py`

**Suggested test cases:**
1. Happy path - normal input
2. Edge case - empty input
3. Error case - invalid input
4. Integration - database operations
```

### Architecture Violation

```markdown
This violates the layered architecture pattern.

**Issue:** Business logic in route handler

**Current:**
```python
@router.post("/items")
async def create_item(data: ItemCreate, db: Session):
    # Business logic here (violation)
    if data.value > 100:
        data.value = 100
    item = Item(**data.dict())
    db.add(item)
```

**Should be:**
```python
# In service layer
async def create_item(db: Session, data: ItemCreate) -> Item:
    if data.value > 100:
        data.value = 100
    item = Item(**data.dict())
    db.add(item)
    return item

# In route
@router.post("/items")
async def create_item_route(data: ItemCreate, db: Session):
    return await create_item(db, data)
```
```

### Missing Type Hints

````markdown
Please add type hints to these functions:

```suggestion
async def get_schedule(
    db: AsyncSession,
    schedule_id: str
) -> Optional[Schedule]:
    """Retrieve a schedule by ID."""
    ...
```
````

## Examples

### Example 1: Standard PR Review (Feature Addition)

**Context:** PR #523 adds resident work hour summary endpoint

**Input:**
```bash
gh pr view 523 --json title,files,commits
```

**Process:**
1. **Gather context:**
   - Title: "feat: Add work hour summary endpoint"
   - Files changed: 3 (route, service, tests)
   - Commits: 2 commits
2. **Check CI status:**
   ```bash
   gh pr checks 523
   # ✓ Tests: passing
   # ✓ Lint: passing
   # ✗ Coverage: 65% (below 70% threshold)
   ```
3. **Review code:**
   - Route follows layered architecture ✓
   - Service has business logic ✓
   - Tests added but incomplete (missing edge cases)
4. **Run quality gates locally:**
   ```bash
   git fetch origin pull/523/head:pr-523
   git checkout pr-523
   pytest --cov=app.services.work_hour_service --cov-fail-under=70
   # FAIL: 65% coverage
   ```

**Output:**
```markdown
## PR Review: #523 - Add work hour summary endpoint

**Decision:** REQUEST CHANGES

### Quality Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| Tests | ✓ | 12 tests pass |
| Linting | ✓ | No errors |
| Types | ✓ | No errors |
| Coverage | ✗ | 65% (target 70%) |

### Required Changes (Blocking)
1. **Insufficient test coverage** (app/services/work_hour_service.py:45-78)
   - Missing tests for edge cases:
     - Empty assignment list
     - Assignments spanning multiple weeks
     - Null duration handling
   - Add tests to bring coverage to 70%+

### Suggestions (Non-blocking)
1. Consider caching work hour calculations (line 56)
   - Reduces database load for frequently accessed residents
   - Use Redis with 15-minute TTL

### Approval Checklist
- [x] Architecture follows patterns
- [x] Tests exist
- [ ] Coverage >= 70% (BLOCKING)
- [x] Linting passes
- [x] Types valid

**Next Steps:** Add missing tests, push update, request re-review.
```

### Example 2: Security-Critical PR Review

**Context:** PR #478 modifies authentication middleware

**Input:**
```python
# Changed file: backend/app/api/deps.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    # CHANGE: Removed JWT expiration check
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload.get("sub")
```

**Process:**
1. **Identify security-sensitive area:** Authentication code
2. **Compare with previous version:**
   ```diff
   - if payload.get("exp") < time.time():
   -     raise HTTPException(401, "Token expired")
   + # Expiration check removed
   ```
3. **Assess impact:** CRITICAL - allows expired tokens
4. **Trigger security-audit skill** for full analysis

**Output:**
```markdown
## PR Review: #478 - Update auth middleware

**Decision:** :red_circle: BLOCK MERGE - CRITICAL SECURITY ISSUE

### Security Finding

**Severity:** CRITICAL
**Issue:** JWT Expiration Check Removed

This change allows expired tokens to authenticate, violating authentication security.

**Security Impact:**
- Tokens never expire (OWASP A07:2021 - Authentication Failures)
- Compromised tokens remain valid indefinitely
- No mechanism to revoke access
- Violates standard JWT security practices

**Required Fix:**
1. Revert expiration check removal
2. Add explicit test for expired token rejection
3. Security review required before merge

**Escalation:** Triggered security-audit skill for full assessment.

### Action Required
- [ ] Revert to include expiration check
- [ ] Add test: `test_expired_token_rejected()`
- [ ] Human security review before re-submit
```

### Example 3: Database Migration PR Review

**Context:** PR #501 adds `email_verified` field to User model

**Input:**
```bash
gh pr diff 501 --name-only
# backend/app/models/user.py
# backend/alembic/versions/abc123_add_email_verified.py
```

**Process:**
1. **Check model and migration together:** ✓ Both files present
2. **Review migration:**
   ```python
   def upgrade() -> None:
       op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=False))
   ```
3. **Identify issue:** Adding non-nullable column to table with existing rows will fail
4. **Verify locally:**
   ```bash
   alembic upgrade head
   # ERROR: column "email_verified" contains null values
   ```

**Output:**
```markdown
## PR Review: #501 - Add email_verified field

**Decision:** REQUEST CHANGES

### Database Migration Issue

**Problem:** Non-nullable column added to table with existing rows

This migration will fail in production because:
1. Existing users don't have `email_verified` value
2. Column is `nullable=False` (requires value)
3. No default provided

**Current Migration:**
```python
op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=False))
```

**Required Fix - Three-Phase Migration:**
```python
# Migration 1: Add as nullable
op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=True))

# Migration 2: Backfill
op.execute("UPDATE users SET email_verified = false WHERE email_verified IS NULL")

# Migration 3: Make non-nullable
op.alter_column('users', 'email_verified', nullable=False)
```

**Testing:**
- [ ] Test migration on database with existing data
- [ ] Verify downgrade path works
- [ ] Document rollback procedure

**Escalation:** Deferred to database-migration skill for implementation.
```

## Lesson Learned: PR #442 (2025-12-26)

**What happened:** A fix changed a filter from one value to another, but the new value
was also incorrect because comments/docs said "outpatient" while code used "clinic".

**Prevention checklist for filter/constant changes:**
- [ ] Verify value against seed data (`scripts/seed_templates.py`)
- [ ] Check if comments describe different behavior than code implements
- [ ] Cross-reference with canonical data source (e.g., BLOCK_10_ROADMAP)
- [ ] Confirm the filter will actually find matching records

**Key insight:** Always ask "will this filter find what we expect?" and verify empirically.

## Common Failure Modes

| Failure Mode | Symptom | Root Cause | Recovery Steps |
|--------------|---------|------------|----------------|
| **CI Passes But Code Broken** | All checks green, but feature doesn't work | Insufficient test coverage or wrong tests | 1. Manual testing reveals issue<br>2. Add missing test cases<br>3. Re-run CI with new tests |
| **Merge Conflict During Review** | PR becomes outdated while under review | Long review cycle, active main branch | 1. Request author to rebase<br>2. Re-run quality gates after rebase<br>3. Re-review changed sections only |
| **False Positive Security Alert** | Bandit flags safe code as vulnerable | Static analysis limitation | 1. Manual review confirms false positive<br>2. Add `# nosec` comment with justification<br>3. Document in review |
| **Coverage Drops After Merge** | PR shows 80% coverage, but repo drops to 65% | Coverage calculated only for changed files | 1. Check overall repo coverage before approve<br>2. Require tests for affected areas, not just new code<br>3. Use `--cov=app` not `--cov=app.services.new_module` |
| **Database Migration Not Tested** | Migration file present but untested | CI doesn't run migrations in test environment | 1. Manually test migration locally<br>2. Request author to test `upgrade` and `downgrade`<br>3. Add migration testing to CI |
| **Breaking API Change Undetected** | Pydantic schema changed without version bump | No API contract testing | 1. Check schema diff against previous version<br>2. Determine if breaking (required field added, field removed)<br>3. Require API version bump or revert change |

## Validation Checklist

After reviewing a PR, verify:

- [ ] **PR Description:** Clear summary of what/why
- [ ] **Linked Issues:** References issue number or motivation
- [ ] **CI Checks:** All automated checks pass
- [ ] **Tests Added:** New code has corresponding tests
- [ ] **Coverage:** >= 70% for changed files
- [ ] **Linting:** No lint errors
- [ ] **Type Checking:** No type errors
- [ ] **Security:** No vulnerabilities detected
- [ ] **Architecture:** Follows layered pattern
- [ ] **Database Migrations:** If model changed, migration present and tested
- [ ] **Breaking Changes:** Documented or avoided
- [ ] **Documentation:** Updated if needed (README, API docs)
- [ ] **No Secrets:** No hardcoded credentials or sensitive data
- [ ] **Dependency Changes:** If `requirements.txt` changed, justified
- [ ] **Manual Testing:** For complex features, manually verified
- [ ] **Conflicts Resolved:** No merge conflicts present

## Escalation Rules

**Request human review when:**

1. Changes touch authentication/authorization
2. Database migrations involved
3. ACGME compliance logic affected
4. Breaking API changes
5. Complex business logic unclear
6. Performance-critical code
7. Third-party integration changes
8. **Filter/constant value changes** - verify against canonical data sources

**Can approve automatically:**

1. Documentation-only changes
2. Test additions (without code changes)
3. Dependency updates (minor versions)
4. Code formatting fixes
5. Comment improvements

## Integration with Other Skills

### With code-review
For detailed code analysis:
1. PR-reviewer handles workflow and gates
2. Code-review handles line-by-line analysis
3. Combine findings in final review

### With security-audit
For security-sensitive PRs:
1. Detect sensitive file changes
2. Trigger security-audit skill
3. Include security findings in review

### With automated-code-fixer
For simple fixes:
1. Suggest fixes inline
2. If accepted, automated-code-fixer applies
3. Re-run quality gates
4. Update PR status

## Workflow Diagram

```
┌───────────────────────────────────────────────────────────────────┐
│                   PR REVIEW WORKFLOW                              │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  STEP 1: Gather Context                                           │
│  ┌──────────────────────────────────────────────────┐             │
│  │ gh pr view <number> --json ...                   │             │
│  │ gh pr diff <number>                              │             │
│  │ gh pr checks <number>                            │             │
│  │ Understand: What, Why, How                       │             │
│  └──────────────────────────────────────────────────┘             │
│                         ↓                                         │
│  STEP 2: Checkout and Test Locally                                │
│  ┌──────────────────────────────────────────────────┐             │
│  │ git fetch origin pull/<N>/head:pr-<N>            │             │
│  │ git checkout pr-<N>                              │             │
│  │ Run tests, linting, type checks                  │             │
│  └──────────────────────────────────────────────────┘             │
│                         ↓                                         │
│  STEP 3: Quality Gate Checks                                      │
│  ┌──────────────────────────────────────────────────┐             │
│  │ Tests: ALL PASS?                                 │             │
│  │ Linting: 0 errors?                               │             │
│  │ Types: No critical issues?                       │             │
│  │ Security: No vulnerabilities?                    │             │
│  │ Coverage: >= 70%?                                │             │
│  └──────────────────────────────────────────────────┘             │
│                         ↓                                         │
│  STEP 4: Code Review Categories                                   │
│  ┌──────────────────────────────────────────────────┐             │
│  │ A. Code Quality  B. Testing                      │             │
│  │ C. Security      D. Architecture                 │             │
│  │ E. Documentation                                 │             │
│  └──────────────────────────────────────────────────┘             │
│                         ↓                                         │
│  STEP 5: Make Decision                                            │
│  ┌──────────────────────────────────────────────────┐             │
│  │ All gates PASS → APPROVE                         │             │
│  │ Major issues   → REQUEST CHANGES                 │             │
│  │ Questions only → COMMENT                         │             │
│  └──────────────────────────────────────────────────┘             │
│                         ↓                                         │
│  STEP 6: Post Review                                              │
│  ┌──────────────────────────────────────────────────┐             │
│  │ gh pr review <number> --approve/--request-changes│             │
│  │ Include summary, gate results, feedback          │             │
│  └──────────────────────────────────────────────────┘             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

## Concrete Usage Example: Reviewing PR #123

**Scenario:** Review PR that adds a new ACGME constraint for call spacing.

### Complete Review Walkthrough

**Step 1: Gather Context**

```bash
# View PR details
gh pr view 123 --json title,body,author,state,reviews,files,commits

# Output:
# {
#   "title": "feat: add minimum call spacing constraint",
#   "author": "developer",
#   "state": "OPEN",
#   "body": "Adds 72-hour minimum spacing between call shifts..."
#   "files": [
#     "backend/app/scheduling/constraints/call_spacing.py",
#     "backend/app/scheduling/constraints/__init__.py",
#     "backend/app/scheduling/constraints/manager.py",
#     "backend/tests/test_call_spacing_constraint.py"
#   ]
# }

# View the diff
gh pr diff 123 > pr123.diff

# Check CI status
gh pr checks 123

# Output:
# ✓ Backend Tests   passed
# ✓ Frontend Tests  passed
# ✓ Lint Check      passed
# ✗ Type Check      failed
```

**Analysis:**
- What: New constraint for call spacing
- Why: ACGME requirement for resident wellbeing
- How: Soft constraint with weight 8.0
- Issue: Type check failing ⚠️

**Step 2: Checkout and Test Locally**

```bash
cd /home/user/Autonomous-Assignment-Program-Manager

# Fetch PR
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Run quality checks
cd backend

# Tests
pytest
# Output: 47 passed, 0 failed ✓

# Linting
ruff check app/ tests/
# Output: All clear ✓

# Type check (this was failing in CI)
mypy app/ --python-version 3.11
# Output:
# app/scheduling/constraints/call_spacing.py:45: error: Incompatible return type
# Expected "ConstraintResult", got "None"
```

**Found the issue!** Type check fails because `validate()` method doesn't return value in all code paths.

**Step 3: Quality Gate Results**

| Gate | Status | Notes |
|------|--------|-------|
| Tests | :white_check_mark: PASS | 47 passed |
| Linting | :white_check_mark: PASS | 0 errors |
| Types | :x: FAIL | Missing return in validate() |
| Security | :white_check_mark: PASS | No issues |
| Coverage | :white_check_mark: PASS | 85% (target 70%) |
| Architecture | :warning: NEEDS REVIEW | Constraint pattern followed |

**Decision:** REQUEST CHANGES (type error is blocking)

**Step 4: Code Review by Category**

**A. Code Quality**
```python
# ❌ Issue found in call_spacing.py line 45
def validate(self, assignments, context):
    violations = []
    for person_id, person_assignments in group_by_person(assignments):
        # ... logic ...
        if spacing < self.min_hours:
            violations.append(...)
    # ❌ MISSING: return ConstraintResult(violations)
```

**Suggestion:**
```python
def validate(self, assignments, context) -> ConstraintResult:
    violations = []
    for person_id, person_assignments in group_by_person(assignments):
        # ... logic ...
        if spacing < self.min_hours:
            violations.append(...)
    # ✓ FIX: Add return statement
    return ConstraintResult(
        passed=len(violations) == 0,
        violations=violations,
        score=1.0 - (len(violations) * 0.1)
    )
```

**B. Testing**
- :white_check_mark: Unit tests added
- :white_check_mark: Registration test included
- :white_check_mark: Edge cases covered (24-hour call, overnight)
- :warning: Suggested: Add integration test with scheduler

**C. Security**
- :white_check_mark: No sensitive data in logs
- :white_check_mark: Input validation present
- :white_check_mark: No SQL injection risk

**D. Architecture**
- :white_check_mark: Follows SoftConstraint base class
- :white_check_mark: Exported in __init__.py
- :white_check_mark: Registered in manager.py
- :white_check_mark: Weight (8.0) positioned correctly in hierarchy

**E. Documentation**
- :white_check_mark: Docstring explains constraint purpose
- :white_check_mark: Clinical rationale documented
- :white_check_mark: ACGME rule cited
- :warning: Suggested: Add example to docstring

**Step 5: Generate Review Summary**

```markdown
## Review Summary

**Decision:** REQUEST CHANGES

### What This PR Does
Adds CallSpacingConstraint to enforce 72-hour minimum spacing between
inpatient call shifts, implementing ACGME burnout prevention guidelines.

### Quality Gate Results
| Gate | Status | Notes |
|------|--------|-------|
| Tests | :white_check_mark: | 47 passed |
| Linting | :white_check_mark: | 0 errors |
| Types | :x: | **BLOCKING**: Missing return in validate() |
| Security | :white_check_mark: | bandit clear |
| Coverage | :white_check_mark: | 85% (target 70%) |

### Changes Reviewed
- `app/scheduling/constraints/call_spacing.py` - New constraint implementation
- `app/scheduling/constraints/manager.py` - Registration (verified)
- `tests/test_call_spacing_constraint.py` - Test coverage

### Required Changes (Blocking)

#### 1. [call_spacing.py:45] Missing return statement
**Impact:** Type check fails, method returns None instead of ConstraintResult

**Fix:**
```python
def validate(self, assignments, context) -> ConstraintResult:
    violations = []
    # ... validation logic ...
    return ConstraintResult(  # ← Add this
        passed=len(violations) == 0,
        violations=violations,
        score=1.0 - (len(violations) * 0.1)
    )
```

### Suggestions (Non-blocking)

#### 1. Add integration test with scheduler
Suggested test:
```python
async def test_call_spacing_integration_with_scheduler(db):
    """Test call spacing is enforced during schedule generation."""
    # Generate schedule, verify no call shifts within 72 hours
```

#### 2. Add concrete example to docstring
```python
class CallSpacingConstraint(SoftConstraint):
    """
    Enforce minimum spacing between call shifts.

    Example:
        If resident has call Monday 5pm-Tuesday 5pm (24 hours),
        they cannot take another call until Thursday 5pm (72 hours later).
    """
```

### Testing Notes
Tested locally:
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual verification: weight hierarchy correct

### Merge Checklist
- [ ] Fix type error in validate()
- [ ] Type check passes (`mypy app/`)
- [ ] Re-run CI checks
- [ ] Address suggestions (optional)
```

**Step 6: Post Review**

```bash
# Post review with feedback
gh pr review 123 --request-changes --body "$(cat <<'EOF'
## Review Summary

**Decision:** REQUEST CHANGES

[... full review summary from above ...]

EOF
)"

# Add inline comment on specific line
gh api repos/{owner}/{repo}/pulls/123/comments \
  -f body="Missing return statement here. See main review for fix." \
  -f commit_id="abc123" \
  -f path="backend/app/scheduling/constraints/call_spacing.py" \
  -f position=45
```

**Follow-up after fixes applied:**

```bash
# Author pushes fix
# Re-check the PR

gh pr checks 123
# Output: All checks passing ✓

# Re-review
gh pr review 123 --approve --body "$(cat <<'EOF'
## Re-Review Summary

**Decision:** APPROVE ✓

### Changes Verified
- ✓ Type error fixed - validate() now returns ConstraintResult
- ✓ All CI checks passing
- ✓ Type check passes

Ready to merge!
EOF
)"
```

## Failure Mode Handling

### Failure Mode 1: CI Checks Failing

**Symptom:**
```bash
$ gh pr checks 123

✗ Backend Tests   failed
✗ Type Check      failed
✓ Lint Check      passed
```

**Recovery:**

```bash
# 1. Checkout PR locally
git fetch origin pull/123/head:pr-123
git checkout pr-123

# 2. Run tests to see failures
cd backend
pytest -v

# Output shows which tests failed

# 3. Request changes with specific test failures
gh pr review 123 --request-changes --body "$(cat <<'EOF'
CI checks are failing. Please fix before re-review:

**Failed Tests:**
- test_call_spacing_overnight - AssertionError on line 45
- test_call_spacing_edge_case - Expected 2 violations, got 0

**Type Errors:**
- call_spacing.py:45 - Missing return type

Please address these issues and push updates.
EOF
)"
```

### Failure Mode 2: PR Changes Core Security Code

**Symptom:** PR modifies `backend/app/core/security.py`

**Recovery:**

```bash
# 1. Immediately invoke security-audit skill
# (Don't approve without security review)

# 2. Flag for human review
gh pr comment 123 --body "$(cat <<'EOF'
⚠️ **SECURITY REVIEW REQUIRED**

This PR modifies core security code (`core/security.py`).
Flagging for human security review before approval.

@security-team please review authentication changes.
EOF
)"

# 3. Mark as REQUEST CHANGES until security cleared
gh pr review 123 --request-changes --body "$(cat <<'EOF'
Holding for security review. See comment above.

Changes to security code require human approval.
EOF
)"
```

### Failure Mode 3: Database Migration Without Testing

**Symptom:** PR includes Alembic migration but no evidence of upgrade/downgrade testing

**Recovery:**

```bash
# 1. Verify migration testing in PR description or commits
gh pr view 123 --json body | grep -i "alembic\|migration\|upgrade\|downgrade"

# If no evidence found:

# 2. Request testing evidence
gh pr review 123 --request-changes --body "$(cat <<'EOF'
⚠️ **Database Migration Detected**

This PR includes a database migration but doesn't show testing evidence.

**Required before approval:**
- [ ] Demonstrate `alembic upgrade head` succeeds
- [ ] Demonstrate `alembic downgrade -1` succeeds
- [ ] Demonstrate `alembic upgrade head` succeeds again
- [ ] Verify application starts with new schema
- [ ] Verify all tests pass

Please add this evidence to PR description or commit message.
EOF
)"
```

### Failure Mode 4: Coverage Drop Below Threshold

**Symptom:**
```bash
$ pytest --cov=app --cov-fail-under=70

FAILED: Coverage 65% is below threshold 70%
```

**Recovery:**

```bash
# 1. Identify uncovered code
pytest --cov=app --cov-report=html
# Open htmlcov/index.html

# 2. Request additional tests
gh pr review 123 --request-changes --body "$(cat <<'EOF'
Test coverage dropped to 65% (below 70% threshold).

**Uncovered code:**
- `call_spacing.py` lines 45-52 (edge case handling)
- `call_spacing.py` lines 78-82 (error handling)

Please add tests for these code paths.
EOF
)"
```

### Failure Mode 5: Unclear PR Purpose

**Symptom:** PR description says "fixes stuff" with no details

**Recovery:**

```bash
# Request clarification before reviewing
gh pr comment 123 --body "$(cat <<'EOF'
Could you please provide more context in the PR description?

**Helpful information:**
- What problem does this solve?
- What approach did you take?
- How was it tested?
- Are there any breaking changes?

This helps with review and serves as documentation for future reference.
EOF
)"

# Don't approve until description is clear
```

## Integration Examples (Extended)

### With code-review (Detailed)

```
[PR #123 opened]
[pr-reviewer activated]

Step 1: pr-reviewer gathers context
→ Identifies 4 files changed
→ Detects new constraint code

Step 2: Invoke code-review for line-by-line analysis
→ code-review examines call_spacing.py
→ Finds: Missing return statement, unclear variable name, missing type hint

Step 3: pr-reviewer synthesizes findings
→ Combines code-review findings with quality gates
→ Generates unified review with inline suggestions

Step 4: Post review
→ gh pr review 123 --request-changes
→ Includes both structural issues (gates) and code quality issues (code-review)
```

### With security-audit (Detailed)

```
[PR #456 modifies auth logic]
[pr-reviewer activated]

→ Detects security-sensitive file: backend/app/api/routes/auth.py
→ STOP: Do not auto-approve

[Invoke security-audit skill]
→ Checks for: password handling, token generation, SQL injection, XSS
→ Finds: Hardcoded secret key in test (violation)

[pr-reviewer includes security findings]
Review:
"🔒 Security Review Required

security-audit found:
- Hardcoded secret 'test123' in test_auth.py line 45
- Missing rate limiting on new endpoint
- No input validation on email parameter

These must be addressed before approval."
```

### With automated-code-fixer (Detailed)

```
[PR #789 has simple linting errors]
[pr-reviewer activated]

→ Runs quality gates
→ Linting: 5 errors (missing imports, unused variables, formatting)

Instead of requesting changes:

[Invoke automated-code-fixer]
→ automated-code-fixer runs ruff check --fix
→ All 5 errors auto-fixed
→ Push fixes to PR branch

[pr-reviewer re-runs gates]
→ All gates now PASS
→ Post review: "Auto-fixed linting errors. Approved after fixes."
```

## Validation Checklist (Extended)

### Pre-Review Checklist
- [ ] PR has clear description
- [ ] PR is not too large (< 500 lines ideal)
- [ ] PR targets correct base branch
- [ ] PR has been rebased on latest main (no conflicts)
- [ ] Author has reviewed own code first

### Context Gathering Checklist
- [ ] Read PR title and description
- [ ] View changed files list
- [ ] Check commit history
- [ ] Review CI check status
- [ ] Read any linked issues

### Local Testing Checklist
- [ ] Successfully checked out PR branch
- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Application runs without errors
- [ ] No obvious regressions observed

### Code Quality Review Checklist
- [ ] Code follows project architecture
- [ ] Type hints on all functions
- [ ] Docstrings on public APIs
- [ ] No hardcoded values
- [ ] DRY principle followed
- [ ] Error handling appropriate
- [ ] No obvious performance issues

### Security Review Checklist
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Auth checks in place
- [ ] No sensitive data in logs
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities prevented
- [ ] Rate limiting on new endpoints

### Testing Review Checklist
- [ ] Tests added for new code
- [ ] Tests cover edge cases
- [ ] Tests are readable
- [ ] Coverage >= 70%
- [ ] No flaky tests
- [ ] Tests document expected behavior

### Architecture Review Checklist
- [ ] Follows layered architecture
- [ ] Database changes have migrations
- [ ] Async/await used correctly
- [ ] Pydantic schemas for I/O
- [ ] No circular dependencies
- [ ] Integration points documented

### Documentation Review Checklist
- [ ] PR description is clear
- [ ] Complex logic commented
- [ ] API docs updated if needed
- [ ] CHANGELOG updated for features
- [ ] Breaking changes documented
- [ ] Code/comment consistency verified

### Special Cases Checklist

**If PR includes database migration:**
- [ ] Model and migration committed together
- [ ] Upgrade tested
- [ ] Downgrade tested
- [ ] Data safety verified
- [ ] Backup plan documented

**If PR modifies security code:**
- [ ] Security-audit skill invoked
- [ ] Human review requested
- [ ] No obvious vulnerabilities
- [ ] Authentication not weakened
- [ ] Authorization maintained

**If PR adds constraint:**
- [ ] Constraint-preflight skill invoked
- [ ] Registration verified
- [ ] Weight hierarchy correct
- [ ] Clinical rationale documented

### Post-Review Checklist
- [ ] Decision made (approve/request-changes/comment)
- [ ] Review summary posted
- [ ] Inline comments added
- [ ] Blocking vs. non-blocking issues clear
- [ ] Follow-up actions specified

## References

- `/review-pr` slash command
- `.github/PULL_REQUEST_TEMPLATE.md` (if exists)
- `docs/development/AI_RULES_OF_ENGAGEMENT.md` - PR workflow rules
