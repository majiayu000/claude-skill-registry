---
name: dev-verify
description: "This skill should be used when the user asks to 'verify completion', 'check that tests pass', 'confirm feature works', or REQUIRED Phase 7 of /dev workflow (final). Enforces fresh runtime evidence before claiming completion."
version: 1.0.0
---

Announce: "Using dev-verify (Phase 7) to confirm completion with fresh evidence."

## Contents

- [The Iron Law of Verification](#the-iron-law-of-verification)
- [Red Flags - STOP Immediately If You Think](#red-flags---stop-immediately-if-you-think)
- [The Gate Function](#the-gate-function)
- [Claims Requiring Evidence](#claims-requiring-evidence)
- [Insufficient Evidence](#insufficient-evidence)
- [Verification Patterns](#verification-patterns)
- [User Acceptance (Final Step)](#user-acceptance-final-step)
- [Bottom Line](#bottom-line)

# Verification Gate

<EXTREMELY-IMPORTANT>
## Your Job is to Write Automated Tests

**The automated test IS your deliverable. The implementation just makes the test pass.**

Reframe your task:
- ❌ "Implement feature X, and test it"
- ✅ "Write an automated test that proves feature X works. Then make it pass."

The test proves value. The implementation is a means to an end.

Without a REAL automated test (executes code, verifies behavior), you have delivered NOTHING.
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Verification

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. This is not negotiable.**

Before claiming ANYTHING is complete, you MUST:
1. IDENTIFY - Which command proves your assertion?
2. RUN - Execute the command fresh (not from cache/memory)
3. READ - Review full output and exit codes
4. VERIFY - Confirm output supports your claim
5. Only THEN make the claim

This applies even when:
- "I just ran it a moment ago"
- "The agent said it passed"
- "It should work"
- "I'm confident it's fine"

**If you catch yourself about to claim completion without fresh evidence, STOP.**
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Catch Yourself Thinking:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "It should work" | "Should" isn't evidence | Run the command |
| "I'm pretty sure it passes" | Confidence isn't verification | Run the command |
| "The agent reported success" | Agent reports need confirmation | Run it yourself |
| "I ran it earlier" | Earlier isn't fresh | Run it again |
| "The code exists" | Existing ≠ working | Run and check output |
| "Grep shows the function" | Pattern match ≠ runtime test | Run the function |

## The Gate Function

Before making ANY status claim:

```
1. IDENTIFY → Which command proves your assertion?
2. RUN     → Execute the command fresh
3. READ    → Review full output and exit codes
4. VERIFY  → Confirm output supports your claim
5. CLAIM   → Only after steps 1-4
```

**Skipping any step is dishonest, not verification.**

## Claims Requiring Evidence

| Claim | Required Evidence |
|-------|-------------------|
| "Tests pass" | Test output showing 0 failures |
| "Build succeeds" | Exit code 0 from build command |
| "Linter clean" | Linter output showing 0 errors |
| "Bug fixed" | Test that failed now passes |
| "Feature complete" | All acceptance criteria verified |
| **"User-facing feature works"** | **E2E test output showing PASS** |

<EXTREMELY-IMPORTANT>
## The E2E Evidence Gate

**USER-FACING CLAIMS REQUIRE E2E EVIDENCE. Unit tests are insufficient.**

| Claim | Unit Test Evidence | E2E Evidence Required |
|-------|--------------------|-----------------------|
| "API works" | ❌ Insufficient | ✅ Full request/response test |
| "UI renders" | ❌ Insufficient | ✅ Playwright snapshot/interaction |
| "Feature complete" | ❌ Insufficient | ✅ User flow simulation |
| "No regressions" | ❌ Insufficient | ✅ E2E suite passes |

### Fake E2E Patterns - STOP

**These are NOT E2E tests. They are observability, not verification.**

| ❌ Fake E2E | ✅ Real E2E |
|-------------|-------------|
| "Log shows function was called" | "Screenshot shows correct UI rendered" |
| "grep papirus in logs" | "grim screenshot + visual diff confirms icon changed" |
| "Console output contains 'success'" | "Playwright assertion: element.textContent === 'Success'" |
| "File was created" | "E2E test opens file and verifies contents" |
| "Process exited 0" | "Functional test verifies actual output matches spec" |
| "Mock returned expected value" | "Real integration returns expected value" |

**Red Flag:** If you catch yourself thinking "logs prove it works" - STOP, you're about to claim false verification. Logs prove code executed, not that it produced correct results. E2E means verifying the actual output users see.

### Rationalization Prevention (E2E)

| Thought | Reality |
|---------|---------|
| "Unit tests cover it" | Unit tests don't simulate users. Where's YOUR E2E? |
| "E2E would be redundant" | YOU'LL catch bugs with redundancy. Write E2E. |
| "No time for E2E" | YOU don't have time to fix production bugs? Write E2E. |
| "Feature is internal" | Does it affect user output? Then YOU need E2E. |
| "I manually tested" | YOU provided no evidence. Automate it. |
| **"Log checking verifies it works"** | **YOUR log checking only verifies code executed, not results. Not E2E.** |
| **"E2E with screenshots is too complex"** | **If YOU can't verify it simply, your feature isn't done. Complexity = bugs hiding.** |
| **"Implementation is done, testing is just verification"** | **Testing IS YOUR implementation. Untested code is unfinished code.** |

### The E2E Gate Function

For user-facing changes, add to verification:

```
1. IDENTIFY → Which E2E test proves user-facing behavior?
2. RUN     → Execute E2E test fresh
3. READ    → Review full output (screenshots if visual)
4. VERIFY  → User flow works as specified
5. CLAIM   → Only after E2E evidence exists
```

**"Unit tests pass" is not "feature complete" for user-facing changes.**

### GUI Application Gate (CRITICAL)

<EXTREMELY-IMPORTANT>
**For GUI applications, you MUST complete the 6-gate sequence from dev-tdd BEFORE E2E testing:**

```
GATE 1: BUILD
GATE 2: LAUNCH (with file-based logging)
GATE 3: WAIT
GATE 4: CHECK PROCESS
GATE 5: READ LOGS ← MANDATORY, CANNOT SKIP
GATE 6: VERIFY LOGS
THEN AND ONLY THEN: E2E tests/screenshots
```

**You cannot skip GATE 5 (READ LOGS).** If you catch yourself about to take screenshots without reading logs first, STOP.

See `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/dev-tdd/SKILL.md")` for the full gate sequence with examples.
</EXTREMELY-IMPORTANT>
</EXTREMELY-IMPORTANT>

## Insufficient Evidence

These do NOT count as verification:

- Previous runs (must be fresh)
- Assumptions ("it should work")
- Partial checks (ran some tests, not all)
- Agent reports without independent confirmation
- "I think..." / "It seems..." / "Probably..."

## Honesty Requirement

<EXTREMELY-IMPORTANT>
**Claiming completion without fresh evidence is LYING.**

When you say "Feature complete", you are asserting:
- You ran the verification commands yourself (fresh)
- You saw the output with your own tokens
- The output confirms the claim

Saying "complete" based on stale data or agent reports is not "summarizing" - it is LYING about project state.

**"Still verifying" is honest. "Complete" without evidence is fraud.**
</EXTREMELY-IMPORTANT>

## Rationalization Prevention

These thoughts mean STOP—you're about to claim falsely:

| Thought | Reality |
|---------|---------|
| "I just ran it" | "Just" = stale. YOU must run it AGAIN. |
| "The agent said it passed" | Agent reports need YOUR confirmation. YOU run it. |
| "It should work" | "Should" is hope. YOU run and see output. |
| "I'm confident" | YOUR confidence ≠ verification. YOU run the command. |
| "We already verified earlier" | Earlier ≠ now. YOU need fresh evidence only. |
| "User will verify it" | NO. YOU verify before claiming. User trusts YOUR claim. |
| "Close enough" | Close ≠ complete. YOU verify fully. |
| "Time to move on" | YOU only move on after FRESH verification. |

**STRUCTURAL VERIFICATION IS NOT RUNTIME VERIFICATION:**

| ❌ NOT Verification | ✅ IS Verification |
|---------------------|-------------------|
| "Code exists in file" | "Code ran and produced output X" |
| "Function is defined" | "Function was called and returned Y" |
| "Grep found the pattern" | "Program output shows expected behavior" |
| "ast-grep found the code" | "Test executed and passed with output" |
| "Diff shows the change" | "Change tested with actual input/output" |
| "Implementation looks correct" | "Ran test, saw PASS in logs" |

**The key difference:**
- Structural: "The code IS THERE" (useless)
- Runtime: "The code WORKS" (valid)

If you find yourself saying "the code exists" or "I verified the implementation" without running it, **STOP** - you're doing structural analysis, not verification.

## Verification Patterns

### Tests
```bash
# Run tests (e.g., npm test, pytest, cargo test)
npm test

# Check results: "34/34 pass" = can claim tests pass
# "33/34 pass" = cannot claim success (partial fail)
```

**Tool description:** Run automated test suite to verify all tests pass

### Regression Test
```bash
# 1. Write test → run (should fail initially)
# 2. Apply fix → run (should pass)
# 3. Revert fix → run (must fail again to confirm fix)
# 4. Restore fix → run (must pass to confirm success)
```

**Tool description:** Execute regression test cycle to validate bug fix reproducibility

### Build
```bash
npm run build && echo "Exit code: $?"
# Must see "Exit code: 0" to claim success
```

**Tool description:** Build application and verify exit code is 0

## User Acceptance (Final Step)

After technical verification passes, confirm with user. Use the AskUserQuestion pattern:

**Tool description:** Request user confirmation that implementation meets specified requirements

```yaml
question: "Does this implementation meet your requirements?"
options:
  - label: "Yes, requirements met"
    description: "Feature works as designed, ready to merge"
  - label: "Partially"
    description: "Core works but missing some requirements"
  - label: "No"
    description: "Does not meet requirements, needs more work"
```

Reference `.claude/SPEC.md` when asking—remind user of the success criteria they defined.

If user responds "Partially" or "No":
1. Ask which specific requirement is not met
2. Return to `/dev-implement` to address gaps
3. Re-run verification

**Only claim COMPLETE when:**
- [ ] All technical tests pass (automated)
- [ ] User confirms requirements met (manual)

## Bottom Line

**Two types of verification required:**

1. **Technical** - Run commands, see output, confirm no errors
2. **Requirements** - Ask user if it does what they wanted

Both must pass. No shortcuts exist.

## Workflow Complete

When user confirms "Yes, requirements met":

Announce: "Dev workflow complete. All 7 phases passed."

The `/dev` workflow is now finished. Offer to:
- Commit the changes
- Clean up `.claude/` files
- Start a new feature with `/dev`

---

## Key Principles

**Fresh Evidence Always:** Every claim requires proof from a fresh command execution, not cached results or agent reports.

**Runtime Over Structural:** Verify code works by running it, not by checking if code exists. Structural analysis cannot prove behavior.

**E2E for User-Facing:** User-visible features require end-to-end evidence (screenshots, user flow tests), not unit tests alone.

**Honesty Requirement:** Claiming completion without fresh evidence is misrepresenting project state. Only advance when fully verified.
