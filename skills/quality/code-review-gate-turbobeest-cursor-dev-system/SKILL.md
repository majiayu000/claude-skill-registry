---
activation_code: CODE_REVIEW_GATE_V1
phase: 8
prerequisites:
  - Phase 7 implementation complete
  - Tests passing
  - Coverage thresholds met
outputs:
  - Code review report
  - .signals/code-review-complete.json
description: |
  Human code review gate for critical components. Activates automatically
  for security-sensitive paths, high-complexity code, or large changes.

  Activation trigger: [ACTIVATE:CODE_REVIEW_GATE_V1]
---

# Code Review Gate Skill

## Purpose

This skill provides a **human code review gate** between implementation (Phase 7) and integration testing (Phase 9). It ensures that code quality, security, and maintainability are validated by human eyes before proceeding.

## When This Gate Triggers

### Automatic Triggers (Cannot Skip)

1. **Security-Sensitive Paths**
   - `src/auth/` - Authentication logic
   - `src/security/` - Security utilities
   - `src/crypto/` - Cryptographic operations
   - `api/` - API endpoints
   - `services/` - External service integrations

2. **High Complexity Code**
   - Any function with cyclomatic complexity > 15
   - Files with > 500 lines
   - Functions with > 50 lines

3. **Large Changes**
   - > 10 files modified in a phase
   - > 500 lines added/modified

### Manual Triggers

- User says "review code" or "code review"
- User says "check my implementation"
- Activated via `/code-review` command

## Review Checklist

### Security Review

- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] Input validation on all external inputs
- [ ] Output encoding to prevent XSS
- [ ] SQL queries use parameterized statements
- [ ] Authentication checks on protected routes
- [ ] Authorization checks for resource access
- [ ] Sensitive data not logged
- [ ] HTTPS enforced for external calls

### Code Quality Review

- [ ] Functions have single responsibility
- [ ] No code duplication (DRY)
- [ ] Meaningful variable/function names
- [ ] Complex logic has comments explaining WHY
- [ ] Error handling is appropriate
- [ ] No silent failures (catch without action)
- [ ] Resource cleanup (files, connections, etc.)

### Architecture Review

- [ ] Follows layer boundaries (L0-L5)
- [ ] Dependencies flow downward only
- [ ] Interface contracts respected
- [ ] No circular dependencies
- [ ] Separation of concerns maintained

### Test Coverage Review

- [ ] Critical paths have 100% coverage
- [ ] Edge cases are tested
- [ ] Error paths are tested
- [ ] Assertions are meaningful (not just execution)
- [ ] No mocks in production code

### Documentation Review

- [ ] Public functions have docstrings/JSDoc
- [ ] Complex algorithms are explained
- [ ] API changes documented
- [ ] README updated if needed

## Review Process

### Step 1: Gather Changes

```bash
# Show all files changed in this phase
git diff --stat HEAD~10..HEAD

# Show detailed diff
git diff HEAD~10..HEAD

# List files by complexity (if radon available)
radon cc -s src/
```

### Step 2: Analyze Risk

The skill analyzes changes and categorizes them:

| Category | Action | Blocking |
|----------|--------|----------|
| Security-critical | Must review all changes | YES |
| High-complexity | Must review flagged functions | YES |
| API changes | Must review contracts | YES |
| Internal changes | Spot-check recommended | NO |

### Step 3: Present to Human

```
═══════════════════════════════════════════════════════════════
  CODE REVIEW REQUIRED
═══════════════════════════════════════════════════════════════

Trigger: Security-sensitive files modified

Files for Review:
  1. src/auth/login.py (52 lines added)
     - New authentication logic
     - Complexity: 8/10
     - Security: HIGH PRIORITY

  2. src/auth/tokens.py (34 lines added)
     - JWT token handling
     - Complexity: 5/10
     - Security: HIGH PRIORITY

  3. api/users.py (78 lines added)
     - User CRUD operations
     - Complexity: 6/10
     - Security: MEDIUM PRIORITY

Review Checklist:
  [ ] Security review completed
  [ ] Code quality acceptable
  [ ] Architecture boundaries respected
  [ ] Test coverage verified

Actions:
  - "approve" - Proceed to Phase 6
  - "reject [reason]" - Return to implementation
  - "comment [file:line] [note]" - Add review comment
  - "show [file]" - Display file contents
  - "diff [file]" - Show file diff
═══════════════════════════════════════════════════════════════
```

### Step 4: Human Decision

**Approve:**
```
approve

✅ CODE REVIEW APPROVED
Proceeding to Phase 9 (Integration Testing)
[SIGNAL:CODE_REVIEW_COMPLETE]
[ACTIVATE:INTEGRATION_VALIDATOR_V1]
```

**Reject:**
```
reject Security: Missing input validation on user_id parameter in api/users.py:45

❌ CODE REVIEW REJECTED
Reason: Security: Missing input validation on user_id parameter in api/users.py:45

Returning to Phase 7 for fixes.
Please address the review feedback and re-submit.
```

**Add Comment:**
```
comment src/auth/login.py:23 Consider using constant-time comparison for password check

📝 Comment added to review log
Continue with: approve | reject | more comments
```

## Output Files

### Review Report

`.claude/reports/code-review-report.json`:
```json
{
  "phase": 5.5,
  "timestamp": "2025-12-19T12:00:00Z",
  "status": "approved",
  "reviewer": "human",
  "trigger": "security_sensitive_paths",
  "files_reviewed": 3,
  "security_items": 2,
  "complexity_items": 1,
  "comments": [
    {
      "file": "src/auth/login.py",
      "line": 23,
      "comment": "Consider using constant-time comparison for password check"
    }
  ],
  "checklist": {
    "security": true,
    "code_quality": true,
    "architecture": true,
    "test_coverage": true,
    "documentation": true
  }
}
```

### Completion Signal

`.claude/.signals/code-review-complete.json`:
```json
{
  "phase": 8,
  "status": "approved",
  "timestamp": "2025-12-19T12:00:00Z",
  "next_phase": 9,
  "trigger_next": true
}
```

## Configuration

In `config/quality-rules.json`:

```json
{
  "code_review_gate": {
    "enabled": true,
    "trigger_on": {
      "security_sensitive_paths": [
        "src/auth/",
        "src/security/",
        "api/"
      ],
      "high_complexity_threshold": 15,
      "file_changes_threshold": 10
    }
  }
}
```

To disable for a project:
```json
{
  "code_review_gate": {
    "enabled": false
  }
}
```

## Bypass (Emergency Only)

For emergency situations only, the gate can be bypassed:

```
bypass-review --reason "Production hotfix for CVE-2025-XXXXX" --ticket JIRA-1234
```

Bypass requirements:
- Must provide reason
- Must provide ticket/tracking number
- Logged to audit trail
- Triggers post-deployment review

## Integration with Pipeline

```
Phase 7: TDD Implementation
    ↓
Phase 8: Code Review Gate (NEW)
    ├─ Automatic for security/complexity triggers
    ├─ Human reviews code
    └─ Approve/Reject decision
    ↓
Phase 9: Integration Testing
```

## See Also

- `hooks/code-quality-validator.sh` - Automated quality checks
- `config/quality-rules.json` - Quality thresholds
- `skills/prd-audit/SKILL.md` - PRD quality audit
