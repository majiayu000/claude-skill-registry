---
name: lp-design-spec
description: Translate a feature requirement into a concrete frontend design specification mapped to the design system, theme tokens, and per-business brand language. Sits between fact-find and plan.
---

# Design Spec

Produce a design specification that maps a feature requirement to concrete design-system components, semantic tokens, and layout decisions — grounded in the business's brand language. Feeds directly into `/lp-do-plan` to raise confidence on UI tasks.

## Operating Mode

**ALLOWED:** Read codebase, read docs, read theme tokens, create/update design spec docs, create/update brand language docs.
**NOT ALLOWED:** Write application code, modify components, change tokens, run builds. Design only — implementation is `/lp-do-build`'s job.

## When to Use

- New page, section, or significant UI component
- Visual refresh or rebrand work
- Any feature where fact-find flags `Design-Spec-Required: yes`
- When `/lp-do-plan` produces low-confidence UI tasks (design decisions unmade)
- Standalone brand language bootstrapping for a new business

## Invocation

### Fast Path

```
/lp-design-spec <feature-slug>
```

Expects `docs/plans/<feature-slug>-fact-find.md` to exist. Reads it, resolves the business unit, loads brand language, and begins spec creation.

### Discovery Path

```
/lp-design-spec
```

No argument — presents the app-to-business mapping and asks what you're designing for.

### Brand Bootstrap Mode

```
/lp-design-spec --bootstrap <BIZ-CODE>
```

Runs GATE-BD-07 pre-flight for the business unit without producing a feature design spec. Blocks and redirects to `/lp-assessment-bootstrap <BIZ>` if Brand Dossier is not Active. Use when checking brand-dossier readiness before onboarding a new business.

## Inputs

| Source | Path | Purpose |
|--------|------|---------|
| Business registry | `docs/business-os/strategy/businesses.json` | Resolve app → business unit → theme package |
| Brand language | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | Per-business visual identity, tone, audience |
| Design profile | `packages/themes/<theme>/src/design-profile.ts` | Art-direction defaults and guidance for the brand |
| Theme assets | `packages/themes/<theme>/src/assets.ts` | Available fonts, gradients, shadows, keyframes, brand colors |
| Recipe catalogue | `packages/themes/<theme>/src/recipes.ts` | Branded surface compositions and page motifs |
| Theme tokens | `packages/themes/<theme>/src/tokens.ts` | Concrete token values for the target app |
| Base tokens | `packages/themes/base/src/tokens.ts` | Default token system (overridden by theme) |
| Design system handbook | `docs/design-system-handbook.md` | Component catalog, atomic design layers |
| Token reference | `.claude/skills/tools-design-system/SKILL.md` | Quick-reference for token classes |
| Typography & color | `docs/typography-and-color.md` | Font model, HSL system, dark mode |
| Fact-find (optional) | `docs/plans/<slug>-fact-find.md` | Feature context, audience, requirements |

### App-to-Business Resolution

Use `businesses.json` to resolve which business owns the target app, then locate:
1. **Brand language doc**: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`
2. **Theme package**: `packages/themes/<theme>/` (mapped from app name)
3. **Strategy context**: `docs/business-os/strategy/<BIZ>/plan.user.md`

**Resolution:** Read `docs/business-os/strategy/businesses.json` to resolve app → business unit → theme package. Do not use hardcoded mappings.

## Workflow

### Step 0: Context Resolution

1. **Identify the target app** from the feature slug, fact-find, or user input.
2. **Resolve business unit** via `businesses.json`.
3. **Load brand language** doc. If it doesn't exist or Status ≠ Active:
   - **STOP.** Emit GATE-BD-07 error (see Step 6).
   - Do NOT offer to proceed without brand language.
4. **Load design profile** from `packages/themes/<theme>/src/design-profile.ts` — art-direction defaults and guidance for the brand. If the file does not exist, note that the theme has no design profile (use base defaults).
5. **Load theme assets** from `packages/themes/<theme>/src/assets.ts` — available fonts, gradients, shadows, keyframes, brand colors. If the file does not exist or exports empty collections, note that the brand has no custom assets.
6. **Load recipe catalogue** from `packages/themes/<theme>/src/recipes.ts` — branded surface compositions. If the file does not exist or is empty, note that no recipes exist yet.
7. **Load theme tokens** for the target app's theme package.
8. **Load fact-find** if a feature slug was provided.

### Step 1: Audience and Intent

Extract from brand language + fact-find:

- **Who sees this?** Target demographic, device context, usage scenario.
- **What feeling?** Brand personality (from brand language `## Voice & Tone`).
- **What action?** Primary CTA or user goal for this feature.
- **Where in the app?** Navigation context — is this a new page, a section in an existing page, a modal, a flow?

If any of these are unclear, ask the user. Do not assume.

### Step 2: Current State Audit (Modification Only)

