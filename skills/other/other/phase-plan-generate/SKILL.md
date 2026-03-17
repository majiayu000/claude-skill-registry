---
name: phase-plan-generate
description: "Generate comprehensive plan documentation following Template 1 format. Use when creating plan.md files for new components or subsections."
mcp_fallback: none
category: phase
phase: Plan
user-invocable: false
---

# Plan Generation Skill

Generate plan documentation following ML Odyssey's standard 9-section Template 1 format.

## When to Use

- Creating new `plan.md` files for components or subsections
- Starting planning phase documentation
- Generating planning specifications before implementation
- Need to follow Template 1 format with all 9 sections

## Quick Reference

```bash
# Validate existing plan has all 9 sections
grep -E "^## (Overview|Parent Plan|Child Plans|Inputs|Outputs|Steps|Success Criteria|Notes)" plan.md

# Generate from template
cat > plan.md << 'EOF'
# Component Name

## Overview
Brief description (2-3 sentences)

## Parent Plan
[Link or "None (top-level)"]

## Child Plans
[Links or "None (leaf node)"]

## Inputs
- Prerequisite 1

## Outputs
- Deliverable 1

## Steps
1. Step 1

## Success Criteria
- [ ] Criterion 1

## Notes
Additional context
EOF
```

## Workflow

1. **Create plan.md** with all 9 required sections
2. **Use relative paths** for links (e.g., `../plan.md`, not absolute)
3. **Make inputs specific** (list dependencies clearly)
4. **Make outputs measurable** (actual deliverables, not vague goals)
5. **Make steps actionable** (numbered, clear sequence)
6. **Make criteria verifiable** (checkboxes with specific outcomes)
7. **Update parent plan's** "Child Plans" section after creation
8. **Regenerate GitHub issues**: `python3 scripts/regenerate_github_issues.py --section <section>`

## Template 1 Format (9 Sections)

```markdown
# Component Name

## Overview
Brief description (2-3 sentences) of what this component does.

## Parent Plan
[../parent/plan.md](../parent/plan.md)
Or: "None (top-level)" for section-level plans

## Child Plans
- [child1/plan.md](child1/plan.md)
- [child2/plan.md](child2/plan.md)
Or: "None (leaf node)" for lowest-level plans

## Inputs
- Prerequisite 1
- Prerequisite 2
- Dependency 3

## Outputs
- Deliverable file/artifact 1
- Deliverable file/artifact 2
- Test files or documentation

## Steps
1. First step
2. Second step
3. Third step

## Success Criteria
- [ ] Criterion 1 (verifiable outcome)
- [ ] Criterion 2 (measurable result)

## Notes
Additional context, assumptions, or considerations.
```

## Phase Dependencies

- **Precedes**: Test, Implementation, Package phases (plan must complete first)
- **Receives input from**: Design phase (specifications, architecture decisions)
- **Produces for**: All subsequent phases (implementation specifications)

## Output Location

- **Planning**: GitHub issue body and comments
- **Specifications**: `/notes/review/` for architectural decisions
- **Issue tracking**: GitHub issue comments

## Error Handling

| Error | Fix |
|-------|-----|
| Missing sections | Add all 9 sections from template |
| Broken links | Use relative paths (`../` notation) |
| Vague inputs/outputs | Make specific and measurable |
| No success criteria | Add verifiable checkboxes |
| Broken hierarchy | Verify parent/child links exist |

## References

- `CLAUDE.md` - "GitHub Issue Structure" section
- `.claude/shared/github-issue-workflow.md` - GitHub issue workflow
- `/notes/review/` - Example specifications in repository

---

**Template location**: `templates/plan_template.md` in skill directory (if available)
