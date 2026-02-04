---
name: spec-specify
description: Create or update a feature specification from a natural language description. Use when user says "/spec-specify", "create a spec", "write a specification", "I want to build...", or describes a new feature to implement. This is the FIRST step in the Spec-Driven Development workflow.
---

# Spec-Specify

Create feature specifications from natural language descriptions.

**Prerequisites**: Project must have `.specify/` directory. See `specify-resources` skill for setup.

## Workflow

1. **Parse input** - Extract feature description
2. **Generate branch name** - Create 2-4 word short name (e.g., "user-auth")
3. **Check existing branches** - Find highest feature number
4. **Create feature** - Run `.specify/scripts/bash/create-new-feature.sh --json "description" --short-name "name" --number N`
5. **Load template** - Read `.specify/templates/spec-template.md`
6. **Generate spec** - Fill with user stories, requirements, success criteria
7. **Validate** - Create checklist at `FEATURE_DIR/checklists/requirements.md`
8. **Report** - Output branch name, spec path, next steps

## Script Usage

```bash
.specify/scripts/bash/create-new-feature.sh --json "Feature description" --short-name "feature-name" --number N
```

Output: `{"BRANCH_NAME":"004-feature-name","SPEC_FILE":"/path/to/spec.md","FEATURE_NUM":"004"}`

## Spec Guidelines

### Content Rules
- Focus on WHAT users need, not HOW to implement
- No tech stack, APIs, or code structure
- Written for business stakeholders
- Maximum 3 `[NEEDS CLARIFICATION]` markers

### User Stories
- Independently testable (P1, P2, P3...)
- Include Given/When/Then scenarios
- Each can be an MVP increment

### Success Criteria
- Measurable metrics
- Technology-agnostic
- User-focused outcomes

## Next Steps

After `/spec-specify`:
- `/spec-clarify` - Reduce ambiguity
- `/spec-plan` - Create technical plan
