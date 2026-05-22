---
name: pre-pr-checklist
description: Validate documentation requirements before creating a PR. Checks for scratchpad entries, CHANGELOG updates, tests, and plan files based on change type. Use before creating pull requests to ensure all documentation gates are satisfied.
---

# Pre-PR Checklist Skill

Validates that all required documentation and artifacts exist before creating a pull request. Prevents PRs from being created with missing documentation, tests, or planning artifacts.

## When This Skill Activates

- Before creating a pull request
- When user runs `/pre-pr-checklist`
- When user asks to validate PR readiness
- After completing work, before committing

## Documentation Requirements Matrix

| Change Type | Scratchpad | CHANGELOG | Tests | Plan File |
|-------------|:----------:|:---------:|:-----:|:---------:|
| **New feature** | Required | Required | Required | Required |
| **Bug fix** | If complex | Required | Required | If complex |
| **Code change** | If complex | If user-facing | Required | If complex |
| **Documentation only** | No | If significant | No | No |
| **Refactoring** | If complex | No | Required | If complex |
| **Dependency update** | No | If major | No | No |

### Complexity Indicators

A change is "complex" if any of these apply:
- Touches 5+ files
- Modifies database models or migrations
- Changes core business logic (scheduling, ACGME, constraints)
- Requires coordination across frontend/backend
- Has non-obvious implementation details
- Required debugging or multiple iterations

## Pre-Flight Verification Steps

### Step 1: Classify the Change

```bash
# Get list of changed files
git diff --cached --name-only
git diff origin/main...HEAD --name-only

# Count files changed
git diff origin/main...HEAD --stat | tail -1

# Check for database changes
git diff origin/main...HEAD --name-only | grep -E "(alembic|models)"

# Check for frontend/backend span
git diff origin/main...HEAD --name-only | grep -c "^frontend/"
git diff origin/main...HEAD --name-only | grep -c "^backend/"
```

Determine change type:
- [ ] New feature
- [ ] Bug fix
- [ ] Code change (enhancement)
- [ ] Documentation only
- [ ] Refactoring
- [ ] Dependency update

### Step 2: Check Scratchpad Entry

**Location:** `docs/development/scratchpad/` or `docs/planning/`

For complex work, verify a scratchpad or planning document exists:

```bash
# Check for recent scratchpad entries
find docs/development -name "*.md" -mtime -1 | head -10

# Check for session handoffs
find docs/development -name "SESSION_*.md" -mtime -1

# Check for planning docs
find docs/planning -name "*.md" -mtime -1 | head -10
```

**Scratchpad must contain:**
- [ ] Problem statement / motivation
- [ ] Approach taken
- [ ] Key decisions and rationale
- [ ] Files modified
- [ ] Testing approach

### Step 3: Check CHANGELOG Update

**Location:** `CHANGELOG.md` (project root)

```bash
# Check if CHANGELOG was modified
git diff origin/main...HEAD --name-only | grep "CHANGELOG.md"

# View CHANGELOG additions
git diff origin/main...HEAD -- CHANGELOG.md | grep "^+" | head -20
```

**CHANGELOG entry must:**
- [ ] Be under `## [Unreleased]` section
- [ ] Use correct category (Added, Changed, Fixed, Removed, Security)
- [ ] Describe what changed from user perspective
- [ ] Include date if significant

### Step 4: Check Test Coverage

**Backend tests:** `backend/tests/`
**Frontend tests:** `frontend/__tests__/` or `*.test.ts(x)`

```bash
# Check for new/modified tests
git diff origin/main...HEAD --name-only | grep -E "test_.*\.py$|\.test\.(ts|tsx)$|\.spec\.(ts|tsx)$"

# Run backend tests
cd backend && pytest --tb=short -q

# Run frontend tests
cd frontend && npm test -- --watchAll=false
```

**Test requirements:**
- [ ] Tests exist for new code
- [ ] Tests pass locally
- [ ] Coverage maintained or improved
- [ ] Edge cases covered

### Step 5: Check Plan File (If Complex)

**Location:** `docs/planning/` or `docs/development/`

For complex work, verify a plan document exists:

```bash
# Check for plan files
ls -la docs/planning/*PLAN*.md 2>/dev/null
ls -la docs/planning/*IMPLEMENTATION*.md 2>/dev/null
```

**Plan must contain:**
- [ ] Scope and objectives
- [ ] Implementation approach
- [ ] Success criteria
- [ ] Risk considerations

## Quick Validation Script

Run this before creating a PR:

