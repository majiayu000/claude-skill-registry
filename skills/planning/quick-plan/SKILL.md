---
name: quick-plan
description: This skill should be used when the user asks to "create a quick plan", "draft a plan", "capture this idea", "plan this feature", or wants a lightweight plan without full feature planning. Creates concise plans in backlog/plans/ for later expansion.
---
# Quick Plan

Create a lightweight plan document for: **$ARGUMENTS**

## Overview

This skill creates concise plan documents in `backlog/plans/` using the standard template. Suitable for:
- Capturing ideas quickly before context is lost
- Scoping small-to-medium features
- Creating starting points for later `/planner` expansion

For complex features requiring full analysis, spec, research, and TDD task breakdown, use `/planner` instead.

## Workflow

### Step 1: Generate Filename

Create filename using today's date and a slug derived from the input:
- Format: `YYYYMMDD-short-description.md`
- Example: `20260127-add-user-authentication.md`

### Step 2: Gather Context (Optional)

When input references existing code or systems:
- Briefly scan relevant files to understand current state
- Note obvious constraints or dependencies

Limit context gathering to under 2 minutes. Extensive research indicates `/planner` may be more appropriate.

### Step 3: Create Plan

Create the plan file at `backlog/plans/{filename}`:

```markdown
---
title: "{Descriptive title}"
status: open
priority: {low|medium|high|critical}
created: {YYYY-MM-DD}
---

# {Plan Title}

## Summary

{1-2 sentences describing what this plan achieves}

## Motivation

{Why is this needed? What problem does it solve? 2-3 sentences.}

## Proposal

### Goals

- {Primary goal}
- {Secondary goal if applicable}

### Non-Goals

- {What this explicitly does NOT cover}

## Design

{High-level approach in 3-5 sentences or bullet points. Include key technical decisions if obvious.}

## Tasks

- [ ] {Task 1}
- [ ] {Task 2}
- [ ] {Task 3}

## Open Questions

- {Any uncertainties requiring resolution}
```

### Step 4: Output Summary

After creating the plan:

```
Created: backlog/plans/{filename}

{title}
Priority: {priority}
Tasks: {count}

Next steps:
- Review and refine the plan
- Adjust priority if needed
- Expand with /planner if complexity warrants
- Or start implementation directly for simple plans
```

## Guidelines

| Guideline | Detail |
|-----------|--------|
| Concise | Quick capture, not exhaustive planning |
| Priority inference | Blocking issues = high, nice-to-have = low |
| Task count | 3-7 tasks; more than 7 suggests `/planner` |
| Optional sections | Omit "Open Questions" if none exist |
| Time limit | Context gathering under 2 minutes |
