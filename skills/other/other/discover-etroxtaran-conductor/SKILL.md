---
name: discover
tags:
  technology: [python, typescript, javascript]
  feature: [workflow, documentation]
  priority: high
summary: Read product and technical docs to summarize requirements and identify gaps
version: 1
---

# Discover

## When to use

- Starting a new project or feature
- Requirements are spread across multiple documents
- Need to understand the full scope before planning

## Instructions

1. Read docs in this order:
   - `Docs/**/*.md` (or `Documents/`)
   - `docs/**/*.md`
   - root `PRODUCT.md` / `README.md`

2. Summarize the following:
   - **What we're building**: Core functionality and features
   - **Why (problem statement)**: Business need or user pain point
   - **Acceptance criteria**: Clear definition of done
   - **Constraints**: Technical, time, or resource limitations

3. Ask 1–3 targeted questions if critical info is missing:
   - Focus on blockers that prevent planning
   - Be specific about what information is needed
   - Suggest possible answers if you have assumptions

## Output Format

```markdown
## Discovery Summary

### What We're Building
[Description]

### Problem Statement
[Why this is needed]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Constraints
- [List constraints]

### Questions (if any)
1. [Specific question]
```
