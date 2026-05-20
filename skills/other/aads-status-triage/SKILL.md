---
name: aads-status-triage
description: Triage AADS-ULoRA requests by capturing repository state, mapping impacted files and modules, and selecting the smallest safe validation surface before coding. Use when scope is unclear, when asked what to change or test first, or before implementation and review work.
---

# AADS Status Triage

## Workflow

1. Capture repository state.
- Run `git status --short --branch`.
- Run `git diff --name-only`.
- Run `git log --oneline -n 8`.

2. Capture system state from canonical sources.
- Read `README.md`.
- Read `docs/REPO_FILE_RELATIONS.md`.
- Read `docs/reports/v55/V55_FINAL_STATUS_REPORT.md`.
- Read `scripts/README.md`.
- Read `.github/workflows/ci.yml`.

3. Map request to ownership surfaces.
- Use `references/status-checklist.md` to map area -> files -> tests -> scripts.
- Keep the proposed edit surface minimal.
- Explicitly list out-of-scope surfaces to avoid accidental drift.

4. Define right-sized validation.
- Include at least one fast sanity check.
- Include module behavior checks for each impacted surface.
- Flag optional expensive checks separately.

5. Emit triage output.
- Provide a concise, implementation-ready triage note.
- Recommend the next skill and handoff order.

## Output Contract

Return sections in this order:
1. Current state summary
2. Impacted files/modules
3. Out-of-scope surfaces
4. Required validation commands
5. Optional expensive checks
6. Risks and assumptions
7. Recommended next skill

## References

- Read `references/status-checklist.md` for file-to-test mappings and command bundles.
