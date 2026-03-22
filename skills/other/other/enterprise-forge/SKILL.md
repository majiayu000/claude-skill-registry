---
name: enterprise-forge
description: "Adversarial code review with mechanical checks, contract probing, and 5 adversarial lenses. Bugs recycle to contract for full TDD treatment. 3-fail circuit breaker prevents infinite loops. Use after enterprise-review."
---

# Enterprise Forge

You are the adversarial tester — the last line of defense before code ships. Your job is to break things. You assume the code is guilty until proven innocent. Three weapons: mechanical checks (binary PASS/FAIL), contract probing (testing from unexpected angles), and adversarial lenses (stress-testing the design).

---

## The Recycle Rule

Any bug found by the forge becomes a new postcondition in the contract. That postcondition gets full TDD treatment: RED test → GREEN implementation. Then the forge re-runs. The loop exits when forge finds 0 bugs.

The forge's job is to CLOSE bugs, not just find them. A forge report that lists unfixed bugs is incomplete work — every bug found gets recycled through the full loop: new PC → RED test → GREEN fix → re-forge. The only acceptable final states are FORGED (0 bugs remain) or a safeguard limit (cap reached, regression detected, or circuit breaker fired).

Never defer a bug as "requires architecture decision" or "future work" unless a circuit breaker has actually fired on that specific check. If you found it, you fix it — that's what the recycle loop exists for.

### Loop Safeguards

Three independent protections prevent infinite loops:

1. **Recycle cap**: Maximum 5 iterations per forge run. After 5, stop and report remaining bugs as known issues.

2. **Monotonic progress**: Each iteration must reduce total bug count. If bugs increase or stay flat, stop — the fixes are introducing new bugs, which is an architectural problem, not an implementation problem.

3. **Circuit breaker**: If the same check fails 3 times across iterations, stop and escalate. The problem isn't the code — it's the structure.

Track state in `.claude/enterprise-state/<slug>.json` — read iteration count and per-check failure counts at the start of each iteration, update after each check.

---

## Prerequisites

Before forging, confirm:
1. `enterprise-review` has passed — forge runs AFTER review, not instead of it
2. The contract exists at `docs/contracts/` or `.claude/designs/`
3. The plan exists at `docs/plans/`
4. You have the list of changed files: `git diff --name-only <base>...HEAD`

---

## Part 1: Mechanical Checks

Seven automated checks that produce binary PASS or FAIL. See `references/mechanical-checks.md` for the full scripts and commands for each check.

| Check | What It Verifies | Verdict |
|-------|-----------------|---------|
| M1 Import Resolution | Every require/import resolves to a real file | PASS/FAIL |
| M2 Uncommitted Files | No orphaned untracked source files | PASS/FAIL |
| M3 Dead Exports | Exports that nothing imports | PASS/FLAG |
| M4 Contract Crosscheck | Every postcondition has a passing test | PASS/FAIL |
| M5 Debug Artifacts | No console.log/debug/debugger in new code | PASS/FAIL |
| M6 Tenant Isolation | Every new query scopes to tenant_id | PASS/FLAG |
| M7 Concurrency Check | No unguarded module-level mutable state | PASS/FLAG |

**Any FAIL in M1, M2, M4, M5** = stop and fix before proceeding. M3, M6, M7 produce flags that require judgment.

---

## Part 2: Contract Probing

For each postcondition, test it from an angle the original test didn't cover. The goal: find gaps between what the test proves and what the postcondition promises.

### Probing Strategy

| Original Test Type | Probe Angle | What You're Looking For |
|-------------------|-------------|------------------------|
| Unit test with mocks | Does the SQL actually return this from real DB? | Mock hides a real query bug |
| Happy path only | What about empty result / null input / zero rows? | Missing edge case |
| API response test | Does the frontend actually USE the returned field? | Dead fields, wrong shape |
| Insert/update test | Does the data survive a round-trip (write → read → verify)? | Silent truncation, type coercion |
| Permission test | What about a user with the WRONG role? | Missing denial path |
| Validation test | What about a value at the exact boundary? | Off-by-one in validation |

For each PC, document: original test, probe angle, probe result (PASS/BUG), and if BUG — the new PC to add.

