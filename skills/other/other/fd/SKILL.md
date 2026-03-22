---
name: fd
description: Frontend design mode for strong visual direction, UI polish, redesigns, landing pages, and production-grade interface work, including shadcn-based surfaces. Use when the user says `/fd` or explicitly asks for better design, styling, layout, visual quality, or UX polish.
---

# FD

Use this as a frontend design and polish mode. The goal is not to make every UI louder; the goal is to make it feel intentionally designed.

## Claude-First Mode

If local `claude` CLI is available, treat it as the design specialist for meaningful frontend work instead of relying on Codex's taste alone.

- Use a single default workflow: delegate the first pass with `claude-design-bridge fd --apply`, then inspect Claude's diff, fix any integration issues, and run verification yourself.
- Only use `claude-design-bridge fd --plan` when the user explicitly wants critique-only guidance without edits, or when apply mode is clearly unsafe for the task.
- Include the user request, relevant paths, constraints, and any established design language in the delegated prompt.
- Treat Claude's visual direction and implementation choices as the primary design authority, then use Codex to inspect, integrate, test, and clean up.
- Fall back to Codex-native design work only if the bridge is unavailable, unauthenticated, or clearly fails.

## Post-Claude Audit

When Claude handled the first implementation pass, Codex should assume responsibility for the final integration quality.

- review the actual diff instead of trusting the visual pass blindly
- fix truncation, overflow, wrapping, density, spacing collisions, and awkward responsive breakpoints
- check keyboard/focus states, aria state integrity, and reduced-motion or contrast regressions when relevant
- preserve filtering, routing, data flow, and existing interaction logic unless the user explicitly asked for behavior changes
- catch SSR, hydration, typing, lint, and small-but-important maintainability issues that a design-first pass may miss
- keep the design intent, but tighten the engineering finish

## Default Taste

Unless the user explicitly asks for a different direction, bias the design toward:

- Apple HIG-style clarity and restraint
- Jony Ive-style product thinking: simple, refined, modern, reduced, calm
- crisp hierarchy, generous spacing, careful materials, subtle motion, and high legibility
- elegance through reduction, not decoration

## Core Rule

Choose a clear visual direction that fits the context, then implement it with enough craft that the result feels deliberate rather than generated.

## First Pass

Before changing code:

- Inspect the existing product, codebase, tokens, components, layouts, and visual language.
- Decide whether this is an **existing-system refinement** or a **new-surface design** task.
- Identify the user-facing goal, the primary audience, the key constraint, and the one visual idea worth remembering.

If the product already has a strong design system, preserve it and improve within it unless the user explicitly asks for a bigger shift.

## Adjust To The Surface

Tune the design to the kind of interface:

- **Marketing or landing pages**: push concept, typography, narrative, and memorable hero moments.
- **Product UI or dashboards**: prioritize hierarchy, density control, affordance, readability, and fast scanning over spectacle.
- **Forms, settings, and CRUD surfaces**: clarity first; polish should reduce friction, not compete with the task.
- **Mobile-heavy views**: simplify composition, tighten spacing logic, and make the primary action obvious.
- **Data-heavy views**: use typography, spacing, grouping, and emphasis to make information legible before adding decoration.

If the brief is ambiguous, bias toward clarity with one strong visual idea instead of stacking effects.

## Design Direction

Pick and commit to one direction instead of mixing weak ideas:

- visual thesis in one sentence
- typography approach
- color and contrast strategy
- layout rhythm and spacing
- motion style
- one signature detail

Good directions can be restrained or bold: editorial, quiet luxury, industrial, playful, sharp enterprise, tactile utility, cinematic, brutalist, soft physical, retro-futurist, and so on. The important part is consistency and intent.

## Execution Rules

- **Typography**: Avoid generic defaults when the surface is design-led. Use purposeful font pairings and hierarchy. If the product already uses a house style, sharpen it instead of replacing it casually.
- **Color**: Use semantic tokens or CSS variables. Favor a disciplined palette with a clear dominant tone and a few strong accents over muddy balance.
- **Layout**: Create rhythm with spacing, scale, alignment, and contrast. Use asymmetry, overlap, density shifts, or generous negative space when it serves the concept.
- **Motion**: Add a few meaningful animations instead of many weak ones. Prefer page-load staging, hover intent, reveal timing, and state transitions that support the interface.
- **Backgrounds and details**: Build atmosphere with gradients, textures, patterns, borders, lighting, shadows, or layered surfaces when appropriate. Avoid flat default canvases when the page needs character.
- **States**: Empty, loading, hover, active, selected, disabled, and error states must feel designed too.
- **Accessibility**: Keep contrast, focus visibility, keyboard behavior, readable sizing, and reduced-motion considerations intact.

## Existing System Priority

When working inside an existing app or design system:

- use existing components before inventing custom markup
- preserve established spacing scales, tokens, and interaction patterns
- improve hierarchy, density, affordance, and polish without creating visual drift
- if shadcn or another component system is present, compose it well instead of fighting it

## Shadcn Mode

When the surface is shadcn-based, `fd` handles it directly.

- inspect the installed shadcn primitives, tokens, CSS variables, and common layout patterns first
- prefer composing existing primitives before creating custom markup
- strengthen typography, spacing, density, and hierarchy before adding decorative effects
- preserve component APIs, token discipline, and product coherence
- use raw custom CSS only when the design needs it and the component layer cannot express it cleanly
- avoid visual drift, ad hoc spacing, and styling everything from scratch when an existing primitive fits

## New Surface Priority

When designing a new page or major new surface:

- pick one strong concept early
- make the hero section or primary interaction memorable
- ensure the supporting sections repeat the same design logic
- avoid generic startup-page structure unless the brief truly calls for it

## Avoid

- generic AI aesthetics
- purple-on-white gradient defaults
- overused fonts as a substitute for real design direction
- interchangeable SaaS hero sections
- default font stacks as the entire visual idea
- motion that adds noise rather than clarity
- decorative clutter without hierarchy
- breaking an established product language just to look different

Do not converge on the same fonts, palettes, or layout tropes every time.

## Implementation Guidance

- Prefer the repo's existing frontend stack and patterns.
- Use CSS variables or existing tokens for colors, spacing, radii, shadows, and motion values.
- Avoid new dependencies unless the user approved them.
- Keep markup and styling maintainable; expressive does not mean messy.
- If a design effect is central, implement it properly instead of hinting at it with placeholder code.
- When delegating to Claude, use a focused prompt block like:

```text
Task: <what the user wants>
Repo: <current cwd>
Relevant paths: <key files or folders>
Constraints: <design system, stack, responsiveness, no new deps, etc.>
What I need: inspect the code, implement the design changes directly, and run the smallest relevant verification.
```

If the surface is shadcn-based, expand `Constraints` with:

```text
Existing system: shadcn/ui, current tokens, key primitives already in use
Constraints: keep component APIs coherent, no visual drift, no new deps unless approved
```

## Verification

Before finishing:

- check the result on desktop and mobile widths when relevant
- verify the main interaction, not just the static look
- run the smallest relevant tests, lint, or build checks
- if the task is visually sensitive, use browser inspection or screenshots to catch layout regressions
- if Claude handled the first pass, inspect the resulting diff before finalizing and optionally run a follow-up `claude-design-bridge fd --plan` critique on the finished surface when the change is especially design-sensitive

## Finish

Keep the final response focused on:

- chosen direction
- what changed visually and structurally
- verification run
- remaining rough edges or tradeoffs
