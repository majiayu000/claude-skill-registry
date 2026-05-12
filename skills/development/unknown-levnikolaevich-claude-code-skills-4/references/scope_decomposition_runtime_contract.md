<!-- SOURCE-OF-TRUTH: shared/references/scope_decomposition_runtime_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Scope Decomposition Runtime Contract

Runtime contract for `ln-200`.

Canonical phase/status names: `references/runtime_status_catalog.md`

## Identifier

- scope identifier

## Phases

- `PHASE_0_CONFIG`
- `PHASE_1_DISCOVERY`
- `PHASE_2_EPIC_DECOMPOSITION`
- `PHASE_3_STORY_LOOP`
- `PHASE_4_PRIORITIZATION_LOOP`
- `PHASE_5_FINALIZE`
- `PHASE_6_SELF_CHECK`
- `DONE`
- `PAUSED`

## Required State

- `discovery_summary`
- `epic_summary`
- `story_summaries`
- `prioritization_enabled`
- `expected_prioritization_epics`
- `prioritization_summaries`
- `scope_summary`
- `final_result`
- `self_check_passed`

## Guard Rules

- no transition without current-phase checkpoint
- `PHASE_2_EPIC_DECOMPOSITION` requires discovery summary
- `PHASE_3_STORY_LOOP` requires epic summary
- `PHASE_4_PRIORITIZATION_LOOP` requires at least one `story-plan` coordinator summary
- `PHASE_5_FINALIZE` requires all expected `story-prioritization-worker` summaries when prioritization is enabled
- `PHASE_6_SELF_CHECK` requires `scope-decomposition` coordinator summary
- `DONE` requires `self_check_passed` and `final_result`

## Downstream Artifacts

`ln-200` advances only from validated artifacts:
- `epic-plan` from `ln-210`
- `story-plan` from `ln-220`
- `story-prioritization-worker` from `ln-230`

After `PHASE_5_FINALIZE`, `ln-200` writes its own `scope-decomposition` coordinator artifact.
