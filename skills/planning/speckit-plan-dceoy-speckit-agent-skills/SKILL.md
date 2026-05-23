---
name: speckit-plan
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
allowed-tools: Bash, Read, Write, Grep, Glob
handoffs:
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
---

# Spec-Kit Plan

Generate comprehensive technical implementation plan from feature specification. Second step in spec-kit workflow.

## When to Use

- After creating spec.md with `speckit-specify`
- Need technical architecture and design
- Ready to plan implementation details

## Execution Workflow

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` to get FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH paths
2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`, load IMPL_PLAN template
3. **Execute plan workflow**:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - **Phase 0: Research** - Resolve all NEEDS CLARIFICATION before design
     - Extract unknowns from Technical Context
     - Research best practices for each unknown (web search, documentation)
     - Generate research.md with decision rationale and alternatives considered
     - **MUST complete Phase 0 before Phase 1**
   - **Phase 1: Design** - Generate technical artifacts
     - data-model.md: Extract entities from spec, define fields/relationships/validation
     - contracts/: Generate API contracts (OpenAPI/GraphQL) from functional requirements
     - quickstart.md: Create test scenarios and setup instructions
     - **Update agent context**: Run `.specify/scripts/bash/update-agent-context.sh claude`
       - Adds new technology from plan to agent-specific context
       - Preserves manual additions between markers
   - Re-evaluate Constitution Check post-design (verify no violations introduced)
4. **Report**: Command ends after planning. Report branch, IMPL_PLAN path, and generated artifacts

## Key Points

- Research unknowns thoroughly before design
- Document decision rationale (why chosen, alternatives considered)
- Design for testability following project conventions
- Avoid over-engineering - only what's needed
- Follow semantic versioning and architecture patterns
- Constitution check is non-negotiable - must align with principles
- Update agent-specific context files with new technology

## Next Steps

After creating plan.md:

- **Generate tasks** with `speckit-tasks`
- **Analyze** for consistency with `speckit-analyze`
- **Create checklist** for quality validation

## See Also

- `speckit-specify` - Create feature specifications
- `speckit-tasks` - Break plan into actionable tasks
- `speckit-analyze` - Validate cross-artifact consistency
- `speckit-checklist` - Generate custom validation checklists
