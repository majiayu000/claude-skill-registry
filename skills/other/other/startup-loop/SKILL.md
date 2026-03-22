---
name: startup-loop
description: Chat command wrapper for operating Startup Loop runs. Supports /startup-loop start|status|submit|advance with strict stage gating, prompt handoff, and Business OS sync checks. Routes to lp-* stage skills at each stage.
---

# Startup Loop

Operate the Startup Loop through a single chat command surface. This skill is an operator wrapper. It does not replace the DO processes (`/lp-do-fact-find`, `/lp-do-analysis`, `/lp-do-plan`, `/lp-do-build`).

## Operating Mode

**ORCHESTRATE + GATE + HANDOFF**

Allowed:
- Read canonical Startup Loop docs and current business artifacts.
- Determine current stage and gate status.
- Hand user exact prompt files and output paths when input/research is missing.
- Validate submitted artifact path and stage fit.
- Enforce Business OS sync actions before stage advance.

Not allowed:
- Silent stage skipping.
- Advancing while required artifacts or BOS sync actions are incomplete.
- Treating markdown mirrors of cards/ideas as source of truth.

## Invocation

- `/startup-loop start --business <BIZ> --mode <dry|live> --launch-surface <pre-website|website-live> [--start-point <problem|product>]`
  - `--start-point` is optional. Default is `product`. Existing runs that omit this flag are unaffected.
- `/startup-loop status --business <BIZ>`
- `/startup-loop submit --business <BIZ> --stage <STAGE_ID> --artifact <path>`
- `/startup-loop advance --business <BIZ>`

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Command Module Routing

Load the relevant module per command:

| Command | Module |
|---|---|
| `start` | `modules/cmd-start.md` |
| `status` | `modules/cmd-status.md` |
| `submit` | `modules/cmd-submit.md` |
| `advance` | `modules/cmd-advance.md` |

**Internal modules** (called automatically — not operator-invocable):

| Module | Trigger |
|---|---|
| `modules/assessment-intake-sync.md` | Called by `cmd-start` and `cmd-advance` as part of ASSESSMENT-09 Intake contract validation (`GATE-ASSESSMENT-00`). Writes or refreshes `<BIZ>-<YYYY-MM-DD>assessment-intake-packet.user.md` from ASSESSMENT-01–ASSESSMENT-08 precursors. No-op when precursors are unchanged. |
| `modules/cmd-advance/advance-contract.md` | Shared `advance` contract: BOS sync expectations, blocked-packet requirements, operator sequence, and red flags. |
| `modules/cmd-advance/assessment-gates.md` | `cmd-advance` submodule for ASSESSMENT gate family (`GATE-A08-00`, `GATE-ASSESSMENT-00`, `GATE-ASSESSMENT-01`). |
| `modules/cmd-advance/market-product-website-gates.md` | `cmd-advance` submodule for MARKET / PRODUCT / WEBSITE gate family (`GATE-BD-03`, `GATE-PRODUCT-02-01`, `GATE-WEBSITE-DO-01`). |
| `modules/cmd-advance/signals-gates.md` | `cmd-advance` submodule for SIGNALS weekly advance routing (`/lp-weekly`, `GATE-BD-08`). |
| `modules/cmd-advance/sell-gates.md` | `cmd-advance` submodule for SELL strategy/activation gates and SELL-01 secondary dispatch. |
| `modules/cmd-advance/s9b-gates.md` | `cmd-advance` submodule for S9B→SIGNALS advance gates. `GATE-LAUNCH-SEC` (Hard): blocks when security domain fails or QA report is absent/stale (>30 days). `GATE-UI-SWEEP-01` (Hard): blocks when no recent business-scoped rendered UI contrast sweep artifact exists, or when artifact is stale/incomplete/has S1 blockers. |
| `modules/cmd-advance/gap-fill-gates.md` | `cmd-advance` submodule for ongoing loop gap-fill dispatch gates (`GATE-LOOP-GAP-01/02/03`). |

## Required Output Contract

For `start`, `status`, and `advance`, return this exact packet:

