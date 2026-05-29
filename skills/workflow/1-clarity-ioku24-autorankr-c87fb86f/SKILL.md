---
name: clarity
description: Establish clarity before starting work. Use when beginning any significant task, when input is vague or stream-of-consciousness, or when requirements seem unclear. Handles messy voice input efficiently. This is the first system in the 5-system framework.
---

# Clarity System

> **Purpose:** Never start significant work without shared understanding.
> **When to trigger:** Beginning any task, feature, fix, or when confusion arises.

---

## Messy Input Protocol (Token-Efficient)

**When to use:** Only when input is vague, stream-of-consciousness, or unclear.
**When to skip:** If the request is already clear, go straight to execution.

### The Process

1. **Listen fully** - Let the user finish their thought
2. **Extract core intent** in 2-3 lines max:
   ```
   WHAT: [one line]
   WHY: [one line, if apparent]
   SCOPE: [brief bounds, if mentioned]
   ```
3. **Confirm briefly:** "Is that right?"
4. **If gaps exist:** Ask 1-2 specific questions (not a list of 10)
5. **Once confirmed:** Execute immediately - don't over-document

### Example

```
User: "I want to like... maybe add something where users can
      see their stuff performing, you know what I mean?"

Claude: "Got it:
        WHAT: Add performance metrics for articles
        WHY: Users want to see if content is working

        Should this use GSC data or something else?"

User: "Yeah GSC"

Claude: [Executes - no further ceremony needed]
```

### Efficiency Rules

- **Clear request** → Skip this, just do it
- **Slightly unclear** → One-line confirm, then do it
- **Very unclear** → Extract + confirm + 1-2 questions max
- **Never** over-document simple tasks

---

## The Full Clarity Protocol

For significant/complex work, complete these steps:

### Step 1: WHAT (Problem Definition)

Ask and document:
- What exactly are we trying to accomplish?
- What does "done" look like? (Specific acceptance criteria)
- What is the expected outcome?

### Step 2: WHY (Context & Impact)

Ask and document:
- Why does this matter?
- What's the user/business impact?
- What happens if we don't do this?
- How does this connect to the larger goal?

### Step 3: HOW (Constraints & Boundaries)

Ask and document:
- What technical constraints exist?
- What's the scope boundary? (What are we NOT doing?)
- What dependencies exist?
- What existing code/patterns must we work with?

### Step 4: KNOWN UNKNOWNS

Ask and document:
- What questions remain unanswered?
- What assumptions are we making?
- What could invalidate our approach?
- What do we need to investigate first?

## Output Requirements

After completing the clarity protocol, update `.claude/active-context.md` with:

```markdown
# Active Context

## Current Task
[One sentence description]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Scope Boundaries
**In Scope:**
- Item 1
- Item 2

**Out of Scope:**
- Item 1
- Item 2

## Constraints
- Constraint 1
- Constraint 2

## Open Questions
- Question 1
- Question 2

## Assumptions
- Assumption 1
- Assumption 2

---
*Last updated: [timestamp]*
```

## Rules

1. **Never skip clarity for significant work** - Even if it seems obvious, document it
2. **Ask before assuming** - If requirements are ambiguous, ask the user
3. **Update when scope changes** - If understanding evolves, update active-context.md
4. **Reference SOURCE_OF_TRUTH.md** - Check existing project context before starting

## Transition

Once clarity is established:
- If there might be blockers → Proceed to **Identity System**
- If priorities are unclear → Proceed to **Priority System**
- If everything is clear → Proceed to **Execution System**

---

*This is System 1 of 5: Clarity → Identity → Priority → Execution → Reset*
