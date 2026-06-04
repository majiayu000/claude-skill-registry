---
name: html-draft
description: Use when user wants a standalone HTML diagram in flat engineering blueprint style — architecture diagrams, system flows, technical spec sheets, component maps. Generates one HTML file using Tailwind v4 (browser CDN) for layout and D3 v7 (CDN) for SVG diagrams. User-invoked only — do NOT auto-trigger. Triggers on "/html-draft", "сделай blueprint", "технический чертёж", "архитектурная схема", "инженерная схема", "blueprint diagram", "engineering blueprint", "technical spec sheet", "architecture diagram", "system flow diagram".
---

# html-draft — Flat Engineering Blueprint Diagrams

Generate one HTML page that renders a technical diagram in a strict flat-blueprint aesthetic — the look of a printed engineering specification sheet, not a marketing landing.

**Stack:** Tailwind v4 via `@tailwindcss/browser` CDN for layout + utilities, D3 v7 via jsDelivr CDN for SVG-based diagrams (nodes, connectors, layouts, animations).

**Use this when** the user wants an architecture diagram, system flow, technical spec sheet, or component map as a standalone HTML artifact (suitable for slides, reports, exports).

**Don't use this for:**
- Inline schemas inside markdown documents — use a mermaid renderer instead
- Newspaper / reading-first single-column pages with monospace ink-on-cream feel
- Multi-section interactive explainers with pill navigation

## Design philosophy

Precise. Objective. High data-ink ratio (Tufte). Every pixel earns its place; nothing decorative. The stack is modern (Tailwind + D3) but the output looks like a printed engineering doc.

## Visual rules

### Flat, outlined, monochrome

- **No** drop shadows, gradients, glassmorphism, blur, rounded buttons
- 1px or 2px solid borders define structure
- White content blocks on a light-gray canvas
- Accent: black, or a single semantic color (red for error, etc.) used sparingly
- Do **not** import a Tailwind component library — pure utility classes only

### Design tokens (declared once via `@theme`)

```css
@theme {
  --color-c-bg: #f8fafc;          /* page background — slate-50 */
  --color-c-canvas: #ffffff;      /* diagram canvas */
  --color-c-border: #cbd5e1;      /* slate-300 */
  --color-c-text-main: #0f172a;   /* slate-900 */
  --color-c-text-sub: #64748b;    /* slate-500 */
  --color-c-accent: #b91c1c;      /* red-700 — semantic only */
  --font-ui: system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-mono: 'SF Mono', Monaco, Consolas, monospace;
}
```

Tokens become Tailwind utilities automatically: `bg-c-canvas`, `border-c-border`, `text-c-text-sub`, `font-mono`.

### Typography

- Headings, labels: sans-serif (`font-ui`)
- Data, paths, code, IDs, version strings: `font-mono`
- Never link Google Fonts — the system stack already covers both roles

### Layout

- Whole diagram lives in a `.diagram-canvas` — bordered box with generous padding (`p-8` or more)
- Header: title + UPPERCASE subtitle, separated from body by a 1px bottom border
- Strict alignment via `grid` / `flex` utilities; no eyeballing

### Connectors

- Thin straight or orthogonal lines (1px solid)
- Dashed lines for abstract / logical relationships, never structural ones
- D3-rendered SVG for non-orthogonal arrows; Tailwind `border-t` / `border-l` for orthogonal CSS connectors

### Icons & badges

- Icons: simple stroke SVG (no fills, no detail) drawn via D3 or inline `<svg>`
- Badges: outlined or solid black/gray block, small uppercase mono text

## Hard requirements

1. **Tailwind v4 via browser CDN** — version-pinned `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4`
2. **D3 v7 via jsDelivr CDN** — version-pinned `https://cdn.jsdelivr.net/npm/d3@7`
3. **Return only** the HTML — no markdown wrapper, no commentary outside the file
4. **Complete document** — `<!DOCTYPE html>` through `</html>`
5. **Design tokens** declared in a single `<style type="text/tailwindcss">` `@theme` block — no scattered custom CSS
6. **Custom CSS minimal** — only what Tailwind utilities cannot express (e.g. SVG marker definitions, complex pseudo-elements)
7. **No external fonts** (no Google Fonts, no Adobe Fonts) — only Tailwind + D3 CDNs

