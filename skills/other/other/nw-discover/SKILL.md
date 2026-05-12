---
name: nw-discover
description: "Conducts evidence-based product discovery through customer interviews and assumption testing. Use at project start to validate problem-solution fit."
user-invocable: true
argument-hint: '[product-concept] - Optional: --interview-depth=[overview|comprehensive] --output-format=[md|yaml]'
---

# NW-DISCOVER: Evidence-Based Product Discovery

**Wave**: DISCOVER | **Agent**: Scout (nw-product-discoverer)

## Overview

Execute evidence-based product discovery through assumption testing and market validation. First wave in nWave (DISCOVER > DISCUSS > SPIKE > DESIGN > DEVOPS > DISTILL > DELIVER).

Scout establishes product-market fit through rigorous customer development using Mom Test interviewing principles and continuous discovery practices.

## Output Tiers (per D2)

Provenance: feature `lean-wave-documentation` — D2 (schema-typed sections), D10 (one-line expansion descriptions). The DISCOVER wave emits a single `feature-delta.md` whose headings are typed `[REF]` (always emitted) or `[WHY]/[HOW]` (lazy expansions). Tier-1 is the always-on baseline; Tier-2 is the lazily-rendered expansion catalog.

### Tier-1 [REF] — always emitted

Tier-1 sections constitute the lean-default baseline. Every DISCOVER run emits at minimum these sections under `## Wave: DISCOVER / [REF] <Section>` headings:

- Persona ID — one-line user identifier mapped to the journey
- Opportunity statement — single-sentence problem/opportunity framing
- Validated assumptions — list with confidence level per item
- Invalidated assumptions — list with evidence reference per item
- Dropped options — alternatives weighed and rejected (one-line each)
- Decision gate (G1-G4) — pass/fail status per gate
- Constraints established — evidence-backed constraints from interviews
- Pre-requisites — dependencies on prior waves or features

### Tier-2 EXPANSION CATALOG — lazy, on-demand (per D10)

Tier-2 items are NOT emitted by default. They are rendered only when explicitly requested via `--expand <id>` (DDD-2) or via the wave-end interactive prompt when `expansion_prompt = "ask"`. Each item has a one-line description (per D10) so the menu fits in a single render. Each emitted Tier-2 section is headed `## Wave: DISCOVER / [WHY] <Section>` or `## Wave: DISCOVER / [HOW] <Section>`.

| Expansion ID | Tier label | One-line description |
|---|---|---|
| `discovery-interview-transcripts` | [WHY] | Full interview transcripts with verbatim quotes (Mom Test compliance evidence) |
| `jtbd-analysis` | [WHY] | Jobs-to-be-Done analysis: functional/emotional/social dimensions per job |
| `taste-evaluation-rationale` | [WHY] | Decision rationale for each evaluated opportunity (why fit, why not) |
| `alternative-opportunities` | [WHY] | Alternative product opportunities considered and rejected |
| `four-forces-narrative` | [WHY] | Push/Pull/Anxiety/Habit narrative analysis per primary job |
| `lean-canvas-walkthrough` | [HOW] | Lean canvas section-by-section walkthrough for stakeholder reviews |
| `interview-protocol` | [HOW] | Step-by-step interview script with Mom Test follow-up patterns |
| `expansion-catalog-rationale` | [WHY] | Why this set of expansions, why these defaults, why D10 enforces one-line descriptions |

## Density resolution (per D12)

Provenance: D12 (rigor cascade), DDD-5 (density resolver shared utility). Before emitting any Tier-1 section, resolve the active documentation density:

1. **Read** `~/.nwave/global-config.json`. Treat missing/malformed config as empty dict (fall back to defaults).
2. **Call** `resolve_density(global_config)` from `scripts/shared/density_config.py`. The function returns a `Density` value object with fields `mode` (`"lean"` | `"full"`), `expansion_prompt` (`"ask"` | `"always-skip"` | `"always-expand"` | `"smart"`), and `provenance` (the cascade branch that produced this result).
3. **Branch on `density.mode`**:
   - `lean` → emit ONLY Tier-1 `[REF]` sections under `## Wave: DISCOVER / [REF] <Section>` headings. Do NOT auto-render Tier-2 items.
   - `full` → emit Tier-1 `[REF]` sections PLUS all Tier-2 expansion items rendered under their `[WHY]` / `[HOW]` headings. This is auto-expansion (no menu).
