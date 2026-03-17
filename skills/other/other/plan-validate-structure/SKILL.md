---
name: plan-validate-structure
description: "DEPRECATED: The notes/plan/ directory has been removed. Planning is now done directly through GitHub issues. See gh-read-issue-context and gh-post-issue-update skills instead."
mcp_fallback: none
category: plan
deprecated: true
user-invocable: false
---

# Plan Structure Validation Skill (DEPRECATED)

**DEPRECATED**: This skill is no longer used. The `notes/plan/` directory has been removed.
Planning is now done directly through GitHub issues.

See `.claude/shared/github-issue-workflow.md` for the new workflow.

## Replacement Skills

- `gh-read-issue-context` - Read context from GitHub issues
- `gh-post-issue-update` - Post structured updates to GitHub issues

---

## Legacy Documentation (for reference only)

Validate plans follow Template 1 format and hierarchy rules.

## When to Use

- After creating new plans
- Before committing plan changes
- Before creating GitHub issues
- Troubleshooting plan errors

## Quick Reference

```bash
# Validate all plans
./scripts/validate_all_plans.sh

# Validate specific section
./scripts/validate_plans.sh notes/plan/01-foundation

# Validate single plan
./scripts/validate_plan.sh notes/plan/01-foundation/plan.md
```

## Validation Checks

### 1. Template Format

- All 9 sections present
- Sections in correct order
- Proper markdown formatting
- No empty mandatory sections

### 2. Hierarchy

- Parent/child links valid
- No circular references
- Correct nesting level
- All referenced files exist

### 3. Content

- Title present (# heading)
- Overview is 2-3 sentences
- Steps numbered correctly
- Success criteria have checkboxes

### 4. Links

- All use relative paths
- Links point to existing files
- No broken references

## Template 1 Sections

Required sections in order:

1. Title - `# Component Name`
2. Overview - Description of component
3. Parent Plan - Link or "None (top-level)"
4. Child Plans - Links or "None (leaf node)"
5. Inputs - Prerequisites
6. Outputs - Deliverables
7. Steps - Numbered steps
8. Success Criteria - Checkboxes
9. Notes - Additional context

## Common Issues

| Issue | Error | Fix |
|-------|-------|-----|
| Missing section | "Missing section: ## Steps" | Add missing section |
| Wrong order | Section ordering error | Reorder sections correctly |
| Broken link | "Broken link: ../bad.md" | Fix or create referenced file |
| No checkboxes | "Success criteria must use - [ ]" | Convert to checkbox format |

## Validation Workflow

```bash
# 1. Edit plan
vim notes/plan/section/component/plan.md

# 2. Validate locally
./scripts/validate_plan.sh notes/plan/section/component/plan.md

# 3. If errors, fix them
# ... edit plan.md ...

# 4. Re-validate
./scripts/validate_plan.sh notes/plan/section/component/plan.md

# 5. If passing, commit
git add notes/plan/section/component/plan.md
git commit -m "docs: add component plan"
```

## Format Checklist

- [ ] Title is `# Heading` (single #)
- [ ] Overview is 2-3 sentences
- [ ] Parent Plan link is correct
- [ ] Child Plans links exist
- [ ] All 5 Inputs listed
- [ ] All 5 Outputs listed
- [ ] Steps are numbered 1, 2, 3...
- [ ] Success Criteria use `- [ ]`
- [ ] Notes section present
- [ ] All links use relative paths
- [ ] No broken references
- [ ] No empty sections

## Error Handling

| Error | Solution |
|-------|----------|
| Script not found | Verify script in `scripts/` |
| Permission denied | Run: `chmod +x scripts/*.sh` |
| Invalid path | Use absolute or correct relative path |
| File not found | Create referenced file or fix path |

## Validation Scripts

- `scripts/validate_all_plans.sh` - Validate everything
- `scripts/validate_plans.sh <dir>` - Validate directory
- `scripts/validate_plan.sh <file>` - Validate single plan
- `scripts/validate_plan_hierarchy.sh` - Check hierarchy

## References

- Template 1 format: CLAUDE.md
- Related skill: `plan-create-component` for creating plans
- Related skill: `plan-regenerate-issues` for issue generation