```text
run_id: SFS-<BIZ>-<YYYYMMDD>-<hhmm>
business: <BIZ>
loop_spec_version: 3.15.0
current_stage: <STAGE_ID>
current_stage_label: <label_operator_short for current_stage>
current_stage_display: <label_operator_long for current_stage>
next_stage_label: <label_operator_short for next eligible stage or null>
next_stage_display: <label_operator_long for next eligible stage or null>
status: <ready|blocked|awaiting-input|complete>
blocking_reason: <none or exact reason>
next_action: <single sentence command/action>
prompt_file: <path or none>
required_output_path: <path or none>
naming_gate: <null>  # deprecated field; retained for backwards-compat
bos_sync_actions:
  - <required sync action 1>
  - <required sync action 2>
```

## Stage Addressing

| Flag | Behavior |
|---|---|
| `--stage <ID>` | Canonical stage ID. Case-insensitive. Always primary. Legacy IDs `S3` and `S10` are accepted and remapped to map-canonical IDs (`SIGNALS-01`, `SIGNALS`) for compatibility. |
| `--stage-alias <slug>` | Deterministic slug from `stage-operator-map.json` alias_index. Fail-closed on unknown. |
| `--stage-label <text>` | Exact match against `label_operator_short` or `label_operator_long`. Case-sensitive. Fail-closed on near-match. |

Resolver: `scripts/src/startup-loop/stage-addressing.ts`
Canonical alias source: `docs/business-os/startup-loop/_generated/stage-operator-map.json`

When a stage reference cannot be resolved, return fail-closed with deterministic suggestions. Do not infer or guess stage IDs from near-matches.

## Stage Model

Canonical source: `docs/business-os/startup-loop/specifications/loop-spec.yaml` (spec_version 3.15.0).
Stage labels: `docs/business-os/startup-loop/_generated/stage-operator-map.json`.

Stages (canonical IDs from loop-spec):

