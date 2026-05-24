---
name: prototype
description: Rapid UI prototyping — generates 3 visually distinct HTML/CSS components from a text prompt, each driven by a unique physical/material metaphor. Use when user runs /prototype, asks to "prototype a UI", "mock up a component", "generate HTML mockups", "create UI variations", "design exploration", "quick UI concept", or wants to see multiple visual approaches to a component. Also trigger when user says "show me different ways to build...", "explore different designs for...", or wants rapid visual exploration of a UI idea — even without saying "prototype" explicitly.
argument-hint: "<component description> [--vary <1|2|3>] [--dir <output-dir>]"
---

# Prototype

Generate 3 visually distinct, high-fidelity HTML/CSS UI components from a single text prompt. Each component adopts a unique design persona based on physical/material metaphors — producing genuinely different visual approaches, not just color swaps.

## Quick Start

Parse `$ARGUMENTS` for the component description, optional `--vary N` flag, and optional `--dir <path>`.

If `--vary N` is present, skip to the [Variation Workflow](#variation-workflow) section.

If the description is vague (e.g., "button", "form"), just generate — don't ask clarifying questions. The value of this skill is speed. Interpret vague prompts generously and produce something interesting.

Follow these 3 phases in order for new generation. Do not pause between phases or ask for confirmation — generate everything in one pass.

### Phase 1: Style Direction

Think of 3 distinct design direction names for the user's prompt. Each name uses a physical/material metaphor — never artist names, brands, or copyrighted references.

**Name pattern**: `[Adjective] + [Material/Process] + [Form/Action]`

**Tone guide** (invent your own, do not copy these):
- "Asymmetrical Rectilinear Blockwork" (Grid-heavy, primary pigments, thick structural strokes)
- "Grainy Risograph Layering" (Tactile paper texture, overprinted translucent inks, dithered gradients)
- "Kinetic Wireframe Suspension" (Floating silhouettes, thin balancing lines, organic primary shapes)
- "Spectral Prismatic Diffusion" (Glassmorphism, caustic refraction, soft-focus morphing gradients)

Each metaphor should imply fundamentally different CSS techniques — not just different colors. See the materiality-to-CSS mapping in [WORKFLOW.md](WORKFLOW.md).

### Phase 2: Artifact Generation

For each of the 3 style directions, generate a complete, self-contained HTML page.

**Scope**: Each artifact is a focused, single-screen component — typically 100-300 lines of HTML. Enough structure to demonstrate the design direction clearly, but limited to one viewport. Not a full multi-section website.

**Visual execution rules:**
1. **Materiality**: The style metaphor drives every CSS choice (e.g., Risograph → `feTurbulence` for grain, `mix-blend-mode: multiply` for ink layering)
2. **Typography**: Use Google Fonts via `<link>`. Pair a bold sans-serif with a refined monospace for data
3. **Motion**: Include subtle CSS animations — hover transitions, entry reveals, micro-interactions
4. **IP Safeguard**: No artist names, brand names, or trademarks anywhere in the output
5. **Layout**: Be bold with negative space and visual hierarchy. Avoid generic card grids
6. **Content**: Use realistic placeholder content (names, dates, numbers) — not lorem ipsum

**Output format**: Each artifact is a complete `<!DOCTYPE html>` page with:
- Inline `<style>` block (no external CSS files except Google Fonts)
- Complete HTML structure with realistic placeholder content
- Optional `<script>` for interactions
- No markdown fences — raw HTML only

### Phase 3: Output

1. Create output directory (default: `.prototype/`, or `--dir` value)
2. Write each artifact with position prefix: `01-{slug}-{style-slug}.html`, `02-...`, `03-...`
3. Write `manifest.json` mapping positions to filenames and style names
4. Generate `index.html` with all 3 artifacts displayed in iframes side-by-side
5. Print file paths and suggest: `open .prototype/index.html`

See [WORKFLOW.md](WORKFLOW.md) for the index page template, manifest format, and file naming details.

## Variation Workflow

When `--vary N` is passed (where N is 1, 2, or 3):

1. Read `manifest.json` from the output directory to find the Nth artifact
2. Read the existing artifact HTML file to understand the current design
3. Generate 3 radical conceptual variations using different physical metaphors
4. Each variation gets a unique persona name and complete HTML/CSS rewrite
5. Write variation files as `{original-slug}-var-1.html`, `-var-2.html`, `-var-3.html`
6. Update `index.html` to show variations

See [WORKFLOW.md](WORKFLOW.md) for the full variation workflow.

## References

- [WORKFLOW.md](WORKFLOW.md) — Detailed guidance, index page template, materiality-to-CSS mapping
- [EXAMPLES.md](EXAMPLES.md) — Usage examples and sample outputs
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
