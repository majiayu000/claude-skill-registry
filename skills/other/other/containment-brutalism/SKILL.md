---
name: containment-brutalism
description: Enforce Containment Instrument Brutalism on all UI, rendering, and visualization code. Emotional target — billion-dollar research lab reactor display. Material rule — crude but expensive.
---

# Containment Instrument Brutalism

Emotional target: **billion-dollar research lab reactor display.**
Material rule: **crude but expensive.**

This is not a style guide. It's a constraint field. Every pixel must look like it was machined for a facility where the equipment costs more than the building.

## Identity

TRENCH is a containment instrument. The UI is the faceplate of a reactor monitoring station — not a consumer product, not a DAW plugin, not a website. It exists because someone with clearance needs to see what's happening inside the cascade.

The aesthetic is the intersection of:
- Industrial sensor displays (thick bezels, recessed indicators, zero decoration)
- Nuclear/particle physics control rooms (status-first, density over beauty)
- Military flight instruments (information survives at a glance under stress)

## Hard Rules

1. **No anti-aliasing on traces.** Aliased 1px lines only. Smooth curves look consumer-grade.
2. **No gradients, no drop shadows, no glow.** Light doesn't diffuse on instrument glass.
3. **No rounded corners.** Containment vessels have seams, not curves.
4. **Monospace only.** Share Tech Mono. Precision readouts to 6 decimal places where applicable.
5. **Palette is material, not decorative:**
   - Background: `#0A0A0A` (instrument cavity black)
   - Primary trace: `#00FFCC` (reactor coolant cyan)
   - Warning trace: `#FF4500` (thermal orange)
   - Inactive/label: `#3A3A3A` (machined graphite)
   - Bezel highlight: `#1A1A1A` (milled edge catch)
6. **Bezels are structural.** 2px hard inset (not decorative border). They look like the display is recessed into a metal panel.
7. **Information density over whitespace.** Every square pixel earns its place. Dead space is a design failure.
8. **No hover states, no transitions, no animations** unless they represent a real-time measurement changing.
9. **Labels are terse.** "FREQ" not "Frequency". "Q" not "Resonance". Stenciled, not typeset.

## When Using Scientific Skills for Visualization

Strictly output raw vertex data for wgpu or aliased 1px Canvas lines. No anti-aliased SVG. No matplotlib. No d3.js. No high-level plotting libraries unless explicitly requested. The math is rigorous; the rendering is crude.

## When Writing wgpu Pipelines

- Disable MSAA. `sample_count: 1`.
- SDF-based recessed bezels (2px hard inset).
- Interlace flicker on 2D traces (1px scanline at 50% opacity, alternating rows).
- Vertex colors, not texture maps. The display is self-illuminated, not lit.

## Decision Test

"Does this look like it belongs on a $200M reactor console, or a $5/month SaaS dashboard?"

If dashboard — delete it and start over.
