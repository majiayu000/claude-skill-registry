---
name: visual-explainer
description: Generate self-contained HTML pages that visually explain systems, data stories, investigations, editorial workflows, and code changes. Use when the user asks for diagrams, architecture views, visual diffs, data tables, timelines, source maps, or any structured visualization that would be painful to read as terminal output. Also activates for tables with 4+ rows or 3+ columns. Adapted from nicobailon/visual-explainer with journalism, newsroom, and academic design sensibilities.
version: 0.1.0
license: MIT
---

# Visual explainer

Generate self-contained HTML files for technical diagrams and data visualizations. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering**: When about to output a table with 4+ rows or 3+ columns, render it as styled HTML instead of ASCII. Open in browser.

## Workflow

### 1. Think (5 seconds, not 5 minutes)

- **Audience**: Developer? Editor? Reporter? PM? Public reader?
- **Diagram type**: Pick from the routing table below.
- **Aesthetic direction**: Pick one that fits. Don't default to the same look every time.
  - Monochrome terminal
  - Editorial broadsheet
  - Blueprint / technical
  - Neon dashboard
  - Paper and ink
  - Hand-drawn sketch
  - IDE-inspired
  - Data-dense / wire service
  - Gradient mesh
  - Newsroom board (cork/pushpin)
  - Investigation wall (red string)
  - Magazine feature
  - Academic / research paper

**The swap test**: If you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything. Push further.

### 2. Structure

Read reference templates before generating:

- `./templates/architecture.html` — text-heavy architecture / editorial structure
- `./templates/mermaid-flowchart.html` — flowcharts, sequences, diagrams
- `./templates/data-table.html` — data tables, audits, comparisons

Read `./references/css-patterns.md` for CSS and layout patterns.
Read `./references/responsive-nav.md` for multi-section pages with sticky navigation.
Read `./references/libraries.md` for Mermaid theming, Chart.js, anime.js, and font pairings.

#### Rendering approach by diagram type

| Type | Approach | Rationale |
|------|----------|-----------|
| Architecture (text-heavy) | CSS Grid cards + flow arrows | Rich card content needs CSS control |
| Architecture (topology) | Mermaid | Connections need auto edge routing |
| Flowchart / pipeline | Mermaid | Auto node positioning and edge routing |
| Sequence diagram | Mermaid | Lifelines and activation boxes need layout |
| Data flow | Mermaid with edge labels | Connections and data descriptions |
| ER / schema | Mermaid | Relationship lines need auto-routing |
| State machine | Mermaid | State transitions with labeled edges |
| Mind map | Mermaid | Hierarchical branching positioning |
| Data table / comparison | HTML `<table>` | Semantic markup and accessibility |
| Timeline / chronology | CSS (central line + cards) | Simple linear layout |
| Dashboard / metrics | CSS Grid + Chart.js | Card grid with embedded charts |
| Source network | Mermaid or CSS Grid | Map relationships between sources |
| Editorial workflow | Mermaid flowchart | Story lifecycle from pitch to publish |
| Investigation map | CSS Grid cards + Mermaid | Connect entities, documents, events |
| Story structure | CSS Grid | Visualize narrative arc and sections |

#### Mermaid theming

- Use `theme: 'base'` with custom `themeVariables` — built-in themes ignore most overrides.
- Use `look: 'handDrawn'` for sketch aesthetic, `look: 'classic'` for clean.
- Use `layout: 'elk'` for complex graphs (requires `@mermaid-js/layout-elk` CDN import).
- Always include zoom controls (+/−/reset buttons) on `.mermaid-wrap` containers.
- Support Ctrl/Cmd+scroll zoom and click-and-drag panning.

### 3. Style

**Typography**: Pick a distinctive font pairing from Google Fonts (display/heading + mono or body). Never use Inter, Roboto, Arial, or system-ui as primary. For editorial contexts, serif display fonts work well (Playfair Display, Libre Baskerville, Source Serif Pro). Load via `<link>` in `<head>`. Include system font fallback.

