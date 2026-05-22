---
name: test
description: "Use when the user wants to know if something works — the answer requires running code, not analyzing it. Output is a verdict backed by evidence: passed, failed, or broken. Primary triggers: 'run the tests', 'does X still work after my change?', 'did the merge break anything?', 'verify the fix worked', 'check if the endpoint returns X', 'confirm nothing regressed', 'run tests/unit/test_foo.py', 'let me know the results', 'make sure my changes didn't break anything'. Hard stops — do NOT use for: reviewing test code for quality/coverage gaps, debugging why test infrastructure/databases/seed scripts are misbehaving, writing or fixing tests, diagnosing root causes of unexpected behavior. The deciding question: is the user asking for the result of executing something, or asking for help understanding/analyzing/improving something? If it's the latter, use diagnose or review-code instead."
argument-hint: what-to-test-and-outcome
---

## Route fast

| Situation | Steps |
| --- | --- |
| `run tests` or a specific test path | 3 → 5 → 6 |
| The verification claim is already clear from the request or recent context | 4 → 5 → 6 |
| Behavioral claim but no tests exist | 1 → 4 manual path → 5 → 6 |
| Vague claim or broad change | Full flow |

Skip steps whose answers are already known from the conversation.

## Flow

### 1. Define the claim

Figure out what must be true before running anything.

Possible sources:
- explicit argument
- stated request or acceptance criteria
- recent conversation
- recent diff or git status as fallback

Good claim: `expired tokens return 401`.
Bad claim: `the app works`.

If the claim is mushy, sharpen it before you touch the tools. Weak claims create noisy verification.

### 2. Scope only when needed

Skip if the claim is already scoped.

Use the change set to identify:
- **deliverables** — what must hold true
- **coverage** — what existing tests or manual checks could prove each deliverable
- **blast radius** — what nearby behavior could regress

For shared code, config, auth, schema, or similar cross-cutting changes, read `references/regression-strategy.md` before deciding how wide to test.

### 3. Find the project's real test entrypoints

Check in this order:
1. `CLAUDE.md`
2. `package.json`, `Makefile`, `justfile`, `Taskfile`
3. CI config
4. test framework config
5. existing test layout

Prefer project-defined commands over raw framework commands.

### 4. Choose the proof lane

Match the claim to the execution lane.

| Claim type | Lane |
| --- | --- |
| logic, transforms, business rules | direct tests |
| API behavior or contracts | backend verification |
| UI behavior or rendering | frontend verification |
| visual UI criteria | frontend visual verification |
| DB persistence | backend verification |
| CLI behavior | direct command verification |
| type or schema correctness | direct static verification |
| compile/build correctness | direct static/build verification |

Once you've picked a lane, read the relevant reference before executing. Let the reference own the execution details.

## Reference map

- `references/backend-verification.md` — API, DB, services, and background jobs
- `references/frontend-verification.md` — browser, component, and visual verification
- `references/regression-strategy.md` — how wide to test once the main claim is proven

The right method is the one that can disprove the claim fastest without pretending to offer more confidence than it really does.

If no relevant tests exist, use a manual path instead of calling the result inconclusive. Follow the selected lane's reference rather than rebuilding the checklist inline.

For command-line claims, run the command and inspect output directly.

Keep these guardrails in mind:
- once a lane is chosen, follow its reference instead of rebuilding the same checklist inline
- keep verification outcome-first: prove the user-visible or system-visible result, not just an intermediate action
- when regression is warranted, widen in rings: direct dependents → feature area → full suite

Only use **INCONCLUSIVE** when neither an automated path nor a manual path is feasible.

### 5. Pre-flight and execute

Before running verification, confirm required infra is already available. If a server, DB, queue worker, mock service, or migration is needed and not running, stop and tell the user the exact command to start it. Do **not** start it yourself.

When you run verification, capture evidence:
- exact command
- exit code
- relevant output
- non-zero test count when a suite was run
- warnings, skipped tests, and flaky behavior that matter to the claim

Start with the most direct proof. Expand into broader regression only when the blast radius justifies it.

### 6. Report

Use this structure:

```md
## Verification Report

**Claim**: {what was tested}
**Verdict**: CONFIRMED | REFUTED | PARTIAL | INCONCLUSIVE

### Evidence
- {command}: exit {code} — proves or refutes {deliverable}

### Failures
- {test or command}: {error snippet} — {what it means}

### Gaps
- {deliverable or regression area still unverified}

### Suite Stats
Total: X | Passed: X | Failed: X | Skipped: X | Duration: Xs
Coverage: Lines X% | Branches X% (if available)
```

Use these verdicts consistently:
- **CONFIRMED** — every deliverable has passing evidence
- **REFUTED** — at least one deliverable failed with clear evidence
- **PARTIAL** — some deliverables are proven, others remain unverified
- **INCONCLUSIVE** — verification was blocked by missing infra, environment issues, or unavailable access

## Common verification situations

### Bug-fix verification
Prove the original failure no longer reproduces and check one regression ring around the changed area.

### Feature verification
Prove the stated acceptance criteria and include type-check evidence when that meaningfully covers changed contracts.

### Standalone verification
Take the claim from the argument or, if needed, infer it from recent changes.

## Rules

- Run and report only. Do not fix failures.
- A passing suite is not proof if it never exercised the claim.
- Coverage gaps stay in the report even when existing tests pass.
- Flaky behavior and pre-existing failures are findings, not noise.
- If a lane points to a reference, read it before improvising tactics.
- Temporary, verification-only app changes are allowed when they make the proof materially better and the app is ours to edit. Keep them minimal, use them to verify the claim, then remove them before reporting.
- Do not leave verification hooks behind unless the user asked for a durable selector as part of the product change.
- Never start dev servers, databases, builds, or migrations yourself.

## Verification Target

<target>$ARGUMENTS</target>
