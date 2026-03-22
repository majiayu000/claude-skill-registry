---
name: architecture
description: Build an interactive architecture map for an organization, open source project, or tech platform
argument-hint: <subject> [style-name]
allow-model-invocation: true
---

# Build an Architecture Map

Create an interactive architecture map for **$ARGUMENTS**.

The map must be self-contained HTML with inline CSS, Google Fonts only, Mermaid.js loaded from CDN (`https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`), no build step. Target 800-1200 lines. Focus on clarity and navigability over exhaustive detail.

## Subjects

Architecture maps can cover three types of subjects:

1. **Organizations** (VA OIT, DoD, IRS, a bank) — org structure, major systems, integrations, data flows, modernization status
2. **Open source projects** (Kubernetes, PostgreSQL, Linux kernel) — component architecture, module breakdown, data/control flow, extension points
3. **Tech platforms/stacks** (Supabase, Vercel, AWS) — service architecture, API layers, infrastructure, how services compose

## Phase 0 — Plan (interactive)

1. Parse the argument: the main subject, and an optional style name.
2. If no style was specified:
   - Read the **Style Guide Catalog** table in `README.md` to see which styles are available
   - Suggest 3-4 unused styles that thematically fit the subject (e.g., `blueprint` for infrastructure, `federal-night` for government, `circuit-board` for tech)
   - Ask the user to pick one
3. Read the chosen style's HTML file from `styles/{name}.html` to extract the design system (CSS variables, fonts, color palette).
4. Read `architecture/va-oit/index.html` as the reference template for structure, Mermaid config, and fullscreen viewer code.
5. Propose an outline of 8-12 sections with a brief description of each, plus which diagram types suit each section:
   - `graph TD` — hierarchies, org charts, component trees
   - `graph LR` — data flows, request paths, pipelines
   - `flowchart` — decision flows, request routing
   - `timeline` — evolution, version history, modernization
   - `block-beta` — layered architectures, stack diagrams
   - `sequenceDiagram` — API call flows, auth sequences
6. Discuss with the user before proceeding.

## Phase 1 — Research (2 parallel Sonnet subagents)

Launch 2 **sonnet** subagents in parallel. Each should use WebSearch extensively and WebFetch for documentation pages, GitHub READMEs, and architecture docs.

**Agent 1 — Structure & Systems:**
- Organizational/project structure (teams, divisions, maintainers, SIGs)
- Complete inventory of major systems, services, or components
- Technology stack details (languages, frameworks, databases, cloud)
- Budget/scale figures if applicable (public data only for orgs)
- Return a structured list with: name, acronym, category/domain, purpose, tech stack

**Agent 2 — Connections & Status:**
- System interconnections: what talks to what, data flows, API boundaries
- Integration patterns (REST, gRPC, message queues, shared DBs, event buses)
- Authentication/identity flows
- Modernization status, migration efforts, known pain points
- Public APIs, developer portals, open source repos
- Return a structured list of connections: source → target, protocol/method, data exchanged

Both agents should cite their sources for the appendix.

## Phase 2 — Build (2 sequential Opus subagents)

Use 2 sequential **opus** subagents:

### Agent 1 — Skeleton + Sections 01-07

Create the full HTML file with:

**Infrastructure (copy from reference):**
- Complete `<head>` with Google Fonts from the chosen style
- All CSS adapted from the style guide's palette for: hero, jump nav, sections, diagram containers, info cards, data tables, callouts, stat rows, status indicators, domain badges, acronym grid, footer
- Fullscreen diagram viewer (overlay HTML + CSS + JS) — copy the pattern from `architecture/va-oit/index.html`
- Mermaid initialization with `themeVariables` mapped to the style's palette:
  - `background`, `primaryColor`, `primaryTextColor`, `primaryBorderColor` etc. all from style CSS vars
  - `fontFamily` matching the style's body font
  - `useMaxWidth: false` in flowchart config
- The `mermaid.run().then(...)` expand-button injection code

