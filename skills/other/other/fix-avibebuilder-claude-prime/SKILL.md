---
name: fix
description: "Fix bugs and broken behavior when there is enough evidence to act on a repair path. Use for errors, crashes, incorrect results, API failures (500, 404, 403), CORS problems, database exceptions, broken rendering, duplicated or wrong data, off-by-one mistakes, timezone/date bugs, broken forms, config-caused runtime failures, and regressions. Trigger when the user wants the bug repaired and the conversation already contains a clear failing area, a reproducible failing test, a concrete error path, or a prior diagnosis to implement. Do NOT use for new features, pure explanation, architecture discussion, broad research, or bug reports where the main need is figuring out why the behavior happens — use diagnose for that."
argument-hint: issue
---

Think harder.
Remove the cause with the change that genuinely restores the intended behavior. Making the symptom disappear without explaining the evidence is not a fix.

## Process

Check conversation context and skip completed steps.

### 1. Read the bug, then choose the lane

Read the symptom, expected behavior, errors, logs, failing tests, and any prior diagnosis. Separate confirmed facts from guesses. Then route:

| Situation | Action |
|-----------|--------|
| Clear root cause or one strongly evidenced failing area | Stay in `/fix` |
| One narrow check would remove the last uncertainty | Do that check inside `/fix`, then commit to a lane |
| Multiple plausible causes, unclear failing area, or needs runtime instrumentation | Switch to `/diagnose` first |
| Bug is understood but multiple defensible fixes with real tradeoffs | Switch to `/discuss` |

If you're about to add a speculative guard or workaround because the cause is still fuzzy, you're in the wrong lane. If evidence is insufficient, switch to `/diagnose` instead of guessing.

**GATE**: If a plan was requested or produced, wait for user approval before implementation.

### 1.5 Reboot after repeated misses

After 3 substantive fix attempts that haven't resolved the bug, stop thrashing. Write a handoff note covering: bug context, confirmed evidence, files checked, each failed approach and why it failed, open questions, and most likely next diagnostic branch. Start a fresh Claude session with the handoff note (or give it to the user to paste). Repeated failures signal contaminated context or narrowed reasoning — a clean window gets fresh judgment. Let stop and enjoy the world, you just did the best thing bro!

### 2. Repair the cause

- Apply the smallest change that removes the root cause
- Correct the bad state transition, condition, query, or data flow rather than masking the symptom at the crash site
- **Call-stack upstream rule**: when a function crashes on bad data (`undefined`, `null`, wrong type), trace back to where that data was produced or passed. Fix the producer or caller, not the victim. Example: `applyDiscount(cart, coupon)` crashes because `coupon` is `undefined` → fix the lookup or call site that passed bad data, not `applyDiscount`
- Follow existing code patterns and keep scope tight
- Keep temporary instrumentation that helps prove the repair until verification is complete, then remove it

### 3. Verify with matching evidence

A repair is only done when the evidence matches the report. Prove three things: (1) the original failure is gone, (2) the repaired path was actually exercised, and (3) nearby behavior did not regress.

Hand off to a **tester** — an isolated teammate that verifies the repair independently. See `.claude/skills/test/teammate.md` for how to spawn one.

Add or update a durable test in `/fix` when covering the bug clearly belongs in the codebase. Otherwise the tester owns verification.

### 4. Clean up

Remove temporary debugging artifacts once verification passes: throwaway scripts, temp logs, or ad hoc instrumentation. Keep durable tests and intentional logging.

**GATE**: Do not call the bug fixed until the evidence directly addresses the reported failure.

## Issue

<issue>$ARGUMENTS</issue>