4. **At wave end**, branch on `density.expansion_prompt`:
   - `"ask"` → present the expansion menu (Tier-2 catalog above with one-line descriptions per D10) and append user-selected items as `## Wave: DISCOVER / [WHY|HOW] <Section>` headings.
   - `"always-skip"` → no menu, no extra sections (idempotent re-runs, CI mode).
   - `"always-expand"` → equivalent to `mode = "full"` for this run; auto-render every Tier-2 item.
   - `"smart"` → out of scope for v1 (per OQ-3); treat as `"ask"` until heuristic is empirically tuned.

The resolver itself encodes the D12 cascade: explicit `documentation.density` override > `rigor.profile` mapping (`lean`→`lean`, `standard`→`lean`+`ask`, `thorough`→`full`, `exhaustive`→`full`+all-expansions, `custom`→`lean`+`ask`) > hard default `lean`+`ask`. This skill MUST NOT replicate the cascade locally — call `resolve_density(global_config)` and trust its output.

**Section heading prefix convention (per D2)**: every emitted section starts with `## Wave: DISCOVER / [REF] <Section>` for Tier-1; `## Wave: DISCOVER / [WHY] <Section>` or `## Wave: DISCOVER / [HOW] <Section>` for Tier-2. Validator `scripts/validation/validate_feature_delta.py` enforces the regex `^## Wave: \w+ / \[(REF|WHY|HOW)\] .+$` on every wave heading.

### Ad-hoc override — user request mid-session

Even when `density.mode = "lean"` and `density.expansion_prompt = "always-skip"`, the user may ask DURING the wave session for specific expansions:

- "expand jtbd" / "expand jtbd-narrative" / "more on jtbd"
- "add alternatives considered"
- "show migration playbook"
- "tell me why" (interpretive — append the WHY rationale section relevant to the most recent decision)
- "more on <X>" (where `<X>` is one of the expansion catalog items for this wave)

When the user makes such a request:

1. Append the corresponding `[WHY]` or `[HOW]` section to `feature-delta.md` under the current wave's heading.
2. Emit a `DocumentationDensityEvent` with `choice="expand"` and `expansion_id=<the requested item>` to `JsonlAuditLogWriter`.
3. Do NOT modify `~/.nwave/global-config.json`. The override is ONE-SHOT for this wave only.

If the user's request matches NO item in this wave's Expansion Catalog, respond with the catalog list (one-line description per item per D10) and ask for clarification — do NOT improvise an expansion outside the catalog.

## Telemetry (per D4 + DDD-6)

Provenance: D4 (telemetry schema instrumented day-one), D6 (first-install pedagogical prompt creates audit signal), DDD-6 (telemetry event class lives in DES domain, writer reused). Every expansion choice — whether the user expanded an item or skipped the menu — emits a structured event to the existing `JsonlAuditLogWriter` driven adapter.

**Event type**: `DocumentationDensityEvent` (dataclass at `src/des/domain/telemetry/documentation_density_event.py`).

**Schema fields** (per D4):

```
{
  "feature_id": "<feature-id>",
  "wave": "DISCOVER",
  "expansion_id": "<id-from-catalog-or-'*'-for-skip-all>",
  "choice": "skip" | "expand",
  "timestamp": "<ISO-8601 datetime>"
}
```

**Emission pattern**:

1. Construct a `DocumentationDensityEvent(feature_id=..., wave="DISCOVER", expansion_id=..., choice=..., timestamp=...)`.
2. Call `event.to_audit_event()` to convert to the open `AuditEvent` shape (`event_type="DOCUMENTATION_DENSITY"` and the schema fields nested under `data`).
3. Dispatch via `JsonlAuditLogWriter().log_event(audit_event)`.

The wave-skill harness invokes the helper `scripts/shared/telemetry.py:write_density_event(...)` which performs all three steps. This skill MUST NOT bypass the helper or write JSONL directly — every density telemetry event flows through the shared helper to keep the audit-log schema consistent.

**When to emit**:
- One event per user choice in the expansion menu when `expansion_prompt = "ask"` (`choice = "expand"` for selected items, `choice = "skip"` with `expansion_id = "*"` if the user skips the entire menu).
- One synthetic `choice = "skip"` event with `expansion_id = "*"` when `expansion_prompt = "always-skip"` (records the skipped menu opportunity).
- One `choice = "expand"` event per Tier-2 item rendered when `mode = "full"` or `expansion_prompt = "always-expand"`.

This telemetry feeds the post-pilot propagation success metric: tracking whether DISCOVER feeders into DISCUSS need additional rationale (downstream `--expand` invocations are a signal the lean baseline is too thin).

## Context Files Required

- docs/project-brief.md — Initial product vision (if available)
- docs/market-context.md — Market research and competitive landscape (if available)

## Previous Artifacts

None (DISCOVER is the first wave).

