---
name: analysis-phase
description: Validates cross-artifact consistency and detects breaking changes during feature analysis. Use when running /analyze command, validating spec-plan alignment, checking task-implementation consistency, or identifying API/database/UI breaking changes before deployment. (project)
allowed-tools: Read, Edit, Grep, Bash
---

<objective>
Validates cross-artifact consistency and detects breaking changes during the /analyze phase. Ensures spec requirements align with plan components, tasks match implementation, and breaking changes are identified before deployment.
</objective>

<quick_start>
Validate cross-artifact consistency and detect breaking changes:

1. Check spec → plan → tasks alignment
2. Detect breaking changes (API, database, UI, auth)
3. Validate dependencies
4. Generate analysis-report.md with findings

**Inputs**: spec.md, plan.md, tasks.md
**Outputs**: analysis-report.md
</quick_start>

<workflow>
<step number="1">
**Check spec-plan consistency**

Read spec.md requirements, verify each has corresponding plan component. Flag missing mappings in analysis report.

See references/examples.md for grep commands.
</step>

<step number="2">
**Verify task-implementation alignment**

Read plan.md components, verify each broken into tasks in tasks.md.

Validate:

- Each plan component has ≥1 task
- Task acceptance criteria match spec success criteria
- No orphaned tasks (tasks without plan component)
  </step>

<step number="3">
**Detect breaking changes**

Scan for patterns indicating breaking changes:

- **API changes**: Endpoint signature modifications, required parameter additions, response format changes
- **Database changes**: Schema modifications, required field additions, migrations affecting existing data
- **UI changes**: Component interface changes, prop requirement additions
- **Auth changes**: Permission model modifications, authentication flow changes

Flag with impact level (Low/Medium/High) using reference rubric.
</step>

<step number="4">
**Validate dependencies**

Cross-reference:

- Imports and integrations mentioned in plan
- External dependencies in tasks
- Integration points in spec

Verify all dependencies documented and accounted for.
</step>

<step number="5">
**Generate analysis report**

Create specs/NNN-slug/analysis-report.md:

```markdown
# Analysis Report

## Consistency Check

- Spec-Plan: [✓/✗] Description
- Plan-Tasks: [✓/✗] Description

## Breaking Changes

- [High/Medium/Low] Description and impact

## Dependency Validation

- [✓/✗] Dependencies documented

## Recommendations

- Action items to fix inconsistencies
```

Update state.yaml: `analysis.status = completed`
</step>
</workflow>

<validation>
After analysis, verify:

- All spec requirements have plan component coverage
- All plan components have task breakdown
- Breaking changes flagged with impact level (Low/Medium/High)
- Analysis report generated with actionable findings
- No orphaned artifacts (tasks without plan, plan without spec)
  </validation>

<anti_patterns>
<pitfall name="missing_breaking_changes">
**❌ Don't**: Assume no breaking changes without scanning
**✅ Do**: Explicitly check API signatures, database schema, required fields, auth changes

**Why**: Breaking changes missed in analysis cause production issues post-deployment
</pitfall>

<pitfall name="inconsistent_artifacts">
**❌ Don't**: Assume spec and plan are aligned
**✅ Do**: Explicitly validate each spec requirement has corresponding plan component

**Why**: Missing mappings lead to incomplete implementation
</pitfall>

<pitfall name="no_cross_reference">
**❌ Don't**: Skip dependency validation
**✅ Do**: Cross-reference all imports, integrations, external dependencies

**Why**: Undocumented dependencies cause integration failures
</pitfall>

<pitfall name="vague_findings">
**❌ Don't**: Write vague findings like "inconsistencies found"
**✅ Do**: Specify exact artifacts, line numbers, and recommended fixes

**Why**: Actionable findings enable quick remediation
</pitfall>
</anti_patterns>

<success_criteria>

- [ ] All spec requirements mapped to plan components (no gaps)
- [ ] All plan components broken into tasks (no orphans)
- [ ] Breaking changes documented with impact level (High/Medium/Low)
- [ ] Dependencies validated and documented
- [ ] analysis-report.md generated with actionable findings
- [ ] state.yaml updated (analysis.status = completed)
      </success_criteria>

<references>
See references/ for:
- Cross-artifact consistency matrix
- Breaking change detection patterns
- Impact assessment rubric
- Real-world analysis examples
</references>
