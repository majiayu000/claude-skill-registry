---
name: aads-config-pipeline-guardrails
description: Guard AADS-ULoRA configuration and pipeline contracts by managing schema/key/default changes, pipeline assembly behavior, and artifact compatibility with migration-safe validation. Use when changing src/core, src/pipeline, config JSON files, or configuration-driven integration behavior.
---

# AADS Config and Pipeline Guardrails

## Workflow

1. Identify contract scope.
- Classify requested changes as config schema, config loading/default behavior, pipeline assembly, or artifact contract updates.
- Read `references/config-pipeline-checklist.md`.

2. Preserve compatibility boundaries.
- Keep existing config keys and default semantics unless explicit migration is requested.
- Keep artifact manifest and model registry load paths backward compatible where possible.
- Separate true interface changes from internal implementation changes.

3. Implement minimal contract-safe changes.
- Touch only required files under `src/core/*`, `src/pipeline/*`, and `config/*.json`.
- Avoid bundling unrelated behavior changes in the same patch.

4. Run required validation.
- Run unit schema and validation checks first.
- Run targeted integration checks for configuration and full pipeline behavior when contract surfaces changed.
- Run broader sanity checks only when user-facing flow or integration risk is affected.

5. Emit compatibility-focused summary.
- Classify deltas as compatible, soft-incompatible, or incompatible.
- Provide migration steps and rollback direction for any incompatible change.

## Output Contract

Return sections in this order:
1. Contract surfaces changed
2. Interface/config deltas
3. Compatibility classification
4. Validation commands and results
5. Migration and rollback notes
6. Residual risks

## References

- Read `references/config-pipeline-checklist.md` for file mappings, validation commands, and compatibility rules.
