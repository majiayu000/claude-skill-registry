---
name: design
description: Use for any UI-facing task (design, implementation, review, refactor, bugfix) as the primary design entrypoint; then route to specialized design skills based on task shape.
---

Use this skill FIRST for any UI-facing task. Do not jump straight to implementation patterns, component tweaks, or styling edits before setting design direction and applying these guardrails.

If this skill applies and you skip it, generic UI is the usual result: weak hierarchy, default-library aesthetics, and interaction quality that feels assembled rather than designed.

## Related Skills
- [design-interaction-motion-craft](../design-interaction-motion-craft/SKILL.md): motion behavior validation
- [copywriting](../writing-copy/SKILL.md): marketing copy generation and rewrite support
- [humanizer](../writing-humanizer/SKILL.md): remove AI-writing artifacts in UI copy

Routing discipline:
- Announce design-skill usage before substantial UI work.
- Establish design direction before writing or revising UI code.
- Route specialized subproblems immediately after direction-setting: motion to `design-interaction-motion-craft`; marketing copy to `copywriting`; anti-slop copy polish to `humanizer`.
- Keep shared goal explicit: we want interfaces that feel intentional, usable, and specific to the product.

Craft foundations:
- Use subtle layering: surfaces should differ just enough to express hierarchy.
- Keep borders quiet but legible; avoid border-forward composition.
- Pick one depth strategy per screen family (borders-only, subtle shadows, or layered shadows), do not mix arbitrarily.
- Typography is structural; semantics and hierarchy outrank decoration.
- Controls and data require full state coverage: default, hover/focus/active/disabled, plus loading/empty/error/success for data flows.

## Integrated Web Execution Guardrails
Use this block when implementing web UI code.

Architecture + dependency rules:
- Verify dependencies in `package.json` before importing third-party packages.
- Default to React/Next.js server-first composition; isolate interactive leaf components with `'use client'`.
- Keep global state for real shared-state needs; use local state by default.
- Tailwind version lock: do not emit v4 syntax into v3 projects.

Layout + responsiveness hard constraints:
- Never use `h-screen` for full-height hero sections; use `min-h-[100dvh]`.
- Prefer grid for multi-column structures; avoid fragile flex percentage math.
- Use stable container bounds (`max-w-7xl` or equivalent) and explicit breakpoint behavior.
- High-variance desktop layouts must collapse to strict single-column on small viewports.

Interaction + motion constraints:
- Ship full state cycles: loading, empty, error, success/confirmation.
- Use transform/opacity for animation; avoid layout-property animation.
- Isolate heavy perpetual motion in small client components; avoid parent re-render coupling.
- Use stagger orchestration intentionally; parent/children choreography must share one client tree.
- If `MOTION_INTENSITY > 5`, prefer Framer motion values over React render-loop state for continuous hover/physics effects.
- Do not mix GSAP/Three and Framer in the same component tree; isolate engine boundaries.

Performance constraints:
- Keep decorative grain/noise off scrolling containers.
- Use strict z-index scales; avoid arbitrary z-index inflation.
- Ensure animation effects degrade safely under reduced-motion preferences.

Anti-generic enforcement (critical examples):
- Avoid AI fingerprint patterns: neon glows, purple/blue default gradient palettes, decorative gradient headline text, repetitive equal-card triplets, templated hero-metric blocks.
- Do not rely on emoji as interface icons.
- Avoid placeholder-data clichés (generic names, synthetic round numbers, fake startup naming).
- If using component libraries, customize tokens/radii/shadows to product identity; never ship untouched defaults.
- Avoid centered-template bias for higher-variance layouts (`DESIGN_VARIANCE > 4`): prefer split or asymmetric compositions.
- For dense dashboard contexts, avoid unnecessary card boxing; use spacing/dividers when elevation is not semantically needed.

Priority order for fixes when tradeoffs exist:
1. Accessibility
2. Touch/interaction correctness
3. Performance
4. Layout/responsiveness
5. Typography/color system
6. Animation quality
7. Style/data-viz polish

Pre-delivery checks:
- visible keyboard focus + valid contrast
- tap targets at or above platform minimums
- no unintentional mobile horizontal scroll
- no hidden content under fixed headers
- `prefers-reduced-motion` respected
- interactive affordances visibly interactive
- iconography is consistent and non-emoji
- motion timing stays in controlled ranges and avoids novelty fatigue
- light/dark readability and border legibility are verified

