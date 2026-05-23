---
name: issue-planning
description: Guide structured analysis of problems and planning of implementation. Use when starting work on a new feature, encountering a bug, refactoring existing functionality, or any task that benefits from thinking before coding. Helps create well-defined GitHub issues with clear scope, acceptance criteria, and implementation steps.
---

# Issue Analysis & Planning

This skill guides structured problem analysis and implementation planning before coding.

## Workflow Overview

```
1. Discovery        → Add summary to doc/plans/module_issues.md
2. Planning         → Create gi_draft_<module>_<desc>.md with detailed plan
3. Review           → Review plan with user, refine until ready
4. Publish          → User creates GitHub issue, rename file to gi_<id>_<desc>.md
5. Implementation   → Work on issue, PRs link automatically
6. Completion       → Close GitHub issue, update module_issues.md status
```

**Important**: This skill creates LOCAL draft files only. The user reviews and manually publishes to GitHub.

---

## Step 1: Problem Analysis

### 1.1 What is the current state?
- What exists now?
- What is the observed behavior?
- Where does this sit in the broader system?

### 1.2 What is the desired state?
- What should happen instead?
- Who benefits and how?
- What does "done" look like?

### 1.3 What is the gap?
- Why doesn't the current state meet the need?
- What's blocking progress?
- Are there dependencies or prerequisites?

### 1.4 What is the scope?
- What's included in this issue?
- What's explicitly excluded (for later)?
- What are the boundaries?

---

## Step 2: Problem Description

Write a clear, concise problem statement following this structure:

```
**Context:** [Where does this fit? What's the background?]

**Problem:** [What's wrong or missing? One or two sentences.]

**Impact:** [Why does this matter? Who is affected?]

**Desired outcome:** [What should be true when this is resolved?]
```

---

## Step 3: Implementation Planning

### 3.1 Approach options
List 2-3 possible approaches. For each:
- Brief description
- Pros
- Cons
- Rough effort estimate

### 3.2 Recommended approach
Select one approach and explain why.

### 3.3 Break into steps
List concrete implementation steps. Each step should be:
- Small enough to complete in one focused session
- Testable or verifiable
- Independent where possible

Example:
```
1. [ ] Create data model for X
2. [ ] Build function to fetch Y
3. [ ] Add validation for Z
4. [ ] Write tests for steps 1-3
5. [ ] Integrate with existing component W
```

### 3.4 Identify risks & unknowns
- What might go wrong?
- What do you need to learn or verify first?
- Are there external dependencies?

---

## Step 4: Create Local Issue File

### File naming

**Draft** (before GitHub publication):
```
doc/plans/issues/gi_draft_<module>_<short_description>.md
```

**Published** (after GitHub issue created):
```
doc/plans/issues/gi_<github_id>_<short_description>.md
```

### Module abbreviations

| Module | Abbreviation |
|--------|--------------|
| preprocessing_runoff | `prepq` |
| preprocessing_gateway | `prepg` |
| preprocessing_station_forcing | `prepf` |
| linear_regression | `lr` |
| machine_learning | `ml` |
| postprocessing_forecasts | `pp` |
| forecast_dashboard | `fd` |
| configuration_dashboard | `cd` |
| pipeline | `p` |
| iEasyHydroForecast | `iEHF` |
| reset_forecast_run_date | `r` |
| cross-module/infrastructure | `infra` |

### Issue file template

The issue file must be **standalone** — a junior developer should be able to implement it without access to the full project context.

