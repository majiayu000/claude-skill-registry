---
name: lp-do-assessment-15-packaging-brief
description: Packaging design brief for new startups (ASSESSMENT-15). Conditional on physical-product profile. Reads brand identity, product naming, logo brief, and distribution plan to produce a complete packaging brief covering structural format, regulatory requirements, surface design, and designer handoff checklist.
---

# lp-do-assessment-15-packaging-brief — Packaging Brief (ASSESSMENT-15)

Produces a designer-ready packaging design brief for physical product businesses. This skill is conditional: it only runs when the business has a `physical-product` profile flag. For digital-only businesses it emits a skip message and halts cleanly.

The brief combines deterministic derivation (packaging format from product type + channel, regulatory requirements from the reference data file) with targeted operator elicitation (aesthetic preferences for surface design). It does not attempt to be a regulatory compliance audit — it produces an operator-reviewed requirements checklist sourced from `regulatory-requirements.md`.

Load: ../_shared/assessment/assessment-base-contract.md

## Invocation

```
/lp-do-assessment-15-packaging-brief --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

MIXED

- **Deterministic derivation:** structural packaging format (from product type + distribution channel), regulatory requirements checklist (from reference data file for product category)
- **Operator elicitation:** surface design aesthetic preferences (3 targeted questions only)

Does NOT:
- Perform regulatory compliance audits or provide legal advice
- Generate packaging artwork, structural dielines, or print-ready files
- Cover product categories that are out of scope for the reference data (medical devices, pharmaceuticals, electrical goods, children's toys — see regulatory-requirements.md out-of-scope section)

## Conditionality Gate (Step 1 — execute first)

**Read the business profile** to determine whether `physical-product` flag is set.

The business profile flag may be documented in:
- ASSESSMENT intake packet (Section A — business type or product profile)
- ASSESSMENT-03 option selection artifact (product category)
- Operator context document

If `physical-product` is NOT in the business profile (e.g., SaaS, digital content, service business), emit:
> "This business does not have a physical-product profile. Packaging brief (ASSESSMENT-15) is not applicable — skipping. If this changes (e.g., the business adds a physical product line), re-run `/lp-do-assessment-15-packaging-brief --business <BIZ>`."

Then halt cleanly. Do not create any output artifact.

If `physical-product` IS in the business profile, proceed to Step 2.

## Required Inputs (pre-flight)

| Source | Path | Required |
|--------|------|----------|
| Product option selection | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-option-selection.user.md` | Yes — product type and product category |
| Distribution plan | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-launch-distribution-plan.user.md` | Yes — channels determine packaging format and barcode requirement |
| Brand identity dossier | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | Yes — brand assets (colour tokens, typography) for Surface Design section |
| Product naming document | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-product-naming.user.md` | Yes — confirmed product name for label text |
| Logo brief | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-logo-brief.user.md` | Yes — logo variants for Brand Assets section |
| Regulatory reference data | `.claude/skills/lp-do-assessment-15-packaging-brief/regulatory-requirements.md` | Yes — source for Regulatory Requirements Checklist |

If `<YYYY-MM-DD>-logo-brief.user.md` is absent, halt and emit:
> "Logo brief not found at `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-logo-brief.user.md`. Run `/lp-do-assessment-14-logo-brief --business <BIZ>` first."

---

## Steps

Load: modules/steps.md

## Output Contract

Load: modules/output-template.md

## Quality Gate

Load: modules/quality-gate.md

## Completion Message

> "Packaging brief recorded: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-packaging-brief.user.md`. Structural format: [format]. Regulatory category: [category]. Regulatory checklist: [N] items. EAN barcode: [required / not required]. Designer handoff: [N] items ready, [M] items pending."
>
> "ASSESSMENT stage complete for physical-product profile. Next step: review the packaging brief with your supplier, then run `/lp-readiness --business <BIZ>` to enter S1."

---

## Integration

**Upstream (ASSESSMENT-14):**
- Reads `<YYYY-MM-DD>-logo-brief.user.md` as a required input for the Brand Assets section and Designer Handoff Checklist.

**Upstream (ASSESSMENT-13):**
- Reads `<YYYY-MM-DD>-product-naming.user.md` for the confirmed product name used in Structural Format.

**Upstream (ASSESSMENT-11):**
- Reads `<YYYY-MM-DD>-brand-identity-dossier.user.md` for colour tokens and typography used in Surface Design Scope and Print Specification Notes.

**Downstream:** This skill produces the final ASSESSMENT deliverable for physical-product profiles. The output is an operator/designer handoff document — there is no further automated ASSESSMENT skill downstream. The operator proceeds to `/lp-readiness --business <BIZ>` (S1).

**Regulatory reference data:** This skill reads `.claude/skills/lp-do-assessment-15-packaging-brief/regulatory-requirements.md` at runtime. If that file is absent, halt and emit: "Regulatory reference data not found. The file `.claude/skills/lp-do-assessment-15-packaging-brief/regulatory-requirements.md` is required for this skill to produce an authoritative checklist. Contact the system operator to restore this file."

**GATE-ASSESSMENT-01:** This skill's output (`<YYYY-MM-DD>-packaging-brief.user.md`) must exist for businesses with `physical-product` profile before GATE-ASSESSMENT-01 allows ASSESSMENT→MEASURE transition. For non-physical businesses, GATE-ASSESSMENT-01 does not require this artifact.
