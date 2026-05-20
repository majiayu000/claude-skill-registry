---
name: doc-review
description: Review documentation for accuracy, drift, and duplication. No code changes.
---

# Doc Review

Review documentation for correctness, alignment with code and GitHub state, and minimal duplication. No fixes — findings only.

## Inputs

Which docs (or PR) to review. Audience focus (dev workflow vs player-facing).

## Review-aware

Before starting: check if `<slug>.findings.md` exists for these docs. If it does, build on prior findings.

## Workflow

1. **Load docs** — Read the target doc(s). Load `docs/DOCUMENTATION_POLICY.md` to know what format and accuracy standards apply.

2. **Cross-check** — Validate each claim against:
   - Code (grep for referenced function names, file paths, constants)
   - GitHub state (`gh issue list`, `gh pr list`) for workflow accuracy
   - Design pillars (`design/`) for design claim accuracy
   - Other docs for duplication (flag the single best source of truth)

3. **Report** — Group findings by severity (Critical/Major/Minor) with `path:line` and suggested fix. Note any sections that are outdated, missing, or contradicted by code.

4. **Use `/findings`** — Write findings to `<slug>.findings.md` so the author can respond without copy-paste.

## Reference

- Documentation policy: `docs/DOCUMENTATION_POLICY.md`
