---
name: vellum-editorial
description: "Scaffold editorial documentation sites with the Vellum design system — OKLCH palette, Bodoni Moda / Source Serif 4 / Inconsolata typography, crosshatch texture, 20+ semantic components (state cards, parity matrices, debugger panels, ring visualizations, phase timelines, glossaries). Static HTML, zero build step. Use when building competitive intelligence pages, internal documentation, roadmaps, or multi-page static sites that need a designed, non-generic aesthetic."
argument-hint: [project-name]
---

Build editorial documentation sites with the Vellum design system. Warm parchment tones, OKLCH color science, three-font typographic hierarchy, 20+ semantic components. Static HTML with zero build step — deploys to Cloudflare Pages, GitHub Pages, or any static host.

## Creative Direction

The aesthetic is "vellum manuscript" — warm cream backgrounds with a subtle SVG crosshatch texture, deep ink-brown text, copper accents, editorial typography with dramatic scale jumps. Not dark mode, not minimalist — warm and authoritative, like a well-made journal.

If the `minoan-frontend-design` skill is available, read it for broader aesthetic principles. Vellum encodes those principles into a concrete design system. Pages built with Vellum should score 16+/20 on `/design-audit` and 28+/40 on `/design-critique`.

## Quick Start

Scaffold a new project:

```bash
python3 ~/.claude/skills/vellum-editorial/scripts/init_project.py <project-name> [--pages N] [--auth] [--no-auth]
```

This generates a working site with CSS, starter HTML, and optionally a client-side auth gate. Open `index.html` in a browser — fonts load from Google Fonts, icons from Phosphor Icons CDN.

## Design System

Three fonts: Bodoni Moda (display/headlines, italic), Source Serif 4 (body text), Inconsolata (monospace/labels/badges). All loaded from Google Fonts.

OKLCH palette with 43+ custom properties organized as `base / bg / border` triples for each semantic color. The core palette — `--ink`, `--copper`, `--bg`, `--bg-warm`, `--bg-card`, `--border`, `--text-body`, `--text-muted`, `--ghost` — defines the vellum character. Severity tiers (`--dealbreaker`, `--high`, `--moderate`), platform colors (`--subq`, `--claude`, `--cursor`, `--codex`), and status indicators (`--planned`, `--building`, `--shipped`, `--blocked`) extend it.

Full token reference: `references/design-tokens.md`.

## Component Library

21 components across 5 groups: **layout** (breadcrumb, page-nav, header, section, footer), **cards** (state-card, hook-card, cap-panel, further-card, quote-card, req-card), **data display** (matrix, matrix-note, glossary, ring, debugger-panel), **indicators** (status-dot, status-chip, tier-badge, chip), and **editorial** (toc, pullquote, savings-callout, supersession, advantage-row, phase-timeline). Each supports multiple color variants following the semantic palette.

Copy-paste HTML snippets for every component: `references/component-catalog.md`.

## Page Architecture

Two page patterns:

**Landing page**: breadcrumb → page-nav → header (icon, tag, h1, subtitle) → main (numbered sections with ghost `section-num`) → footer

**Deep-dive page**: breadcrumb (with back link) → page-nav → header (logo, tag, h1, subtitle) → main (TOC → numbered sections) → footer

Every page includes: skip link (`<a href="#main" class="skip-link">`), `_shared.css` (core system), `_components.css` (components), Google Fonts preconnect, Phosphor Icons CDN. Auth gate (`_auth.js`) loads before body content when enabled.

Full page structure patterns: `references/page-architecture.md`.

## Customization

Adapt for a different client by editing `:root` custom properties in `_shared.css`:

1. **Color swap** (~5 min): Change `--copper` hue, adjust `--ink`/`--bg` warmth, update platform colors to match client brands.
2. **Semantic rename** (~30 min): Rename `--subq` → `--brand-primary`, update corresponding CSS class variants.
3. **Structural additions**: Add new component variants following the `base / bg / border` triple pattern and BEM-like naming.

The 43 CSS custom properties are the entire theming surface. No build step, no preprocessor.

## Auth Gate

Optional client-side courtesy gate using FNV-1a hashing with sessionStorage. Not real security — a visibility gate for non-public docs. To change the password, compute a new FNV-1a hash and update the `HASH` constant in `_auth.js`. Default password: `subqcode`, hash: `90eb3833`.

## Diagrams (Optional)

Vellum pages can include Mermaid diagrams rendered as inline SVGs via the `beautiful-mermaid` skill. No JavaScript dependency — diagrams are static SVG inlined at build time.

**Generate a vellum-themed SVG:**

```bash
printf 'graph TD\n  A --> B --> C' | \
  node ~/.claude/skills/beautiful-mermaid/scripts/mermaid.mjs \
  -f svg -t vellum --transparent -o diagram.svg -
```

**Inline into a diagram panel:**

```html
<figure class="diagram-panel">
  <p class="diagram-panel__label">System Architecture</p>
  <!-- Paste SVG output here (remove width/height, keep viewBox) -->
  <figcaption class="diagram-panel__caption">Request flow from API gateway to storage</figcaption>
</figure>
```

The `vellum` theme uses cream/ink/copper colors matching the design system. The `--transparent` flag lets the panel's `--bg-card` background show through. Supported diagram types: flowchart, state, sequence, class, ER. See `references/component-catalog.md` for component variants (`--copper`, `--bleed`).

## QA Workflow

After building pages, run these passes in order:

1. `/design-audit` — Technical checks (a11y, performance, responsive, theming, anti-patterns)
2. `/design-critique` — UX review (Nielsen's heuristics, cognitive load, persona red flags)
3. `/design-polish` — Final pass (alignment, spacing, interaction states, transitions)

## Anti-Patterns

Never use `border-left` accent stripes on cards — use `::before` top-bar (like state-card). Never use gradient text (`background-clip: text`). Never use `system-ui` or default fonts. Always include `skip-link` and `prefers-reduced-motion`. Break up sequences of more than 6 state-cards with a pullquote or section break.

## References

| File | When to consult |
|------|-----------------|
| `references/design-tokens.md` | Building new components or customizing the palette |
| `references/component-catalog.md` | Need HTML snippets for any component |
| `references/page-architecture.md` | Setting up page structure, nav, TOC, or glossary |
