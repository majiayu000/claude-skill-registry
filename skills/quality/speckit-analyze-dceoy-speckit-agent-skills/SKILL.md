---
name: speckit-analyze
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
allowed-tools: Bash, Read, Grep, Glob
---

# Spec-Kit Analyze

Cross-artifact consistency and quality analysis for feature specifications. Validation step after creating tasks.md.

## When to Use

- After creating tasks.md with `speckit-tasks`
- Before starting implementation with `speckit-implement`
- Need to identify gaps or conflicts before coding

## Execution Workflow

**STRICTLY READ-ONLY** - Does not modify any files.

1. **Initialize analysis context**: Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` to get FEATURE_DIR and AVAILABLE_DOCS. Derive paths:
   - SPEC = FEATURE_DIR/spec.md
   - PLAN = FEATURE_DIR/plan.md
   - TASKS = FEATURE_DIR/tasks.md
   - CONSTITUTION = .specify/memory/constitution.md
2. **Load artifacts** (progressive disclosure - minimal context):
   - From spec.md: Overview, Functional Requirements, Non-Functional Requirements, User Stories, Edge Cases
   - From plan.md: Architecture/stack choices, Data Model references, Phases, Technical constraints
   - From tasks.md: Task IDs, Descriptions, Phase grouping, Parallel markers `[P]`, File paths
   - From constitution.md: Project principles, MUST/SHOULD requirements
3. **Build semantic models** (internal representations):
   - Requirements inventory with stable keys
   - User story/action inventory with acceptance criteria
   - Task coverage mapping (maps tasks to requirements)
   - Constitution rule set (principle names and normative statements)
4. **Detection passes** (maximum 50 findings total - aggregate overflow):
   - **Duplication**: Near-duplicate requirements, lower-quality phrasing
   - **Ambiguity**: Vague adjectives (fast, scalable, secure, intuitive, robust), unresolved placeholders (TODO, ???, `<placeholder>`)
   - **Underspecification**: Requirements missing object/outcome, user stories missing acceptance criteria, tasks referencing undefined files
   - **Constitution Alignment**: Conflicts with MUST principles (ALWAYS CRITICAL), missing mandated sections/gates
   - **Coverage Gaps**: Requirements with zero tasks, tasks with no mapped requirement, missing non-functional task coverage
   - **Inconsistency**: Terminology drift, data entities in plan but not spec, task ordering contradictions, conflicting requirements
5. **Severity assignment**:
   - CRITICAL: Violates constitution MUST, missing core spec artifact, requirement with zero coverage blocking baseline
   - HIGH: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
   - MEDIUM: Terminology drift, missing non-functional task coverage, underspecified edge case
   - LOW: Style/wording improvements, minor redundancy
6. **Produce compact analysis report** (Markdown, no file writes):
   - Findings table: ID, Category, Severity, Location(s), Summary, Recommendation
   - Coverage summary: Requirement → Tasks mapping
   - Constitution alignment issues table
   - Unmapped tasks table
   - Metrics: Total requirements, total tasks, coverage %, ambiguity count, duplication count, critical/high/medium/low issues
7. **Next actions**:
   - If CRITICAL: Must resolve before implementation
   - If only LOW/MEDIUM: May proceed with improvements recommended
   - Provide explicit command suggestions
8. **Offer remediation**: Ask if user wants concrete edit suggestions (not applied automatically)

## Key Points

- **NEVER modify files** - read-only analysis
- **Constitution violations are ALWAYS CRITICAL** - non-negotiable
- **Progressive disclosure** - load artifacts incrementally, don't dump all content
- **Token-efficient output** - tables over prose, limit to 50 findings, aggregate overflow
- **Deterministic results** - rerunning without changes produces consistent IDs and counts
- **Coverage % guidelines**:
  - 100%: Perfect (rare)
  - 80-99%: Excellent
  - 60-79%: Good (review gaps)
  - < 60%: Poor (significant gaps)
- **Report zero issues gracefully** - emit success report with coverage statistics

## Next Steps

After analysis:

- **Fix CRITICAL** - Update spec/plan/tasks
- **Start implementation** - Use `speckit-implement`
- **Re-analyze** - After fixes to verify

## See Also

- `speckit-plan` - Create technical implementation strategy
- `speckit-tasks` - Break plan into actionable tasks
- `speckit-implement` - Execute implementation plan
