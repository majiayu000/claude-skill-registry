---
name: dev-debug
version: 1.0
description: "This skill should be used when the user asks to 'debug', 'fix bug', 'investigate error', 'why is it broken', 'trace root cause', 'find the bug', or needs systematic debugging and course-correction with verification-driven methodology using ralph loops."
---

**Announce:** "I'm using dev-debug for systematic debugging and course-correction."

<EXTREMELY-IMPORTANT>
## GUI Application Debugging Gate

When debugging GUI applications, you MUST complete the execution gates from dev-tdd during REPRODUCE and VERIFY phases:

```
GATE 1: BUILD
GATE 2: LAUNCH (with file-based logging)
GATE 3: WAIT
GATE 4: CHECK PROCESS
GATE 5: READ LOGS ← MANDATORY, CANNOT SKIP
GATE 6: VERIFY LOGS
THEN: Test reproduction or verification
```

**Critical phases requiring gates:**

**REPRODUCE phase:**
- Build → Launch with logs → Wait → Check running → **READ LOGS** → Verify bug appears in logs
- Only after reading logs can you claim "bug reproduced"

**VERIFY phase:**
- Build → Launch with logs → Wait → Check running → **READ LOGS** → Verify bug is gone from logs
- Only after reading logs can you claim "bug fixed"

**You loaded dev-tdd via ralph-loop. Follow the gates for GUI debugging.**
</EXTREMELY-IMPORTANT>

## Where This Fits

```
Main Chat (you)                    Task Agent
─────────────────────────────────────────────────────
dev-debug (this skill)
  → ralph loop (one per bug)
    → dev-delegate (spawn agents)
      → Task agent ──────────────→ investigates
                                   writes regression test
                                   implements fix
```

**Main chat orchestrates.** Task agents investigate and fix.

## Contents

