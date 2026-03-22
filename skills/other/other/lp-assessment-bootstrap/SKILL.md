---
name: lp-assessment-bootstrap
description: Bootstrap a <YYYY-MM-DD>-brand-identity-dossier.user.md for a business entering the startup loop. Gathers context from strategy docs, existing UI, and theme packages, then fills the shared template. Used at S0/S1 when the doc is missing, or at DO before /lp-design-spec.
operating_mode: EXECUTE
---

# Brand Bootstrap

Initialize brand language documentation for a business in the startup loop.

> **Note**: In the startup loop ASSESSMENT stage, use `/lp-do-assessment-11-brand-identity` instead. `lp-assessment-bootstrap` remains available for standalone Draft dossier creation outside the loop. It does **not** promote Status to Active — that requires operator review and explicit confirmation.

## When to Use

- **S0/S1 gate**: Startup loop detects missing `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`
- **DO prerequisite**: `/lp-do-fact-find` flags `Design-Spec-Required: yes` but no brand language exists
- **Manual**: Operator invokes `/lp-assessment-bootstrap <BIZ>` at any time

## Inputs

| Source | Path | Required |
|--------|------|----------|
| Strategy plan | `docs/business-os/strategy/<BIZ>/plan.user.md` | Yes |
| Business registry | `docs/business-os/strategy/businesses.json` | Yes |
| Brand language template | `.claude/skills/_shared/brand-language-template.md` | Yes |
| Naming shortlist | `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/latest-naming-shortlist.user.md` | No — read if present; provides `recommended_business_name` via YAML front matter |
| Launch forecast | `docs/business-os/strategy/<BIZ>/*-launch-forecast*.user.md` | No |
| Theme package | `packages/themes/<theme>/src/tokens.ts` | No — only if app exists |
| Existing app UI | `apps/<app>/src/app/layout.tsx`, key pages | No — only if app exists |
| Existing brand doc (BRIK) | `docs/business-os/strategy/BRIK/<YYYY-MM-DD>-brand-identity-dossier.user.md` | No — reference example |

## Workflow

### Step 1: Resolve Business Context

1. Read `businesses.json` to get business name, apps, and theme mappings
2. Read strategy plan for audience, positioning, and product description
3. Read launch forecast (if exists) for demographic data and channel strategy
4. Check for naming shortlist (GATE-BD-00 output):
   - If `docs/business-os/strategy/<BIZ>/assessment/naming-workbench/latest-naming-shortlist.user.md` exists:
     - Parse YAML front matter to extract `recommended_business_name` and `shortlist` array
     - Use `recommended_business_name` as the primary name input when filling the brand dossier template
     - Include `shortlist` as context when writing the Audience and Personality sections
     - If front matter is absent or malformed: emit advisory and continue without pre-fill:
       `Advisory: Naming shortlist found at latest-naming-shortlist.user.md but front matter could not be parsed — fill business name in brand dossier manually.`
   - If file absent: skip gracefully, no message needed

### Step 2: Gather Design Evidence

If the business has an existing app:
1. Read theme tokens file for current palette, typography, spacing
2. Scan key pages (layout.tsx, homepage) for current design patterns
3. Note any hardcoded Tailwind values that bypass the token system

If the business has no app yet:
1. Note as `TBD — app not yet built`
2. Fill what you can from strategy context (audience, personality, voice)

### Step 3: Fill Template

1. Copy the template from `.claude/skills/_shared/brand-language-template.md`
2. Fill every section you have evidence for
3. Mark unknowns as `TBD — {specific thing needed}`
4. Set `Status: Draft`

### Step 4: Write and Report

1. Save to `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`
2. Report completion status:
   - Sections complete vs TBD
   - Recommended next actions to resolve TBDs
   - Whether the doc is sufficient for `/lp-design-spec` to proceed

## Quality Checks

- [ ] Template structure fully preserved (all sections present)
- [ ] All TBD items include "what's needed" rationale
- [ ] Audience section is non-TBD (minimum viable brand doc)
- [ ] Personality section has at least 3 adjective pairs
- [ ] File saved at correct path with correct frontmatter
- [ ] Status set to Draft (not Active — requires operator review)

## Integration

- **Consumed by**: `/lp-design-spec` (reads brand language for token bindings and component decisions)
- **Updated by**: `/lp-design-spec` (writes back stable patterns to Signature Patterns section)
- **Referenced by**: `/lp-do-build` (for UI implementation guidance)
- **Loop position**: S0/S1 (setup) or DO (pre-design-spec)

## Example Invocation

```
/lp-assessment-bootstrap BRIK
/lp-assessment-bootstrap HEAD
/lp-assessment-bootstrap PET
```
