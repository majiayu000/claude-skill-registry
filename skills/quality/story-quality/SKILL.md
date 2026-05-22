---
name: story-quality
description: "Review user stories for quality, proper sizing, sequencing, and acceptance criteria. Use before converting to prd.json. Triggers on: review stories, check user stories, story quality, validate stories."
---

# User Story Quality Review

Review user stories for proper sizing, clear descriptions, dependency ordering, and comprehensive acceptance criteria before autonomous execution.

---

## The Job

1. Read the PRD with user stories
2. Evaluate each story against quality criteria
3. Identify issues and propose fixes
4. Ensure stories are ready for autonomous implementation

**Output:** Quality report with specific improvements for each story.

---

## Quality Criteria

### 1. Story Description (1-2 Lines Max)

**Good descriptions are:**
- Single sentence or two short sentences maximum
- Written as "As a [user], I want [feature] so that [benefit]"
- Focused on ONE capability
- Clear about who benefits and why

**Red flags:**
- Description longer than 2 lines
- Multiple "and" conjunctions (doing too many things)
- Vague benefit ("so that it works better")
- Missing user perspective

**Examples:**

BAD (too long, multiple things):
```
As a user, I want to be able to create new tasks, edit existing tasks,
delete tasks, and also mark them as complete, with validation on all
fields and proper error handling so that I can manage my workflow.
```

GOOD (split into focused stories):
```
As a user, I want to create new tasks so that I can track my work.
```

### 2. Story Scope (One Context Window)

Each story must be completable in ONE autonomous agent iteration. This is critical for Ralph/Claude Code loops.

**Right-sized stories:**
- Add a database column/table
- Create one UI component
- Implement one API endpoint
- Add one form with validation
- Update one existing feature

**Too large (needs splitting):**
- "Build the entire dashboard"
- "Add authentication"
- "Implement the checkout flow"
- "Create the admin panel"

**Rule of thumb:** If you can't describe the implementation in 2-3 sentences, split it.

### 3. Dependency Ordering

Stories must be ordered so earlier stories don't depend on later ones.

**Correct order:**
1. Schema/database changes first
2. Backend logic/API endpoints second
3. UI components that use the backend third
4. Integration/polish features last

**Check for:**
- UI story before the API it needs
- Feature story before schema it requires
- Delete/update before create exists

### 4. Acceptance Criteria Quality

**Good acceptance criteria are:**
- Verifiable (can check if done)
- Specific (not vague)
- Complete (cover the full story)
- Testable (can write a test for it)

**Every story must include:**
```
- [ ] Typecheck passes
```

**UI stories must also include:**
```
- [ ] Verify in browser
```

**Bad criteria (vague):**
- "Works correctly"
- "Good user experience"
- "Handles errors properly"
- "Is fast"

**Good criteria (specific):**
- "Button disabled while request is pending"
- "Error message shown below input field"
- "Response time < 200ms for 1000 items"
- "Empty state shows 'No items yet' message"

---

## Review Checklist

For each user story, check:

### Description Quality
- [ ] 1-2 lines maximum
- [ ] Follows "As a... I want... so that..." format
- [ ] Single focused capability
- [ ] Clear user and benefit

### Scope Assessment
- [ ] Can be implemented in one session
- [ ] Describable in 2-3 implementation sentences
- [ ] No "and also" or multiple features
- [ ] Doesn't require multiple file types of changes

### Dependency Check
- [ ] Doesn't depend on later stories
- [ ] Database changes come before code that uses them
- [ ] API exists before UI that calls it

### Acceptance Criteria
- [ ] All criteria are verifiable
- [ ] No vague language
- [ ] Includes "Typecheck passes"
- [ ] UI stories include browser verification
- [ ] Covers happy path
- [ ] Covers obvious error cases

---

## Output Format

```markdown
# Story Quality Review for [PRD Name]

## Summary
- Total stories: X
- Ready for implementation: X
- Needs revision: X

## Story-by-Story Review

### US-001: [Title]
**Status:** Ready | Needs Revision

**Description Review:**
- Length: OK (1 line) | TOO LONG (X lines)
- Format: Follows template | Missing [user/want/benefit]
- Focus: Single capability | Multiple capabilities (split)

**Scope Assessment:**
- Size: Appropriate | Too large (split into X stories)
- Complexity: One context window | Risk of overflow

**Dependency Check:**
- Dependencies: None | Depends on US-00X (OK, comes after) | ISSUE: Depends on US-00X (comes before!)

**Acceptance Criteria:**
- Verifiable: All | Issues with: [list vague criteria]
- Complete: Yes | Missing: [list missing scenarios]
- Includes typecheck: Yes | NO (add it!)
- Includes browser check: Yes | NO (add it!) | N/A (not UI)

**Recommended Changes:**
1. [Specific change]
2. [Specific change]

---

### US-002: [Title]
...

## Recommended Story Splits

### Original: US-003 "Build user dashboard"
**Problem:** Too large - involves schema, API, and multiple UI components

**Split into:**
1. US-003a: "Add dashboard_preferences table to database"
2. US-003b: "Create dashboard API endpoint"
3. US-003c: "Build dashboard layout component"
4. US-003d: "Add widget rendering to dashboard"

## Reordering Recommendations

Current order has dependency issues:

| Story | Current Position | Should Be | Reason |
|-------|------------------|-----------|--------|
| US-005 | 5 | 2 | Creates schema that US-003 needs |
| US-002 | 2 | 4 | Uses API from US-003 |

**Recommended order:** US-001, US-005, US-003, US-002, US-004

## Updated Acceptance Criteria

### US-001 (add these):
- [ ] Typecheck passes
- [ ] Loading state shown during API call
- [ ] Error state shown on failure

### US-004 (make specific):
- Before: "Handles errors properly"
- After: "Shows 'Failed to save. Try again.' on 500 error"
```

---

## Common Issues and Fixes

### Issue: Story too large
**Fix:** Split by layer (schema → backend → frontend) or by feature (list → create → edit → delete)

### Issue: Vague acceptance criteria
**Fix:** Ask "How would I verify this?" - if no clear answer, make it specific

### Issue: Missing error handling
**Fix:** Add criteria for: empty states, loading states, error states, edge cases

### Issue: Wrong order
**Fix:** Map dependencies and reorder so each story only uses what exists

### Issue: Missing typecheck/browser verification
**Fix:** Always add "Typecheck passes" and "Verify in browser" for UI stories

---

## Tips

- **Be ruthless about scope:** Smaller stories are always better for autonomous execution
- **Think in iterations:** Each story = one Ralph/Claude iteration
- **Verify means verify:** If you can't write a test for it, it's not verifiable
- **Order matters:** Wrong order = broken builds and wasted iterations
