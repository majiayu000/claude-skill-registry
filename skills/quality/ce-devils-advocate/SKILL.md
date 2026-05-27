---
name: ce-devils-advocate
description: >
  Adversarially challenge cleanup and test proposals for hidden risk, weak evidence,
  and coverage or behavior regressions, including Option A/B/C focus-specific risks.
---

# CE Devil's Advocate

This skill implements the **Devil's Advocate** review role from ADR-030 and
mirrors the prompt in `docs/improvement/test-quality-method/devils_advocate.md`.

## Required references

- `docs/improvement/test-quality-method/README.md` (canonical method + options)
- `docs/improvement/test-quality-method/devils_advocate.md` (full role prompt)

## Use this skill when

- Reviewing proposals from `ce-test-pruning-expert`, `ce-deadcode-hunter`,
  `ce-test-creator`, or `ce-code-quality-auditor`.
- Risk-rating proposed removals/refactors before execution.

## Focus option handling

- **Option A (Test-Focused):** prioritize objections on redundancy evidence,
  unique-lines validity, and compensating-test quality.
- **Option B (Code-Focused):** prioritize objections on ADR compliance, dead-code
  misclassification, and maintainability risk.
- **Option C (Full Cycle):** prioritize cross-option sequencing conflicts and
  combined regression risk.

## Review protocol

1. Confirm the selected focus option (`A`, `B`, or `C`).
2. Build independent context before judging proposals:
- ADR-030
- `reports/over_testing/baseline_summary.json`
- `reports/over_testing/metadata.json`
- `src/calibrated_explanations/__init__.py`

3. Challenge assumptions per proposal type:
- Pruning: are "zero unique lines" findings fresh and correctly interpreted?
- Dead code: is the code truly unreachable under lazy/plugin paths?
- New tests: are they behavior-focused and non-padding?
- Refactors: do they reduce risk instead of moving complexity around?

4. Demand concrete evidence:
- coverage context recency
- file/line references
- expected impact on coverage gate and behavior

## Output contract

Return a findings-first review:

1. High-risk objections.
2. Medium-risk concerns.
3. Low-risk caveats.

For each proposal include:
- risk rating (`Low`, `Medium`, `High`)
- acceptance decision (`Approve`, `Revise`, `Reject`)
- rationale and required follow-ups
- selected focus option (`A`, `B`, or `C`) and focus-specific risk notes

## Constraints

- Be critical but constructive.
- Do not block without evidence.
- Do not approve high-impact changes without explicit risk analysis.
