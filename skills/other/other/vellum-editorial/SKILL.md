---
name: vellum-editorial
description: "Scaffold editorial documentation sites with the Vellum design system — OKLCH palette, Bodoni Moda / Source Serif 4 / Inconsolata typography, warm or dark space theme, 35 semantic components (state cards, parity matrices, entity dossiers, stat stacks, utterance blocks, editorial notes, entity flows, fact blocks, sub-navigation, source lists, debugger panels, ring visualizations, phase timelines, glossaries, subject-intro, stat-bar, hero-image with lightbox, gallery/masonry grid, audio player with Web Audio API). Static HTML, zero build step. Use when building competitive intelligence pages, personal archives, internal documentation, roadmaps, or multi-page static sites that need a designed, non-generic aesthetic."
argument-hint: [project-name]
---

Build editorial documentation sites with the Vellum design system. Two theme variants (warm parchment, dark space), OKLCH color science, three-font typographic hierarchy, 35 semantic components. Static HTML with zero build step — deploys to Cloudflare Pages, GitHub Pages, or any static host.

## Creative Direction

Two theme variants, each with a distinct character:

**Warm (default):** "Vellum manuscript" — warm cream backgrounds with a subtle SVG crosshatch texture, deep ink-brown text, copper accents. Authoritative, like a well-made journal.

**Dark:** "Space archive" — deep blue-black backgrounds with CSS starfield (box-shadow stars + nebula gradients), bright gold copper accents, cool blue-gray text. Atmospheric, like a command center or digital archaeology site.

Both themes share the same typography, component library, and layout system. The palette transformation is purely in `:root` custom properties — no structural CSS changes needed.

If the `minoan-frontend-design` skill is available, read it for broader aesthetic principles. Vellum encodes those principles into a concrete design system. Pages built with Vellum should score 16+/20 on `/design-audit` and 28+/40 on `/design-critique`.

## Quick Start

Scaffold a new project:

```bash
python3 ~/.claude/skills/vellum-editorial/scripts/init_project.py <project-name> \
  [--style editorial|instrument] [--template landing|one-pager] \
  [--pages N] [--theme warm|dark] [--auth] [--no-auth] \
  [--password <string>] [--deploy-ready] [--no-deploy-ready] \
  [--audio] [--no-audio]
```

This generates a deploy-ready site with CSS, starter HTML, OG/Twitter social meta tags, a light/dark theme toggle, and optionally a client-side auth gate and ambient audio player. By default, `--deploy-ready` generates `_headers` (CF Pages security headers) and `robots.txt` (crawl prevention). The `--theme dark` flag transforms the palette to a dark space aesthetic with CSS starfield background. Open `index.html` in a browser — fonts load from Google Fonts, icons from Phosphor Icons CDN.

**Styles** control the visual aesthetic:
- `editorial` (default) — Bodoni Moda / Source Serif 4 typography, SVG crosshatch texture. Scholarly manuscript character.
- `instrument` — Manrope typography, grid-dot texture. Precision instrument panel character for technical product overviews.

**Templates** control the content scaffolding:
- `landing` (default) — Simple 3-section page with overview, features, comparison.
- `one-pager` — 8-section technical overview with TOC, state-card grids, configuration matrix, phase timeline, and deployment section.

## Design System

Three fonts: Bodoni Moda (display/headlines, italic), Source Serif 4 (body text), Inconsolata (monospace/labels/badges). All loaded from Google Fonts.

OKLCH palette with 50+ custom properties organized as `base / bg / border` triples for each semantic color. The core palette — `--ink`, `--copper`, `--bg`, `--bg-warm`, `--bg-card`, `--border`, `--text-body`, `--text-label`, `--text-muted`, `--ghost` — defines the vellum character. Navigation state (`--nav-active` / `--nav-active-bg` / `--nav-active-border`), severity tiers (`--dealbreaker`, `--high`, `--moderate`), platform colors (`--subq`, `--claude`, `--cursor`, `--codex`), and status indicators (`--planned`, `--building`, `--shipped`, `--blocked`) extend it. Content organized by era or category uses additional `--era-*` color triples.

Full token reference: `references/design-tokens.md`.

## Component Library

35 components across 7 groups: **layout** (breadcrumb, page-nav, header, section, footer), **cards** (state-card, hook-card, cap-panel, further-card, quote-card, req-card), **data display** (matrix, matrix-note, glossary, ring, debugger-panel), **indicators** (status-dot, status-chip, tier-badge, chip), **editorial** (toc, pullquote, savings-callout, supersession, advantage-row, phase-timeline), **intelligence** (dossier, stat-stack, utterance, editorial-note, entity-flow, fact-block, sub-navigation, source-list), and **media** (subject-intro, stat-bar, hero-image with lightbox, gallery/masonry-grid, audio-player). Each supports multiple color variants following the semantic palette.

