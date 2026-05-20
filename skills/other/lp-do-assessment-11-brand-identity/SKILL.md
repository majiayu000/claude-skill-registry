---
name: lp-do-assessment-11-brand-identity
description: Visual brand identity for new startups (ASSESSMENT-11). Reads brand-strategy artifact and produces brand-dossier with colour palette, typography, imagery direction, and token overrides. Upstream of S1.
---

# lp-do-assessment-11-brand-identity — Brand Identity (ASSESSMENT-11)

Synthesizes brand strategy and product context into concrete visual identity decisions. Reads `<YYYY-MM-DD>-brand-profile.user.md` (ASSESSMENT-10 output) and the ASSESSMENT intake packet, then produces a `<YYYY-MM-DD>-brand-identity-dossier.user.md` with colour palette, typography, shape/elevation, imagery direction, and token overrides. Does not re-elicit audience or personality — these are carried forward from ASSESSMENT-10.

Load: ../_shared/assessment/assessment-base-contract.md

## Invocation

```
/lp-do-assessment-11-brand-identity --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

EXECUTE

This skill synthesizes inputs into design decisions rather than eliciting them field-by-field. The operator may not know specific hex codes or token names — this skill makes reasoned visual decisions grounded in the brand strategy and surfaces them for operator review.

Does NOT:
- Re-elicit audience, personality, or voice & tone (these come from ASSESSMENT-10)
- Require an existing app or theme package to proceed
- Skip sections — every template section must appear in the output (TBD is acceptable for Signature Patterns and App Coverage)

## Required Inputs (pre-flight)

| Source | Path | Required |
|--------|------|----------|
| Brand strategy | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-profile.user.md` | Yes — primary input; blocks if absent |
| ASSESSMENT intake packet | `docs/business-os/startup-baselines/<BIZ>/<YYYY-MM-DD>-assessment-intake-packet.user.md` | Yes — provides product context, ICP, positioning |
| Brand language template | `.claude/skills/_shared/brand-language-template.md` | Yes — structural reference |
| Theme tokens | `packages/themes/<theme>/src/tokens.ts` | No — read if a theme package exists for this business |
| Existing app UI | `apps/<app>/src/app/layout.tsx`, key pages | No — read if an app already exists |
| BRIK brand dossier (reference) | `docs/business-os/strategy/BRIK/<YYYY-MM-DD>-brand-identity-dossier.user.md` | No — reference example of a complete dossier |

If `<YYYY-MM-DD>-brand-profile.user.md` is absent, halt and emit:
> "ASSESSMENT-10 artifact not found at `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-profile.user.md`. Run `/lp-do-assessment-10-brand-profiling --business <BIZ>` first."

## Steps

### Steps 1–3: Read Context, Derive Visual Identity, Produce Token Overrides

Load: modules/steps-01-03.md

### Steps 4–6: Save Dossier, Generate HTML Preview, Report

Load: modules/steps-04-06.md

## Output Contract

**Primary path:** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`

**Secondary path (auto-produced):** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-preview.user.html`

**Frontmatter:**

```yaml
---
Type: Brand-Language
Stage: ASSESSMENT-11
Business-Unit: <BIZ>
Business-Name: <confirmed operating name>
Status: Draft
Created: <date>
Updated: <date>
Last-reviewed: <date>
Owner: <operator>
---
```

**Sections (all must be present — TBD is acceptable for Signature Patterns and App Coverage):**
- Audience
- Personality
- Visual Identity (Colour Palette, Typography, Shape & Elevation, Imagery Direction)
- Voice & Tone
- Token Overrides
- Signature Patterns
- App Coverage
- References

## Quality Gate and Red Flags

Load: modules/quality-gate.md

## Completion Message

> "Brand identity recorded: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`. Colour palette: <N> tokens. Typography: <font family>. Token overrides: <N rows>."
>
> "Brand discovery document produced: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-preview.user.html`. Open in a browser to review the visual identity."
>
> "ASSESSMENT stage complete. Next step: run `/lp-readiness --business <BIZ>` to enter S1."

---

## Integration

**Upstream (ASSESSMENT-10):** Reads `<YYYY-MM-DD>-brand-profile.user.md` as required input. Audience, Personality, and Voice & Tone sections are carried forward directly.

**Downstream (S1):** After ASSESSMENT-11 saves the brand dossier, the operator proceeds to S1 (`/lp-readiness`). There is no ASSESSMENT gate.

**Later consumption:** `/lp-design-spec` reads `<YYYY-MM-DD>-brand-identity-dossier.user.md` at DO+ and writes back stable new patterns to the Signature Patterns section. `/lp-do-build` references it for UI implementation guidance.

**Replaces:** This skill supersedes `/lp-assessment-bootstrap` as the canonical brand identity skill within the startup loop ASSESSMENT stage. `lp-assessment-bootstrap` remains available for standalone use outside the loop.
