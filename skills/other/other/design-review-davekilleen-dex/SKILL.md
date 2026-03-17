---
name: design-review
description: Prepare for or document design review
role_groups: [design, product]
jtbd: |
  Design reviews need context and decisions get lost. This gathers project context 
  and requirements, surfaces customer feedback related to design, prompts for key 
  decisions and rationale, and documents outcomes so design choices are preserved.
time_investment: "20-30 minutes per review"
---

## Purpose

Prepare for design reviews or document design decisions with full context.

## Usage

- `/design-review [project]` - Review for specific project

---

## Steps

1. **Gather project context:**
   - Search 04-Projects/ for project file
   - User stories and requirements
   - Technical constraints

2. **Surface relevant feedback:**
   - Customer feedback on current design
   - Usability issues reported
   - Competitive design references

3. **Prompt for design decisions:**
   - What options were considered?
   - Why this approach?
   - What user needs does it solve?

4. **Document review outcomes:**
   - Decisions made
   - Feedback received
   - Next steps

---

## Output Format

```markdown
# Design Review: [Project]

**Date:** [Today]
**Participants:** [Names]

## Context
[Project background and requirements]

## Design Decisions

### [Decision 1]
- **Options considered:** [List]
- **Choice:** [Selected option]
- **Rationale:** [Why]

## User Feedback Considered
- [Feedback point 1]

## Next Steps
- [ ] [Action 1] - Owner: [Name]
```
