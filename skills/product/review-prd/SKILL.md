---
name: review-prd
description: Review a PRD for completeness, quality, and actionability
---

# Review PRD Skill

Review a Product Requirements Document for completeness, measurability, and implementation readiness.

## Arguments

The user provides a PRD path or number. If not given, ask which PRD to review.

## Workflow

1. **Locate PRD**: Find the PRD file (check `wiki/inbox/`, `wiki/active/`, `wiki/completed/`)
2. **Read PRD**: Read the full document
3. **Run checklist**: Evaluate each section against the criteria below
4. **Report findings**: Output a structured review with pass/fail per section
5. **Suggest improvements**: Provide specific, actionable feedback

## Review Checklist

### Metadata

- [ ] PRD ID is set and unique
- [ ] Title is concise and descriptive
- [ ] Status matches the directory location
- [ ] Dependencies reference valid PRD IDs
- [ ] Blocks field lists downstream PRDs

### Section 1: Problem Statement

- [ ] Clearly states the pain point
- [ ] Explains why it matters (impact)
- [ ] Not a solution disguised as a problem

### Section 2: Success Criteria

- [ ] Uses a table format
- [ ] Each criterion is measurable (number, yes/no, specific outcome)
- [ ] Includes measurement method
- [ ] Includes target value

### Section 3: Scope

- [ ] In Scope is specific (not vague)
- [ ] Out of Scope explicitly excludes related work
- [ ] Assumptions are stated and reasonable

### Section 4: System Context

- [ ] Dependency diagram exists
- [ ] "Depends On" table lists upstream components
- [ ] "Consumed By" table lists downstream consumers

### Section 5: Technical Design

- [ ] Data model defined (if applicable)
- [ ] Architecture decisions documented with rationale
- [ ] API contracts specified (inputs, outputs)
- [ ] File structure listed

### Section 6: Implementation Plan

- [ ] Task table has all columns (Task #, Description, Estimate, Dependencies, Claude Code Candidate, Notes)
- [ ] Tasks are ordered by dependency
- [ ] Estimates use t-shirt sizes
- [ ] Claude Code candidates have annotation blocks
- [ ] Each annotation has: Context needed, Constraints, Done state, Verification command

### Section 7: Testing Strategy

- [ ] Test pyramid covers unit, integration, E2E
- [ ] Key test scenarios are listed
- [ ] Matches test patterns from CLAUDE.md

### Section 8: Non-Functional Requirements

- [ ] Table format with Requirement, Target, How Verified
- [ ] Performance targets are specific
- [ ] Security considerations included

### Section 9: Rollout & Migration

- [ ] Deployment steps are listed
- [ ] Rollback plan exists

### Section 10: Open Questions

- [ ] Uses table format
- [ ] Each question has impact and owner
- [ ] No blockers remain unresolved for active PRDs

### Section 11: Revision History

- [ ] At least one entry (initial version)

## Output Format

```markdown
## PRD Review: PRD-NNN — Title

### Overall: PASS / NEEDS WORK / FAIL

| Section              | Status    | Notes |
| -------------------- | --------- | ----- |
| Metadata             | PASS/FAIL | ...   |
| 1. Problem Statement | PASS/FAIL | ...   |
| ...                  | ...       | ...   |

### Key Issues

1. [Issue description and suggested fix]
2. ...

### Strengths

1. [What's done well]
```