| Stage | Name | Skill | Conditional |
|---|---|---|---|
| ASSESSMENT-01 | Problem framing | `/lp-do-assessment-01-problem-statement` | start-point=problem |
| ASSESSMENT-02 | Solution-profiling scan | `/lp-do-assessment-02-solution-profiling` | start-point=problem |
| ASSESSMENT-03 | Solution selection | `/lp-do-assessment-03-solution-selection` | start-point=problem |
| ASSESSMENT-04 | Candidate names | `/lp-do-assessment-04-candidate-names` | start-point=problem |
| ASSESSMENT-05 | Name selection | `/lp-do-assessment-05-name-selection` | start-point=problem AND naming_refinement_requested (optional) |
| ASSESSMENT-06 | Distribution profiling | `/lp-do-assessment-06-distribution-profiling` | start-point=problem |
| ASSESSMENT-07 | Measurement profiling | `/lp-do-assessment-07-measurement-profiling` | start-point=problem |
| ASSESSMENT-08 | Current situation | `/lp-do-assessment-08-current-situation` | start-point=problem |
| ASSESSMENT-09 | Intake | `/startup-loop start` | — |
| ASSESSMENT-10 | Brand profiling | `/lp-do-assessment-10-brand-profiling` | — |
| ASSESSMENT-11 | Brand identity | `/lp-do-assessment-11-brand-identity` | — |
| ASSESSMENT-13 | Product naming | `/lp-do-assessment-13-product-naming` | — |
| ASSESSMENT-14 | Logo design brief | `/lp-do-assessment-14-logo-brief` | — |
| ASSESSMENT-15 | Packaging brief | `/lp-do-assessment-15-packaging-brief` | physical-product |
| ASSESSMENT | Brand (container) | — | — |
| IDEAS | Ideas pipeline (standing) | — | event-driven trigger paths |
| IDEAS-01 | Pack diff scan | `/idea-scan` | layer_a_pack_diff OR operator_inject |
| IDEAS-02 | Backlog update | `/lp-do-ideas` | semi-automated; operator confirms MERGE/SPLIT |
| IDEAS-03 | Promote to DO | `/lp-do-fact-find` | operator gate |
| MEASURE-00 | Problem framing and ICP | prompt handoff | — |
| MEASURE-01 | Agent-Setup | prompt handoff | — |
| MEASURE-02 | Results | prompt handoff | — |
| PRODUCT | Product (container) | — | — |
| PRODUCT-01 | Product from photo | prompt handoff | — |
| PRODUCTS | Products (container, standing intelligence) | — | — |
| PRODUCTS-01 | Product line mapping | prompt handoff | — |
| PRODUCTS-02 | Competitor product scan | prompt handoff | — |
| PRODUCTS-03 | Product performance baseline | prompt handoff | — |
| PRODUCTS-04 | Bundle and packaging hypotheses | prompt handoff | — |
| PRODUCTS-05 | Product-market fit signals | prompt handoff | — |
| PRODUCTS-06 | Product roadmap snapshot | prompt handoff | — |
| PRODUCTS-07 | Aggregate product pack | prompt handoff | — |
| LOGISTICS | Logistics (container, conditional) | — | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-01 | Supplier and manufacturer mapping | prompt handoff | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-02 | Lead time and MOQ baseline | prompt handoff | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-03 | Fulfillment channel options | prompt handoff | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-04 | Cost and margin by route | prompt handoff | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-05 | Returns and quality baseline | prompt handoff | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-06 | Inventory policy snapshot | prompt handoff | business_profile=logistics-heavy OR physical-product |
| LOGISTICS-07 | Aggregate logistics pack | prompt handoff | business_profile=logistics-heavy OR physical-product |
| MARKET | Market (container) | — | — |
| MARKET-01 | Competitor mapping | prompt handoff | — |
| MARKET-02 | Demand evidence | prompt handoff | — |
| MARKET-03 | Pricing benchmarks | prompt handoff | — |
| MARKET-04 | Channel landscape | prompt handoff | — |
| MARKET-05 | Assumptions and risk register | prompt handoff | — |
| MARKET-06 | Offer design | `/lp-offer` | — |
| MARKET-07 | Post-offer synthesis | prompt handoff | — |
| MARKET-08 | Demand evidence pack assembly | prompt handoff | — |
| MARKET-09 | ICP refinement | prompt handoff | — |
| MARKET-10 | Market aggregate pack (draft) | prompt handoff | — |
| MARKET-11 | Market aggregate pack (validated) | prompt handoff | — |
| SIGNALS-01 | Forecast (parallel with SELL-01) | `/lp-forecast` | — (legacy alias: `S3`) |
| PRODUCT-02 | Adjacent product research (PRODUCT container, post-offer) | `/lp-other-products` | growth_intent=product_range |
| SELL | Sell (container) | — | — |
| SELL-01 | Channel strategy + GTM | `/lp-channels`, `/lp-seo`, `/draft-outreach` | — |
| SELL-02 | Channel performance baseline | prompt handoff | — |
| SELL-03 | Outreach and content standing | prompt handoff | — |
| SELL-04 | SEO standing | prompt handoff | — |
| SELL-05 | Paid channel standing | prompt handoff | — |
| SELL-06 | Partnership and referral standing | prompt handoff | — |
| SELL-07 | Sell aggregate pack | prompt handoff | — |
| SELL-08 | Activation readiness (pre-spend) | `/startup-loop advance` | paid_spend_requested |
| S4 | Baseline merge + manifest commit (join barrier) | `/lp-baseline-merge` | — |
| WEBSITE | Website (container) | — | — |
| WEBSITE-01 | L1 first build framework | `/lp-site-upgrade` (auto-handover to DO sequence `/lp-do-fact-find --website-first-build-backlog` -> `/lp-do-analysis` -> `/lp-do-plan` -> `/lp-do-build` once Active) | launch-surface=pre-website |
| WEBSITE-02 | Site-upgrade synthesis | `/lp-site-upgrade` (L1 Build 2 auto-mode: image-first merchandising for visual-heavy catalogs) | launch-surface=website-live |
| DO | Do | `/lp-do-fact-find`, `/lp-do-analysis`, `/lp-do-plan`, `/lp-do-build` | — |
| S9B | QA gates | `/lp-launch-qa`, `/lp-design-qa`, `/tools-ui-contrast-sweep` | — |
| SIGNALS | Weekly decision | `/lp-experiment` (Phase 0 fallback) / `/lp-weekly` (Phase 1 default) | — (legacy alias: `S10`) |

## Global Invariants

- Never allow silent stage skipping.
- Never bypass the S4 merge-and-commit boundary before WEBSITE/DO progression.
- Canonical source of truth is always `loop-spec.yaml` — not markdown mirrors of cards or ideas.
- All stage references are resolved via stage-addressing.ts — never guess stage IDs.
