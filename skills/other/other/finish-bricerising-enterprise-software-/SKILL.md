---
name: finish
description: 'Run a final "definition of done" check before shipping: verify correctness, tighten contracts/docs, and produce a change summary. Use at the end of non-trivial work to confirm nothing was missed before merge/release. NOT for writing tests (use testing); NOT for adversarial code review (use review); NOT for initial planning (use plan).'
metadata: {"stage":"Verify","tags":["definition-of-done","verification","release-readiness","change-summary","ship","merge-readiness","checklist","learning-loop","retrospective","owner-backed-actions"],"aliases":["done","ship","merge","release","pre-merge","definition-of-done"]}
---

# Finish

## Overview

Turn “it works on my machine” into “this is ready to ship” by running verification, checking boundary discipline, and reporting changes in a consistent format.

## Chooser (What To Verify By Change Type)

- **Tiny change (typo, copy, rename)**: lint/format + typecheck. No spec/contract check needed.
- **Normal change (behavior/feature)**: unit tests + typecheck + lint + boundary spot-check (resilience/security/observability where touched) + cleanup.
- **Big change (cross-service, migration)**: full verification (tests + typecheck + lint + build + dependency scan) + spec/contract alignment check + executive + engineer packets.
- **Refactor (no behavior change)**: characterization tests pass before and after + typecheck + lint. No new spec artifacts unless contracts changed.
- **Security-sensitive change**: add security spot-check (authn/authz, input validation, safe logging) even for normal scope.

## Workflow

1. Re-check intent artifacts:
   - if contracts/semantics changed: specs/contracts are updated (`spec`)
   - if shared primitives were added/changed: API surface + adoption notes are clear (`platform`)
   - for non-trivial work: objective function, measurement ladder, and kill criteria are documented
   - if 2+ viable approaches existed: decision table includes assumptions (facts vs assumptions) and opportunity costs
2. Run verification (prefer narrow → broad):
   - unit tests / focused tests
   - typecheck
   - lint/format (if configured)
   - dependency/security scan (if configured)
   - build (if relevant)
3. Boundary discipline spot-check (only where the change touched boundaries):
   - timeouts/cancellation/retry safety (`resilience`)
   - authn/authz + input validation + safe logging (`security`)
   - logs/traces/metrics correlation + low-cardinality labels (`observability`)
   - architecture health regression: run `archobs report --suggestions-provider rules` and **wait for the report to complete** — then run `archobs show summary --format json` and `archobs show risks --top 5 --format json` to verify that top file risk scores and cluster leakage did not increase compared to the previous run; if no prior `.archobs/` baseline exists, create one now so future runs can detect regressions (`archobs`)
4. Cleanup:
   - remove dead code, debug logs, commented-out blocks
   - ensure errors are actionable and don’t leak secrets/PII
   - update quickstarts or runbooks if needed
5. Translation check:
   - write an executive packet (decision bandwidth)
   - write an engineer packet (implementation bandwidth)
   - use clear framing: recommendation, evidence, remaining risks, and explicit owner/date for next action (this is sufficient for most cases)
   - for formal hand-offs needing extra rigor (multi-stakeholder PRs, ADR recommendations), optionally use **Recommendation Brief** from [`../references/structured-thinking-templates.md`](../references/structured-thinking-templates.md)
6. Micro-retrospective (non-trivial work):
   - what happened vs what was expected?
   - key assumption confirmed or updated (one sentence — always include this, even when expectations were met)
   - if expectations diverged (rollback, incident, surprise scope, or assumption failure):
     - what one process/control change would reduce repeat risk? (flag for human to assign owner)
     - if divergence is significant, flag a follow-up using the **Retrospective / Postmortem** template ([`../references/structured-thinking-templates.md`](../references/structured-thinking-templates.md)) — do not run it inline during the finish pass

## Guardrails

- Don’t claim verification you didn’t run; report “not run” and why.
- Prefer explicit commands and outputs over vague statements (“tests passed”).
- Don’t expand scope; if you find unrelated issues, list as follow-ups.
- Close the loop for non-trivial work: include at least one explicit learning update and flag owner assignment for human review.

## References

- Architecture health regression checks: [`archobs`](../archobs/SKILL.md)
- CI quality workflow template: [`../../specs/templates/ci/github-actions-quality.yml`](../../specs/templates/ci/github-actions-quality.yml)
- Change workflow: [`../../specs/004-change-process.md`](../../specs/004-change-process.md)
- Structured-thinking references (learning loop, retrospective, recommendation brief): [`../references/`](../references/)

## Output Template

Return:

- **Executive packet** (non-trivial changes):
  - goal and decision/bet
  - primary trade-off and risk
  - success/failure signals + review ritual owner/cadence
  - kill criteria / reversal trigger
  - immediate next step
- **Engineer packet**:
  - what changed (3–7 bullets; behavior + contract impact)
  - files touched (key paths only)
  - verification (commands run + results, or why not run)
  - risks/follow-ups (including rollout watchpoints)
- **Learning loop** (non-trivial changes):
  - outcome vs expectation
  - key assumption confirmed or updated (always — even when expectations were met)
  - one process/control change to reduce repeat risk (only when expectations diverged; flag for human to assign owner)
  - Examples:
    - Good: "Assumption: Redis cache would reduce p99 by 40%. Confirmed: p99 dropped 38%. No action needed."
    - Good: "Assumption: existing auth middleware handles multi-tenant isolation. Updated: it doesn't check tenant on write paths. Action: add tenant-scoped write guard (owner: @backend-team, by 03-01)."
    - Bad: "Things went as expected. No changes."
