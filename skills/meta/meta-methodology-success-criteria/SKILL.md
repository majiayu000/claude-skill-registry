---
name: meta-methodology-success-criteria
description: Success criteria template - every task needs explicit, measurable criteria defining "done". Specific, measurable, achievable, verifiable requirements with verification checklist.
---

# Success Criteria

> **Quick Guide:** Every task needs explicit, measurable criteria defining "done". Specific, measurable, achievable, verifiable. Verify each criterion and provide evidence.

---

<critical_requirements>

## CRITICAL: Define Success Before Starting

**(Every task needs explicit, measurable success criteria)**

**(Criteria must be specific, measurable, achievable, verifiable)**

**(Verify each criterion after implementation)**

**(Provide evidence of completion)**

</critical_requirements>

---

<success_criteria_template>

Every task needs explicit, measurable criteria that define "done." This prevents agents from stopping too early or continuing unnecessarily.

Success criteria must be:

1. **Specific** - No ambiguity about what "done" means
2. **Measurable** - Can verify with tests, checks, or observations
3. **Achievable** - Within scope of the task
4. **Verifiable** - Can provide evidence of completion

## Template Structure

Use this structure when defining success criteria:

```xml
<success_criteria>
Your implementation must meet these criteria:

**Functional Requirements:**
1. [Specific behavior that must work]
2. [Another specific behavior]

**Technical Requirements:**
3. All existing tests continue to pass
4. New functionality is covered by tests with >80% coverage
5. Code follows existing patterns in [specific files]

**Constraints:**
6. No new dependencies are introduced
7. Changes are limited to [specific files/modules]
8. Performance is equivalent to or better than [baseline]

**After Implementation:**
- Run the test suite and report results
- Verify each criterion is met
- Report any criteria that aren't met and explain why
</success_criteria>
```

</success_criteria_template>

---

<examples>

### Good vs. Bad Success Criteria

**Bad (vague, unmeasurable):**

```
- Feature works well
- Code is clean
- No bugs
- Good user experience
```

**Problem:** No specific, measurable targets. What does "works" mean? Which tests? How do you know it's "clean"?

**Good (specific, measurable):**

```
1. User can click "Edit Profile" button and modal appears
2. Modal displays current values (name, email, bio)
3. Email validation prevents invalid formats (test@test passes, test fails)
4. Form submission updates user record in database
5. Success message displays after save
6. All tests in profile-editor.test.ts pass
7. New tests cover: happy path, validation errors, network errors
8. No modifications to authentication system (auth.py unchanged)
9. Follows form pattern from SettingsForm.tsx (lines 45-89)
```

**Why better:** Each criterion can be verified with a simple yes/no check.

</examples>

---

<verification_process>

### Verification Process

After completing work, systematically verify:

```xml
<verification_checklist>
For each success criterion:
1. State the criterion
2. Describe how you verified it
3. Provide evidence (test output, behavior observed, file comparison)
4. Mark as PASS (met) or FAIL (not met)

If any criterion is FAIL:
- Explain why it's not met
- Indicate if it's a blocker or acceptable deviation
- Suggest what's needed to meet it
</verification_checklist>
```

**Example Verification:**

```
Criterion 1: User can click "Edit Profile" and see modal with current values
PASS Verified: Tested in browser, modal opens with user's current name, email, bio
Evidence: Screenshot attached, manual test passed

Criterion 5: All tests in profile-editor.test.ts pass
PASS Verified: Ran `npm test profile-editor.test.ts`
Evidence: All 12 tests passing, 0 failures

Criterion 7: No modifications to authentication system
PASS Verified: git diff shows no changes to auth.py or related files
Evidence: `git diff main...feature-branch -- auth.py` returns empty
```

</verification_process>

---

<agent_types>

### For Different Agent Types

**Developer Agent**
Focus on functional behavior and technical implementation:

- Features work as specified
- Tests pass
- Patterns followed
- No unintended changes

**Tester Agent**
Focus on test coverage and quality:

- All specified behaviors have tests
- Edge cases are covered
- Tests fail before implementation (red)
- Tests pass after implementation (green)

**Reviewer Agent**
Focus on quality gates:

- Code follows conventions
- No security issues
- Performance is acceptable
- Patterns are consistent

**PM Agent**
Focus on completeness and clarity:

- Requirements are clear and actionable
- Patterns are referenced with specific files
- Constraints are explicit
- Success criteria are measurable

</agent_types>

---

<workflow_integration>

## Integration with Workflow

Success criteria should be:

1. **Defined by PM** in the initial specification
2. **Understood by Developer** before starting implementation
3. **Verified by Developer** after implementation
4. **Confirmed by Reviewer** during code review
5. **Tracked in progress.md** as tasks complete

</workflow_integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(Every task needs explicit, measurable success criteria)**

**(Criteria must be: Specific, Measurable, Achievable, Verifiable)**

**(Verify each criterion after implementation)**

**(Provide evidence of completion for each criterion)**

**(Mark criteria as PASS/FAIL with explanation)**

</critical_reminders>