**Color**: Use CSS custom properties. Define minimum: `--bg`, `--surface`, `--border`, `--text`, `--text-dim`, plus 3–5 accent colors (each with full and dim variant). Name semantically. Support both themes:

```css
/* Light-first */
:root { /* light values */ }
@media (prefers-color-scheme: dark) { :root { /* dark values */ } }

/* Dark-first */
:root { /* dark values */ }
@media (prefers-color-scheme: light) { :root { /* light values */ } }
```

**Surfaces**: Build depth through subtle lightness shifts (2–4% between levels), not dramatic color. Borders should be low-opacity rgba (`rgba(255,255,255,0.08)` dark, `rgba(0,0,0,0.08)` light).

**Backgrounds**: Don't use flat solid colors. Use subtle gradients, faint grid patterns via CSS, or gentle radial glows.

**Visual weight**: Not every section deserves equal treatment. Executive summaries and key metrics dominate viewport. Reference sections stay compact. Use `<details>/<summary>` for useful but non-primary content.

**Surface depth**: Vary card depth to signal importance:
- Hero sections: elevated shadows, accent-tinted backgrounds (`node--hero`)
- Body content: flat default (`.node`)
- Secondary content: recessed feeling (`node--recessed`)

**Animation**: Staggered fade-ins on page load almost always worth it. Mix animation types by role:
- `fadeUp` for cards
- `fadeScale` for KPIs and badges
- `drawIn` for SVG connectors
- `countUp` for hero numbers

Always respect `prefers-reduced-motion`. Use CSS transitions and keyframes primarily. For orchestrated sequences, anime.js via CDN is available.

**Accessibility**: All generated pages must meet WCAG 2.1 AA minimum. This means:
- Color contrast ratios: 4.5:1 for text, 3:1 for large text and UI components
- Status indicators use shape/text alongside color (never color alone)
- Tables have proper `<thead>`, `<th scope>`, and `<caption>` elements
- Charts include data table alternatives
- Focus indicators visible for keyboard navigation
- Language declared in `<html lang="en">`

### 4. Deliver

**Output location**: `~/.agent/diagrams/`

**Filename**: Descriptive, based on content. Examples: `authentication-flow.html`, `source-network.html`, `budget-analysis.html`, `editorial-pipeline.html`.

**Open in browser**:
- macOS: `open ~/.agent/diagrams/filename.html`
- Linux: `xdg-open ~/.agent/diagrams/filename.html`

Tell user the file path.

---

## Diagram types — detail

### Architecture / system diagrams

**Text-heavy overviews**: CSS Grid with explicit placement, rounded cards, colored borders, monospace labels, vertical flow arrows. Good for newsroom systems, CMS architecture, data pipeline overviews.

**Topology-focused**: Mermaid with auto edge routing. Good for showing how systems connect.

### Flowcharts / pipelines

Mermaid. Use `graph TD` (top-down) or `graph LR` (left-right). Use `look: 'handDrawn'` for sketch. Color-code nodes via `classDef` or `themeVariables`. Good for editorial workflows (pitch → assign → draft → edit → publish), FOIA request processes, verification workflows.

### Sequence diagrams

Mermaid `sequenceDiagram`. Lifelines, messages, activation boxes, notes, loops with auto layout. Good for showing interaction between reporters, editors, sources, and systems.

### Data tables / comparisons / audits

Real `<table>` HTML element for semantic markup and accessibility. Use proactively for any structured rows/columns.

Layout patterns:
- Sticky `<thead>`
- Alternating row backgrounds via `tr:nth-child(even)` (2–3% lightness shift)
- First column optionally sticky for wide tables
- Responsive wrapper with `overflow-x: auto`
- Column width hints via `<colgroup>` or `th` widths
- Row hover highlight

