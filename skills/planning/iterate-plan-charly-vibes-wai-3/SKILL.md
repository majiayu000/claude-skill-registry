---
name: iterate-plan
description: Update an existing implementation plan based on feedback, grounded in codebase reality. Makes surgical edits while preserving completed work.
---

# Iterate Implementation Plan

Update an existing implementation plan based on feedback, grounded in codebase reality.

## When Invoked

**Three scenarios:**

1. **No plan file provided**: Ask for the plan path (list available plans in `plans/`)
2. **Plan file provided but NO feedback**: Ask what changes to make
3. **Both provided**: Proceed directly with updates

## Process

### Step 1: Understand Current Plan

1. **Read the existing plan file completely** (no limit/offset)
2. Understand the overall structure and approach
3. Note the phases, success criteria, and implementation decisions
4. Check for existing checkmarks (work already completed)
5. Identify what worked and what needs changing

### Step 2: Understand Requested Changes

**Listen carefully to what the user wants:**
- Are they adding new requirements?
- Changing the approach?
- Adding/removing phases?
- Adjusting scope?
- Fixing errors or omissions?

**Ask clarifying questions if unclear:**
- Use AskUserQuestion tool for ambiguous requests
- Confirm understanding before making changes
- Get specific about what success looks like

### Step 3: Research If Needed

**Only if changes require new technical understanding:**

1. Create a todo list for research tasks
2. Search for relevant patterns in the codebase
3. Read files that will be affected by changes
4. Check for existing documentation or specs
5. Validate feasibility of requested changes

**Use parallel research when possible** - run multiple searches/reads simultaneously.

**Skip research if:**
- Changes are straightforward (adding success criteria, clarifying wording)
- You already understand the technical context
- Changes are scope/organizational, not technical

### Step 4: Confirm Understanding

**Before making changes, confirm with the user:**

```
Based on your feedback, I understand you want to:
- [Change 1 with specific detail]
- [Change 2 with specific detail]

[If research was done:]
My research found:
- [Relevant code pattern or constraint]
- [Relevant existing implementation]

I plan to update the plan by:
1. [Specific modification to plan section X]
2. [Specific modification to plan section Y]

Does this align with your intent?
```

**Wait for confirmation before proceeding.**

### Step 5: Update the Plan

1. **Make focused, precise edits** to the existing plan
2. **Maintain existing structure** unless explicitly changing it
3. **Update success criteria** if scope changed
4. **Add new phases** following existing pattern
5. **Preserve completed work** - don't remove checkmarks or completed phases

**Ensure consistency:**
- If adding a phase, match the format of existing phases
- If modifying scope, update "Out of Scope" section
- If changing approach, update affected phases and success criteria
- Maintain automated vs manual success criteria distinction
- Update "Related" section if new specs/research referenced

**Use Edit tool for surgical changes:**
- Change specific sections, don't rewrite whole file
- Preserve good content
- Keep version history implicit (plan files don't need changelog)

### Step 6: Present Changes

```
I've updated the plan at `plans/[filename].md`

**Changes made:**
1. [Specific change 1 - section affected]
2. [Specific change 2 - section affected]
3. [Specific change 3 - section affected]

**Why these changes:**
[Brief rationale tying back to user's feedback]

**Impact:**
- [How this affects implementation effort, time, or approach]
- [Any new risks or dependencies]

Would you like any further adjustments?
```

### Step 7: Iterate If Needed

If user has more feedback:
- Repeat from Step 2
- Continue until plan is approved
- Track iterations with todo list if multiple rounds

## Guidelines

1. **Be Skeptical**: Question vague feedback, verify technical feasibility
2. **Be Surgical**: Make precise edits, preserve good content
3. **Be Thorough**: Read entire plan, understand context before changing
4. **Be Interactive**: Confirm understanding before making changes
5. **No Open Questions**: Ask immediately if changes raise questions
6. **Respect Completed Work**: Don't undo or modify completed phases without good reason
7. **Maintain Quality**: Updated plan should still be specific, actionable, and complete

## Common Iteration Scenarios

### Adding a New Phase

**User feedback:** "We also need to add API caching"

**Process:**
1. Understand where in sequence this phase belongs
2. Research existing caching patterns in codebase
3. Draft new phase following existing format
4. Update dependencies between phases if needed
5. Add to success criteria and testing strategy

### Changing Approach

**User feedback:** "Let's use Redis instead of in-memory caching"

**Process:**
1. Research Redis usage patterns in codebase
2. Identify all phases affected by this change
3. Update implementation approach in affected phases
4. Update success criteria (Redis-specific checks)
5. Update risks & mitigations section

### Adding Details

**User feedback:** "The authentication phase is too vague"

**Process:**
1. Identify what's unclear or missing
2. Research authentication implementation patterns
3. Add specific file paths and changes
4. Add detailed test requirements
5. Make success criteria more specific

### Removing Scope

**User feedback:** "Let's skip the admin UI for now"

**Process:**
1. Identify all phases related to admin UI
2. Move removed work to "Out of Scope" section
3. Remove dependencies on removed phases
4. Verify remaining phases still make sense
5. Update overall timeline/effort estimate

### Splitting a Phase

**User feedback:** "Phase 3 is too large, can we break it up?"

**Process:**
1. Identify logical split points in the phase
2. Create Phase 3a and 3b (or 3 and 4)
3. Divide success criteria appropriately
4. Add dependencies if one must come before the other
5. Renumber subsequent phases

### Correcting Errors

**User feedback:** "That approach won't work with our auth system"

**Process:**
1. Understand the constraint or conflict
2. Research the correct approach
3. Update affected phases with correct approach
4. Verify no other phases have same error
5. Update risks section if this revealed gaps

## Handling Difficult Iterations

### Plan is Fundamentally Wrong

If the plan needs >50% rewrite:
```
After reviewing your feedback and the codebase, I believe the current plan needs substantial restructuring rather than iteration.

Issues:
- [Fundamental issue 1]
- [Fundamental issue 2]

Recommendation: Create a new plan incorporating:
- [What to preserve]
- [What to change]

Would you like me to create a new plan, or should I attempt to salvage this one?
```

### Feedback Conflicts with Plan Structure

```
Your requested change [X] conflicts with existing Phase [N] which does [Y].

Options:
1. Modify Phase [N] to accommodate new change (impacts: ...)
2. Add new phase before/after [N] (impacts: ...)
3. Replace Phase [N] entirely (impacts: ...)

Which approach do you prefer?
```

### Feedback is Technically Infeasible

```
After researching, I found that [requested change] is not feasible because [technical reason].

Evidence:
- [File/code showing constraint]
- [Documentation or pattern showing limitation]

Alternative approaches:
1. [Alternative 1 - achieves similar goal]
2. [Alternative 2 - different tradeoff]

Which direction should we take?
```
