---
name: structured-output
description: 'Consult this skill when formatting final review deliverables. Use when
  formatting final review outputs, ensuring consistent deliverable structure, making
  findings comparable across reviews. Do not use when capturing evidence during analysis
  - use evidence-logging. DO NOT use when: reviewing changes - use diff-analysis or
  review-core first.'
category: output-patterns
tags:
- formatting
- deliverables
- consistency
- reporting
- structure
dependencies:
- imbue:evidence-logging
tools: []
usage_patterns:
- deliverable-formatting
- report-structure
- consistent-output
complexity: beginner
estimated_tokens: 1000
---
## Table of Contents

- [When to Use](#when-to-use)
- [Activation Patterns](#activation-patterns)
- [Required TodoWrite Items](#required-todowrite-items)
- [Step 1: Select Template (`structured-output:template-selected`)](#step-1:-select-template-(structured-output:template-selected))
- [Step 2: Format Findings (`structured-output:findings-formatted`)](#step-2:-format-findings-(structured-output:findings-formatted))
- [Step 3: Assign Actions (`structured-output:actions-assigned`)](#step-3:-assign-actions-(structured-output:actions-assigned))
- [Step 4: Attach Appendix (`structured-output:appendix-attached`)](#step-4:-attach-appendix-(structured-output:appendix-attached))
- [Output Quality Checklist](#output-quality-checklist)
- [Exit Criteria](#exit-criteria)


# Structured Output

## When To Use
- When finalizing any review or analysis.
- To format findings in a consistent and actionable way.
- Before presenting results to stakeholders or committing them to documentation.

## When NOT To Use

- Capturing evidence during analysis - use evidence-logging
- Reviewing changes - use diff-analysis or review-core first

## Activation Patterns
**Trigger Keywords**: format, structure, deliverable, report, organize, present, consistent
**Contextual Cues**:
- "format this as a report" or "structure the output"
- "create a deliverable" or "present these findings"
- "organize this consistently" or "standardize the format"
- "make this actionable" or "prepare for stakeholders"

**Auto-Load When**: Finalizing any analysis deliverable or when consistent formatting is requested.

## Required TodoWrite Items
1. `structured-output:template-selected`
2. `structured-output:findings-formatted`
3. `structured-output:actions-assigned`
4. `structured-output:appendix-attached`

Mark each item complete as you finish the corresponding step.

## Step 1: Select Template (`structured-output:template-selected`)
- Choose output format based on deliverable type:
  - **Review Report**: Summary, Findings, Recommendations, Evidence.
  - **PR Description**: Summary, Changes, Test Plan, Notes.
  - **Release Notes**: Highlights, Breaking Changes, Fixes, Credits.
  - **Incident Report**: Timeline, Impact, Root Cause, Remediation.
- Confirm audience and required detail level.

## Step 2: Format Findings (`structured-output:findings-formatted`)
- Use consistent finding structure:
  ```markdown
  ### [SEVERITY] Finding Title
  **Location**: file.rs:123
  **Category**: Security | Performance | Correctness | Style
  **Description**: Brief explanation of the issue.
  **Evidence**: [E1, E2] - Reference to evidence log.
  **Recommendation**: Specific remediation steps.
  ```
  **Verification:** Run the command with `--help` flag to verify availability.
- Severity levels: CRITICAL, HIGH, MEDIUM, LOW, INFO.
- Order findings by severity, then by file location.

## Step 3: Assign Actions (`structured-output:actions-assigned`)
- Convert findings to actionable items:
  ```markdown
  ## Action Items
  - [ ] [HIGH] Fix SQL injection in auth.py:45 (@security-team, P1)
  - [ ] [MEDIUM] Add input validation to API endpoint (@backend, P2)
  - [ ] [LOW] Update deprecated dependency (@devops, P3)
  ```
  **Verification:** Run the command with `--help` flag to verify availability.
- Include owner assignment where known.
- Add priority indicators (P1/P2/P3) for triage.
- Note dependencies between actions.

## Step 4: Attach Appendix (`structured-output:appendix-attached`)
- Compile supporting materials:
  ```markdown
  ## Appendix
  ### A. Commands Run
  [Full evidence log from imbue:evidence-logging]

  ### B. External References
  [Citations and documentation links]

  ### C. Raw Data
  [Large outputs, full diffs, or data exports]
  ```
  **Verification:** Run the command with `--help` flag to verify availability.
- Keep main report concise; details in appendix.
- validate appendix is navigable with clear section headers.

## Output Quality Checklist
Before finalizing:
- [ ] All findings have evidence references.
- [ ] Severity levels are justified.
- [ ] Recommendations are specific and actionable.
- [ ] No orphaned sections or placeholder text.
- [ ] Format renders correctly in target medium (GitHub, Confluence, etc.).

## Exit Criteria
- Todos completed with formatted deliverable.
- Output follows selected template structure.
- Stakeholders can act on findings without clarification.
## Troubleshooting

### Common Issues

**Command not found**
Ensure all dependencies are installed and in PATH

**Permission errors**
Check file permissions and run with appropriate privileges

**Unexpected behavior**
Enable verbose logging with `--verbose` flag