**Content — sections 01-07:**
- Hero with title, tagline, meta badges (key stats)
- Sticky jump nav with ALL section anchors
- Overview section with stat row
- 6 more sections, each with:
  - Section number + title + description
  - 1-2 Mermaid diagrams with `diagram-label`
  - Supporting content (cards, tables, callouts as appropriate)
  - Mermaid node styles using colors from the style's palette

**Mermaid diagram rules:**
- Every `<pre class="mermaid">` must be inside a `<div class="diagram-container">` with a `<div class="diagram-label">`
- Use inline `style` declarations on nodes for colors: `style NODE fill:#hex,stroke:#hex,color:#hex`
- Keep diagrams focused: 8-15 nodes max per diagram. Split complex systems across multiple diagrams.
- Use subgraphs to group related components
- Use `<br/>` for multi-line node labels

**Mermaid node text contrast (REQUIRED):**
Mermaid's `primaryTextColor` theme variable overrides per-node `color` in style directives — the `color` doesn't propagate through `foreignObject` to HTML labels. You MUST include a post-render `fixNodeLabelColors` function that:
1. Runs inside `mermaid.run().then()` wrapped in `requestAnimationFrame`
2. Iterates all `.node` elements, reads the shape's fill via `getComputedStyle(shape).fill`
3. Computes luminance: `(0.299*r + 0.587*g + 0.114*b) / 255`
4. Sets text color on `foreignObject *` with `!important`: dark (`#0a0010`) if lum > 0.4, white (`#ffffff`) otherwise
5. Also sets `fill` attribute on `text`/`tspan` elements for SVG text fallback
6. Is also called on cloned SVGs in the fullscreen viewer (`fixNodeLabelColors(clone)`)

Copy the implementation from `architecture/openclaw/index.html`.

### Agent 2 — Sections 08-12 + Finish

Read the file, then append:
- Remaining sections (interconnections overview, modernization/status, acronym reference)
- The interconnection map: one large diagram showing the full system-to-system picture
- Modernization tracker table with status indicators
- Acronym grid
- Footer with source attribution
- Close all HTML tags

**Critical rules for both build agents:**
- Each agent MUST read the current file before writing
- Use Edit to append content — find closing `</body>` or last `</section>` and insert before it
- Never rewrite the entire file
- All section `id` attributes must match jump nav anchors
- Back link: `<a href="../index.html" class="back-link">Architecture Maps</a>`
- File goes in `architecture/{kebab-case-name}/index.html`

## Phase 3 — Polish (1 Opus subagent)

One **opus** subagent reads the complete file and:

1. **Diagram audit**: Verify every `<pre class="mermaid">` is valid syntax. Check node IDs don't collide across diagrams. Ensure all `style` declarations reference defined nodes.
2. **Navigation audit**: Verify all jump nav `href` anchors match section `id` attributes.
3. **Visual consistency**: Check that node colors across diagrams use a consistent palette (same domain = same color family). Verify diagram labels are present.
4. **Content check**: Look for placeholder text, incomplete sentences, or TODO markers. Verify acronym grid includes all acronyms used in the document.
5. **Responsive check**: Ensure diagram containers have `overflow-x: auto`. Verify mobile breakpoint styles exist.
6. Fix any issues found.

## Phase 4 — Index & Ship

1. If `architecture/index.html` exists, read it and add a card for the new map. If it doesn't exist, create a hub page following the project's index pattern (card grid linking to each map).
2. Update the master `/index.html` if there's no Architecture section link yet.
3. Commit with message: `Add {subject} architecture map ({style-name} style)`
4. Push using: `git config --global credential.helper store && echo "https://GGPrompts:$(gh auth token --user GGPrompts)@github.com" > ~/.git-credentials && git push origin main`

## Reference

- Template: `architecture/va-oit/index.html` (Federal Night style, ~1200 lines)
- Mermaid contrast fix reference: `architecture/openclaw/index.html` (has `fixNodeLabelColors` implementation)
- Style guides: `styles/{name}.html`
- Available styles: **Style Guide Catalog** table in `README.md`
- Mermaid docs: https://mermaid.js.org/syntax/flowchart.html
