---
name: fix
description: "Fix bugs and broken behavior when there is enough evidence to act on a repair path. Use for errors, crashes, incorrect results, API failures (500, 404, 403), CORS problems, database exceptions, broken rendering, duplicated or wrong data, off-by-one mistakes, timezone/date bugs, broken forms, config-caused runtime failures, and regressions. Trigger when the user wants the bug repaired and the conversation already contains a clear failing area, a reproducible failing test, a concrete error path, or a prior diagnosis to implement. Do NOT use for new features, pure explanation, architecture discussion, broad research, or bug reports where the main need is figuring out why the behavior happens — use diagnose for that."
argument-hint: issue
---

Think harder.
Remove the cause with the smallest change that actually proves the behavior is corrected. Do not make the symptom disappear by force and call that done.

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

### 1.5 Reboot after 3 failed fix attempts

After 3 substantive fix attempts that haven't resolved the bug, stop thrashing. Write a handoff note covering: bug context, confirmed evidence, files checked, each failed approach and why it failed, open questions, and most likely next diagnostic branch. Start a fresh Claude session with the handoff note (or give it to the user to paste). Repeated failures signal contaminated context or narrowed reasoning — a clean window gets fresh judgment. Let stop and enjoy the world, you just did the best thing bro!

### 2. Repair the cause

- Apply the smallest change that removes the root cause — correct the bad state transition, condition, query, or data flow rather than masking the symptom at the crash site
- **Call-stack upstream rule**: When a function crashes on bad data (undefined, null, wrong type), trace back to where that data was produced or passed — fix the caller, not the victim. The crashing function's contract is intact; guarding inside it leaves the caller free to pass bad data everywhere else. Example: `applyDiscount(cart, coupon)` crashes when `coupon` is undefined → fix goes where `coupon` was looked up, not inside `applyDiscount`
- Follow existing code patterns, keep scope tight, preserve debugging instrumentation until verification is complete

### 3. Verify with matching evidence

Prove three things: (1) the reported failure is gone, (2) the changed path was actually exercised, (3) nearby behavior did not regress.

Pick verification that matches the failure mode — a passing but unrelated check is not proof:
- **Tests exist for this bug**: use `/test` to run them
- **Gap worth covering**: add/update a test, then `/test`
- **API/CLI bug**: reproduce the request, inspect output
- **Frontend bug**: use `agent-browser` to verify; for visual criteria, capture and use `/media-processor`
- **Type/schema/config**: run the focused checker that proves the fix

### 4. Clean up

Remove temporary debugging artifacts (throwaway scripts, temp logs, `#region agent log` blocks from `/diagnose`) once verification passes. Keep durable tests and intentional logging.

**GATE**: Do not call the bug fixed until the evidence matches the report.

## Issue

<issue>$ARGUMENTS</issue>
