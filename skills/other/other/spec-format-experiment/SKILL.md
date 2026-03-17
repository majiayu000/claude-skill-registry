---
name: spec-format-experiment
description: "Run A/B experiment comparing GWT vs EARS+properties as spec formats for AI agent implementers. Generates specs in both formats for 5 test features, dispatches implementers, scores results. Use when evaluating spec format effectiveness for the pipeline-v3 spec writer."
user-invocable: true
model: opus
argument-hint: "run-specs | run-impl | score | all | feature-N"
---

# Spec Format Experiment: GWT vs EARS+Properties

> **Note:** This skill is a **manual experiment protocol**, not automated tooling. The operator runs each step manually by dispatching subagents with the reference prompts and recording results. Future iteration: could be automated with an orchestrator skill.

## Purpose

Compare two behavioral spec formats for AI coding agents:
- **GWT** (Given-When-Then): Scenario-based, verbose, explicit test data
- **EARS+Properties** (Easy Approach to Requirements Syntax + universal invariants): Requirement-based, compact, invariant-focused

Both formats sit on top of the same **contract-as-code** (compiled C# DTOs). Only the behavioral spec format varies.

## Hypothesis

- **H0:** GWT and EARS+properties produce equivalent results
- **H1:** EARS+properties is more token-efficient with equal or better completeness and implementer success

## Commands

| Argument | Action |
|----------|--------|
| `run-specs` | Generate specs for all 5 features in both formats (3 runs each = 30 total) |
| `run-specs feature-N` | Generate specs for feature N only |
| `run-impl` | Dispatch backend-implementer for all primary specs (2 trials each = 20 total) |
| `run-impl feature-N` | Dispatch implementer for feature N only |
| `score` | Score all generated specs on completeness, precision, tokens |
| `all` | Run full experiment: specs → score → implement → measure → verdict |
| *(no arg)* | Show experiment status and next steps |

## Protocol

### Phase 1: Generate Specs

For each feature (1-5), for each format (GWT, EARS):
1. Load the spec writer prompt from `references/gwt-spec-writer-prompt.md` or `references/ears-spec-writer-prompt.md`
2. Load the feature description from `references/feature-descriptions.md`
3. Dispatch a spec writer subagent (Opus) with the prompt + feature + contracts
4. Save output to `_docs/spec-format-experiment/specs/feature-{N}-{format}-run{R}.md`
5. Repeat 3x per feature per format for consistency measurement
6. Use **run 1** as the primary spec for implementation

### Phase 2: Score Specs

For each of the 10 primary specs:
1. Load the scoring rubric from `references/scoring-rubric.md`
2. Load the completeness checklist for the feature from `references/feature-descriptions.md`
3. Score: completeness (binary per item), precision (binary per assertion), token count
4. Save scores to `_docs/spec-format-experiment/results/raw-scores.md`

### Phase 3: Implement From Specs

For each of the 10 primary specs:
1. Create a fresh project scaffold with the feature's Contracts/
2. Dispatch `saurun:backend-implementer` with:
   - The spec (GWT or EARS format)
   - The compiled contract types
   - Standard conventions from CLAUDE.md
3. Run 2 trials per spec (20 total dispatches)
4. After each trial, measure:
   - `dotnet build` pass? (yes/no)
   - Contract compliance (curl each endpoint, check status + response shape)
   - Auth boundary correctness
5. Save results to `_docs/spec-format-experiment/results/impl-results.md`

### Phase 4: Verdict

Load all scores. Apply weights:
- Completeness: 30%
- Precision: 20%
- Token efficiency: 15%
- Implementer success: 25%
- Consistency: 5%
- Readability: 5%

| Result | Action |
|--------|--------|
| EARS wins >= 4/5 features | Adopt EARS+properties as pipeline default |
| GWT wins >= 4/5 features | Keep GWT as pipeline default |
| Mixed | Investigate hybrid (EARS for requirements, GWT for state transitions) |
| Tie | Choose based on token efficiency |

## Minimum Viable Experiment

If full 5-feature run is too expensive, use 3-feature subset:
- Feature 1 (baseline CRUD)
- Feature 3 (auth boundaries)
- Feature 4 (state machine)

This covers key differentiators in ~60% of cost.

## Token Budget

| Activity | Dispatches | Tokens/dispatch | Total |
|----------|-----------|----------------|-------|
| Spec generation (30 runs) | 30 | ~3,000 | ~90,000 |
| Implementation (20 runs) | 20 | ~15,000 | ~300,000 |
| **Total** | **50** | | **~390,000** |

## Bias Mitigation

- Both prompts frozen before experiment starts — no revision during
- Completeness scoring is binary (covers or doesn't) — no "close enough"
- 2 implementation trials per spec for non-determinism control
- 3 spec generation runs for consistency measurement
- Features alternate dispatch order (Feature 1 GWT first, Feature 2 EARS first)

## Reference Files

- `references/gwt-spec-writer-prompt.md` — GWT format spec writer prompt
- `references/ears-spec-writer-prompt.md` — EARS+properties format spec writer prompt
- `references/feature-descriptions.md` — All 5 test features with completeness checklists
- `references/scoring-rubric.md` — Full scoring rubric with weights
- `references/experiment-protocol.md` — Detailed step-by-step execution guide
