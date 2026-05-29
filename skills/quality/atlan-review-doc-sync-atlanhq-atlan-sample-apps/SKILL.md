---
name: atlan-review-doc-sync
description: Run findings-first review for Atlan app changes and synchronize app documentation with implemented behavior. Use when completing a change set, preparing handoff, or auditing regressions.
---

# Atlan Review Doc Sync

Produce high-signal review findings and keep docs aligned.

## Workflow
1. Review code and tests with bug/risk/regression priority.
2. Report findings first, then brief change summary.
3. Update app-level docs (README, architecture notes, test notes) to match actual behavior.
4. Run `atlan-fact-verification-gate` if behavior-critical claims need source confirmation.
5. Validate implementation against selected quality tier from `../_shared/references/app-quality-bar.md`.
6. Confirm SDK/CLI remain untouched.
7. If CLI mismatch surfaced during review, append proposal entry.

## Rules
- Prioritize correctness, regression risk, and missing tests.
- Keep review findings concrete with file references.
- Do not modify SDK or CLI docs/code.

## References
- Review checklist: `references/review-checklist.md`
- Quality bar: `../_shared/references/app-quality-bar.md`
- CLI proposals: `../_shared/references/cli-change-proposals.md`