## Design Direction

Before implementation, commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision before coding major UI structure. Bold maximalism and refined minimalism both work; uncommitted middle-ground usually reads as template output.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Contrasting Aesthetics Protocol
→ *Consult [contrasting aesthetics reference](reference/articles/rauno-contrasting-aesthetics.md) when composing mixed visual languages.*

- Define a dominant base aesthetic first; treat contrast as a controlled deviation.
- Keep 2-3 invariants stable (for example grid rhythm, typography cadence, token semantics).
- Vary only one or two axes at once (shape, saturation, texture, motion character).
- Use strongest contrast for low-frequency/high-significance moments, not repetitive UI loops.
- If contrast reduces scannability or affordance clarity, reduce it before polishing.

## Gestalt + Hierarchy Protocol
→ *Consult [Gestalt and hierarchy reference](reference/articles/gestalt-visual-hierarchy.md) when structuring any screen.*

- Design grouping intentionally: proximity and similarity are interpreted as relationship by default.
- Keep grouping cues aligned: spacing, enclosure, type scale, and color contrast should point to the same hierarchy.
- Use a limited emphasis ladder (for example primary/secondary/tertiary) and reserve strongest contrast for highest-priority tasks.
- Keep figure-ground separation explicit for interactive elements; avoid ambiguous layered surfaces.
- Ensure semantic structure (headings/order) matches visual hierarchy; never rely on visual styling alone for meaning.

## Grid Discipline Protocol
→ *Consult [Müller-Brockmann grid systems reference](reference/articles/muller-brockmann-grid-systems.md) when defining layout structure.*

- Treat the grid as a decision system (columns, gutters, margins, baseline), not decorative scaffolding.
- Select grid complexity from content hierarchy and density; avoid arbitrary field counts.
- Keep baseline and column rhythm stable across related surfaces to preserve scanning continuity.
- Use a small sanctioned set of spans/placements; prefer repeatable composition patterns over ad-hoc placement.
- Break the grid only for high-significance moments; return immediately to system rhythm.
- If rigid adherence harms comprehension, adjust the grid model rather than forcing content into it.
- Remember: grid discipline improves clarity probability; it does not replace typographic and semantic judgment.

## Emotional Design Protocol (Norman)
→ *Consult [emotional design reference](reference/articles/emotional-design-norman.md) when shaping emotional quality.*

- Frame desired emotional outcome per user context before visual polish.
- Evaluate and design at all three levels:
  - `Visceral`: first impression, sensory tone, immediate affect.
  - `Behavioral`: usability-in-action, perceived competence and control.
  - `Reflective`: meaning, identity, memory, and long-term attachment.
- Resolve cross-level conflicts: never trade behavioral usability for visceral novelty.
- Prioritize interventions that reinforce at least two levels simultaneously.
- Validate with lightweight checks:
  - first-impression read (visceral)
  - task success/effort (behavioral)
  - recall/meaning signal (reflective)

## Frontend Aesthetics Guidelines

### Typography
→ *Consult [typography reference](reference/typography.md) for scales, pairing, and loading strategies.*

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

**DO**: Use a modular type scale with fluid sizing (clamp)
**DO**: Vary font weights and sizes to create clear visual hierarchy
**DON'T**: Use overused fonts—Inter, Roboto, Arial, Open Sans, system defaults
**DON'T**: Use monospace typography as lazy shorthand for "technical/developer" vibes
**DON'T**: Put large icons with rounded corners above every heading—they rarely add value and make sites look templated

### Color & Theme
→ *Consult [color reference](reference/color-and-contrast.md) for OKLCH, palettes, and dark mode.*

Commit to a cohesive palette. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

**DO**: Use modern CSS color functions (oklch, color-mix, light-dark) for perceptually uniform, maintainable palettes
**DO**: Tint your neutrals toward your brand hue—even a subtle hint creates subconscious cohesion
**DON'T**: Use gray text on colored backgrounds—it looks washed out; use a shade of the background color instead
**DON'T**: Use pure black (#000) or pure white (#fff)—always tint; pure black/white never appears in nature
**DON'T**: Use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds
**DON'T**: Use gradient text for "impact"—especially on metrics or headings; it's decorative rather than meaningful
**DON'T**: Default to dark mode with glowing accents—it looks "cool" without requiring actual design decisions

