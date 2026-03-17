---
name: plan-create-component
description: "DEPRECATED: The notes/plan/ directory has been removed. Planning is now done directly through GitHub issues. See gh-read-issue-context and gh-post-issue-update skills instead."
mcp_fallback: none
category: plan
deprecated: true
user-invocable: false
---

# Create Component Plan Skill (DEPRECATED)

**DEPRECATED**: This skill is no longer used. The `notes/plan/` directory has been removed.
Planning is now done directly through GitHub issues.

See `.claude/shared/github-issue-workflow.md` for the new workflow.

## Replacement Workflow

To create a new component, create a GitHub issue directly:

```bash
gh issue create --title "[Plan] Component Name" --body "$(cat <<'EOF'
## Overview
Brief description

## Objectives
- Objective 1
- Objective 2

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
EOF
)"
```

## Replacement Skills

- `gh-read-issue-context` - Read context from GitHub issues
- `gh-post-issue-update` - Post structured updates to GitHub issues

---

## Legacy Documentation (for reference only)

Create new component plans and integrate into hierarchy.

## When to Use

- Adding new component to plan
- Extending existing section
- New subsection needed
- Modifying plan structure

## Quick Reference

```bash
./scripts/create_component_plan.sh "Component Name" "parent/path"
# Example
./scripts/create_component_plan.sh "Tensor Operations" "notes/plan/02-shared-library/01-core"
```

## Workflow

1. **Create plan** - Run generator script with component name
2. **Edit plan** - Fill in 9-section template
3. **Update parent** - Add to parent's Child Plans section
4. **Regenerate issues** - Update github_issue.md files
5. **Validate structure** - Verify format compliance

## Template 1 Format (9 Sections)

All plans must have these sections in order:

1. **Title** - `# Component Name`
2. **Overview** - 2-3 sentence description
3. **Parent Plan** - Link to parent or "None (top-level)"
4. **Child Plans** - Links to children or "None (leaf node)"
5. **Inputs** - Prerequisites and dependencies
6. **Outputs** - Deliverables and results
7. **Steps** - Numbered implementation steps
8. **Success Criteria** - Measurable checkboxes
9. **Notes** - Additional context

## Creation Workflow

```bash
# 1. Generate plan
./scripts/create_component_plan.sh "New Component" "notes/plan/section"

# 2. Edit generated file
vim notes/plan/section/new-component/plan.md

# 3. Update parent's Child Plans
vim notes/plan/section/plan.md
# Add: - [new-component/plan.md](new-component/plan.md)

# 4. Regenerate issues
python3 scripts/regenerate_github_issues.py --section section

# 5. Validate
./scripts/validate_plan.sh notes/plan/section/new-component/plan.md
```

## Plan Structure Example

```markdown
# Component Name

## Overview
2-3 sentence description of what this component does.

## Parent Plan
[../plan.md](../plan.md) or "None (top-level)"

## Child Plans
- [child1/plan.md](child1/plan.md)
- [child2/plan.md](child2/plan.md)
Or "None (leaf node)"

## Inputs
- Input 1: Description
- Input 2: Description

## Outputs
- Output 1: Description
- Output 2: Description

## Steps
1. Step 1: Description
2. Step 2: Description
3. Step 3: Description

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Notes
Additional context and considerations.
```

## Error Handling

| Issue | Fix |
|-------|-----|
| Script not found | Check script exists in `scripts/` |
| Parent path wrong | Verify parent directory structure |
| Template incomplete | Ensure all 9 sections present |
| Links broken | Use relative paths (../plan.md) |

## Validation

```bash
# Validate single plan
./scripts/validate_plan.sh notes/plan/path/plan.md

# Validate all plans in section
./scripts/validate_plans.sh notes/plan/section/

# Check hierarchy
./scripts/validate_plan_hierarchy.sh
```

## References

- Template 1 format: CLAUDE.md
- Related skill: `plan-regenerate-issues` for issue creation
- Related skill: `plan-validate-structure` for validation