Status indicators (styled `<span>`, never emoji):
- Match/pass/yes: colored dot or checkmark with green background
- Gap/fail/no: colored dot or cross with red background
- Partial/warning: amber indicator
- Neutral/info: dim text or muted badge

Cell content:
- Wrap long text naturally
- Use `<code>` for technical references
- Secondary detail in `<small>` with dimmed color
- Right-align numeric columns with `tabular-nums`

### Timeline / chronology

Vertical or horizontal timeline with central line (CSS pseudo-element). Phase markers as circles. Content cards branching left/right (alternating) or one side. Date labels on line. Color progression from past (muted) to future (vivid). Good for investigation timelines, event chronologies, project histories.

### Dashboard / metrics overview

Card grid layout. Hero numbers large and prominent. Sparklines via inline SVG `<polyline>`. Progress bars via CSS `linear-gradient`. For real charts use Chart.js via CDN. KPI cards with trend indicators (up/down arrows, percentage deltas). Good for newsroom analytics, grant reporting dashboards, audience metrics.

### Source network

Map relationships between sources in an investigation or story. Can use Mermaid for connection-heavy maps or CSS Grid cards for detail-heavy source profiles. Include: source name, role, credibility indicators, what they provided, cross-references to other sources.

### Investigation map

Connect entities (people, organizations, documents, events) with visual links. CSS Grid cards for entity profiles, Mermaid for relationship diagrams. Color-code by entity type. Show strength of connections. Good for investigative reporting, following the money, mapping power structures.

### Editorial workflow

Mermaid flowchart showing story lifecycle: pitch → assign → research → draft → edit → legal review → publish → distribute. Color-code stages. Show decision gates (kill/revise/approve). Include role labels on transitions.

### Story structure

CSS Grid visualization of narrative arc. Show sections, word counts, source distribution, multimedia placement. Good for planning longform features or reviewing story architecture before publication.

---

## File structure

Every diagram is a single self-contained `.html` file. No external assets except CDN links.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Descriptive Title</title>
  <link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
  <style>
    /* CSS custom properties, theme, layout, components — all inline */
  </style>
</head>
<body>
  <!-- Semantic HTML: sections, headings, lists, tables, inline SVG -->
  <!-- Optional: <script> for Mermaid, Chart.js, or anime.js when used -->
</body>
</html>
```

## Quality checks

Before delivery, verify:

- **The squint test**: Blur eyes. Can you still perceive hierarchy? Sections visually distinct?
- **The swap test**: Would generic dark theme replacement make this indistinguishable from template? If yes, push aesthetic further.
- **Both themes**: Toggle OS light/dark. Both should look intentional.
- **Information completeness**: Does diagram convey what user asked for?
- **No overflow**: Resize browser to different widths. No clipping. Every grid/flex child needs `min-width: 0`. Avoid `display: flex` on `<li>` for markers (use absolute positioning instead). See overflow protection in `./references/css-patterns.md`.
- **Mermaid zoom controls**: Every `.mermaid-wrap` needs +/−/reset buttons, Ctrl/Cmd+scroll zoom, click-and-drag panning. Cursor changes to `grab`/`grabbing`.
- **Accessibility**: Color contrast passes. Status indicators don't rely on color alone. Tables have proper semantic markup.
- **File opens cleanly**: No console errors, no broken fonts, no layout shifts.

## Related skills

- **data-journalism** — data analysis and storytelling
- **accessibility-compliance** — WCAG compliance, accessible charts
- **zero-build-frontend** — CDN patterns, React via esm.sh, Leaflet maps
- **pdf-design** — print-ready documents with brand system
- **source-verification** — SIFT method, verification trails
- **editorial-workflow** — assignment tracking, deadline management

---

*Adapted from [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) (MIT) with design principles from [Anthropic's frontend-design skill](https://github.com/anthropics/skills). Tailored for journalism, media, and academic workflows.*