Copy-paste HTML snippets for every component: `references/component-catalog.md`.

## Page Architecture

Six page patterns:

**Landing page**: breadcrumb → page-nav → header (icon, tag, h1, subtitle) → main (numbered sections with ghost `section-num`) → footer

**Deep-dive page**: breadcrumb (with back link) → page-nav → header (logo, tag, h1, subtitle) → main (TOC → numbered sections) → footer

**Section hub**: breadcrumb → page-nav → sub-nav → header (badge) → main (key findings + further-card grid) → footer

**Profile dossier**: breadcrumb → page-nav → sub-nav → header → subject-intro or editorial-note → primary dossier → secondary dossiers → sources → footer

**Feature comparison**: breadcrumb → page-nav → sub-nav → header → TOC → comparison panels with dimension grids → matrix → sources → footer

**Analysis/implications**: breadcrumb → page-nav → sub-nav → header → TOC → state-card grid (gaps) → advantage-rows → recommendations → sources → footer

Every page includes: skip link (`<a href="#main" class="skip-link">`), `_shared.css` (core system), `_components.css` (components), Google Fonts preconnect, Phosphor Icons CDN. Auth gate (`_auth.js`) loads before body content when enabled. Audio player (`_audio-player.js`) loads at end of body when enabled.

Full page structure patterns: `references/page-architecture.md`.

## Customization

Adapt for a different client by editing `:root` custom properties in `_shared.css`:

1. **Theme selection** (scaffold time): Use `--theme dark` to start with a dark palette, or accept the default warm theme.
2. **Color swap** (~5 min): Change `--copper` hue, adjust `--ink`/`--bg` warmth, update platform colors to match client brands.
3. **Semantic rename** (~30 min): Rename `--subq` → `--brand-primary`, update corresponding CSS class variants.
4. **Era/category colors**: Add `--era-*` triples (base / bg / border) for content organized by time period, category, or entity type. See `design-tokens.md` for the pattern and lightness guidelines.
5. **Structural additions**: Add new component variants following the `base / bg / border` triple pattern and BEM-like naming.

The 50+ CSS custom properties are the entire theming surface. No build step, no preprocessor.

## Auth Gate

Optional client-side courtesy gate using FNV-1a hashing with sessionStorage. Not real security — a visibility gate for non-public docs. Set a password at scaffold time with `--password <string>` — the init script computes the FNV-1a hash automatically and writes the correct constant into `_auth.js`. Each project gets a unique sessionStorage key (`vellum_auth_{project-name}`) to avoid cross-site collisions.

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

## Deploy to Cloudflare Pages

After building and QA:

1. **Create project** (first time only):
   ```bash
   wrangler pages project create <project-name> --production-branch main
   ```

2. **Deploy:**
   ```bash
   wrangler pages deploy <project-dir> --project-name <project-name>
   ```

3. **Verify headers:**
   ```bash
   curl -sI https://<project-name>.pages.dev/ | grep -iE 'x-robots|x-frame|content-security'
   ```

The scaffolded `_headers` and `robots.txt` handle security and crawl prevention automatically. Use `--no-deploy-ready` to skip these files for local-only development.

## Social Preview (OG Image)

Every scaffolded page includes OG and Twitter Card meta tags pointing to `og-image.png`. Generate a 1200x630 OG image with ImageMagick:

```bash
magick -size 1200x630 xc:'#111111' \
  -gravity West -font Inconsolata-Bold -pointsize 52 \
  -fill '#C4956A' -annotate +140+0 'Project Title' \
  -pointsize 22 -fill '#8A8A8A' -annotate +140+50 'Subtitle line' \
  og-image.png
```

Or use `/badge-generator` for a medallion-style icon, then composite onto the dark background. Test the preview by pasting the deployed URL into Slack or the Twitter Card validator.

## Anti-Patterns

Never use `border-left` accent stripes on cards — use `::before` top-bar (like state-card). Never use gradient text (`background-clip: text`). Never use `system-ui` or default fonts. Always include `skip-link` and `prefers-reduced-motion`. Break up sequences of more than 6 state-cards with a pullquote or section break.

## References

| File | When to consult |
|------|-----------------|
| `references/design-tokens.md` | Building new components or customizing the palette |
| `references/component-catalog.md` | Need HTML snippets for any component |
| `references/page-architecture.md` | Setting up page structure, nav, TOC, or glossary |
| `references/advanced-patterns.md` | Ghost watermarks, asymmetric grids, fluid typography, opacity hierarchy, logo handling |