Skip this step for net-new pages/components.

For modifications to existing UI:
1. **Read the current component(s)** being modified.
2. **Identify existing patterns**: layout structure, component choices, token usage.
3. **Flag violations**: arbitrary values, hardcoded colors, missing dark mode, accessibility gaps.
4. **Note reusable elements**: what should be preserved vs. replaced.

### Step 3: Component Map

Using the three-tier architecture (`@acme/design-system` → `@acme/ui` → app-level):

1. **List existing components** that can be reused for this feature.
   - Search `packages/design-system/src/` for primitives/atoms/molecules.
   - Search `packages/ui/src/` for domain components.
   - Search the target app's `src/components/` for app-specific components.
2. **Identify gaps** — components that don't exist yet.
3. **Decide layer** for new components:
   - Pure presentation, no domain logic → `@acme/design-system`
   - Domain-specific (e-commerce, booking, etc.) → `@acme/ui`
   - App-specific, unlikely to be shared → app-level `src/components/`

Output a component tree showing the composition hierarchy.

### Step 4: Token Binding

For each visual property in the design, specify the exact semantic token:

| Property | Token | Value (from theme) | Rationale |
|----------|-------|---------------------|-----------|
| Primary action bg | `bg-primary` | `hsl(6 78% 57%)` | Brand coral per brand language |
| Body text | `text-fg` | (from base) | Default readable text |
| Card/surface-2 bg | `bg-[hsl(var(--surface-2))]` | (from base) | Standard surface pattern |
| ... | ... | ... | ... |

**Rules:**
- Every color must map to a semantic token. No hex, no Tailwind palette colors.
- Reference `tools-design-system` skill for the canonical token list.
- If a needed token doesn't exist, document it as a prerequisite (new token to add to theme package).
- Dark mode: verify every chosen token has a dark variant. Flag gaps.

**Evidence requirement:** For each token binding, cite the source file and token key where the value is defined (e.g., `packages/themes/prime/src/tokens.ts → --color-primary`). If no theme package exists, cite `packages/themes/base/src/tokens.ts`.

### Step 5: Layout and Behavior

Define:

1. **Layout skeleton** — CSS Grid/Flexbox structure with responsive breakpoints.
   - Mobile-first. Specify `md:` and `lg:` breakpoint changes.
   - Use design system spacing tokens only (`gap-4`, `p-6`, etc.).
2. **Interaction states** — hover, active, disabled, loading, error, empty.
   - Map each state to token classes (e.g., `hover:bg-primary-hover`).
3. **Accessibility** — WCAG AA minimum:
   - Focus order (tab sequence).
   - ARIA roles/labels for non-standard elements.
   - Contrast compliance (note if any token combinations need checking).
   - Touch target sizes (`min-h-11 min-w-11` for interactive elements).
4. **Animation** — only if required. Use `motion-safe:` prefix. Respect `prefers-reduced-motion`.

### Step 6: Brand Dossier Pre-flight (GATE-BD-07)

**Before writing the design spec**, verify the Brand Dossier is Active:

1. **Check** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` exists AND frontmatter `Status: Active`.
2. **Check** the strategy index `docs/business-os/strategy/<BIZ>/index.user.md` — Brand Dossier row must show `Active`.

**Gate result:**

- **PASS** (Status == Active): proceed to Step 7.
- **FAIL** (missing or Status != Active): **STOP immediately.**
  - Error: `GATE-BD-07: Brand Dossier must be Active before running design spec.`
  - Remediation: `Run /lp-do-assessment-11-brand-identity --business <BIZ> to create the Brand Dossier, then have the operator promote it to Active before re-running /lp-design-spec.`
  - Do NOT create or populate <YYYY-MM-DD>-brand-identity-dossier.user.md from within this skill. That is the job of `/lp-assessment-bootstrap`.

**Note:** GATE-BD-01 at S1 advance requires brand-dossier at Draft minimum. GATE-BD-07 here requires Active. The gap (Draft → Active) is the operator's responsibility before running lp-design-spec.

**Exception — Base-System businesses:** For businesses whose theme resolves to `packages/themes/base/` and which have no customer-facing brand identity (e.g. PLAT, BOS, PIPE, XA), the Brand Dossier gate is waived. Use `packages/themes/base/src/tokens.ts` directly as the design reference. Add a note to the design spec frontmatter: `Brand-Language: None — base theme (no brand dossier for this business)`. To confirm a business is base-system, read `docs/business-os/strategy/businesses.json`.

### Step 7: Write Design Spec

Create `docs/plans/<feature-slug>-design-spec.md` using the template below.

### Step 8: Brand Language Feedback Loop

After completing the spec, check if any design decisions made during this spec should feed back into the brand language doc:

- **New pattern established** (e.g., "cards in this app always use `rounded-lg shadow-sm`") → add to brand language `## Signature Patterns`.
- **Token gap filled** (e.g., new token added for this business) → update brand language `## Token Overrides`.
- **Audience insight** (e.g., fact-find revealed new demographic data) → update brand language `## Audience`.

