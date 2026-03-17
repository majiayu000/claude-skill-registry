---
name: atlan-fact-verification-gate
description: Verify Atlan app behavior against SDK docs/code and CLI docs/code before behavior-changing decisions; use lightweight checks by default and deep checks when risk is high.
---

# Atlan Fact Verification Gate

Create a lightweight verification checkpoint before behavior-changing decisions.

## Workflow
1. Classify task as `build`, `modify`, `test`, `review`, or `release`.
2. Read source guide: `../_shared/references/verification-sources.md`.
3. Verify only what is required for the current decision:
   - SDK behavior for runtime/data-path decisions.
   - CLI behavior for scaffold/run/test/release commands.
4. Resolve SDK evidence using portable fallback order:
   - local checkout (if present)
   - installed package source
   - remote source/docs
5. For build tasks, classify app quality tier (`quickstart-utility` or `connector-standard`) using `../_shared/references/app-quality-bar.md`.
6. Create `verification_manifest.json` using `../_shared/assets/verification_manifest.json` as template.
7. Validate manifest:
   `python ../_shared/scripts/validate_verification_manifest.py verification_manifest.json`
8. Continue if status is `ready`; otherwise resolve unknowns or ask user.
9. If CLI mismatch is found, append proposal entry to `../_shared/references/cli-change-proposals.md`.

## Output Contract
- Produce `verification_manifest.json` for non-trivial behavior changes.
- Record what was inspected, including exact command/flag facts when command behavior matters.
- Never edit SDK or CLI repositories.

## References
- Checklist: `references/checklist.md`
- Artifact schema: `../_shared/references/artifact-templates.md`
- Quality bar: `../_shared/references/app-quality-bar.md`
- Multi-agent compatibility: `../_shared/references/agent-surface-compatibility.md`
