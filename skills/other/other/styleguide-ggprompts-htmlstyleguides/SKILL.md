---
name: styleguide
description: Build a complete CSS design system style guide
argument-hint: <aesthetic-name>
allow-model-invocation: true
---

# Build a Style Guide

Create a complete CSS design system style guide for the **$ARGUMENTS** aesthetic.

Follow the full conventions in `styles/CLAUDE.md`. The guide must be self-contained HTML with inline CSS, Google Fonts only, 450-2000 lines, CSS variables in `:root`, responsive design, and semantic HTML.

## Phase 0 — Plan (interactive)

1. Parse the argument as the aesthetic name (e.g., "steampunk", "memphis", "ukiyo-e").
2. Check the **Style Guide Catalog** table in `README.md` and `styles/{name}.html` — if the style already exists, inform the user.
3. Read `styles/CLAUDE.md` for the template and conventions.
4. Read 1-2 existing style guides to match structure and depth — pick ones with a similar vibe.
5. Propose a design direction:
   - Color palette (5-7 colors with hex values and rationale)
   - Typography (2-3 Google Fonts that fit the aesthetic)
   - Key visual motifs (borders, shadows, textures, gradients)
   - Sections to include beyond the required 6
6. Discuss with the user before proceeding.

## Phase 1 — Research (parallel Sonnet subagents)

Launch 2-3 **sonnet** subagents in parallel:
- **Design history**: Research the aesthetic movement — key figures, principles, color palettes, typography conventions, visual hallmarks
- **Font selection**: Search Google Fonts for typefaces that match the aesthetic. Find 2-3 display + body pairings.
- **CSS techniques**: Research CSS techniques needed (gradients, textures, blend modes, clip-paths, etc.)

Each subagent returns structured design research.

## Phase 2 — Build (sequential Opus subagents)

Use 2-3 sequential **opus** subagents:

1. **First agent**: Create the full HTML file with complete `:root` CSS variables, all component styles, and sections 01-04 (Color Palette, Typography, Spacing, Buttons). This agent writes the most CSS — the entire design system foundation.
2. **Second agent**: Read the file, add sections 05-07+ (Forms, Cards/Panels, Alerts, and any extra sections like Navigation, Modals, Grid System, or Design Principles). Close the HTML.
3. **Third agent (polish)**: Read complete file. Verify visual consistency, responsive breakpoints work, all CSS variables are used, no orphan styles. Ensure color contrast is readable.

**Critical rules for build agents:**
- Each agent MUST read the current file before writing
- ALL colors, spacing, and fonts must be CSS custom properties in `:root`
- Include `@media (max-width: 768px)` responsive breakpoint
- Use semantic HTML: `<section>`, `<header>`, `<footer>`, `<label>`
- File goes in `styles/{kebab-case-name}.html`

## Phase 3 — Index & Ship

1. Read `/index.html` (the master project index) to understand the card format.
2. Add a themed card with class `.card-{name}` and matching CSS that reflects the new style's palette.
3. Add the new style to the **Style Guide Catalog** table in `README.md` (new row, both columns empty).
4. Commit with message: `Add {name} style guide`
5. Push using: `git config --global credential.helper store && echo "https://GGPrompts:$(gh auth token --user GGPrompts)@github.com" > ~/.git-credentials && git push origin main`