```bash
#!/bin/bash
# Pre-PR Checklist Validation

echo "============================================================"
echo "PRE-PR CHECKLIST VALIDATION"
echo "============================================================"

# Get changed files
CHANGED_FILES=$(git diff origin/main...HEAD --name-only)
FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l)

echo ""
echo "Changed files: $FILE_COUNT"
echo "$CHANGED_FILES" | head -10
echo ""

# Complexity check
echo "============================================================"
echo "COMPLEXITY ANALYSIS"
echo "============================================================"

COMPLEX=0

if [ "$FILE_COUNT" -gt 5 ]; then
    echo "[!] 5+ files changed - marked as COMPLEX"
    COMPLEX=1
fi

if echo "$CHANGED_FILES" | grep -q "alembic\|models"; then
    echo "[!] Database changes detected - marked as COMPLEX"
    COMPLEX=1
fi

if echo "$CHANGED_FILES" | grep -q "scheduling\|constraints\|acgme"; then
    echo "[!] Core business logic changed - marked as COMPLEX"
    COMPLEX=1
fi

FE_COUNT=$(echo "$CHANGED_FILES" | grep -c "^frontend/" || true)
BE_COUNT=$(echo "$CHANGED_FILES" | grep -c "^backend/" || true)
if [ "$FE_COUNT" -gt 0 ] && [ "$BE_COUNT" -gt 0 ]; then
    echo "[!] Frontend + Backend changes - marked as COMPLEX"
    COMPLEX=1
fi

if [ "$COMPLEX" -eq 0 ]; then
    echo "[OK] Change appears straightforward"
fi

echo ""

# CHANGELOG check
echo "============================================================"
echo "CHANGELOG CHECK"
echo "============================================================"

if echo "$CHANGED_FILES" | grep -q "CHANGELOG.md"; then
    echo "[OK] CHANGELOG.md modified"
else
    echo "[?] CHANGELOG.md not modified - required if user-facing change"
fi

echo ""

# Test check
echo "============================================================"
echo "TEST CHECK"
echo "============================================================"

TEST_FILES=$(echo "$CHANGED_FILES" | grep -E "test_.*\.py$|\.test\.(ts|tsx)$|\.spec\.(ts|tsx)$" || true)
if [ -n "$TEST_FILES" ]; then
    echo "[OK] Test files modified:"
    echo "$TEST_FILES" | head -5
else
    echo "[?] No test files modified - required for code changes"
fi

echo ""

# Scratchpad/Plan check (if complex)
echo "============================================================"
echo "DOCUMENTATION CHECK"
echo "============================================================"

if [ "$COMPLEX" -eq 1 ]; then
    echo "[!] Complex change - checking for documentation..."

    RECENT_DOCS=$(find docs/development docs/planning -name "*.md" -mtime -1 2>/dev/null | head -5)
    if [ -n "$RECENT_DOCS" ]; then
        echo "[OK] Recent documentation found:"
        echo "$RECENT_DOCS"
    else
        echo "[?] No recent documentation found - consider adding scratchpad/plan"
    fi
else
    echo "[OK] Simple change - detailed documentation optional"
fi

echo ""
echo "============================================================"
echo "SUMMARY"
echo "============================================================"

echo ""
echo "Before creating PR, ensure:"
if [ "$COMPLEX" -eq 1 ]; then
    echo "  [ ] Scratchpad entry exists (complex change)"
    echo "  [ ] Plan file exists (complex change)"
fi
echo "  [ ] CHANGELOG updated (if user-facing)"
echo "  [ ] Tests added/updated (if code change)"
echo "  [ ] All tests pass"
echo ""
```

## Checklist by Change Type

### New Feature Checklist

- [ ] **Scratchpad entry** - Document motivation, approach, decisions
- [ ] **CHANGELOG entry** - Under `### Added` with user-friendly description
- [ ] **Unit tests** - Cover happy path and edge cases
- [ ] **Integration tests** - If applicable
- [ ] **Plan file** - `docs/planning/FEATURE_NAME_PLAN.md`
- [ ] **API docs** - If new endpoints (docstrings + OpenAPI)
- [ ] **User guide update** - If user-facing

### Bug Fix Checklist

- [ ] **Scratchpad entry** - If debugging was complex
- [ ] **CHANGELOG entry** - Under `### Fixed` with what was broken
- [ ] **Regression test** - Test that reproduces the bug
- [ ] **Root cause documented** - In commit message or scratchpad

### Code Change (Enhancement) Checklist

- [ ] **Scratchpad entry** - If complex
- [ ] **CHANGELOG entry** - Under `### Changed` if user-facing
- [ ] **Tests updated** - Reflect new behavior
- [ ] **Existing tests pass** - No regressions

### Documentation Only Checklist

- [ ] **CHANGELOG entry** - Under `### Changed` if significant
- [ ] **Links verified** - All internal links work
- [ ] **Spelling/grammar** - Proofread

## Output Format

After running validation, report:

```markdown
## Pre-PR Checklist Results

### Change Classification
- **Type:** [New Feature / Bug Fix / Code Change / Documentation / Refactoring]
- **Complexity:** [Simple / Complex]
- **Files Changed:** [count]

### Required Documentation Status

| Requirement | Status | Notes |
|-------------|--------|-------|
| Scratchpad Entry | [OK/MISSING/N/A] | [path or reason] |
| CHANGELOG Update | [OK/MISSING/N/A] | [path or reason] |
| Tests | [OK/MISSING/N/A] | [path or reason] |
| Plan File | [OK/MISSING/N/A] | [path or reason] |

### Blockers
[List any missing requirements that must be addressed]

### Recommendations
[List optional improvements]

### Verdict
[READY TO CREATE PR / BLOCKED - address items above]
```

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `session-documentation` | Provides scratchpad entries |
| `changelog-generator` | Can generate CHANGELOG entries |
| `test-writer` | Generates missing tests |
| `pr-reviewer` | Uses this checklist for review |
| `code-quality-monitor` | Runs quality gates |

## Escalation Rules

**Block PR creation when:**
1. Code changes have no tests
2. User-facing changes have no CHANGELOG entry
3. Complex changes have no documentation
4. Tests are failing

**Allow with warning when:**
1. Documentation is minimal but present
2. CHANGELOG entry is generic
3. Only dependency updates

## References

- Session Documentation skill for scratchpad requirements
- CHANGELOG.md format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- Test requirements: `CLAUDE.md` Testing Requirements section
