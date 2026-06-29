---
name: test-strategy
description: Coverage-design method for qa-engineer — pyramid ratios per archetype, equivalence/boundary/property case selection, mutation score as the real coverage signal, and a flake-quarantine policy. Turns "coverage is 90%" (a number with no method) into a defensible test plan. Emits TEST-STRATEGY-{slug}.md, which the QA gate checks exists.
when_to_use: |
  Apply when:
  - qa-engineer is planning tests for a medium/large feature (>1 file, real behaviour risk)
  - a coverage % is being reported and you need to know whether it MEANS anything
  - deciding what to test (not just measuring what's covered)
  Do NOT apply to:
  - nano / tiny changes (typo, rename) — overhead exceeds value
  - pure docs changes
effort: medium
allowed-tools: Read, Write, Grep, Glob, Bash
paths:
  - "tests/**"
  - "docs/qa-reports/**"
---

# test-strategy

Coverage % is a number with no method. This skill makes the QA plan defensible:
**what** to test, **why** that set, and a **real** signal that the tests bite.

qa-engineer emits `docs/qa-reports/TEST-STRATEGY-{slug}.md` capturing the four
decisions below; the QA gate checks the file exists for medium/large features.

## 1. Pyramid ratio — pick by archetype (not by reflex)

The right unit:integration:e2e mix depends on where the risk lives.

| Archetype | unit | integration | e2e | why |
|-----------|------|-------------|-----|-----|
| library / devtools / cli | 80% | 15% | 5% | logic-dense, few I/O seams |
| web-app / saas | 60% | 30% | 10% | request→db→render seams dominate |
| commerce / fintech / marketplace | 50% | 35% | 15% | money paths need cross-component proof |
| data-platform / streaming | 45% | 45% | 10% | correctness lives in pipelines, not units |
| ai-system / agent-product | 50% | 20% | 10% + **evals 20%** | behaviour is the contract → eval set (see [[decision-eval]]) |

State the chosen ratio in TEST-STRATEGY and justify any deviation.

## 2. Case selection — equivalence / boundary / property

Don't enumerate inputs; **partition** them.
- **Equivalence classes** — one representative per class of behaviour (valid, invalid, empty, max). Testing 5 valid ids ≠ testing 5 classes.
- **Boundaries** — the bug lives at the edge: 0, 1, n-1, n, n+1, off-by-one, empty, overflow, the threshold itself.
- **Property-based** — for pure/transform logic, assert invariants over generated input (round-trip `decode(encode(x))===x`, idempotency, ordering) instead of hand-picked cases. Use fast-check / Hypothesis where the logic warrants it.

## 3. Mutation score — the only coverage that proves the tests bite

Line/branch coverage proves code *ran*, not that a test would *fail* if it broke.
**Mutation testing** (Stryker / mutmut / cargo-mutants) flips operators/conditions
and checks a test catches it. A "90% covered" module with 30% mutation score has
assertion-free tests. Target: mutation score ≥ 60% on changed logic-dense files;
report it in TEST-STRATEGY when the change is logic-heavy. Coverage % is the cheap
proxy; mutation score is the truth.

## 4. Flake quarantine — a flaky test is worse than no test

A test that fails ~randomly trains the team to ignore red. Policy:
- A test that fails non-deterministically is **quarantined** (skipped + tracked in a Beads bug), not left to rot the signal.
- Quarantine is time-boxed: a bug with an owner and a deadline, not `it.skip` forever.
- Root-cause before re-enabling (shared state, timing, real network, ordering).
- This is the same discipline the eval runner needs (see the eval `flaky` flag in
  `tests/eval/runner.mjs` — stddev > 0.1 is a flake signal).

## Output: TEST-STRATEGY-{slug}.md

```
# TEST-STRATEGY-{slug}
- Archetype + chosen pyramid ratio (+ justification for any deviation)
- Equivalence classes & boundaries enumerated per changed unit
- Property-based candidates (which logic, which invariants)
- Mutation-score target + result (for logic-dense changes)
- Quarantine list (flaky tests + their tracking bug)
```

Done = the plan answers "why THIS set of tests", not just "how much is covered".
