---
name: aads-colab-doc-sync
description: Keep Colab notebooks, canonical scripts, and repository documentation synchronized for AADS-ULoRA. Use when notebook flow, script entrypoints, docs navigation, or compatibility alias guidance changes.
---

# AADS Colab and Docs Sync

## Workflow

1. Confirm canonical entrypoints.
- Treat `colab_notebooks/0_AUTO_TRAIN_COMPLETE_PIPELINE.ipynb` as the primary full-flow notebook unless intentionally changed.

2. Synchronize docs and scripts.
- Keep `README.md`, `scripts/README.md`, and `docs/REPO_FILE_RELATIONS.md` aligned with notebook/script changes.
- Keep `docs/README.md` and notebook index pages aligned with renamed or re-prioritized entrypoints.

3. Preserve compatibility policy.
- Keep root wrappers as compatibility aliases unless explicitly deprecating.

4. Validate documentation and import surfaces.
- Run markdown link checks and notebook import validation.
- Run Colab environment checks when relevant.

5. Emit synchronization summary.
- List every file synchronized and any intentional deprecations.

## Output Contract

Return sections in this order:
1. Changed user entrypoints
2. Synced docs/scripts/notebooks
3. Validation commands and results
4. Compatibility/deprecation notes
5. Remaining doc drift risks

## References

- Read `references/colab-doc-sync-checklist.md` for synchronization points.