## Wave Decisions Summary

Before completing DISCOVER, produce `docs/feature/{feature-id}/discover/wave-decisions.md`:

1. **Record Key Decisions** — List each decision as `[D1] {decision}: {rationale} (see: {source-file})`. Gate: every major discovery choice has a rationale entry.
2. **Record Constraints** — List each constraint established from evidence. Gate: all constraints have an evidence source.
3. **Record Validated Assumptions** — List each assumption confirmed, with confidence level. Gate: confidence level stated for each.
4. **Record Invalidated Assumptions** — List each assumption disproved, with evidence reference. Gate: evidence reference present for each invalidation.

This summary enables downstream waves to quickly assess DISCOVER outcomes without reading all artifacts.

## Document Update (Back-Propagation)

DISCOVER is the first wave but it DOES write to SSOT. It has no prior wave to back-propagate to, but it seeds the SSOT for downstream waves:

1. **Seed journeys** — Write initial `docs/product/journeys/{name}.yaml` with the persona, opportunity statement, and the discovered job(s) traced from interviews. DISCUSS will refine and lock this schema.
2. **Seed personas (optional)** — When persona-narrative expansion is triggered, write `docs/product/personas/{name}.yaml` with the validated persona profile. Otherwise leave to DISCUSS.
3. **No prior-wave Changed-Assumptions section** — DISCOVER produces evidence; it does not contradict prior decisions because there are none. The Changed-Assumptions pattern starts in DISCUSS.

Per D5 (lean-wave-documentation): DISCOVER's `docs/product/journeys/` feeder artifact stays Tier-1 — these are seed artifacts for the product SSOT, not feature-delta sections.

## Agent Invocation

1. **Dispatch Agent** — Invoke `@nw-product-discoverer` with `Execute *discover for {product-concept-name}`. Gate: agent dispatched.
2. **Provide Context Files** — Pass `docs/project-brief.md` and `docs/market-context.md` if available. Gate: available context files referenced.
3. **Apply Configuration** — Set `interactive: high`, `output_format: markdown`, `interview_depth: comprehensive`, `evidence_standard: past_behavior`. Gate: configuration confirmed.

## Peer Review Gate

1. **Dispatch Reviewer** — Invoke `@nw-product-discoverer-reviewer` before handoff to DISCUSS. Gate: reviewer dispatched, all discovery artifacts available.
2. **Verify Review Scope** — Reviewer checks: evidence quality (past behavior, not future intent), interview coverage and threshold compliance, assumption validation rigor (G1-G4 gates), lean canvas coherence with interview findings. Gate: all four dimensions assessed.
3. **Handle Rejection** — On REJECTION: revise artifacts per reviewer findings and re-submit. Gate: max 2 attempts; escalate to user if unresolved.
4. **Confirm Approval** — Block handoff to DISCUSS until reviewer returns APPROVED. Gate: explicit approval received.

## Success Criteria

Refer to Scout's quality gates in ~/.claude/agents/nw/nw-product-discoverer.md.

- [ ] All 4 decision gates passed (G1-G4)
- [ ] Minimum interview thresholds met per phase
- [ ] Evidence quality standards met (past behavior, not future intent)
- [ ] Peer review approved by @nw-product-discoverer-reviewer
- [ ] Handoff accepted by product-owner (DISCUSS wave)

## Next Wave

**Handoff To**: nw-product-owner (DISCUSS wave)
**Deliverables**: See Scout's handoff package specification in agent file

## Examples

### Example 1: New SaaS product discovery
```
/nw-discover invoice-automation
```
Scout conducts customer development interviews, validates problem-solution fit through Mom Test questioning, and produces a lean canvas with evidence-backed assumptions.

## Outputs

**Single narrative file**: `docs/feature/{feature-id}/feature-delta.md` — all DISCOVER findings (Tier-1 [REF] sections + any rendered Tier-2 expansions) live here.

**Machine artifacts**: none unique to DISCOVER (no parseable companions are produced).

**SSOT updates** (per Recommendation 3 / back-propagation contract):
- `docs/product/journeys/{name}.yaml` — initial drafts seeding the journey schema (DISCUSS refines)
- `docs/product/personas/{name}.yaml` — optional, only when persona-narrative expansion is rendered

Legacy multi-file outputs (`problem-validation.md`, `opportunity-tree.md`, `solution-testing.md`, `lean-canvas.md`, `interview-log.md`, `wave-decisions.md` as separate files) are NOT produced — that content lives in `feature-delta.md` under `## Wave: DISCOVER / [REF|WHY|HOW] <Section>` headings. Validator: `scripts/validation/validate_feature_layout.py`.
