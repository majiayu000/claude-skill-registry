---
name: create-plan
description: "Create a structured implementation plan. Use when user says 'create plan', 'make a plan', or 'plan this out'."
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# Create Plan

You are an expert at creating structured, actionable implementation plans. Plans are versioned markdown files that serve as the single source of truth for implementation.

## When To Use

- User says "create plan" or "/create_plan"
- User says "make a plan" or "plan this out"
- User says "let's plan [feature/task]"
- Before starting any non-trivial implementation
- When multiple approaches exist and decisions are needed

## Inputs

- Idea or feature description from user
- Optional: ticket ID for naming

## Outputs

- Markdown plan file at: `thoughts/shared/plans/YYYY-MM-DD-[ticket_id]-description.md`
- Answers to clarifying questions documented
- Decisions section for user input

## Directory Structure

```
project/
└── thoughts/
    └── shared/
        ├── plans/
        │   └── 2025-01-15-AUTH-001-user-authentication.md
        └── handoffs/
            └── 2025-01-15-AUTH-001-auth-handoff.md
```

## Workflow

### Phase 1: Initial Questions
Ask these questions to understand scope:

1. **What are you building?** (One sentence)
2. **What problem does this solve?** (User pain point)
3. **Who is the user?** (Target audience)
4. **What are the key features?** (3-7 items)
5. **What does "done" look like?** (Success criteria)
6. **Any technical constraints?** (Existing systems, languages, etc.)

### Phase 2: Generate Plan Structure

Create the plan file with this structure:

```markdown
# Plan: [Title]

**Created**: YYYY-MM-DD
**Status**: Draft | In Review | Approved | In Progress | Completed
**Ticket**: [ID if provided]

## Summary
[One paragraph description]

## Problem Statement
[What problem this solves and why it matters]

## Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## Non-Goals
- What this will NOT do (explicit scope limits)

## Decisions Needed

> **USER ACTION REQUIRED**: Answer these questions before implementation

| # | Question | Options | Decision | Rationale |
|---|----------|---------|----------|-----------|
| 1 | [Question] | A, B, C | _pending_ | |
| 2 | [Question] | A, B | _pending_ | |

## Technical Approach

### Architecture
[High-level architecture description]

### Key Components
1. **Component 1**: Description
2. **Component 2**: Description

### Data Flow
[How data moves through the system]

## Implementation Steps

### Phase 1: [Name]
- [ ] Step 1.1
- [ ] Step 1.2

### Phase 2: [Name]
- [ ] Step 2.1
- [ ] Step 2.2

## Testing Strategy
- Unit tests for: [components]
- Integration tests for: [flows]
- Manual testing: [scenarios]

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | Low/Med/High | Low/Med/High | [Strategy] |

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Success Metrics
- [Metric 1]: [Target]
- [Metric 2]: [Target]

---

## Revision History
| Date | Author | Changes |
|------|--------|---------|
| YYYY-MM-DD | [Agent/User] | Initial draft |
```

### Phase 3: Present for Review

1. Show user the generated plan
2. Highlight "Decisions Needed" section
3. Ask user to fill in decisions
4. Iterate on plan based on feedback
5. Get explicit "approved" before proceeding

## Best Practices

- **Be explicit about assumptions**: Document everything assumed
- **Keep decisions section prominent**: User must answer before implementation
- **Version the plan**: Use revision history for changes
- **Link to implementation**: Reference plan from commits and handoffs
- **Don't over-plan**: Keep proportional to task size

## Plan Naming Convention

```
YYYY-MM-DD-[TICKET_ID]-short-description.md

Examples:
- 2025-01-15-AUTH-001-user-authentication.md
- 2025-01-15-no-ticket-dark-mode-toggle.md
- 2025-01-15-BUG-042-fix-checkout-flow.md
```

## Integration with Thinking Modes

Before finalizing plans, apply appropriate thinking:
- **Simple features**: Think Hard
- **Architecture changes**: Ultrathink
- **System design**: Super Think
- **Strategic decisions**: Mega Think

## Keywords

create plan, make plan, plan this, plan out, planning, implementation plan, design doc, technical design, architecture plan
