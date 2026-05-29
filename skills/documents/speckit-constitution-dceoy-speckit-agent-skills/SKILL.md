---
name: speckit-constitution
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
handoffs:
  - label: Build Specification
    agent: speckit.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

# Spec-Kit Constitution

Create or update the project constitution with versioned principles and governance rules. Foundational step for spec-kit workflows.

## When to Use

- Starting a new project and defining principles
- Updating project values or governance rules
- Need to document non-negotiable project rules
- Before creating specs to ensure alignment with project values

## Execution Workflow

This updates the template at `.specify/memory/constitution.md` containing placeholder tokens `[ALL_CAPS_IDENTIFIER]`.

1. **Load existing constitution template** at `.specify/memory/constitution.md`
   - Identify every placeholder token `[ALL_CAPS_IDENTIFIER]`
   - User might require different number of principles than template - respect that
2. **Collect/derive values** for placeholders:
   - Use user input if supplied
   - Infer from repo context (README, docs, prior versions)
   - For dates: `RATIFICATION_DATE` (original adoption), `LAST_AMENDED_DATE` (today if changes made)
   - `CONSTITUTION_VERSION` increment by semantic versioning:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions
     - MINOR: New principle/section added or materially expanded guidance
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements
3. **Draft updated constitution**:
   - Replace every placeholder with concrete text (no bracketed tokens except intentionally retained with justification)
   - Preserve heading hierarchy
   - Each principle: succinct name, paragraph/bullets capturing non-negotiable rules, explicit rationale
   - Governance: amendment procedure, versioning policy, compliance review expectations
4. **Consistency propagation checklist**:
   - Read and update `.specify/templates/plan-template.md` (Constitution Check aligns with updated principles)
   - Read and update `.specify/templates/spec-template.md` (scope/requirements alignment)
   - Read and update `.specify/templates/tasks-template.md` (task categorization reflects new principle-driven types)
   - Read command files in `.specify/templates/commands/*.md` (verify no outdated references)
   - Read runtime docs (README.md, docs/quickstart.md, agent-specific guidance) - update principle references
5. **Produce Sync Impact Report** (prepend as HTML comment at top of constitution):
   - Version change: old → new
   - Modified principles (old title → new title if renamed)
   - Added/removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if placeholders intentionally deferred
6. **Validation before final output**:
   - No remaining unexplained bracket tokens
   - Version line matches report
   - Dates ISO format YYYY-MM-DD
   - Principles are declarative, testable, free of vague language
7. **Write completed constitution** back to `.specify/memory/constitution.md` (overwrite)
8. **Output final summary**:
   - New version and bump rationale
   - Files flagged for manual follow-up
   - Suggested commit message

## Key Points

- **Semantic versioning strictly enforced** (CONSTITUTION_VERSION):
  - **MAJOR (X.0.0)**: Backward incompatible governance/principle removals or redefinitions
  - **MINOR (0.X.0)**: New principle/section added or materially expanded guidance
  - **PATCH (0.0.X)**: Clarifications, wording, typo fixes, non-semantic refinements
  - **Always justify** version bump type with reasoning
- **Each principle requires** succinct name, description (MUST/SHOULD/MAY), explicit rationale
- **Sync all dependent templates** - plan, spec, tasks, commands
- **No unexplained placeholders** - justify any deferred items in sync report
- **Constitution is non-negotiable** - all specs/plans must align with principles
- **Version tracking** - each amendment adds entry to sync impact report

## Next Steps

After creating/updating constitution:

- **Specify** features with `speckit-specify` (aligned with principles)
- **Plan** implementations with `speckit-plan` (validates against constitution)
- **Review** existing specs for compliance with new principles

## See Also

- `speckit-specify` - Create feature specifications
- `speckit-plan` - Build implementation plans
