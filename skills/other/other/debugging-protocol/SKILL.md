---
name: debugging-protocol
description: >-
  Systematic 4-phase debugging: understand the failure, form hypotheses, test
  one change at a time, fix with confidence. Activate when tests fail
  unexpectedly, errors occur, behavior is wrong, or something that worked
  before is now broken. Triggers on: "debug", "why is this failing", "test
  failure", "unexpected error", "bug", "broken".
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [source-files, test-files, git-history]
  phase: build
  standalone: true
---

# Debugging Protocol

**Value:** Feedback -- systematic investigation produces understanding.
Understanding produces correct fixes. Correct fixes prevent recurrence.
Skipping investigation produces symptom fixes that hide bugs.

## Purpose

Teaches a disciplined 4-phase debugging process that enforces root cause
analysis before any fix attempt. Prevents the most common debugging failure
mode: jumping to a fix without understanding why the problem exists.

## Practices

### The Iron Law: No Fixes Without Investigation

Never change code to fix a bug until you have completed root cause
investigation. When you see an error and immediately know the fix, that is
exactly when you are most likely to be wrong. Investigate first.

**Do:**
- Read the complete error message and stack trace before doing anything else
- Reproduce the bug consistently before investigating
- Understand WHY something is broken, not just WHAT is broken

**Do not:**
- Add a null check because you see a null pointer error (symptom fix)
- Try "a few things" to see what sticks (random debugging)
- Skip investigation because "this is an easy one"

### Phase 1: Understand the Failure

Gather facts. Do not interpret yet.

1. Read the full error message -- every line, not just the first
2. Identify the exact file and line where the failure occurs
3. Reproduce the failure consistently (if it does not reproduce, that is
   important information)
4. Check recent changes: `git log --oneline -10` and `git diff`
5. Note the data flow: where does the bad value come from?

**Output:** A clear statement of what is happening, where, and since when.

### Phase 2: Find Working Examples

Compare broken against working. The difference is the bug.

1. Find similar code that works correctly
2. Compare setup, inputs, state, and configuration
3. Identify what differs between the working and failing case
4. Check dependencies: did a library update? Did an environment change?

**Output:** A specific difference between working and failing cases.

### Phase 3: Test One Hypothesis

Form a single, explicit hypothesis. Test it with one change. Learn from the
result.

1. State the hypothesis: "I believe the bug is caused by [X] because [evidence]"
2. Make ONE change to test it
3. Observe the result
4. If the hypothesis is wrong, UNDO the change completely
5. Form a new hypothesis incorporating what you learned

**Do not** change multiple things at once. If you change the import, the type,
and the logic simultaneously, you cannot know which change mattered.

**Output:** Confirmed or refuted hypothesis with evidence.

### Phase 4: Fix and Verify

Fix with confidence because you understand the root cause.

1. Write a failing test that reproduces the bug (if one does not already exist)
2. Implement the fix targeting the root cause identified in Phase 3
3. Verify: the new test passes, all existing tests still pass
4. Confirm you fixed the cause, not the symptom

**Output:** A fix backed by a test, with all tests green.

### Escalation: Three Strikes Rule

If three fix attempts fail, stop. The problem is not what you think it is.

After the third failure:

1. Stop attempting fixes entirely
2. Document what you tried and why each attempt failed
3. Question your assumptions: wrong abstraction? Wrong domain model? Wrong
   problem entirely?
4. Seek a broader perspective -- architecture review, domain expert, or
   escalate to the user

Three failed fixes almost always signal a design problem, not a code problem.
More code fixes will not help.

**Example:**
```
Attempt 1: Add caching (hypothesis: slow queries) -> Still slow
Attempt 2: Add index (hypothesis: missing index) -> Still slow
Attempt 3: Eager loading (hypothesis: N+1) -> Still slow
STOP. Profile the system.
Result: 90% of time in external API call. Not a database problem at all.
```

## Enforcement Note

This skill provides advisory guidance. It instructs the agent to investigate
before fixing but cannot mechanically prevent premature fix attempts. On
harnesses with plugin support, enforcement plugins can require investigation
artifacts before allowing code changes. On other harnesses, the agent follows
these practices by convention. If you observe the agent skipping investigation,
point it out. For available enforcement plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After debugging guided by this skill, verify:

- [ ] Completed Phase 1 investigation before any code changes
- [ ] Read the complete error message (not just the first line)
- [ ] Reproduced the bug consistently
- [ ] Found a working example to compare against
- [ ] Stated an explicit hypothesis before each fix attempt
- [ ] Made only one change per hypothesis test
- [ ] Undid failed hypotheses before trying new ones
- [ ] Wrote or confirmed a failing test before implementing the fix
- [ ] Verified all tests pass after the fix
- [ ] Did not exceed three fix attempts without escalating

If any criterion is not met, revisit the relevant phase.

## Dependencies

This skill works standalone with no required dependencies. It integrates with:

- **tdd-cycle:** When a test fails unexpectedly during TDD, this skill guides
  investigation before modifying code
- **user-input-protocol:** When debugging reaches an ambiguous decision point,
  pause and ask the user rather than guessing
- **domain-modeling:** If three fixes fail, the root cause may be a domain
  modeling problem -- escalate to domain review

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill tdd-cycle
```
