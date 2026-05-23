````skill
---
name: story-completion-ceremony
description: "Complete story validation ceremony before marking done: verify acceptance criteria, run tests, check coverage, get code review, and call bmad_workflow:complete_story. Use when completing implementation stories. Agent Behavior category skill."
metadata:
  category: Agent Behavior
  priority: high
  is-built-in: true
  session-guardian-id: builtin_story_completion_ceremony
---

# Story Completion Ceremony

Before marking any story as complete, follow this validation ceremony to ensure the work is truly done and meets quality standards.

## The 7-Step Ceremony

### 1. Verify All Acceptance Criteria
- Review each acceptance criterion in the story
- Confirm implementation addresses every requirement
- Mark each criterion as verified in the implementation artifact

### 2. Write Unit Tests (Target ≥80% Coverage)
- Create tests for all new code paths
- Follow Arrange-Act-Assert pattern (see: arrange-act-assert skill)
- Test both happy paths and error scenarios
- Use descriptive test names (see: descriptive-test-names skill)

### 3. Pass All Tests Locally
- Run the full test suite: `npm run test`
- Verify no regressions in existing tests
- Ensure all new tests pass

### 4. Test Edge Cases & Error Scenarios
- Test boundary conditions (empty arrays, null values, max limits)
- Verify error handling paths
- Test failure modes and recovery

### 5. Get Code Review Approval
- For team projects: request review from a teammate
- For solo projects: self-review against code quality standards
- Address any feedback before proceeding

### 6. Update Sprint Status
- Mark story as `done` in sprint-status.yaml
- Update epic status if all stories complete

### 7. Call bmad_workflow:complete_story
Provide validation evidence to complete the story:
```typescript
bmad_workflow({
  action: 'complete_story',
  storyId: 'your-story-id',
  validationEvidence: {
    testsPassed: 25,
    testsFailed: 0,
    coveragePercent: 85,
    codeReviewApproved: true,
    notes: 'All acceptance criteria verified'
  }
})
````

---

## Story Type Checklists

### Code Story Completion

- [ ] All acceptance criteria implemented
- [ ] Unit tests written (≥80% coverage)
- [ ] All tests passing
- [ ] Edge cases tested
- [ ] Code reviewed (self or peer)
- [ ] Implementation artifact updated
- [ ] Sprint status updated
- [ ] bmad_workflow:complete_story called

### Documentation Story Completion

- [ ] All documentation requirements met
- [ ] Spelling and grammar checked
- [ ] Links verified
- [ ] Code examples tested (if applicable)
- [ ] Reviewed for clarity
- [ ] Implementation artifact updated
- [ ] Sprint status updated
- [ ] bmad_workflow:complete_story called with `isDocumentationOnly: true`

### Bug Fix Story Completion

- [ ] Bug root cause identified
- [ ] Fix implemented
- [ ] Regression tests added
- [ ] Original issue verified as fixed
- [ ] No new bugs introduced
- [ ] Code reviewed
- [ ] Implementation artifact updated
- [ ] Sprint status updated
- [ ] bmad_workflow:complete_story called

---

## Integration with suggest_next

After completing a story, use `suggest_next` to find the next work:

```typescript
bmad_workflow({
  action: 'suggest_next',
  epicId: 'epic-19',
  currentStoryId: 'your-completed-story-id',
});
```

This returns:

- Next actionable story in the epic
- Preloaded context (story position, related stories)
- Epic completion status
- Retrospective recommendation if epic is done

---

## Anti-Patterns (What NOT To Do)

### ❌ Marking Done Without Tests

Never mark a code story as done without unit tests. Even "simple" changes can break unexpectedly.

### ❌ Skipping Coverage Requirements

The 80% threshold exists for a reason. Don't rationalize skipping it "this one time."

### ❌ Self-Approving Without Review

If you're working solo, still review your own code critically. Read it as if someone else wrote it.

### ❌ Updating Status Before Verification

Don't mark a story as done in sprint-status.yaml before running the full completion ceremony.

### ❌ Ignoring Failing Tests

Never mark a story complete with failing tests, even if the failures seem "unrelated."

### ❌ Rushing the Ceremony

The ceremony exists to catch issues early. Rushing through it defeats its purpose.

---

## Related Skills

- **arrange-act-assert**: Test organization pattern
- **test-driven-development**: Write tests before code
- **descriptive-test-names**: Make test names informative
- **edge-case-coverage**: Test boundary conditions
- **code-review-mode**: Self-review checklist
- **task-completion**: General task completion criteria

---

## Example Validation Evidence

```typescript
// Complete validation evidence for a code story
const evidence: StoryValidationEvidence = {
  testsPassed: 38, // Number of tests that passed
  testsFailed: 0, // Must be 0 to pass validation
  coveragePercent: 87, // Must be ≥80%
  codeReviewApproved: true, // Confirmed review (self or peer)
  isDocumentationOnly: false, // Set true for doc-only stories
  notes: 'Added 13 new tests for suggest_next enhancement',
};
```

```typescript
// Documentation story evidence
const docEvidence: StoryValidationEvidence = {
  codeReviewApproved: true,
  isDocumentationOnly: true,
  notes: 'Created story-completion-ceremony skill',
};
```

```

```
