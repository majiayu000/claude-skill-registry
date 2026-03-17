---
name: consistency-analysis
description: "Expertise in detecting inconsistencies, gaps, and conflicts across specification documents. Activates when user asks about document quality or consistency. Trigger keywords: consistency, analysis, gap analysis, conflict detection, spec review, cross-reference, traceability"
allowed-tools: Read, Glob, Grep
user-invocable: false
---

# Consistency Analysis Skill

## Purpose

This skill provides expertise in detecting inconsistencies, gaps, and conflicts across specification documents. It performs read-only cross-document analysis to ensure that requirements, tasks, data models, and plans are aligned and complete. The output is a structured analysis report with categorized findings and severity levels.

**IMPORTANT: This skill NEVER modifies files. It is strictly a read-only analysis tool.** All findings are reported for human review and resolution.

## When It Activates

The skill is triggered when the conversation involves:

- Reviewing specification quality or completeness
- Checking cross-document consistency (spec vs. tasks vs. plan)
- Detecting gaps in requirement coverage or task traceability
- Identifying conflicting definitions across documents
- Performing traceability analysis between artifacts

## Analysis Rule Categories

The skill evaluates documents against eight rule categories:

### 1. Requirement Coverage

Verify that every functional requirement (`FR-XXX`) and non-functional requirement (`NFR-XXX`) in the specification is addressed by at least one implementation task or plan item. Flag orphaned requirements with no downstream mapping.

### 2. Task Traceability

Ensure every task in `tasks.md` traces back to a specific requirement or user story in `spec.md`. Flag tasks with missing `[Spec §X.Y]` references or invalid reference targets.

### 3. Plan Alignment

Check that the implementation plan is consistent with the task list and specification. Detect mismatches in scope, ordering assumptions, or phase assignments between documents.

### 4. Data Model Consistency

Verify that entity definitions, field names, types, and relationships are consistent across the specification, data model section, and API contracts. Flag naming mismatches, type conflicts, or missing fields.

### 5. Contract Coverage

Ensure every API endpoint defined in the specification has corresponding tasks for implementation and testing. Flag endpoints missing from the task list or with incomplete request/response schema definitions.

### 6. Constitution Compliance

If a project constitution exists, verify that the specification and tasks comply with its architectural principles, technology constraints, and coding conventions.

### 7. Duplication Detection

Identify duplicate or near-duplicate requirements, tasks, or definitions across documents. Flag redundancies that may lead to conflicting implementations or wasted effort.

### 8. Ambiguity Detection

Scan for vague, unmeasurable, or subjective language in requirements (e.g., "fast," "user-friendly," "scalable"). Flag ambiguous terms that need quantification or clarification.

## Severity Classification

Each finding is assigned a severity level:

| Severity | Meaning | Action Required |
|----------|---------|-----------------|
| **CRITICAL** | Blocking issue that prevents correct implementation | Must resolve before proceeding |
| **HIGH** | Significant gap or conflict likely to cause defects | Should resolve before implementation |
| **MEDIUM** | Inconsistency that may cause confusion or rework | Resolve during implementation |
| **LOW** | Minor style or convention issue | Resolve at convenience |

## Report Output Format

The analysis report is structured as follows:

```markdown
# Consistency Analysis Report

## Summary
- Total findings: N
- Critical: N | High: N | Medium: N | Low: N

## Findings

### [CRITICAL] RC-001: FR-012 has no implementing task
- **Category**: Requirement Coverage
- **Location**: spec.md FR-012
- **Details**: Payment retry logic requirement has no corresponding task in tasks.md.
- **Recommendation**: Add a task in the Stories phase covering FR-012.

### [HIGH] TT-001: Task T008 references non-existent FR-099
- **Category**: Task Traceability
- **Location**: tasks.md T008
- **Details**: The [Spec FR-099] reference does not match any requirement.
- **Recommendation**: Correct the reference or add the missing requirement.
```

Each finding includes an ID, category, location, detailed description, and a recommended resolution.

## References

For detailed analysis rules, severity definitions, and configuration options, consult:

- `references/analysis-rules.md` -- Full rule definitions with detection logic for each category
- `references/severity-levels.md` -- Severity classification criteria and escalation guidelines