```markdown
# <Title>

**Status**: Draft | Ready for Review | Published (GitHub #XX) | In Progress | Complete
**Module**: <module name>
**Priority**: Critical | High | Medium | Low
**Labels**: `<label1>`, `<label2>`

---

## Summary

[One sentence describing what this issue accomplishes]

## Context

[Background — why this matters, where it fits in the system. Include enough detail that someone unfamiliar with the project can understand.]

## Problem

[What's wrong or missing. Be specific about observed vs expected behavior.]

## Desired Outcome

[What "done" looks like — specific, verifiable criteria]

---

## Technical Analysis

### Current Implementation

[Describe relevant existing code. Include file paths and line numbers.]

**Key files:**
- `apps/<module>/path/to/file.py` - Description of what this file does
- `apps/<module>/path/to/other.py:123-145` - Specific function/section

### Root Cause

[For bugs: what is causing the issue. For features: what's missing.]

---

## Implementation Plan

### Approach

[Describe the chosen approach and why it was selected over alternatives.]

### Files to Create

| File | Purpose |
|------|---------|
| `path/to/new_file.py` | Description |

### Files to Modify

| File | Changes |
|------|---------|
| `path/to/existing.py` | Description of changes |

### Implementation Steps

- [ ] Step 1: [Specific, actionable task]
- [ ] Step 2: [Specific, actionable task]
- [ ] Step 3: [Specific, actionable task]

### Code Examples

[Include specific code snippets showing the expected implementation. This helps ensure consistency and reduces ambiguity.]

```python
# Example of new function signature
def new_function(param1: str, param2: int) -> dict:
    """
    Brief description.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value
    """
    pass
```

---

## Testing

### Test Cases

- [ ] Test case 1: [Description of what to test]
- [ ] Test case 2: [Description of what to test]

### Testing Commands

```bash
# How to run tests for this change
cd apps/<module>
uv run pytest tests/ -v -k "test_name"
```

### Manual Verification

[Steps to manually verify the fix/feature works]

---

## Out of Scope

[What this issue explicitly does NOT address — important for preventing scope creep]

## Dependencies

[Other issues, external factors, or prerequisites that must be completed first]

## Acceptance Criteria

- [ ] Criterion 1: [Specific, measurable]
- [ ] Criterion 2: [Specific, measurable]
- [ ] All existing tests pass
- [ ] New tests cover the changes
- [ ] Code follows project conventions (see `.serena/memories/code_style_conventions.md`)

---

## References

- Related issues: #XX, #YY
- Planning docs: `doc/plans/<related_doc>.md`
- External docs: [Link](url)
```

---

## Step 5: Update Issue Index

After creating the issue file, add an entry to `doc/plans/module_issues.md`:

```markdown
### Issue <MODULE>-NNN: [Brief title]
**Status**: Draft | Ready | In Progress | Complete
**Priority**: High | Medium | Low
**File**: `issues/gi_draft_<module>_<desc>.md`
**GitHub**: #XX (after publication)

[One-line description]
```

---

## Checklist Before Marking Ready for Review

- [ ] Problem is clearly understood and documented
- [ ] Scope is defined and bounded
- [ ] Technical analysis includes specific file paths and line numbers
- [ ] Implementation steps are small and testable
- [ ] Code examples show expected patterns
- [ ] Test cases are defined
- [ ] Acceptance criteria are specific and measurable
- [ ] A junior developer could implement this without asking questions
- [ ] Entry added to `doc/plans/module_issues.md`

---

## Tips

**Keep issues small.** If you have more than 5-7 implementation steps, consider splitting into multiple issues.

**Write for a junior developer.** Assume someone unfamiliar with the codebase will implement this. Include file paths, function names, and code examples.

**Define "done" precisely.** Vague outcomes lead to scope creep. "Works correctly" is not a criterion; "Returns valid JSON for all input cases in test suite" is.

**Surface unknowns early.** If something needs investigation, make that a separate spike issue rather than bundling it with implementation.

**Include code examples.** Showing the expected function signature, data structure, or pattern reduces ambiguity and speeds up implementation.

**Reference specific locations.** Use `file.py:123` format for line numbers so implementers can jump directly to relevant code.

---

## Related Skills

- **executing-issues**: Use to implement the issue once the plan is ready
- **brainstorming**: Use before planning if requirements are unclear
- **software-architecture**: Reference for code conventions