## Output template

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>[Diagram Title]</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style type="text/tailwindcss">
      @theme {
        --color-c-bg: #f8fafc;
        --color-c-canvas: #ffffff;
        --color-c-border: #cbd5e1;
        --color-c-border-strong: #94a3b8;
        --color-c-text-main: #0f172a;
        --color-c-text-sub: #64748b;
        --color-c-accent: #b91c1c;
        --font-ui: system-ui, -apple-system, 'Segoe UI', sans-serif;
        --font-mono: 'SF Mono', Monaco, Consolas, monospace;
      }

      body {
        font-family: var(--font-ui);
      }

      .mono {
        font-family: var(--font-mono);
      }
    </style>
  </head>
  <body class="bg-c-bg text-c-text-main p-10">
    <div class="max-w-[1200px] mx-auto bg-c-canvas border-2 border-c-border-strong p-8">
      <header class="border-b border-c-border pb-4 mb-6 flex items-end justify-between">
        <div>
          <h1 class="text-2xl font-semibold">[Title]</h1>
          <p class="mono text-[11px] uppercase tracking-widest text-c-text-sub mt-1">
            [SUBTITLE]
          </p>
        </div>
        <div class="mono text-[11px] text-c-text-sub text-right">
          DOC-[ID]<br/>REV A
        </div>
      </header>

      <!-- Diagram content: Tailwind grid for spec sheets, D3 SVG for flows -->
      <section class="grid grid-cols-2 border border-c-border">
        <!-- spec cells, see snippets below -->
      </section>

      <!-- D3 mount point for SVG diagrams -->
      <svg id="d3-diagram" class="w-full border border-c-border mt-6" height="400"></svg>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <script>
      // D3 diagram rendering — see "D3 patterns" section below
    </script>
  </body>
</html>
```

## Reusable component snippets

### Node / box

```html
<div class="bg-c-canvas border border-c-border p-3">
  <div class="text-[10px] uppercase tracking-wide text-c-text-sub">label</div>
  <div class="mono text-sm">value</div>
</div>
```

### Badge

```html
<span class="inline-block mono text-[10px] uppercase px-1.5 py-0.5 border border-c-text-main">
  ACTIVE
</span>

<span class="inline-block mono text-[10px] uppercase px-1.5 py-0.5 bg-c-text-main text-c-canvas">
  SCHEDULED
</span>

<span class="inline-block mono text-[10px] uppercase px-1.5 py-0.5 bg-c-accent text-c-canvas">
  OVERDUE
</span>
```

### Connector (orthogonal, CSS)

```html
<div class="border-t border-c-border"></div>
<div class="border-t border-dashed border-c-border"></div>
```

### Spec grid cell

```html
<div class="p-4 border-r border-b border-c-border last:border-r-0">
  <div class="text-[10px] uppercase tracking-wide text-c-text-sub mb-1">label</div>
  <div class="mono text-sm">value</div>
</div>
```

## D3 patterns

Use D3 when geometry is non-orthogonal, computed, or large enough that hand-placing nodes is unmaintainable.

### Pattern 1 — explicit nodes + links (architecture diagrams)

```javascript
const svg = d3.select('#d3-diagram');
const nodes = [
  { id: 'api',    x: 100, y: 100, label: 'API'    },
  { id: 'worker', x: 400, y: 100, label: 'Worker' },
  { id: 'db',     x: 250, y: 280, label: 'DB'     },
];
const links = [
  { source: 'api',    target: 'worker', style: 'solid'  },
  { source: 'api',    target: 'db',     style: 'solid'  },
  { source: 'worker', target: 'db',     style: 'dashed' },
];
const byId = Object.fromEntries(nodes.map(n => [n.id, n]));

