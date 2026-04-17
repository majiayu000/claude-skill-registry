---
name: design-md
description: Create or fetch DESIGN.md design system files in the Google Stitch 9-section format. Fetch reference designs from 68 brands (Linear, Stripe, Vercel, etc.) via getdesign CLI, or generate scaffolds from existing CSS custom properties and Tailwind tokens. Pairs with minoan-frontend-design for implementation. Triggers on "DESIGN.md", "create design system file", "extract design tokens", "codify the design", "getdesign", "make it look like [brand]".
---

# DESIGN.md — Design System Library & Generator

DESIGN.md is a plain-text design system document in the [Google Stitch](https://stitch.withgoogle.com/docs/design-md/format/) 9-section format that AI agents read to generate consistent UI. It is the token layer between design intent (`.design-context.md` from `/shape`) and implementation (`/minoan-frontend-design`).

## Two Workflows

### Workflow A: Fetch a reference DESIGN.md

Use the `getdesign` CLI to fetch from a library of 68 brand design systems:

```bash
npx getdesign@latest add <brand>        # Drops DESIGN.md into project root
npx getdesign@latest add stripe --out ./docs/DESIGN.md  # Custom output path
npx getdesign@latest list               # Show all 68 available brands
```

Available brands include: airbnb, apple, claude, cursor, figma, framer, linear.app, nike, notion, shopify, spotify, stripe, supabase, tesla, vercel, and 53 more. Each is a ~350-line file with exact hex values, font stacks, component specs, shadow systems, and responsive breakpoints.

After fetching, `/minoan-frontend-design` reads the DESIGN.md during implementation (its QA normalize step aligns output with project DESIGN.md tokens).

### Pre-fetched Library

All 68 brand DESIGN.md files can be pre-fetched into a local reference library:

```bash
bash ~/.claude/skills/design-md/scripts/fetch_all_design_md.sh         # Fetch all 68
bash ~/.claude/skills/design-md/scripts/fetch_all_design_md.sh --force # Re-fetch
```

The library lives at `~/.claude/skills/design-md/library/<brand>/DESIGN.md`. Read any brand directly without running npx:

```bash
cat ~/.claude/skills/design-md/library/stripe/DESIGN.md
```

The `library/` directory is gitignored — it's a local cache, not distributed with the skill.

### Workflow B: Generate a custom DESIGN.md

Extract design tokens from an existing project's CSS and scaffold a DESIGN.md:

```bash
python3 ~/.claude/skills/design-md/scripts/generate_design_md.py <project-path>
python3 ~/.claude/skills/design-md/scripts/generate_design_md.py . --output DESIGN.md
```

The script scans for CSS files containing `@theme` blocks (Tailwind CSS 4), `:root` custom properties, font declarations, shadows, border radii, and breakpoints. It organizes extracted tokens into the 9-section format with TODO placeholders for prose sections (Visual Theme, Do's/Don'ts) that require human or Claude completion.

After generating the scaffold, fill in the prose sections using project context — the conceptual direction, the atmosphere, the design guardrails. The format spec is at `references/design-md-format.md`.

## The 9-Section Format

| # | Section | Content |
|---|---------|---------|
| 1 | Visual Theme & Atmosphere | Prose: mood, philosophy, conceptual direction |
| 2 | Color Palette & Roles | Grouped: semantic name + hex + functional role |
| 3 | Typography Rules | Font families, hierarchy table (size/weight/tracking/line-height) |
| 4 | Component Stylings | Buttons, cards, inputs, nav — CSS values + states |
| 5 | Layout Principles | Spacing scale, grid, whitespace philosophy, border-radius scale |
| 6 | Depth & Elevation | Shadow system table, surface hierarchy |
| 7 | Do's and Don'ts | Design guardrails and anti-patterns |
| 8 | Responsive Behavior | Breakpoints table, touch targets, collapsing strategy |
| 9 | Agent Prompt Guide | Quick color reference for copy-paste |

See `references/design-md-format.md` for the full annotated spec with examples for each section.

## Pipeline Integration

```
/shape → .design-context.md (intent: audience, mood, anti-goals)
/design-md → DESIGN.md (tokens: hex values, font stacks, shadow systems)
/minoan-frontend-design → implementation (creative direction + materials)
/design-audit + /design-polish → refinement
```

`.design-context.md` and `DESIGN.md` are complementary:
- **`.design-context.md`** captures *who* and *why* — audience, aesthetic direction, design dials (DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY), anti-goals
- **`DESIGN.md`** captures *what exactly* — hex colors, font-size/weight/tracking tables, padding values, shadow stacks, breakpoints

Both live in the project root. `/minoan-frontend-design` consumes both — creative direction from the design context, materials from the design tokens. Tokens are materials, not recipes: creative direction still leads.

## When Not to Use This Skill

- For pattern research (how do other design systems implement tabs?), use `/component-gallery`
- For creative direction and UI implementation, use `/minoan-frontend-design`
- For pre-code design briefs, use `/shape`
- For visual effects (shaders, WebGL), use `/grainient` or `/rocaille-shader`
