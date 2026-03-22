---
name: visual-explainer-extension
description: Generate strikingly well-designed, visually pleasing HTML diagrams and reports. Use when the user asks for a diagram, architecture overview, diff review, plan review, project recap, comparison table, or any visual explanation of technical concepts. Also use proactively when you are about to render a complex ASCII table (4+ rows or 3+ columns) — present it as a styled HTML page instead.
license: MIT
compatibility: Requires a browser to view generated HTML files. Native MCP image generation included.
metadata:
  author: nicobailon
  version: "1.0.0"
---

# Visual Explainer: Next-Level Aesthetics

Generate self-contained HTML files for technical diagrams, visualizations, and data tables. **Your primary goal is aesthetic excellence.** Never fall back to ASCII art or generic "AI slop" when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path.

## The Aesthetic Mandate

You are a senior design engineer. Your output should feel like it was crafted by a human who understands typography, grid systems, and visual hierarchy.

### 1. The Design Workflow (30 Seconds)

Before writing a single line of HTML, orchestrate the visual strategy. Do not default to generic templates.

- **Orchestrate the Palette:** Choose a specific, named color system.
  - **Blueprint:** Deep slate/blue (`#0f172a`), subtle cyan accents (`#22d3ee`), white/gray text.
  - **Editorial:** Warm cream (`#fafaf9`), deep navy (`#1e293b`), terracotta (`#c2410c`) or gold (`#d4a73a`) accents.
  - **Paper/Ink:** Off-white (`#fcfaf7`), sage (`#65a30d`), charcoal text (`#1c1917`).
  - **IDE Theme:** Dracula, Nord, Solarized, Catppuccin — follow the hex codes exactly.
- **Select Typography Pairing:** Never use Inter. Pick a high-character pairing:
  - **Refined:** *Instrument Serif* (headings) + *JetBrains Mono* (code/labels)
  - **Technical:** *IBM Plex Sans* (headings) + *IBM Plex Mono* (body/code)
  - **Modern:** *Bricolage Grotesque* (headings) + *Fragment Mono* (body/code)
- **Define Hierarchy (The Squint Test):** If you blur your eyes, the most important information (KPIs, hero sections, primary flows) must stand out. Use `ve-card--hero` for emphasis and `ve-card--recessed` for background details.

### 2. Implementation: Advanced CSS Patterns

**Use modern CSS to ensure robustness and visual polish:**

- **CSS Layers (`@layer`):** Use layers to manage specificity: `@layer reset, theme, layout, components, animation;`.
- **Design Tokens:** Define all values in `:root` and use them religiously.
- **Container Queries:** For modular cards, use `@container` so they adapt to their grid slot, not just the viewport.
- **Advanced Selectors:** Use `:has()` for parent styling based on children (e.g., a card with a header gets more padding).
- **Asymmetric Layouts:** Avoid 50/50 splits. Try 60/40, 70/30, or a sidebar-main-recessed trio.

### 3. Rendering Approach (The Logic)

| Content type | Approach | Why |
|---|---|---|
| Architecture (Hybrid) | **Mermaid + CSS Cards** | A simple Mermaid topology overview followed by detailed CSS Grid cards. |
| Flowchart / Sequence | **Mermaid (Elk)** | Use `layout: 'elk'` for complex graphs. Always add zoom/pan controls. |
| Data Tables / Audits | **Semantic <table>** | Sticky headers, alternating rows, status badges (no emoji). |
| Code Explanations | **Intent Bridges** | Two-column "Bridge View": User requirement (Intent) → Implementation (Code). |
| Module Overview | **Archetype Cards** | Large cards with generated icons (using `generate_icon`) representing system parts. |

### 4. Native Image Generation (Proactive)

Use the built-in `generate_image`, `generate_icon`, or `generate_pattern` tools to established the "vibe".
- **Hero Banners:** 16:9 image at the top.
- **Module Icons:** 1:1 icons for Archetype Cards.
- **Patterns:** Subtle background patterns to replace flat colors.

## The Anti-Slop Rules (HARD ENFORCEMENT)

Your work will be rejected if it contains "AI slop" signals:

1. **NO Inter/Roboto/Arial** as the primary body font.
2. **NO Indigo/Violet/Fuchsia** as the primary accent (`#8b5cf6`, `#7c3aed`).
3. **NO Emoji** in section headers. Use SVG icons or styled mono labels.
4. **NO "Neon Dashboard"** aesthetics (cyan+magenta on dark) unless specifically requested.
5. **NO Gradient Text** on every heading. Use it once for the hero title *maximum*.
6. **NO Unstructured Code Dumps.** All code must be in `code-block--scroll` or `collapsible` sections.

## Deliverables

- **Location:** `~/.agent/diagrams/`
- **Action:** Open in browser immediately using `open` or `xdg-open`.
- **Communication:** Briefly state the file path and the design choice you made (e.g., "Generated a Blueprint-style architecture overview").

---
**Reference Material:** Always read `./references/css-patterns.md`, `./references/libraries.md`, and the relevant `./templates/` file before starting.
