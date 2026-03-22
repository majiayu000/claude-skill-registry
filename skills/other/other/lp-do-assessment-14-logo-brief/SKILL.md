---
name: lp-do-assessment-14-logo-brief
description: Logo design brief for new startups (ASSESSMENT-14). Synthesises brand identity dossier, brand profile, and product naming to produce a complete logo design brief ready to hand to a designer. Upstream of lp-do-assessment-15-packaging-brief and /lp-design-spec.
---

# lp-do-assessment-14-logo-brief — Logo Design Brief (ASSESSMENT-14)

Produces a designer-ready logo design brief by synthesising the visual identity decisions already made in ASSESSMENT-10 (brand profile) and ASSESSMENT-11 (brand identity dossier). Does not re-elicit audience or personality — those decisions are already made and carried forward. The brief specifies mark type, colour application, typography, deliverables, use cases, and constraints: everything a logo designer needs to begin without additional Q&A.

Load: ../_shared/assessment/assessment-base-contract.md

## Invocation

```
/lp-do-assessment-14-logo-brief --business <BIZ> [--app-dir <path>]
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

Optional:
- `--app-dir <path>` — path to the Next.js app (e.g. `apps/caryina`). If not provided, auto-detected from the business name (lowercase). If the directory cannot be found, logo asset deployment is skipped gracefully.

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

**ASSESSMENT-13 gate:** If no ASSESSMENT-13 product naming artifact is found (see Artifact Discovery Rule below), halt and emit:
> "ASSESSMENT-13 artifact not found matching `docs/business-os/strategy/<BIZ>/*-product-naming.user.md`. A product naming document is required before the logo brief can be produced. Run `/lp-do-assessment-13-product-naming --business <BIZ>` first."

## Operating Mode

EXECUTE

This skill synthesises existing brand strategy inputs into a logo brief. The operator does not provide field-by-field input during execution — they review the produced brief and confirm or request amendments.

The skill makes reasoned decisions about mark type, deliverables, and use cases based on the brand strategy inputs. These are design recommendations for operator review, not fixed specifications.

Does NOT:
- Re-elicit audience, personality, or voice & tone (ASSESSMENT-10)
- Re-elicit colour palette or typography (ASSESSMENT-11)
- Run automated trademark searches
- Produce a designer-quality logo — Steps 12–14 produce a functional text-based SVG from brand fonts; a professional designer refines these into production artwork

## Required Inputs (pre-flight)

| Source | Glob pattern | Required |
|--------|------|----------|
| Brand identity dossier | `*-brand-identity-dossier.user.md` | Yes — primary input; blocks if absent |
| Brand profile | `*-brand-profile.user.md` | Yes — personality adjective pairs, positioning constraints |
| Product naming document | `*-product-naming.user.md` | Yes — confirmed business name, product name, brand-product relationship pattern |
| Distribution plan | `*-launch-distribution-plan.user.md` | No — read if present; informs Use Case List |

All globs are relative to `docs/business-os/strategy/<BIZ>/`.

If no brand identity dossier is found, halt and emit:
> "Brand identity dossier not found matching `docs/business-os/strategy/<BIZ>/*-brand-identity-dossier.user.md`. Run `/lp-do-assessment-11-brand-identity --business <BIZ>` first."

If no brand profile is found, halt and emit:
> "Brand profile not found matching `docs/business-os/strategy/<BIZ>/*-brand-profile.user.md`. Run `/lp-do-assessment-10-brand-profiling --business <BIZ>` first."

---

## Artifact Discovery Rule

**CRITICAL: apply this rule for every required and optional input before reading any file beyond frontmatter (i.e., only frontmatter may be read during discovery).**

Frontmatter is defined as the YAML block at the top of the file, bounded by `---` delimiters. Read only those lines to determine `Updated:` — do not read the rest of the file content until selection is complete.

For each glob pattern, collect all matching files in `docs/business-os/strategy/<BIZ>/`.

**`Updated:` format and parsing:**
- Accepted formats: `YYYY-MM-DD` (preferred), or ISO 8601 with time (`YYYY-MM-DDTHH:MM:SSZ` / `YYYY-MM-DDTHH:MM:SS±HH:MM`).
- If timestamps are present across candidates, compare full timestamps (not just dates).
- If a value is absent or unparseable (e.g., "Feb 2, 2026"), treat it as missing and emit a warning: `Unparseable Updated: <value> in <filename>; ignored for selection.`

Selection order (deterministic):
1. Parse `Updated:` from frontmatter of each candidate. Select the file with the **latest `Updated:` value**.
2. If `Updated:` is absent or unparseable in all candidates, fall back to the **latest `YYYY-MM-DD` prefix in the filename**.
3. If multiple files tie on the same date (or tie after timestamp comparison), choose the **lexicographically last filename** and emit a warning listing all ties.

Record the exact filename selected for each input — these are included in the output contract frontmatter (see `Inputs:`) and in the completion report.

All gate error messages reference the glob pattern, not a single `<YYYY-MM-DD>` path.

---

## Steps

Load: modules/steps-01-10.md
Load: modules/steps-11-15.md

## Output Contract

Load: modules/output-template.md

## Quality Gate

Load: modules/quality-gate.md

## Completion Message

> "Logo design brief recorded: `docs/business-os/strategy/<BIZ>/<date>-logo-brief.user.md`."
>
> "Inputs used: [list exact filenames]. Mark type: [type]. [N] lockup variants. [N] use cases. Forbidden territory: [N] constraints. Wordmark feasibility: [feasible / designer recommended]."
>
> "[Name reconciliation note if names differed — or omit.]"
>
> "AI mock-up prompt ready in Section 9 — paste into ChatGPT (GPT-4o with image generation) to generate concept-quality logo mockups for review before briefing a designer."
>
> **Logo assets deployed to `<app-dir>/public/`:** favicon.svg, apple-touch-icon.png, icon-192.png, icon-512.png, og-image.webp, site.webmanifest. Layout metadata updated in `<app-dir>/src/app/layout.tsx`.
>
> — OR, if app-dir not found —
>
> **Logo assets not deployed** — app directory `apps/<name-lowercase>` not found. When the app is ready, run:
> `` node scripts/generate-logo-assets.mjs --app-dir <dir> --name "<name>" --icon-char "<char>" --primary "<hex>" --accent "<hex>" --bg "<hex>" --font-family "<family>" ``
> Then add the metadata block to `<app-dir>/src/app/layout.tsx` (see Step 15 in SKILL.md).
>
> "Next steps: share this brief with a logo designer, OR run `/lp-do-assessment-15-packaging-brief --business <BIZ>` if this is a physical product business."

---

## Integration

**Upstream (ASSESSMENT-13):**
- Reads `*-product-naming.user.md` as required input. The confirmed **business name** is the source of truth for the logotype name. The product name informs the brand–product relationship note (and whether any descriptor lockup is needed), but typically does not appear in the primary logo for compound patterns.

**Upstream (ASSESSMENT-11/12):**
- Reads `*-brand-identity-dossier.user.md` as the primary source for Colour Specification and Typography Specification. The dossier must exist; if it remains at Draft status (ASSESSMENT-12 not yet run), proceed with a provisional note.

**Downstream (ASSESSMENT-15):**
- `/lp-do-assessment-15-packaging-brief` reads `*-logo-brief.user.md` for the Brand Assets section of the packaging brief.

**Downstream (/lp-design-spec):**
- `/lp-design-spec` reads the brand dossier and (if present) the logo brief for the Logo Brief section populated by TASK-05 in the brand language template.

**Logo asset deployment (Steps 12–15):**
- Shared generation script: `scripts/generate-logo-assets.mjs` — accepts brand token params and app-dir, produces all rasters + `site.webmanifest`.
- Full ASSESSMENT-14 completion = brief doc + SVG source files + rasters deployed to `<app-dir>/public/` + layout.tsx metadata wired.
- If app-dir is not found at brief time, the deployment command is included in the Completion Message for later execution.
- If a designer later supplies production SVG/PNG files, re-run the script with the designer files placed as `logo-wordmark.svg` and `logo-icon.svg` in `<app-dir>/public/`, and re-run raster generation only (or pass them directly to Playwright via the script's render path).

**GATE-ASSESSMENT-01:** This skill's output (`*-logo-brief.user.md`) must exist and pass quality gate before GATE-ASSESSMENT-01 allows ASSESSMENT→MEASURE transition.