Only update with decisions that are **stable and reusable**, not one-off feature specifics.

## Design Spec Template

```markdown
---
Type: Design-Spec
Status: Draft
Feature-Slug: {slug}
Business-Unit: {BIZ}
Target-App: {app-name}
Theme-Package: {theme-package}
Brand-Language: docs/business-os/strategy/{BIZ}/<YYYY-MM-DD>-brand-identity-dossier.user.md | None — base theme
Surface-Mode: {marketing | editorial | operations | campaign}
Created: {DATE}
Updated: {DATE}
Owner: {operator}
---

# Design Spec: {Feature Title}

## Context

**Business:** {business name} ({BIZ})
**App:** {app name}
**Audience:** {from brand language}
**Device:** {mobile-only | responsive | desktop-first}
**Surface Mode:** {marketing | editorial | operations | campaign} — {one sentence justification}

**Feature goal:** {one sentence — what the user accomplishes}

**Fact-find:** `docs/plans/{slug}-fact-find.md` _(or "standalone spec")_

## Design Character

Baseline profile for this brand (from `design-profile.ts`):

- **Radius:** {defaultRadius value, e.g., "sm — small corners"}
- **Elevation:** {defaultElevation value, e.g., "flat — no shadows on surfaces"}
- **Border:** {defaultBorder value, e.g., "subtle — light borders on containers"}
- **Color strategy:** {colorStrategy value, e.g., "restrained — primary + one accent, used sparingly"}
- **Whitespace:** {whitespace value, e.g., "generous — breathing room between sections"}
- **Typography scale:** {scaleRatio value, e.g., "1.25 — moderate size contrast"}
- **Motion:** {motionPersonality value, e.g., "precise — ease-out, no bounce"}

_{If design-profile.ts does not exist for this theme, state "No design profile — using base defaults."}_

## Available Assets

From `assets.ts` for this theme:

- **Fonts:** {list heading and body fonts, or "None — using base font stack"}
- **Gradients:** {list named gradients, or "None"}
- **Shadows:** {list brand shadows, or "None — using token shadow scale"}
- **Keyframes:** {list named animations, or "None"}
- **Brand colors:** {list named brand colors beyond semantic palette, or "None"}

_{If assets.ts does not exist or is empty, state "No custom assets — using base tokens."}_

## Applicable Recipes

From `recipes.ts` for this theme, filtered by surface mode ({mode}):

- {recipe name}: {description} — {usage context}
- ...

_{If no recipes match the surface mode or recipes.ts is empty, state "No applicable recipes — compose from profile defaults and tokens."}_

## Visual Intent

{2-3 sentences describing the desired look and feel, referencing brand language personality, design character from profile, and any specific inspiration. Not a mockup — a north star for implementation decisions.}

## Component Map

### Reused Components

| Component | Package | Usage |
|-----------|---------|-------|
| `Button` | `@acme/design-system` | Primary CTA |
| ... | ... | ... |

### New Components Needed

| Component | Target Package | Rationale |
|-----------|---------------|-----------|
| `{Name}` | `{package}` | {why it doesn't exist yet} |

### Composition Tree

```
PageLayout
├── Header (existing)
├── {SectionName}
│   ├── {Component}
│   │   ├── {Child}
│   │   └── {Child}
│   └── {Component}
└── Footer (existing)
```

## Token Binding

| Element | Property | Token Class | Dark Mode | Notes |
|---------|----------|-------------|-----------|-------|
| Page bg | background | `bg-bg` | auto | |
| Primary CTA | background | `bg-primary` | auto | Brand: {color description} |
| ... | ... | ... | ... | ... |

**New tokens required:**
- _{none, or list with rationale}_

## Layout

### Mobile (default)
{Description or ASCII sketch of mobile layout}

### Tablet (`md:` 768px+)
{Changes from mobile}

### Desktop (`lg:` 1024px+)
{Changes from tablet}

**Spacing:** {key spacing decisions, e.g., "section padding: p-6, card gap: gap-4"}

## Interaction States

| Element | Hover | Active | Disabled | Loading | Error |
|---------|-------|--------|----------|---------|-------|
| Primary CTA | `hover:bg-primary/90` | `active:bg-primary/80` | `opacity-50 cursor-not-allowed` | spinner | - |
| ... | ... | ... | ... | ... | ... |

## Accessibility

- **Focus order:** {tab sequence description}
- **ARIA:** {roles, labels, live regions needed}
- **Contrast:** {any combinations to verify}
- **Touch targets:** All interactive elements `min-h-11 min-w-11`
- **Screen reader:** {any visually-hidden text needed}

## Prerequisites for Plan

- [ ] Brand language: either Active brand dossier at `docs/business-os/strategy/{BIZ}/<YYYY-MM-DD>-brand-identity-dossier.user.md` OR confirmed base-system business (PLAT/BOS/PIPE/XA) — check `businesses.json`
- [ ] Theme package exists: `packages/themes/{theme}/`
- [ ] All required tokens exist (see "New tokens required" above)
- [ ] All reused components verified in component catalog

## Notes

{Any open questions, alternatives considered, or links to reference implementations}

## QA Matrix

Pre-populate from the Token Binding and Layout sections above.
`lp-design-qa` uses this table as its expected-state baseline.

| Element | Expected token / class | QA domain | Check ID |
|---------|------------------------|-----------|----------|
| Page bg | `bg-bg` | tokens | TC-01 |
| Primary CTA | `bg-primary` | tokens + visual | TC-01, VR-02 |
| Body text | `text-fg` | tokens | TC-01 |
| Focus ring | `focus-visible:ring-2 ring-primary` | a11y | A11Y-03 |
| Mobile layout | single-column stack at `< 768px` | responsive | RS-01 |
| ... | ... | ... | ... |

*One row per token-bound element or responsive rule. Remove placeholder rows before handoff to plan.*
```