// arrow marker
svg.append('defs').append('marker')
  .attr('id', 'arrow').attr('viewBox', '0 -5 10 10')
  .attr('refX', 8).attr('refY', 0).attr('markerWidth', 6).attr('markerHeight', 6)
  .attr('orient', 'auto')
  .append('path').attr('d', 'M0,-4L8,0L0,4').attr('fill', '#0f172a');

// links
svg.selectAll('line').data(links).enter().append('line')
  .attr('x1', d => byId[d.source].x).attr('y1', d => byId[d.source].y)
  .attr('x2', d => byId[d.target].x).attr('y2', d => byId[d.target].y)
  .attr('stroke', '#0f172a').attr('stroke-width', 1)
  .attr('stroke-dasharray', d => d.style === 'dashed' ? '4 3' : null)
  .attr('marker-end', 'url(#arrow)');

// nodes
const g = svg.selectAll('g.node').data(nodes).enter().append('g')
  .attr('transform', d => `translate(${d.x - 50}, ${d.y - 18})`);
g.append('rect').attr('width', 100).attr('height', 36)
  .attr('fill', '#fff').attr('stroke', '#0f172a').attr('stroke-width', 1);
g.append('text').attr('x', 50).attr('y', 22)
  .attr('text-anchor', 'middle').attr('font-size', 12)
  .attr('font-family', 'system-ui').text(d => d.label);
```

### Pattern 2 — tree layout (hierarchical structures)

`d3.hierarchy()` + `d3.tree()` for parent/child trees (component maps, org charts). Render with the same flat node style; never use the default rounded D3 examples.

### Pattern 3 — DAG / flow

`d3-dag` (optional) or manual topological layout. For < 15 nodes, hand-place coordinates — it's faster and tighter than a layout algorithm.

### Pattern 4 — sankey / flow volumes

`d3-sankey` plugin (`https://cdn.jsdelivr.net/npm/d3-sankey@0.12`) when volumes matter. Keep ribbons grayscale; one accent only for the watched flow.

### What D3 must not do here

- No force-directed simulations bouncing around — diagrams are static engineering docs
- No smooth zoom/pan unless the user asks — extra interactivity adds noise
- No tooltips / hover popups unless the user asks
- No colorful palettes — the visual rules above still bind

## Composition guide

- **Architecture diagram:** services as D3 rect nodes, data flow as solid SVG lines with arrow markers, dependencies as dashed
- **System flow:** linear stages left-to-right or top-to-bottom; decision points as outlined diamonds (D3 polygons); use Tailwind grid for non-flow sections of the same page
- **Spec sheet:** Tailwind grid of labeled cells, each with a mono value and a sans-serif label; status badge top-right of each cell
- **Component map:** nested boxes in HTML (Tailwind) for top level; D3 hierarchy for deep trees; badges on each node

## Quality bar

1. Every text item earns its space — no decorative copy
2. Alignment is strict — no off-grid placement
3. Mono and sans roles never bleed (don't put labels in mono or data in sans)
4. Color usage stays monochrome unless one semantic accent is justified
5. CDN scripts pinned to specific major versions (`@tailwindcss/browser@4`, `d3@7`)
6. D3 code is readable — named variables, no one-letter chaining beyond what's idiomatic
7. The page renders correctly on first paint even before D3 mounts (no layout jump)

## When input is incomplete

- **No content** → ask for the diagram type (architecture / flow / spec sheet / component map) and the items to render
- **Vague subject** → propose a node list and ask for confirmation before rendering
- **User asks for a different library** (Mermaid inside, Recharts, Chart.js) → push back: this skill is Tailwind + D3 only; suggest `mermaid-diagrams` skill if the user wants Mermaid
- **User asks for interactivity** (tooltips, drag, zoom) → confirm explicitly; default is static print-style

## Source

Methodology adapted from QoderWork's `drafter-diagram` skill (flat-engineering-blueprint visual system), restacked on Tailwind v4 + D3 v7.
