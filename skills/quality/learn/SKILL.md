---
name: learn
description: Consume an immutable Validate verdict and
---
# Learn

> **Purpose:** Bookkeep what an immutable verdict observed and return a bounded
> learning receipt to the orchestrator.

## Critical Constraints

- The input verdict is immutable. Because Learn cannot grade its own input, bind
  it by `input_verdict_ref` and `input_verdict_digest`; never author, edit,
  reinterpret, or replace its value.
- Consume only structured observations already present in the verdict because
  missing evidence remains missing; Learn does not manufacture a lesson.
- Classify bookkeeping outcomes such as `record`, `candidate`, or `no_change`,
  but do not promote a rule or alter the remaining plan in this mode.
- Reconcile finding recurrence by stable defect class and distinct objective.
  Retries inside one objective count once. One objective emits no producer
  candidate; two or more emit one advisory candidate citing each objective.
- Mechanical candidates remain advisory until deterministic replay catches all
  stored positives, passes explicit negative controls, and subsequent warn-only
  shadow evidence demonstrates the activation precision threshold. Learn never
  activates a constraint.
- Postmortem is optional and runs only for retrospective causal analysis. Learn
  may request that specialization; the caller decides whether to invoke it.
- Emit observations plus one Learn receipt. Do not operate proof, repository,
  tracker, delivery, or Premortem authority.
- Emit a `plan_impact` packet for the orchestrator. Learn does not mutate the
  plan and does not invoke Premortem.
- `DONE` requires a schema-valid receipt and phase summary. Unreadable proof is
  `BLOCKED`; incomplete bookkeeping is `PARTIAL`.

## Workflow

1. Resolve the Validate verdict, verify its schema, and compute or confirm its
   SHA-256 digest.
2. Copy structured observations into the Learn receipt without changing their
   `kind`, `summary`, or `evidence_ref`.
3. Record a bounded disposition for each observation: `record`, `candidate`, or
   `no_change`. Reconcile evidence-backed finding observations through the
   deterministic recurrence reducer. Emit `producer_candidates: []` for no
   recurrence or one advisory candidate per class seen in at least two distinct
   objectives. Review retries never increase the recurrence count. This is
   bookkeeping, not promotion.
4. Inspect whether work remains and classify plan impact:
   - `material_change`: cite the evidence and propose concrete remaining-plan
     changes;
   - `no_change`: record that the evidence does not require a plan mutation;
   - `terminal`: no remaining work exists, so the tick closes without another
     Premortem.
   Learn writes this `plan_impact` into its receipt and returns it to the orchestrator.
   Only the orchestrator may mutate the plan or choose the next
   transition.
5. If an explicit retrospective causal question exists, emit a Postmortem
   request as `next_action`; do not perform the retrospective inline.
6. Write `learn-receipt.json` and `.agents/rpi/phase-4-summary.md`.
7. Append the ordered RPI completion receipt:

```json
{
  "phase": "learn",
  "skill": "learn",
  "status": "DONE",
  "artifact": ".agents/rpi/phase-4-summary.md"
}
```

## Output Specification

- **Artifact directory:** the invocation root plus `.agents/rpi/`.
- **Filename convention:** `learn-receipt.json` and `phase-4-summary.md`.
- **Serialization/schema format:** JSON follows
  [learn-receipt.schema.json](schemas/learn-receipt.schema.json); summary is Markdown.
- **Recurrence contract:**
  [producer-defect-register.md](../../docs/contracts/producer-defect-register.md).
- **Validator command:** `bash skills/learn/scripts/validate.sh`.
- **Downstream handoff:** the orchestrator consumes the receipt and alone decides
  whether to continue, re-plan, stop, or route a causal-analysis request.
  Learn is the only post-verdict handoff from Validate, but it is not the
  workflow controller.

## Quality Checklist

- [ ] The receipt binds the immutable verdict reference and digest.
- [ ] Every observation is copied without semantic mutation.
- [ ] Every disposition remains bookkeeping rather than promotion.
- [ ] The phase summary and receipt pass the validator command.

Executable behavior is in [learn.feature](references/learn.feature). The
post-verdict ownership map is in
[post-verdict-actions.md](references/post-verdict-actions.md).
