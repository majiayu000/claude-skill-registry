---
name: parallel-integrate
description: Verify integration after parallel agent execution and generate report
argument-hint: "[--parallel-dir <dir>] [--tech django|typescript|go]"
---

# parallel-integrate

**Category**: Parallel Development

## Usage

```bash
/parallel-integrate [--parallel-dir <dir>] [--tech django|typescript|go]
```

## Arguments

- `--parallel-dir`: Optional - Path to parallel directory (auto-detects if single directory in `parallel/`)
- `--tech`: Optional - Technology stack for specific checks (default: auto-detect)

## Purpose

Verify integration after all parallel agents complete their work. Checks contract compliance, boundary violations, runs tests, and generates an integration report.

## Prerequisites

- All parallel tasks completed
- All feature branches merged to main (or ready to merge)
- Run after `/parallel-decompose` execution

## Execution Instructions for Claude Code

### 0. Determine Parallel Directory

**If `--parallel-dir` provided**:
- Use specified directory (e.g., `parallel/TS-0042-inventory-system`)

**If not provided**:
- Scan `parallel/` for subdirectories
- If single directory found, use it
- If multiple, list and ask user to specify
- If none, error with guidance

Read `manifest.json` from parallel directory:
```bash
PARALLEL_DIR="parallel/TS-0042-inventory-system"
cat "$PARALLEL_DIR/manifest.json"
```

### 1. Verify Branch Status

Check all task branches are complete:
```bash
# List task branches
git branch -a | grep feature/task-

# Check for unmerged branches
git branch --no-merged main | grep feature/task-
```

### 2. Merge Remaining Branches

If unmerged branches exist:
```bash
git checkout main
for branch in $(git branch --no-merged main | grep feature/task-); do
    echo "Merging $branch..."
    git merge $branch --no-edit
done
```

### 3. Technology-Specific Integration

#### For Django Projects

**Migration Merge**:
```bash
# Check for migration conflicts
python manage.py showmigrations | grep "\[ \]"

# If conflicts, merge migrations
python manage.py makemigrations --merge

# Apply all migrations
python manage.py migrate
```

**Verification**:
```bash
# Django system check
python manage.py check

# Run all tests
pytest

# Type checking
mypy apps/

# Linting
ruff check .
```

#### For TypeScript Projects

**Build Verification**:
```bash
# Type check
npx tsc --noEmit

# Lint
npm run lint

# Run tests
npm test

# Build
npm run build
```

#### For Go Projects

```bash
# Build and vet
go build ./...
go vet ./...

# Run tests
go test ./...

# Check formatting
gofmt -d .
```

### 4. Contract Compliance Check

For each task in `$PARALLEL_DIR/tasks/`:

**API Contract Check**:
- Compare implemented endpoints against `$PARALLEL_DIR/contracts/api-schema.yaml`
- Verify request/response schemas match
- Check error formats

**Type Contract Check**:
- Verify types match `$PARALLEL_DIR/contracts/types.py` (or `.ts`)
- Check for missing fields
- Verify enum values

### 5. Boundary Violation Check

For each task, verify:
- Files modified are within declared scope
- No files touched that were in "BOUNDARY" list
- No unauthorized contract modifications

```bash
# Check git history for boundary violations
for task in $(ls $PARALLEL_DIR/tasks/); do
    echo "Checking $task boundaries..."
    # Compare committed files against task scope
done
```

### 6. Tech Spec Compliance Check

Read Tech Spec path from manifest:
```bash
TECH_SPEC=$(jq -r '.tech_spec.path' "$PARALLEL_DIR/manifest.json")
```

If Tech Spec exists, validate implementation:

**Architecture Alignment**:
- Compare implemented components against Tech Spec Design Overview
- Verify component boundaries match spec
- Check that data flow matches documented architecture

**Data Model Compliance**:
- Compare implemented models against Tech Spec Data Model section
- Verify all entities are implemented
- Check field types and constraints match

**API Compliance**:
- Compare implemented endpoints against Tech Spec API Specification
- Verify request/response formats match
- Check error handling matches spec

### 7. Generate Integration Report

Create `$PARALLEL_DIR/integration-report.md`:

