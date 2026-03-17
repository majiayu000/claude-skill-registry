---
name: beads-validation
description: |
  Validates beads issues after creation. Checks dependencies, PRD mapping, order, and issue quality.
  Use when: after creating issues, before TDD loop, before handoff.
  Triggers: "validate beads", "check issues", "verify tasks", "check quality", "validate handoff".
---

# Beads Validation Skill

Validates that beads issues are correctly created and ready for TDD.

## When to Use

1. **After creating issues** (in rust-project-init):
   - Check all PRD features have corresponding issues
   - Check priorities are valid
   - Check issue IDs exist before adding dependencies

2. **Before TDD loop** (in /ship Phase 2.5):
   - Check for circular dependencies
   - Check `bd ready` returns expected first task
   - Check no issues are incorrectly blocked

## Validation Checks

### 1. PRD → Issues Mapping
```bash
# Count features in PRD
grep -c "^###\|^-" docs/PRD.md | head -1

# Count issues created
bd list --status=open | wc -l

# Each MVP feature should have an issue
```

### 2. Dependency Validity
```bash
# List all dependencies
bd list --status=open --json | jq '.[] | .dependencies'

# Check each dependency ID exists
bd show {dep_id}  # Should not error
```

### 3. Circular Dependency Check
```bash
# bd doctor checks for cycles
bd doctor
```

### 4. Ready State Check
```bash
# Should have at least one ready issue
bd ready --limit=1

# If empty, something is blocked incorrectly
```

### 5. Priority Validation
```bash
# All priorities should be 0-4
bd list --json | jq '.[] | .priority' | sort -u
```

### 6. Issue Quality Check (NEW)
```bash
# Check all open issues have required sections
python3 scripts/validate_beads.py --check-quality
```

Validates that issues are self-contained:
- **Minimum length**: Description > 100 characters
- **Summary section**: Overview, Goal, or clear opening statement
- **Files section**: Specific paths mentioned
- **Steps section**: Implementation steps (numbered list)
- **Criteria section**: Acceptance criteria or checkboxes

## Script Usage

```bash
# After creating issues
python3 scripts/validate_beads.py --check-created --prd docs/PRD.md

# Before TDD
python3 scripts/validate_beads.py --check-deps --check-ready

# Check issue quality (for handoff)
python3 scripts/validate_beads.py --check-quality

# Full validation (all checks)
python3 scripts/validate_beads.py --all --prd docs/PRD.md
```

**Output:**
```
## Beads Validation

[PASS] PRD features: 4, Issues created: 4
[PASS] All dependency IDs exist
[PASS] No circular dependencies
[PASS] Ready queue has 1 issue (notes-abc)
[PASS] All 4 open issues pass quality check
[PASS] All priorities valid (0-4)

Result: 6/6 checks passed
```

**Quality check failure output:**
```
## Beads Validation

[WARN] 2/4 issues have quality problems

  Quality issues:
    task-abc:
      - Description too short (45 chars, need 100+)
      - Missing Acceptance Criteria section
    task-xyz:
      - Missing Files to Modify section
```

## Common Issues

### No Ready Issues
```
[FAIL] No issues ready to work on
```
**Cause:** All issues blocked by dependencies
**Fix:** Check dependency chain, ensure at least one issue has no blockers

### Missing Features
```
[WARN] PRD has 5 features, only 3 issues created
```
**Fix:** Create missing issues with `bd create`

### Invalid Dependency
```
[FAIL] Dependency notes-xyz does not exist
```
**Fix:** Check issue ID before `bd dep add`

### Circular Dependency
```
[FAIL] Circular dependency: A → B → C → A
```
**Fix:** Remove one dependency to break cycle

### Low Quality Issue
```
[WARN] task-abc: Description too short (45 chars, need 100+)
[WARN] task-abc: Missing Files to Modify section
```
**Fix:** Use `bd edit <id> --description` and follow the template from `beads-workflow/references/issue-template.md`

## Integration

Called automatically in:
- `rust-project-init.md` → After creating issues
- `ship.md` → Phase 2.5: Before TDD loop
- `beads-workflow` → Before handoff (Phase 5)