### Layout & Space
→ *Consult [spatial reference](reference/spatial-design.md) for grids, rhythm, and container queries.*

Create visual rhythm through varied spacing—not the same padding everywhere. Embrace asymmetry and unexpected compositions. Break the grid intentionally for emphasis.

**DO**: Create visual rhythm through varied spacing—tight groupings, generous separations
**DO**: Use fluid spacing with clamp() that breathes on larger screens
**DO**: Use asymmetry and unexpected compositions; break the grid intentionally for emphasis
**DON'T**: Wrap everything in cards—not everything needs a container
**DON'T**: Nest cards inside cards—visual noise, flatten the hierarchy
**DON'T**: Use identical card grids—same-sized cards with icon + heading + text, repeated endlessly
**DON'T**: Use the hero metric layout template—big number, small label, supporting stats, gradient accent
**DON'T**: Center everything—left-aligned text with asymmetric layouts feels more designed
**DON'T**: Use the same spacing everywhere—without rhythm, layouts feel monotonous

### Visual Details
**DO**: Use intentional, purposeful decorative elements that reinforce brand
**DON'T**: Use glassmorphism everywhere—blur effects, glass cards, glow borders used decoratively rather than purposefully
**DON'T**: Use rounded elements with thick colored border on one side—a lazy accent that almost never looks intentional
**DON'T**: Use sparklines as decoration—tiny charts that look sophisticated but convey nothing meaningful
**DON'T**: Use rounded rectangles with generic drop shadows—safe, forgettable, could be any AI output
**DON'T**: Use modals unless there's truly no better alternative—modals are lazy

### Motion
→ *Consult [motion reference](reference/motion-design.md) for timing, easing, and reduced motion.*

Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.

**DO**: Use motion to convey state changes—entrances, exits, feedback
**DO**: Use exponential easing (ease-out-quart/quint/expo) for natural deceleration
**DO**: For height animations, use grid-template-rows transitions instead of animating height directly
**DON'T**: Animate layout properties (width, height, padding, margin)—use transform and opacity only
**DON'T**: Use bounce or elastic easing—they feel dated and tacky; real objects decelerate smoothly

### Interaction
→ *Consult [interaction reference](reference/interaction-design.md) for forms, focus, and loading patterns.*

Make interactions feel fast. Use optimistic UI—update immediately, sync later.

**DO**: Use progressive disclosure—start simple, reveal sophistication through interaction (basic options first, advanced behind expandable sections; hover states that reveal secondary actions)
**DO**: Keep gesture semantics consistent across the product; same gesture family should imply same intent class
**DO**: For high-frequency flows, prioritize predictable low-novelty interactions over expressive effects
**DO**: Ensure touch interactions preserve feedback visibility (avoid finger-occluded critical state)
**DO**: Design empty states that teach the interface, not just say "nothing here"
**DO**: Make every interactive surface feel intentional and responsive
**DON'T**: Repeat the same information—redundant headers, intros that restate the heading
**DON'T**: Make every button primary—use ghost buttons, text links, secondary styles; hierarchy matters
**DON'T**: Gate all feedback behind thresholds; users need immediate coupled response before commit

### Responsive
→ *Consult [responsive reference](reference/responsive-design.md) for mobile-first, fluid design, and container queries.*

**DO**: Use container queries (@container) for component-level responsiveness
**DO**: Adapt the interface for different contexts—don't just shrink it
**DON'T**: Hide critical functionality on mobile—adapt the interface, don't amputate it

### UX Writing
→ *Consult [ux-writing reference](reference/ux-writing.md) for labels, errors, and empty states.*
→ *Route generation and refinement to [copywriting](../writing-copy/SKILL.md) + [humanizer](../writing-humanizer/SKILL.md).*

**DO**: Make every word earn its place
**DON'T**: Repeat information users can already see

---

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

Review the DON'T guidelines above—they are the fingerprints of AI-generated work from 2024-2025.

---

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

Remember: {{model}} is capable of extraordinary creative work. Don't hold back—show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
