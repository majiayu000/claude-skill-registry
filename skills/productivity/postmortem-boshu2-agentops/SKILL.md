---
name: postmortem
description: 'Test an explicit retrospective causal question against evidence and counterfactuals after Validate and Learn. Triggers: "postmortem", "causal retrospective", "test a retrospective hypothesis".'
practices:
- sre
- lean-startup
hexagonal_role: domain
consumes:
- learn
- toil-mining
produces:
- postmortem-report.md
context_rel:
- kind: customer-of
  with: learn
- kind: customer-of
  with: toil-mining
skill_api_version: 1
user-invocable: true
metadata:
  tier: judgment
  dependencies:
  - council
  - toil-mining
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
output_contract: skills/postmortem/references/postmortem.feature
---

# Postmortem

> **Purpose:** Answer an explicit retrospective causal question using the
> already-validated outcome and evidence.

## Critical Constraints

- Because proof and causal inference are different judgments, Postmortem is retrospective causal analysis, not the general learning umbrella and not a completion gate.
- It consumes an immutable Validate verdict plus Learn receipt and does not re-run acceptance validation by default because Validate already owns that proof.
- Treat causal statements as hypotheses because causal confidence must survive
  alternatives. Separate observed sequence, contributing conditions,
  counterfactuals, and unknowns.
- A correlation is not promoted to cause without evidence that discriminates
  plausible alternatives.
- Because the caller owns delivery decisions, do not rewrite proof, operate
  tracker state, change the remaining plan, or promote a rule. Return evidence
  to the caller.
- Empty or inconclusive analysis is valid; manufacture neither certainty nor a
  lesson to make the retrospective feel useful.

## Workflow

1. Pin the verdict, Learn receipt, delivered artifact, and explicit causal
   question.
2. Reconstruct the evidence-backed timeline without importing hidden author
   reasoning as fact.
3. List candidate contributing conditions and at least one plausible
   alternative explanation.
4. Test each claim against cited evidence and a counterfactual: what should
   differ if the claim were false?
5. Optionally use independent judges to challenge contested causal claims.
6. Emit a report containing supported claims, rejected claims, unknowns,
   evidence references, and suggested experiments. Stop.

## Output Specification

- **Artifact directory:** `.agents/council/`.
- **Filename convention:** `YYYY-MM-DD-postmortem-<topic>.md`.
- **Serialization/schema format:** Markdown with causal question, pinned inputs,
  timeline, hypotheses, evidence, counterfactuals, unknowns, and experiments.
- **Validator command:** `bash skills/postmortem/scripts/validate.sh`.
- **Downstream handoff:** Learn or the orchestrator may consume the analysis; they own
  any bookkeeping, promotion, planning, or delivery decision.

## Quality Checklist

- [ ] The causal question and immutable inputs are pinned.
- [ ] Supported and rejected claims cite discriminating evidence.
- [ ] Alternatives, counterfactuals, and unknowns remain visible.
- [ ] The report stops short of proof, planning, tracker, and delivery authority.

Executable behavior is in [postmortem.feature](references/postmortem.feature).