## Quality Checks

- [ ] Every color references a semantic token — zero arbitrary values
- [ ] Component map distinguishes reused vs. new, with correct package layer
- [ ] Layout specifies all three breakpoints (mobile, tablet, desktop)
- [ ] Dark mode addressed for every token binding
- [ ] Accessibility section is non-empty with concrete ARIA/focus/contrast items
- [ ] Brand Dossier Active (GATE-BD-07 pre-flight passed: Status == Active in <YYYY-MM-DD>-brand-identity-dossier.user.md)
- [ ] Token bindings match actual values in theme package (not invented)
- [ ] Prerequisites list is complete — no hidden assumptions for `/lp-do-plan`
- [ ] `Surface-Mode` field is set in frontmatter with justification in Context section
- [ ] Design Character section populated from design profile (or noted as absent)
- [ ] Available Assets section populated from assets.ts (or noted as absent)
- [ ] Applicable Recipes section populated from recipes.ts filtered by surface mode (or noted as empty)

## Integration

### With `/lp-do-fact-find`

When a fact-find classifies a feature as UI-heavy, it should add to its output:

```yaml
Design-Spec-Required: yes
```

This signals that `/lp-design-spec` should run before `/lp-do-plan`.

### With `/lp-do-plan`

Plan reads the design spec and uses it to:
- Pre-populate `Affects` lists with component file paths from the component map
- Set higher confidence on UI tasks (design decisions already made)
- Create concrete validation contracts referencing the spec's token bindings
- Generate prerequisite tasks for missing tokens or components

### With `/lp-do-build`

During build, the design spec serves as a reference:
- Exact token classes to use (no guessing)
- Component composition tree to follow
- Accessibility requirements to implement and test

### With Brand Language Docs

**Reads from:** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`
**Writes back to:** Same file, when stable new patterns emerge (Step 8).

This creates a virtuous cycle: each design spec strengthens the brand language, which makes future specs faster and more consistent.

## Hand-off Messages

### Spec Complete (has fact-find)

> Design spec complete: `docs/plans/{slug}-design-spec.md`
>
> **Component map:** {N} reused, {M} new components needed.
> **Prerequisites:** {list any blockers for plan}.
>
> Ready for `/lp-do-plan {slug}`. The plan should reference this spec for UI task confidence.

### Spec Complete (standalone)

> Design spec complete: `docs/plans/{slug}-design-spec.md`
>
> This is a standalone spec (no fact-find). To proceed:
> 1. `/lp-do-fact-find {slug}` — if the feature needs broader investigation
> 2. `/lp-do-plan {slug}` — if scope is clear and you want to go straight to planning

### GATE-BD-07 Blocked (Brand Dossier not Active)

> **GATE-BD-07:** Brand Dossier must be Active before running design spec.
>
> **Current Status:** `docs/business-os/strategy/{BIZ}/<YYYY-MM-DD>-brand-identity-dossier.user.md` is missing or Status ≠ Active.
>
> **Remediation:** Run `/lp-do-assessment-11-brand-identity --business {BIZ}` to create the Brand Dossier, then promote to Active before re-running `/lp-design-spec`.

## Red Flags (Invalid Run)

1. Spec contains arbitrary color values (`[#hex]`, `bg-red-500`, etc.)
2. Component map places domain components in `@acme/design-system`
3. No accessibility section or "N/A" without justification
4. Brand language not consulted and no explicit opt-out rationale
5. Token bindings reference tokens that don't exist in the theme package without noting them as prerequisites
6. Layout section missing responsive breakpoints