- [The Iron Law of Debugging](#the-iron-law-of-debugging)
- [The Iron Law of Delegation](#the-iron-law-of-delegation)
- [The Process](#the-process)
- [The Four Phases](#the-four-phases)
- [If Max Iterations Reached](#if-max-iterations-reached)

# Systematic Debugging

<EXTREMELY-IMPORTANT>
## The Iron Law of Debugging

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. This is not negotiable.**

Before writing ANY fix, you MUST:
1. Reproduce the bug (with a test)
2. Trace the data flow
3. Form a specific hypothesis
4. Test that hypothesis
5. Only THEN write a fix (with a regression test first!)

**If you catch yourself about to write a fix without investigation, STOP.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**MAIN CHAT MUST NOT WRITE CODE. This is not negotiable.**

Main chat orchestrates the ralph loop. Task agents do the work:
- **Investigation**: Task agents read code, run tests, gather evidence
- **Fixes**: Task agents write regression tests and fixes

| Main Chat Does | Task Agents Do |
|----------------|----------------|
| Start ralph loop | Investigate root cause |
| Spawn Task agents | Run tests, read code |
| Review findings | Write regression tests |
| Verify fix | Implement fixes |

**If you're about to edit code directly, STOP and delegate instead.**
</EXTREMELY-IMPORTANT>

## The Process

Unlike implementation (per-task loops), debugging uses **ONE loop per bug**:

```
1. Start ralph loop for the bug
   Skill(skill="ralph-loop:ralph-loop", args="Debug: [SYMPTOM] --max-iterations 15 --completion-promise FIXED")

2. Inside loop: spawn Task agent for investigation/fix
   → Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-delegate/SKILL.md")

3. Task agent follows 4-phase debug protocol

4. When regression test passes → output promise
   <promise>FIXED</promise>

5. Bug fixed, loop ends
```

### Step 1: Start Ralph Loop

**IMPORTANT:** Avoid parentheses `()` in the prompt.

```
Skill(skill="ralph-loop:ralph-loop", args="Debug: [SYMPTOM] --max-iterations 15 --completion-promise FIXED")
```

### Step 2: Spawn Task Agent

Use dev-delegate, but with debug-specific instructions:

```
Task(subagent_type="general-purpose", prompt="""
Debug [SYMPTOM] following systematic protocol.

## Context
- Read .claude/LEARNINGS.md for prior hypotheses
- Read .claude/SPEC.md for expected behavior

## Debug Protocol (4 Phases)

### Phase 1: Investigate
- Add debug logging to suspected code path
- Reproduce the bug with a test
- Document: "Reproduced with [test], output: [error]"

### Phase 2: Analyze
- Trace data flow through the code
- Compare to working code paths
- Document findings in LEARNINGS.md

### Phase 3: Hypothesize
- Form ONE specific hypothesis
- Test it with minimal change
- If wrong: document what was ruled out
- If right: proceed to fix

### Phase 4: Fix
- Write regression test FIRST (must fail before fix)
- Implement minimal fix
- Run test, see it PASS
- Run full test suite

## Output
Report:
- Hypothesis tested
- Root cause (if found)
- Regression test written
- Fix applied (or blockers)
""")
```

### Step 3: Verify and Complete

After Task agent returns, verify:
- [ ] Regression test FAILS before fix
- [ ] Regression test PASSES after fix
- [ ] Root cause documented in LEARNINGS.md
- [ ] All existing tests still pass

**If ALL pass → output the promise:**
```
<promise>FIXED</promise>
```

**If ANY fail → iterate (don't output promise yet).**

## The Four Phases

| Phase | Purpose | Output |
|-------|---------|--------|
| **Investigate** | Reproduce, trace data flow | Bug reproduction |
| **Analyze** | Compare working vs broken | Findings documented |
| **Hypothesize** | ONE specific hypothesis | Hypothesis tested |
| **Fix** | Regression test → fix | Tests pass |

## The Gate Function

Before claiming ANY bug is fixed:

```
1. REPRODUCE → Run test, see bug manifest
2. INVESTIGATE → Trace data flow, form hypothesis
3. TEST → Verify hypothesis with minimal change
4. FIX → Write regression test FIRST (see it FAIL)
5. VERIFY → Run fix, see regression test PASS
6. CONFIRM → Run full test suite, no regressions
7. CLAIM → Only after steps 1-6
```

**Skipping any step is guessing, not debugging.**

## Rationalization Prevention

These thoughts mean STOP—you're about to skip the protocol:

| Thought | Reality |
|---------|---------|
| "I know exactly what this is" | Knowing ≠ verified. Investigate anyway. |
| "Let me just try this fix" | Guessing. Form hypothesis first. |
| "The fix is obvious" | Obvious fixes often mask deeper issues. |
| "I've seen this before" | This instance may be different. Verify. |
| "No need for regression test" | Every fix needs a regression test. Period. |
| "It works now" | "Works now" ≠ "fixed correctly". Run full suite. |
| "I'll add the test later" | You won't. Write it BEFORE the fix. |
| **"Log checking proves fix works"** | **Logs prove code ran, not that output is correct. Verify actual results.** |
| **"It stopped failing"** | **Stopped failing ≠ fixed. Could be hiding the symptom. Need E2E.** |
| **"The error is gone"** | **No error ≠ correct behavior. Verify expected output.** |
| **"Regression test is too complex"** | **If too complex to test, too complex to know it's fixed.** |

### Fake Fix Verification - STOP

**These do NOT prove a bug is fixed:**

| ❌ Fake Verification | ✅ Real Verification |
|----------------------|----------------------|
| "Error message is gone" | "Regression test passes + output matches spec" |
| "Logs show correct path taken" | "E2E test verifies user-visible behavior" |
| "No exception thrown" | "Test asserts expected data returned" |
| "Process exits 0" | "Functional test confirms correct side effects" |
| "Changed one line, seems fine" | "Regression test failed before, passes after" |
| "Can't reproduce anymore" | "Regression test reproduces it, fix makes it pass" |

**Red Flag:** If you're claiming "fixed" based on absence of errors rather than presence of correct behavior - STOP. That's symptom suppression, not bug fixing.

### Red Flags - STOP If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "Let's just try this fix" | You're guessing | Investigate first |
| "I'm pretty sure it's this" | "Pretty sure" ≠ root cause | Gather evidence |
| "This should work" | Hope is not debugging | Test your hypothesis |
| "Let me change a few things" | Multiple changes = can't learn | ONE hypothesis at a time |

## If Max Iterations Reached

Ralph exits after max iterations. **Still do NOT ask user to manually verify.**

Main chat should:
1. **Summarize** hypotheses tested (from LEARNINGS.md)
2. **Report** what was ruled out and what remains unclear
3. **Ask user** for direction:
   - A) Start new loop with different investigation angle
   - B) Add more logging to specific code path
   - C) User provides additional context
   - D) User explicitly requests manual verification

**Never default to "please verify manually".** Always exhaust automation first.

## When Fix Requires Substantial Changes

If root cause reveals need for significant refactoring:

1. Document root cause in LEARNINGS.md
2. Complete debug loop with `<promise>FIXED</promise>` for the investigation
3. Use `Skill(skill="workflows:dev")` for the implementation work

Debug finds the problem. The dev workflow implements the solution.

## Failure Recovery Protocol

**Pattern from oh-my-opencode: After 3 consecutive failures, escalate.**

### 3-Failure Trigger

If you attempt 3 hypotheses and ALL fail:

```
Failure 1: Hypothesis A tested → still broken
Failure 2: Hypothesis B tested → still broken
Failure 3: Hypothesis C tested → still broken
→ TRIGGER RECOVERY PROTOCOL
```

### Recovery Steps

1. **STOP** all further debugging attempts
   - No more "let me try one more thing"
   - No guessing or throwing fixes at the wall

2. **REVERT** to last known working state
   - `git checkout <last-working-commit>`
   - Or revert specific files: `git checkout HEAD~N -- file.ts`
   - Document what was attempted in `.claude/RECOVERY.md`

3. **DOCUMENT** what was attempted
   - All 3 hypotheses tested
   - Evidence gathered
   - Why each failed
   - What this rules out

4. **CONSULT** with user
   - "I've tested 3 hypotheses. All failed. Here's what I've ruled out..."
   - Present evidence from investigation
   - Request: additional context, different investigation angle, or pair debugging

5. **ASK USER** before proceeding
   - Option A: Start new ralph loop with different approach
   - Option B: User provides domain knowledge/context
   - Option C: Escalate to more experienced reviewer
   - Option D: Accept this as a blocker and document

**NO EVIDENCE = NOT FIXED** (hard rule)

### Recovery Checklist

Before claiming a bug is fixed after multiple failures:

- [ ] At least 1 hypothesis succeeded (not just "stopped failing")
- [ ] Regression test exists and PASSES
- [ ] Full test suite passes (no new failures)
- [ ] Changes are minimal and targeted
- [ ] Root cause is understood (not just symptom suppressed)

### Anti-Patterns After Failures

**DON'T:**
- Keep trying random fixes ("maybe if I change this...")
- Expand scope to "related" issues
- Make multiple changes at once
- Skip the regression test "this time"
- Claim fix without evidence

**DO:**
- Stop and document what failed
- Revert to clean state
- Consult before continuing
- Follow recovery protocol exactly
- Require evidence for completion

### Example Recovery Flow

```
Attempt 1: "Bug is in parser" → Added logging → Still broken
Attempt 2: "Bug is in validator" → Fixed validation → Still broken
Attempt 3: "Bug is in transformer" → Rewrote transform → Still broken

→ RECOVERY PROTOCOL:
1. STOP (no attempt 4)
2. REVERT all changes: git checkout HEAD -- src/
3. DOCUMENT in .claude/RECOVERY.md:
   - Ruled out: parser, validator, transformer
   - Evidence: logs show data correct at each stage
   - Hypothesis: Bug might be in consumer, not producer
4. ASK USER:
   "I've ruled out the parser/validator/transformer chain.
    Logs show data is correct when it leaves our system.
    Next investigation angle: check the consumer.
    Should I:
    A) Start new loop investigating consumer
    B) Pause for your input on where else to look"
```
