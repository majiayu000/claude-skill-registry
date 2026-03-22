---
name: lp-do-assessment-13-product-naming
description: Full product naming pipeline orchestrator (ASSESSMENT-13). Runs four parts in sequence: (1) produce <YYYY-MM-DD>-product-naming-spec.md from ASSESSMENT docs, (2) agent generates 75 scored candidates across naming territories, (3) TM pre-screen direction for all candidates via tm-prescreen-cli.ts, (4) filter and rank to produce a top-20 shortlist. Delivers a final operator-ready shortlist of scored candidates with EUIPO/WIPO/UIBM search direction pre-generated.
---

# lp-do-assessment-13-product-naming — Product Naming Pipeline (ASSESSMENT-13)

Orchestrates the complete four-part product naming pipeline from a standing start to a TM-prescreened, ranked shortlist. The operator receives a shortlist where every name has a DWPEIC quality score and TM search direction URLs pre-generated for immediate review.

This pipeline is distinct from ASSESSMENT-04/05 (business name pipeline):
- **Business name** (ASSESSMENT-04/05): 250 candidates → RDAP .com availability check → top 20 available
- **Product name** (ASSESSMENT-13): 75 candidates → TM pre-screen direction → top 20 by score

The domain check is not applicable to product names (the brand domain is already owned). The TM pre-screen runs automatically to generate EUIPO, WIPO GBD, and UIBM search direction URLs; the operator reviews the URLs for their preferred candidates before confirming a selection.

Load: ../_shared/assessment/assessment-base-contract.md

## Invocation

```
/lp-do-assessment-13-product-naming --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

**ASSESSMENT-12 note:** Before running this skill, the operator should have run `/lp-do-assessment-12-promote` to promote the brand identity dossier from Draft to Active. ASSESSMENT-12 is a skill-only gate — not enforced by GATE-ASSESSMENT-01. If the dossier remains Draft, proceed with a provisional note but flag the gap to the operator.

**ASSESSMENT-03 gate:** If no ASSESSMENT-03 product option selection artifact exists, halt and emit:
> "ASSESSMENT-03 artifact not found at `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-option-selection.user.md`. A confirmed product option is required before product naming can begin. Run `/lp-do-assessment-03-solution-selection --business <BIZ>` first."

Rerunnable. If a spec and/or candidates file already exist from a prior round, the pipeline resumes from the correct part — see resume logic module.

## Operating Mode

ASSESSMENT ONLY

## Pipeline overview

| Part | Name | What happens | Tool |
|------|------|--------------|------|
| 1 | **Spec** | Read ASSESSMENT docs → write `<YYYY-MM-DD>-product-naming-spec.md` | Inline |
| 2 | **Generate** | Read spec → generate 75 DWPEIC-scored candidates → write `product-naming-candidates-<date>.md` | Spawn general-purpose agent |
| 3 | **TM pre-screen** | Generate EUIPO/WIPO/UIBM search direction for all candidates → write `product-naming-tm-<date>.txt` + sidecar events | Bash (tm-prescreen-cli.ts) |
| 4 | **Shortlist** | Sort by score → write `product-naming-shortlist-<date>.user.md` with top 20 and embedded TM URLs | Inline |

All four parts run sequentially. Each part gates on the output of the prior part.

## Required Inputs (pre-flight)

| Source | Path | Required |
|--------|------|----------|
| ASSESSMENT intake packet | `docs/business-os/startup-baselines/<BIZ>/<YYYY-MM-DD>-assessment-intake-packet.user.md` | Yes — primary source for product definition and ICP |
| Product option selection | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-option-selection.user.md` | Yes — confirmed product type and product category |
| Brand profile | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-profile.user.md` | Yes — personality adjective pairs, voice & tone, positioning constraints |
| Business name shortlist | `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/latest-naming-shortlist.user.md` | Yes if present — confirms the approved business name and expansion-headroom rationale |
| Brand identity dossier | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | No — read if present for imagery direction and aesthetic constraints |
| Distribution plan | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-launch-distribution-plan.user.md` | No — read if present for channel-specific naming constraints (e.g., Etsy character limits) |

## Execution

### Parts 1–2 — Spec and Generate

Load: modules/part-1-2.md

### Parts 3–4 — TM Pre-Screen and Shortlist

Load: modules/part-3-4.md

### Resume Logic and New Round

Load: modules/resume-logic.md

## Quality Gate

Load: modules/quality-gate.md

## Completion message

Present the top 10 from the shortlist inline:

> **Score key:** D = Distinctiveness · W = Wordmark quality · P = Phonetics · E = Expansion headroom · I = ICP resonance · C = Category signal · Score = sum out of 30
>
> **Product naming pipeline complete — <BIZ> Round N**
> 75 candidates generated across N territories. Top 10:
>
> | Rank | Line Name | Full Compound | Score | D | W | P | E | I | C |
> |------|-----------|---------------|-------|---|---|---|---|---|---|
> | 1 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
>
> TM pre-screen direction pre-generated for all 75 candidates.
> Full shortlist (top 20) saved to:
> - `product-naming-shortlist-<date>.user.md` (source of truth)
> - TM direction: `product-naming-tm-<date>.txt`
>
> **Next:** Review the TM direction file for your preferred picks. To select a name, say which one. To reject and try again, say "none of these work" — optionally tell me why and I'll encode it as a constraint for Round 2.

---

## Integration

**Upstream (ASSESSMENT-11/12):**
- Reads `<YYYY-MM-DD>-brand-identity-dossier.user.md` (ASSESSMENT-11) for personality and aesthetic constraints.
- ASSESSMENT-12 (dossier promotion gate) should be run before this skill but is not enforced by GATE-ASSESSMENT-01. If the dossier is still Draft, proceed with a provisional note.

**Upstream (ASSESSMENT-03):**
- Reads the confirmed product option selection as the primary product type input.

**Downstream (ASSESSMENT-14):**
- `product-naming-shortlist-<date>.user.md` is the source for the confirmed product name used by `/lp-do-assessment-14-logo-brief`. ASSESSMENT-14 uses the confirmed Line Name (and Full Compound) to inform the mark type decision and wordmark feasibility check.

**Downstream (ASSESSMENT-15):**
- `/lp-do-assessment-15-packaging-brief` reads the confirmed product name for the Structural Format section.

**GATE-ASSESSMENT-01:** The shortlist artifact (`product-naming-shortlist-<date>.user.md`) must exist and have an operator-confirmed selection before GATE-ASSESSMENT-01 allows ASSESSMENT→MEASURE transition.