```markdown
# Integration Report

Generated: [date]
Parallel Dir: parallel/TS-0042-inventory-system
Source PRD: [from manifest.sources.prd]
Tech Spec: [from manifest.tech_spec.id]
Tasks Integrated: [count]

## Summary

| Check | Status | Details |
|-------|--------|---------|
| Branch Merge | ✅/❌ | X branches merged |
| Contract Compliance | ✅/⚠️/❌ | X/Y endpoints match |
| Tech Spec Compliance | ✅/⚠️/❌ | X deviations |
| Boundary Violations | ✅/❌ | X violations found |
| Tests | ✅/❌ | X passed, Y failed |
| Type Check | ✅/❌ | X errors |
| Lint | ✅/❌ | X warnings |

## Contract Compliance

### API Endpoints

| Endpoint | Status | Notes |
|----------|--------|-------|
| GET /api/users/ | ✅ | Matches spec |
| POST /api/users/ | ⚠️ | Missing validation field |

### Type Definitions

| Type | Status | Notes |
|------|--------|-------|
| UserDTO | ✅ | Matches contract |
| OrderDTO | ⚠️ | Extra field `updated_at` |

## Boundary Violations

| Task | File | Issue |
|------|------|-------|
| task-003 | apps/users/models.py | Modified (owned by task-001) |

## Tech Spec Compliance

| Section | Status | Deviations |
|---------|--------|------------|
| Architecture | ✅ | None |
| Data Model | ⚠️ | Added `updated_at` to User |
| API Spec | ✅ | None |

## Test Results

```
pytest results:
  Passed: 142
  Failed: 2
  Coverage: 84%
```

## Action Items

### Must Fix (Blocking)
1. ❌ Fix failing tests

### Should Fix (Non-Blocking)
1. ⚠️ Add missing validation field

## Next Steps

[If all checks pass]:
1. ✅ Integration complete
2. Create PR for review
```

### 8. Update manifest.json

Update integration status:
```json
{
  "integration": {
    "status": "completed",
    "report_path": "integration-report.md",
    "completed_at": "2025-12-07T18:00:00Z",
    "checks": {
      "branch_merge": "passed",
      "contract_compliance": "warning",
      "boundary_violations": "passed",
      "tests": "passed"
    }
  }
}
```

### 9. Report Results

Output to console:
```
Integration Verification Complete

Parallel Dir: parallel/TS-0042-inventory-system
Tech Spec: TS-0042-inventory-system

┌────────────────────┬────────┬─────────────────────────┐
│ Check              │ Status │ Details                 │
├────────────────────┼────────┼─────────────────────────┤
│ Branch Merge       │ ✅     │ 9 branches merged       │
│ Contract Compliance│ ⚠️     │ 18/20 endpoints match   │
│ Boundary Violations│ ✅     │ 0 violations            │
│ Tests              │ ✅     │ 142 passed              │
│ Type Check         │ ✅     │ 0 errors                │
│ Lint               │ ✅     │ 0 warnings              │
└────────────────────┴────────┴─────────────────────────┘

Full report: parallel/TS-0042-inventory-system/integration-report.md

[If clean]:
✅ Integration successful!

Next steps:
1. Review report
2. Create pull request
3. Deploy to staging
```

## Example

```bash
# Auto-detect parallel directory
/parallel-integrate

# Specify parallel directory
/parallel-integrate --parallel-dir parallel/TS-0042-inventory-system

# With Django-specific checks
/parallel-integrate --parallel-dir parallel/TS-0042-inventory-system --tech django

# After fixing issues, re-run
/parallel-integrate

# View report
cat parallel/TS-0042-inventory-system/integration-report.md
```

## Integration Checklist

- [ ] All feature branches merged
- [ ] No merge conflicts
- [ ] Migrations applied (Django)
- [ ] All tests pass
- [ ] Type checks pass
- [ ] Lint passes
- [ ] No boundary violations
- [ ] Contract compliance verified
- [ ] Tech Spec compliance verified
- [ ] Integration report generated
- [ ] manifest.json updated

## Related Commands

- `/parallel-setup` - One-time project initialization
- `/parallel-decompose` - Create tasks and prompts
