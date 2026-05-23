---
name: story
description: Break PBIs into user stories using vertical slicing and INVEST criteria. Use when creating user stories from PBIs, slicing features, or breaking down requirements. Triggers on keywords like "user story", "create stories", "slice pbi", "story breakdown", "vertical slice".
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite
---

# User Story Creation

Break Product Backlog Items into implementable user stories.

## When to Use
- PBI ready for story breakdown
- Feature needs vertical slicing
- Creating sprint-ready work items

## Quick Reference

### Workflow
1. Read PBI artifact and acceptance criteria
2. Identify vertical slices (end-to-end functionality)
3. Apply INVEST criteria to each story
4. Create user stories with GIVEN/WHEN/THEN
5. Save to `team-artifacts/pbis/stories/`
6. Suggest next: `/test-spec` or `/design-spec`

### INVEST Criteria
- **I**ndependent: No dependencies on other stories
- **N**egotiable: Details can change
- **V**aluable: Delivers user value
- **E**stimable: Can estimate effort
- **S**mall: Completable in sprint
- **T**estable: Clear acceptance criteria

### Output
- **Path:** `team-artifacts/pbis/stories/{YYMMDD}-us-{slug}.md`
- **Format:** As a {role}, I want {goal}, so that {benefit}

### Related
- **Role Skill:** `business-analyst`
- **Command:** `/story`
- **Input:** `/refine` output
- **Next Step:** `/test-spec`, `/design-spec`

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
