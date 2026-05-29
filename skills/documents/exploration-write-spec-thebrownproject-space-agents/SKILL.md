---
name: exploration-write-spec
description: "Produce structured spec.md from brainstorm conversations. Creates a consistent format that feeds cleanly into the planning phase."
---

# /exploration-write-spec - Spec Document Generator

Transform brainstorm conversations into structured spec documents. This skill produces consistent `spec.md` files that the planning phase can reliably parse.

## When to Use

Called at the end of `/brainstorm` when the user confirms they're ready to capture their exploration. Can also be invoked directly if you have a clear idea ready to document.

## The Process

1. **Gather context** - Review the brainstorm conversation (or get user input if invoked directly)
2. **Extract key elements** - Problem, solution, requirements, constraints
3. **Identify gaps** - Note any open questions that would block planning
4. **Write spec.md** - Use the template below
5. **Confirm output location** - Show user the file path

## Output

**Location:** `.space-agents/exploration/ideas/YYYY-MM-DD-<topic>/spec.md`

The spec file lives alongside any exploration notes in the same topic folder. This folder will later move to `planned/` when `/plan` processes it.

## spec.md Template

```markdown
# Exploration: [Topic Title]

**Date:** YYYY-MM-DD
**Status:** [Ready for planning | Needs discussion | Blocked]

---

## Problem

What problem are we solving? Why does this matter?

[1-3 paragraphs describing the problem, its impact, and why it needs solving]

---

## Solution

High-level approach. The "what" not the "how".

[Describe the solution at a conceptual level. Include diagrams/tables if they clarify the approach.]

---

## Requirements

Must-have functionality. Use checklist format for tracking.

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

---

## Non-Requirements

Explicitly out of scope. Prevents scope creep during planning.

- Not doing X
- Not changing Y
- Not supporting Z

---

## Architecture

Components, data flow, key technical decisions.

[Include diagrams, flow descriptions, component interactions. This section should give a developer enough context to understand how the pieces fit together.]

---

## Constraints

Technical limitations, patterns to follow, dependencies.

- [Constraint 1 - e.g., must work with existing API]
- [Constraint 2 - e.g., follow project naming conventions]
- [Constraint 3 - e.g., external dependency requirement]

---

## Success Criteria

How do we know it's done? Checklist format for verification.

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Open Questions

Things still to be decided. Unresolved questions may block planning.

1. [Question 1] - [Context/options if known]
2. [Question 2] - [Context/options if known]

---

## Next Steps

What happens after this exploration.

1. `/plan` to create implementation tasks
2. [Any specific preparatory work needed]
3. [Dependencies to resolve first]
```

## Section Guidelines

| Section | Purpose | Planning Impact |
|---------|---------|-----------------|
| **Problem** | Why are we doing this? | Guides priority decisions |
| **Solution** | What approach? | Shapes feature structure |
| **Requirements** | What must it do? | Becomes task acceptance criteria |
| **Non-Requirements** | What's out of scope? | Prevents scope creep |
| **Architecture** | How do pieces fit? | Informs task breakdown |
| **Constraints** | What limits us? | Affects implementation choices |
| **Success Criteria** | How do we verify? | Defines "done" for feature |
| **Open Questions** | What's unresolved? | Blocks planning if critical |
| **Next Steps** | What's next? | Guides user action |

## Status Values

- **Ready for planning** - All critical questions resolved, can proceed to `/plan`
- **Needs discussion** - Some open questions remain, but not blocking
- **Blocked** - Critical questions must be resolved before planning

## Tips

- Keep Problem and Solution sections concise - save details for Architecture
- Requirements should be testable - if you can't verify it, refine it
- Non-Requirements prevent future scope creep - be explicit
- Open Questions with no resolution path should set status to "Blocked"
- Success Criteria should map roughly to what the feature will deliver

## Folder Lifecycle

```
/brainstorm conversation
    |
    v
/exploration-write-spec creates:
    exploration/ideas/YYYY-MM-DD-<topic>/spec.md
    |
    v
/plan reads spec.md, creates plan.md, moves to:
    exploration/planned/YYYY-MM-DD-<topic>/
    |
    v
/plan creates Beads, moves to:
    mission/staged/YYYY-MM-DD-<topic>/
```