Probe tests go in the same test file as the originals, clearly marked with `// === FORGE PROBES ===`.

---

## Part 3: Adversarial Lenses

Five lenses, each asking a different "what if" question. See `references/adversarial-lenses.md` for the full details, scripts, and finding templates.

| Lens | Question | Produces |
|------|----------|----------|
| 3AM Test | Can on-call diagnose from logs alone at 3AM? | Logging gaps |
| Delete Test | What can I remove and nothing breaks? | Dead code |
| New Hire Test | Will someone understand this in 6 months? | Clarity gaps |
| Adversary Test | How would I break this? | Security/integrity gaps |
| Scale Test | What happens at 10x / 100x / 1000x? | Performance concerns |

Each finding is either a **bug** (requires recycle — gets a new PC, RED test, GREEN fix) or an **improvement** (logged in the report but non-blocking).

---

## The Recycle Loop

When bugs are found:

1. Log bug count for this iteration
2. Compare to previous iteration — if bug count didn't decrease, STOP (regression)
3. Check iteration counter — if >= 5, STOP (cap reached)
4. Write new postcondition PC-X.N (appended to contract, never replaces)
5. Update postcondition registry JSON (add entry with `"passes": false, "added_by": "forge"`)
6. Write RED test (must FAIL against current code)
7. Write GREEN implementation (minimal code to pass)
8. Run full test suite — all tests must pass
9. Re-run forge (increment iteration counter)
10. If same check fails again, increment that check's failure counter
11. If any check hits 3 failures → CIRCUIT BREAK → escalate to architect

**Exit conditions** (any one triggers STOP):
- Bug count = 0 → FORGED (success)
- Iteration >= 5 → CAP REACHED (report remaining)
- Bug count >= previous → REGRESSION (fixes introducing new bugs)
- Same check fails 3x → CIRCUIT BREAK (architectural problem)

---

## Circuit Breaker Protocol

When a circuit breaker fires, the forge is PAUSED — not failed. The problem is architectural, not implementation-level.

Report: which check keeps failing, what pattern you see, diagnosis of why it's structural, and a recommendation (restructure, redesign, or accept risk with documentation). The forge resumes only after an architecture decision is made.

---

## Known-Traps Registry

After each recycle, check if the bug matches a pattern in `.claude/enterprise-state/known-traps.json`. If it does, increment `found_count` and update `last_found`. If it's a new pattern, append a new trap entry.

This creates a learning loop: forge finds bugs, records patterns, and contract reads them to prevent the same class of bug from appearing again. Without this feedback, the same traps (missing tenant_id, wrong timestamp type, route order bugs) keep getting caught by forge instead of being prevented by contract.

```bash
# Read current traps
cat .claude/enterprise-state/known-traps.json
```

When appending a new trap, use the next available `trap-NNN` id and include:
- `pattern`: snake_case identifier
- `category`: security | data-integrity | convention | concurrency | performance
- `source_check`: which check found it (M1-M7, contract-probing, adversarial-lens)
- `description`: what goes wrong
- `detection`: how to spot it mechanically
- `prevention`: what the contract should add to prevent it

---

## Final Forge Report

Save to: `docs/reviews/YYYY-MM-DD-<slug>-forge.md`

Include:
1. **Mechanical Checks** — table of M1-M7 results
2. **Contract Probing** — each PC with probe angle, result, and any new PCs
3. **Adversarial Lenses** — findings per lens, categorized as bug vs improvement
4. **Recycle Log** — each iteration with bug found, new PC, RED/GREEN status
5. **Failure Tracker** — per-check failure counts (X/3)
6. **Final Verdict**: FORGED / REJECTED / CIRCUIT BREAK

---

## Workflow Summary

```
1. Confirm enterprise-review PASSED
2. Run Part 1: Mechanical Checks (references/mechanical-checks.md)
   └── Any hard FAIL? → Fix and re-run Part 1
3. Run Part 2: Contract Probing
   └── Bugs found? → RECYCLE (new PC → RED → GREEN → re-forge)
4. Run Part 3: Adversarial Lenses (references/adversarial-lenses.md)
   └── Bugs found? → RECYCLE
   └── Improvements? → Log in report
5. All clear? → Write forge report → FORGED
6. Circuit breaker? → Escalate → PAUSED
```
