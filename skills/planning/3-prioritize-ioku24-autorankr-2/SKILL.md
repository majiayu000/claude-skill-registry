---
name: prioritize
description: Prioritize tasks and issues to determine what to work on and in what order. Use after identification, when planning work, or when unsure what to do next. This is the third system in the 5-system framework.
---

# Priority System

> **Purpose:** Know what to do and in what order.
> **When to trigger:** After identification, when planning, or when facing multiple options.

## Prioritization Framework

### Step 1: Categorize by Impact

**Critical** - Immediate attention required

- Blocks users completely
- Causes data loss or corruption
- Security vulnerability
- Prevents revenue

**High** - Important, do soon

- Major UX degradation
- Key feature broken
- Significant performance issue
- Blocks other work

**Medium** - Should do

- Quality of life improvements
- Tech debt with growing cost
- Minor feature gaps
- Developer experience issues

**Low** - Nice to have

- Polish and refinement
- Minor optimizations
- Cosmetic improvements
- Future-proofing

### Step 2: Assess Effort

| Level      | Time      | Examples                                       |
| ---------- | --------- | ---------------------------------------------- |
| **Quick**  | < 30 min  | Fix typo, add missing null check, update copy  |
| **Small**  | < 2 hours | Add new component, fix bug with clear cause    |
| **Medium** | < 1 day   | New feature, refactor module, integration work |
| **Large**  | Multi-day | Major feature, architecture change, migration  |

### Step 3: Apply Priority Matrix

|              | Quick  | Small   | Medium  | Large        |
| ------------ | ------ | ------- | ------- | ------------ |
| **Critical** | DO NOW | DO NOW  | DO NOW  | Plan & Start |
| **High**     | DO NOW | Next    | Next    | Plan         |
| **Medium**   | Next   | Queue   | Queue   | Backlog      |
| **Low**      | Queue  | Backlog | Backlog | Skip/Defer   |

### Step 4: Check Dependencies

Before finalizing order:

1. What must happen before this task?
2. What does completing this unblock?
3. Are there resource constraints?
4. What's the cost of delay?

Reorder based on dependencies - a Medium task that unblocks 3 High tasks moves up.

### Step 5: Sequence for Flow

Group related work together:

- Fix all issues in one file before moving to the next
- Complete a feature end-to-end before starting another
- Address blocking issues before blocked ones

## Output Requirements

Update `SOURCE_OF_TRUTH.md` with prioritized list:

```markdown
## Current Priority Stack

### DO NOW (This Session)

1. [ ] [Critical/Quick] Fix auth crash on login - blocks all users
2. [ ] [Critical/Small] Patch XSS in comments - security issue

### NEXT (Soon)

3. [ ] [High/Small] Add error boundary to dashboard
4. [ ] [High/Medium] Implement retry logic for API calls

### QUEUE (This Week)

5. [ ] [Medium/Small] Refactor keyword fetching
6. [ ] [Medium/Medium] Add loading skeletons

### BACKLOG (Future)

7. [ ] [Low/Large] Rewrite onboarding flow
8. [ ] [Low/Medium] Add dark mode
```

Also create focused todo list using TodoWrite for the current session.

## Rules

1. **Impact over effort** - A critical issue is always more important than easy wins
2. **Dependencies first** - Unblock before building
3. **Be ruthless** - Not everything needs to be done now
4. **Revisit regularly** - Priorities change as context changes
5. **Limit WIP** - Maximum 2-3 items in "DO NOW" at once

## Decision Helpers

**When two items seem equal:**

- Which affects more users?
- Which has been waiting longer?
- Which aligns with current goal?
- Which reduces future work?

**When everything feels critical:**

- Step back and reassess with fresh eyes
- Ask: "What's the ONE thing that matters most right now?"
- Consider: What would a user notice first?

## Transition

After prioritization:

- Top priorities clear → Proceed to **Execution System**
- Blocked by unknowns → Return to **Clarity System**
- Need to understand issues better → Return to **Identity System**

---

_This is System 3 of 5: Clarity → Identity → Priority → Execution → Reset_
