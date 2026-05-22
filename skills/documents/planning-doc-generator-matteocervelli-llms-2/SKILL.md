---
name: planning-doc-generator
description: Generate project assessment markdown documents from JSON data with WHY/WHO/WHAT
  sections and GO/NO-GO decision matrix.
allowed-tools: Read, Write, Edit
---

# Planning Document Generator Skill

## Purpose

Generate structured assessment documents from JSON configuration. Converts project planning data into markdown assessment reports with purpose, stakeholder, and scope analysis plus a GO/NO-GO decision framework.

## When to Use

- Creating project assessment documents
- Generating planning documentation from structured data
- Building evaluation reports with decision matrices
- Documenting project vision and scope
- Creating stakeholder alignment assessments
- Generating baseline project documentation

## Input: JSON Format

The skill expects JSON input with the following structure:

```json
{
  "project_name": "Project Name",
  "date": "2025-11-03",
  "why": {
    "exists": "Why does this project exist?",
    "problem": "What problem does it solve?",
    "vision": "What is the desired outcome?"
  },
  "who": {
    "stakeholders": "List of key stakeholders",
    "decision_makers": "Who decides",
    "executors": "Who does the work",
    "concerns": "Their priorities and concerns"
  },
  "what": {
    "building": "What are we building/changing?",
    "features": "Key features and components",
    "out_of_scope": "What is out of scope",
    "success_criteria": "Definition of success"
  },
  "go_no_go": {
    "purpose_clarity": "✓|⚠|✗",
    "stakeholder_alignment": "✓|⚠|✗",
    "scope_definition": "✓|⚠|✗",
    "resource_availability": "✓|⚠|✗",
    "timeline_feasibility": "✓|⚠|✗",
    "risk_assessment": "✓|⚠|✗",
    "success_metrics": "✓|⚠|✗"
  },
  "decision": "GO|CONDITIONAL|NO-GO",
  "rationale": "Explanation of decision"
}
```

## Template Filling Process

1. **Load** `templates/assessment-template.md`
2. **Replace** all `{PLACEHOLDER}` values with JSON data
3. **Calculate** coverage: Count non-empty answers ÷ 17 questions
4. **Insert** status indicators (✓/⚠/✗) from GO/NO-GO section
5. **Generate** markdown with formatted decision matrix
6. **Validate** all sections populated with content (no {ANSWER} remaining)

## Coverage Calculation

Total question count: **17**

**Breakdown:**
- WHY section: 3 questions
- WHO section: 4 questions
- WHAT section: 4 questions
- GO/NO-GO section: 7 assessment items
- Other: 1 additional (missing info summary)

**Formula:**
```
Coverage = (Number of answered/populated fields ÷ 17) × 100
Percentage = Round to nearest whole number
```

## Output Location

Generated documents save to:
```
~/docs/planning/{project_slug}/assessment-{date}.md
```

Example:
```
~/docs/planning/project-name/assessment-2025-11-03.md
```

## Workflow

```
JSON Input
    ↓
Load Template
    ↓
Replace Placeholders
    ↓
Calculate Coverage
    ↓
Format Decision Matrix
    ↓
Validate Completeness
    ↓
Write to ~/docs/planning/
    ↓
Markdown Output
```

## Key Features

### Status Indicators
- ✓ **Green**: Ready to proceed
- ⚠ **Yellow**: Proceed with caution / clarification needed
- ✗ **Red**: Blocker / do not proceed

### Decision Framework
- **GO**: All indicators green, proceed immediately
- **CONDITIONAL GO**: Some yellow flags, proceed with mitigation
- **NO-GO**: Red flags present, do not proceed without resolution

### Coverage Tracking
Automatically calculates and displays:
- Number of questions answered (X/17)
- Percentage coverage
- List of missing information

## Best Practices

1. **Complete All Fields**: Aim for 100% coverage (17/17)
2. **Be Specific**: Use concrete details, not generic placeholders
3. **Stakeholder Buy-in**: Ensure WHO section reflects actual decision-makers
4. **Realistic Assessment**: Be honest in GO/NO-GO evaluation
5. **Document Decisions**: Clear rationale essential for tracking

## Example Usage

```bash
# Command-line usage
planning-doc-generator \
  --input project-plan.json \
  --output ~/docs/planning/myproject/

# Result
~/docs/planning/myproject/assessment-2025-11-03.md
```

## Integration Points

### Input Sources
- Project planning worksheets (converted to JSON)
- Kickoff meeting notes (structured into JSON)
- Requirements documents (parsed to JSON format)
- Stakeholder surveys (aggregated to JSON)

### Output Consumers
- Project stakeholders (for review/approval)
- Project managers (for tracking)
- Decision makers (for GO/NO-GO calls)
- Documentation archives (for reference)

## Validation Rules

Before writing output file:
- All {PLACEHOLDER} values replaced
- No {ANSWER} tokens remaining
- Project name populated
- Date populated (YYYY-MM-DD format)
- Decision field contains valid value (GO, CONDITIONAL, NO-GO)
- Coverage calculated and accurate

---

**Version:** 1.0.0
**Created:** 2025-11-03
**Scope:** Global utility skill