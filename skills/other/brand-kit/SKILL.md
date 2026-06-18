---
name: brand-kit
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Extract visual identity from screenshots (primary) or website URL (fallback) and compile into a DESIGN.md-format brand kit — YAML token frontmatter (colors, typography, rounded, spacing, components) + 8 ordered prose sections. The YAML tokens are machine-authoritative; downstream visual skills consume them directly. Writes to marketing/brand/brand-kit.md. Triggers - "brand kit", "brand identity", "visual identity", "design tokens", "extract brand", "DESIGN.md"
goal: Extract visual identity from screenshots or website into a DESIGN.md-format brand kit with YAML token frontmatter + 8 prose sections.
outcome: marketing/brand/brand-kit.md with machine-authoritative tokens (colors, typography, rounded, spacing, components) + human-readable prose.
primitive: research
ontology_type: brand-kit
review_gate: 2
inputs:
  required: []
  recommended:
    []
outputs:
  - type: brand-kit
    feeds_into:
      - landing-page-wireframe
      - ad-creative-brief
      - sales-deck
owned_by_agent: researcher
mcps_used:
  - exa
triggers:
  slash_commands:
    - /brand-kit
status: draft
---

# brand-kit — Stage 1 + 2 research skill (PMM spine)

Compiles visual identity into a structured brand kit. Output format: DESIGN.md (YAML token frontmatter + 8 prose sections). The YAML tokens are the machine-authoritative source — downstream skills that produce visual output (landing-page wireframes, ad creative briefs, slide decks) consume the tokens directly.

---

## When to use

- When the team refreshes visual identity (new color palette, new typography system)
- Before building any landing page, ad creative, or designed artifact — they need the brand kit as input
- Quarterly refresh

## When NOT to use

- For voice / tone (use `/tov-guidelines` — voice + visual are separate but both live in `marketing/brand/`)
- For positioning or messaging (use `/positioning` or `/product-messaging`)
- For one-off design checks (write a custom gate skill that reads `brand-kit.md` tokens)

## How it works

1. Inputs: screenshots of your product / website (primary, higher fidelity) OR website URL (fallback, lower fidelity).
2. Reads: visual content via Claude's vision (screenshots) or Exa MCP web fetch (URL).
3. Extracts: exact colors (hex codes), typography stack (font family + sizes + weights + line heights + letter spacing), spacing scale, corner radii, component patterns (button states, card styles, input styles, etc.).
4. Produces a DESIGN.md-format brand kit:
   - **YAML token frontmatter** (machine-authoritative): colors, typography, rounded, spacing, components — token references use `{path.to.token}` syntax
   - **8 ordered prose sections**: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts
5. Validates against the design-production doctrine: ≤2 brand colors active per screen, ≤2 font weights per screen, ≤10% accent coverage, no banned patterns (gradient text, side-stripe borders, hero-metric template, icon-tile-above-heading template, cardocalypse, glassmorphism).
6. Writes to `marketing/brand/brand-kit.md` (overwrites prior canonical; git history preserves prior versions).

## Invoke

```
/brand-kit screenshots: [paths to product screenshots]
```

Or URL-fallback:
```
/brand-kit https://yourdomain.com — extract visual identity
```

## Example output

See [`marketing/brand/brand-kit.md`](../../../marketing/brand/brand-kit.md) for the PulseAnalytics seed. Notice the YAML frontmatter is the source of truth; the prose body explains intent. Token references use `{path.to.token}` syntax — every component reference resolves to a defined token. Do's and Don'ts encode quantitative limits (≤2 font weights per screen, ≤10% accent coverage).

## Dependencies

- **Reads from:** source visual content (screenshots or URL — provided as input)
- **Reads via Exa MCP (optional):** website if URL-fallback path is used
- **Writes to:** `marketing/brand/brand-kit.md` (canonical)
- **Downstream readers:** `/landing-page-wireframe`, `/landing-page-copy`, `/ad-creative-brief`, `/sales-deck`, `/linkedin-carousels`, any visual-output skill

## Customization

Add custom token categories if your brand requires them (e.g., `motion` tokens for animation timing, `iconography` tokens for icon style). The YAML frontmatter accepts arbitrary top-level keys; downstream skills consume whatever exists.

Update the Do's and Don'ts when you spot a recurring violation in produced artifacts — add a rule, downstream skills enforce it on next run.

## Where this fits in the Example 1 chain

```
Week 1: /brand-kit (parallel with positioning + voice research) → visual identity locked
Week 2: /landing-page-wireframe + /landing-page-copy read brand kit + messaging
Week 3+: every visual-output skill reads brand kit
```

## Refresh cadence

Quarterly. Trigger sooner on visual identity refresh, new product launch with distinct visual treatment, or major brand update.

## Design production doctrine

See `.claude/rules/design-production.md` (in the Genesys workspace; not duplicated here) for the integration contract — how YAML tokens flow into CSS variables (web), Figma variables (design), and slide / image templates (non-web).
