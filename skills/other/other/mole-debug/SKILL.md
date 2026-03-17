---
name: mole-debug
description: Systematic debugging through methodical hypothesis-driven investigation. The mole follows vibrations to their source. Use when something is broken and nobody knows why, tests fail for unclear reasons, bugs are reported but can't be found, or "it works on my machine." Reproduces first, traces data flow, binary searches the problem space, fixes with a failing test, and seals against recurrence.
---

# The Mole ⛏️

The mole works in the dark. It doesn't need to see — it feels. Vibrations travel through the earth, and the mole follows them to their source with absolute patience. It never guesses. It never panics. It digs methodically, one tunnel at a time, testing the soil ahead before committing.

## When to Activate

- User says "debug this," "why is this failing," "something's broken," or "find this bug"
- User calls `/mole-debug` or mentions mole/debug/investigate/diagnose
- Tests are failing and the cause isn't obvious
- A bug was reported but nobody can locate it
- "It works locally but fails in production" or "it works on my machine"
- Intermittent failures, flaky tests, race conditions
- Error messages that don't point to the actual problem

**IMPORTANT:** The Mole ALWAYS reproduces first. If you can't make it fail on demand, you haven't started debugging — you're just guessing.

**Pair with:** `beaver-build` for regression tests after fix, `panther-strike` when the bug is already located, `bloodhound-scout` for understanding unfamiliar code paths, `eagle-architect` when the Three-Burrow Threshold triggers

---

## The Dig

```
FEEL → DIG → TUNNEL → SURFACE → SEAL
  ↓       ↓       ↓        ↓        ↓
Repro-  Trace   Hypo-    Fix     Prevent
duce    Data    thesis   with    Recur-
Issue   Flow    Test     Test    rence
```

### Phase 1: FEEL

_The mole presses its paw against the earth. Something trembles beneath..._

**Reproduce the issue. Get it to fail on demand. No reproduction, no debugging.**

**Reproduction checklist:**

1. **Exact error** — Full error message, stack trace, HTTP status code. Not a summary.
2. **Exact steps** — What sequence triggers the failure? Write them down.
3. **Exact environment** — Node version, browser, OS, local vs production, which tenant.
4. **Minimal reproduction** — Strip away everything unnecessary. Find the smallest case that still breaks.

**If you CANNOT reproduce:** Widen the search (different browsers, tenants, data states). Check for race conditions. Check git history: `git bisect` narrows the window.

**Record the vibration** in a Vibration Log (see `references/debugging-strategies.md` for template).

**Output:** A reliably reproducible failure, or a clear statement of what blocks reproduction.

---

### Phase 2: DIG

_The mole begins to dig. Not frantically — deliberately..._

**Trace the data flow from entry to exit. Instrument the boundaries.**

Place sensors at strategic points — boundaries between systems, not scattered throughout code. Use `[MOLE:LOCATION]` labels so you can find and remove them later.

```bash
# Find the entry point
gf --agent func "functionName"
gf --agent search "POST /api/endpoint"

# Trace imports and impact
gf --agent usage "ServiceName"
gf --agent impact "src/lib/server/services/affected-file.ts"
```

For Grove-specific debugging patterns (routes, D1, KV, auth, build), see `references/grove-debugging-patterns.md`.

For detailed instrumentation techniques, see `references/debugging-strategies.md`.

**Output:** A map of the data flow with instrumentation at key boundaries.

---

### Phase 3: TUNNEL

_The mole chooses a direction. One tunnel. One hypothesis..._

**Form hypotheses. Test ONE at a time. Binary search the problem space.**

**CRITICAL:** Never change two things between test runs. One variable at a time. Binary search is logarithmic — for a 16-layer call chain, it finds the fault in 4 steps.

Track every hypothesis in the Vibration Log:

```
Hypothesis 1: [description]
Test: [what you did]
Result: [CONFIRMED / REFUTED — why]
```

### The Three-Burrow Threshold

**HARD RULE: After 3 failed fix attempts in different locations, STOP.**

Three failures in three different places = architectural problem, not isolated bug. Surface and call `eagle-architect` for an aerial view. Document everything in the Vibration Log.

**Output:** Either a confirmed root cause, or a Three-Burrow escalation with full documentation.

---

### Phase 4: SURFACE

_The mole breaks through to daylight..._

**Write a failing test that demonstrates the bug. Then fix the code. Then the test passes.**

This order is mandatory:

```
1. Write test that reproduces the bug → TEST FAILS (proves bug exists)
2. Fix the code                       → TEST PASSES (proves fix works)
3. Run full affected CI               → ALL TESTS PASS (proves nothing else broke)
```

```bash
pnpm install
gw ci --affected --fail-fast --diagnose
```

**Output:** A passing test that proves the bug is fixed, and clean CI.

---

### Phase 5: SEAL

_The mole packs the earth behind it, sealing the tunnel forever..._

**Prevent recurrence.**

1. **Regression test** — Already done in SURFACE. Lives permanently in CI.
2. **Root cause comment** — Brief comment at fix site explaining WHY, not WHAT.
3. **Class-of-bug analysis** — Could this happen elsewhere? Search for similar patterns:

```bash
# If schema/query mismatch, check ALL queries
gf --agent search "SELECT.*content.*FROM posts"
# If missing tenant scope, check ALL tenant queries
gf --agent search "FROM posts WHERE"  # Missing tenant_id?
```

4. **Clean up** — Remove ALL `[MOLE:*]` debug logging. The mole seals its tunnels.

```bash
gf --agent search "MOLE:"
```

**Output:** Sealed tunnel. Regression test. Root cause documented. Class-of-bug checked. Debug instrumentation removed.

---

## Quick Decision Guide

| Symptom | Approach |
|---------|----------|
| Test fails, error is clear | Skip to SURFACE — write the fix test, fix it |
| Test fails, error is cryptic | FEEL (reproduce) then DIG (trace data flow) |
| "Works on my machine" | FEEL (compare environments), DIG (check configs) |
| Intermittent failure | FEEL (find trigger pattern), DIG (state snapshots) |
| "It used to work" | Time-travel: `git bisect` to find breaking commit |
| 500 error, no useful message | DIG (instrument boundaries), check server logs |
| Multiple tests failing | Check common dependency — may be architectural |
| "Everything is broken" | Three-Burrow likely — escalate to Eagle immediately |

## MUST DO

- Reproduce the bug before attempting any fix
- Write a failing test before writing the fix
- Test one hypothesis at a time
- Use the Vibration Log to track all attempts
- Binary search the problem space
- Remove all debug instrumentation before committing
- Check for the same class of bug elsewhere
- Run `gw ci --affected --fail-fast --diagnose` before considering complete
- Respect the Three-Burrow Threshold

## MUST NOT

- Scatter console.logs randomly (instrument boundaries strategically)
- Change multiple variables between test runs
- Fix the symptom instead of the root cause
- Skip reproduction ("I think I know what's wrong")
- Leave debug logging in the codebase
- Commit a fix without a regression test
- Dig past the Three-Burrow Threshold without escalating

---

## References

- `references/grove-debugging-patterns.md` — SvelteKit/Cloudflare-specific patterns
- `references/debugging-strategies.md` — Detailed techniques (binary search, boundary instrumentation, state snapshots, git bisect, hypothesis tracking, Vibration Log template)

---

_The earth is quiet now. The vibration has stopped. Somewhere beneath the grove, a sealed tunnel marks where the mole found the truth._ ⛏️
