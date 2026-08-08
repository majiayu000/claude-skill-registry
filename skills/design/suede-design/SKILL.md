---
name: suede-design
description: "Make Suede interfaces feel intentional: tokens, color, components, type, visual hierarchy, motion, dark mode, and visual QA for shipped screens."
---

# Suede Design

## When to use this skill instead of related skills
- **suede-design** (this skill): design system tokens, color ramps, type scale, component-level polish, brand identity decisions
- Visual iteration with the local script harness (craft, shape, audit sub-commands): (private Suede Labs companion, not in this pack: suede-visual-qa)
- UX critique, accessibility audit, information architecture, design handoff docs: (private Suede Labs companion, not in this pack: suede-ui)
- Broad UI/UX pattern lookup, framework examples, palette/font/chart searches, or non-Suede implementation heuristics: (private Suede Labs companion, not in this pack: ui-ux-pro-max)
- Deck-only or HTML presentation generation: (private Suede Labs companion, not in this pack: power-design)
- **johnny-suede-design**: full-stack build combining design + copy + visual QA for a launch or redesign

Use this skill to make Suede interfaces feel intentional, premium, legible, and
alive without drifting into generic AI output. It covers product UI, brand
surfaces, landing pages, dashboards, component systems, responsive polish, and
visual QA.

**Core principle:** strip the logo and the surface must still be unmistakably this product, and render the result before claiming it works.

## Operating Stance

- Work from current source and a rendered screen. Do not design from memory when a repo, live URL, screenshot, or local preview can be checked.
- For Suede branding, use only `docs/assets/suede-ai-logo-transparent.png` from `JasonColapietro/suede-creator-skills` (SHA-256 `83a7ee0317e4debe2e7b076c20ba067feb76a587f9e829dc6310ae4be4b44dfa`). Never redraw, trace, approximate, typeset, recolor, distort, or generate a replacement Suede S. `suede-skill-icon.png` is a Passport icon, not the Suede brand mark. If the approved file is unavailable or its checksum differs, stop and request it; omit the mark rather than improvise.
- Keep Suede public copy anchored in creator ownership, programmable IP, rights, provenance, registry-backed media, royalty routing, and agent commerce. Do not reduce Suede to a generic AI music app.
- Prefer the existing app framework, tokens, components, icon library, and routing patterns. Add a new abstraction only when it removes real complexity or matches an established local pattern.
- For visual work, render the result. Screenshots beat code inspection. Minimum: desktop at 1280px width, mobile at 390px width. For App Store submissions: 1290×2796px (6.7-inch), 1488×2266px (iPad Pro 13-inch).
- To capture the render: `npx playwright screenshot <url> --viewport-size=1280,900 desktop.png` (swap the viewport for mobile/App Store dimensions above; one-time setup: `npx playwright install chromium`), or your environment's built-in preview/screenshot tool if one is available.

Before any design work, read the surface context:
- Local `PRODUCT.md`: users, brand, tone, anti-references, strategic principles
- Local `DESIGN.md`: color tokens, type scale, component inventory, spacing
- `AGENTS.md`, `AI_HANDOFF.md`, or `README.md`: agent guidance and surface context

If PRODUCT.md or DESIGN.md is missing on a major surface, note it and proceed with available context. Offer to create them after completing the task.

Then state this preflight in the working update:

```text
SUEDE_DESIGN_PREFLIGHT: target=<repo-or-folder> surface=<route-or-url> register=<brand|product> context=<pass|partial|none> design_system=<loaded|not_found> git=<pass|skipped:reason> render=<pass|pending|skipped:reason> mutation=open
```

For major design work, reusable systems, reference visual matching, App Store
assets, or public launch surfaces, keep `mutation=open` only after these are
known:

- `PRODUCT.md` or product context status;
- `DESIGN.md` or design-system context status;
- shape brief status for net-new or large redesigns;
- source visual target status when a mock, screenshot, Figma frame, or
  reference URL exists;
- rendered implementation status;
- ship blocker status.

Also apply the shared no-missed gate at
`~/.claude/skills/suede-workflow-skills/references/no-missed-quality-gates.md`
when the work touches copy, design-system, visual QA, Suedify, visibility, or
public launch quality.
(Requires suede-workflow-skills installed from this pack. If not installed, run the Copy Gate, Visual QA Gate, SEO/AEO/AI EO Gate, Design System Gate, and Launch Gate checklists using the criteria in the Implementation Workflow, Ship Gate, and Visual QA Report sections of this skill.)

## Task Router

Choose the smallest path that fits the request.

- **Clear small fix:** inspect current UI, make the narrow edit, verify render,
  and report what changed.
- **Ambiguous or net-new design:** gather context, propose 2-3 approaches with
  tradeoffs, recommend one, and get approval before implementation.
- **Large redesign:** write a compact shape brief first: audience, page job,
  register, scene, color strategy, typography, layout, signature moment,
  constraints, and QA plan.
- **Visual system work:** scan current CSS, tokens, components, spacing,
  shadows, breakpoints, icon usage, and repeated UI patterns before proposing
  changes.
- **Source-to-implementation QA:** if there is a mock, screenshot, Figma frame,
  or image target plus a rendered implementation, compare both visually before
  handoff and save `visual-qa-report.md` in the project root.
- **Long polish loop:** iterate through a visible checklist. If the same failure
  repeats, freeze the loop, reduce scope to the failing unit, and rerun with
  explicit acceptance criteria.

## Delivery Discipline

Before major or important Suede design work, write a compact delivery contract:

- objective: the user-visible outcome;
- surface: repo, route, live URL, branch, and owner;
- done signal: screenshot, build, test, deploy readback, or review artifact;
- constraints: WIP to preserve, routes not to touch, copy claims not yet
  approved, and launch/release boundaries;
- lanes: what can run in parallel, what must wait, and what each lane writes.

Do not call work done because the code changed. Call it done only when the done signal has been checked or the remaining gap is named.

Use `suede-agent-teams` for major design work when several lanes must move at
once, such as copy plus layout plus asset plus implementation plus QA. Use
`suede-code-review` before the ship gate when design work changes shared
components, routing, auth, payments, analytics, release config, or published-statement
truth. Skip both for a small visual or copy fix that can be inspected, patched,
rendered, and verified directly.

## Suede UI Contract

Before a new surface, significant redesign, reusable component family, or
design-system pass, lock the design contract before implementation:

- audience, surface job, primary action, and launch stage;
- spacing scale, grid behavior, breakpoints, and stable dimensions;
- color roles, semantic states, contrast requirements, and dark/light behavior;
- typography roles, hierarchy limits, body measure, and truncation strategy;
- copy vocabulary for buttons, empty states, loading, errors, and success;
- asset sources, logo use, crop rules, screenshot states, and motion rules;
- acceptance checks for desktop, mobile, accessibility, and rendered evidence.

Review the result against copy quality, visuals, color, typography, spacing, and
experience states. If the work is purely backend or a narrow one-element fix,
document only the relevant contract items instead of forcing a full spec.

## Context Checklist

1. Identify the surface: repo/folder, route, live URL, deployment target, branch,
   dirty files, and relevant local docs.
2. Read repo-local `AGENTS.md`, `CLAUDE.md`, `AI_HANDOFF.md`, `README.md`,
   `PRODUCT.md`, `DESIGN.md`, or task docs when present.
3. Decide the register:
   - **Brand:** marketing, launch, campaign, public page, portfolio, editorial.
   - **Product:** app shell, dashboard, tool, form, settings, admin, workflow.
4. Name the physical scene: who uses this, where, under what light, with what
   pressure, and what they need to do next.
5. Inspect the current rendered UI at desktop and mobile breakpoints before
   making claims about quality.

## Design Laws

### Subject First

Strip the logo from any Suede surface. If the remaining visual could belong to a generic SaaS, a crypto exchange, or a music streaming app, the design has failed. Suede surfaces should feel like purpose-built studio infrastructure: precise, traceable, and operator-grade. Every surface should answer: "What does a creator do here, specifically?"

### One Memorable Move

Give each major surface one signature element that earns attention: an
interactive rights passport, a waveform ledger, a chain-of-title timeline, a
studio console, a claim map, a provenance receipt, or another subject-native
device. Keep the surrounding UI disciplined so the signature move carries.

### Color

- Pick a strategy from the Color Strategy Axis below before picking any values.
- Color must earn its position by encoding meaning: ownership, rights status, action type, risk level, state change, tier, or provenance chain. Decorative color is waste.
- First-order reflex to reject: "music/creator tool → dark purple gradient." Second-order trap: avoided purple but landed on muted-teal-on-dark anyway. Go further until the palette is specific to this surface's physical scene.

### Color Strategy Axis

Before picking values, commit to a strategy on this axis:

- **Restrained**: tinted neutrals + one accent ≤10% of surface area. Default for product dashboards, admin, tools, and focus-heavy workflows.
- **Committed**: one saturated color carries 30–60% of the surface. Default for brand pages and identity-driven screens. The "one accent ≤10%" rule does NOT apply here.
- **Full palette**: 3–4 named color roles, each used deliberately. Use for data visualization, campaign pages, and multi-feature products.
- **Drenched**: the surface IS the color. Use for campaign heroes, launch moments, and brand statements.

Pick a strategy before picking values. Avoid defaulting to Restrained for everything. Committed and Full palette designs require it to feel intentional.

For CSS color values, prefer OKLCH. Reduce chroma as lightness approaches 0 or 100 to avoid garish extremes. Tint every neutral toward the brand hue (chroma 0.005–0.01 is enough). Never use pure #000 or #fff.

### Dark Mode

Dark mode is not an inversion. These are the specific rules:

**Surfaces:** Dark surfaces use lightness 10-18 OKLCH, not 0. Background layers stack from dark to slightly lighter: base (L=12) → elevated (L=16) → overlay (L=20) → modal (L=24). Never use pure black as a surface.

**Shadows:** Shadows disappear on dark surfaces. Replace elevation cues with border-based layering: 1px border at `oklch(1 0 0 / 0.08)` on elevated surfaces, `oklch(1 0 0 / 0.12)` on modals. Drop-shadows only appear in dark mode when the element is physically "lifted" (a draggable card, a tooltip, a floating toolbar).

**Contrast minimums:** body text on dark background: minimum 7:1 (WCAG AAA). Secondary text: 4.5:1. Disabled text: 3:1. Do not use near-black text on dark surfaces. Use light text with opacity adjustments (`oklch(1 0 0 / 0.45)` for secondary, `oklch(1 0 0 / 0.25)` for disabled).

**Chroma:** In dark mode, reduce saturated color chroma by 15-25%. `oklch(0.65 0.22 260)` in light → `oklch(0.72 0.17 260)` in dark. Fully saturated accent colors on dark backgrounds feel neon. Pull back.

**Semantic tokens:** define light and dark values for every semantic token at design time. `--color-surface-base`, `--color-surface-elevated`, `--color-border-subtle`, `--color-text-primary`, `--color-text-secondary`, `--color-text-disabled`. Never hardcode hex in component CSS.

### Typography

- Pair typefaces deliberately. Display, body, and utility text should have
  distinct jobs.
- Use scale and weight for hierarchy; keep at least a 1.25 ratio between major
  type steps.
- Keep body copy around 65-75 characters per line.
- Keep letter spacing at 0 by default. Do not use negative letter spacing.
- Match type size to context. Dashboards, cards, and toolbars need compact
  hierarchy, not hero-scale text.

Typography anti-patterns to avoid without explicit justification:
- Overused system fonts: Inter, Roboto, Arial, SF Pro as the display face
- Symmetric type pairing: display and body from the same family
- Uniform weight: same weight across headline, subhead, and body
- Letter-spacing on body copy
- Negative letter-spacing on small text (under 16px)

Pair typefaces deliberately: one font earns the display role (personality, brand signal), one earns the body role (readability, neutrality). They should contrast: a geometric display pairs with a humanist body; a serif display pairs with a sans body.

### Fluid Type Scale

Use `clamp()` for all responsive type. The pattern is `clamp(min, preferred, max)` where preferred is a viewport-relative value.

Reference scale (adjust to match the surface's type role):

```css
--text-xs:   clamp(0.75rem,  0.70rem + 0.25vw,  0.875rem);
--text-sm:   clamp(0.875rem, 0.82rem + 0.28vw,  1rem);
--text-base: clamp(1rem,     0.94rem + 0.30vw,  1.125rem);
--text-lg:   clamp(1.125rem, 1.0rem  + 0.62vw,  1.375rem);
--text-xl:   clamp(1.375rem, 1.1rem  + 1.40vw,  2rem);
--text-2xl:  clamp(1.75rem,  1.3rem  + 2.20vw,  3rem);
--text-3xl:  clamp(2.25rem,  1.6rem  + 3.25vw,  4.5rem);
```

Min is the floor at ~375px viewport. Max is the ceiling at ~1440px. The preferred vw value controls how aggressively the type grows.

Never use fixed `px` font sizes for display, heading, or subheading roles. Fixed sizes are acceptable only for UI chrome (badges, labels, captions) that must not resize with viewport changes.

Line height scales inversely with size: large display text (≥2xl) uses line-height 1.05–1.1. Body text uses 1.5–1.6. Subheadings use 1.2–1.35.

### Layout

- Make structure explain the product. Use bands, rails, timelines, consoles,
  grids, tabs, and split panes because the content needs them.

Spatial composition: intentional layouts use asymmetry, overlap, diagonal flow, and the tension between density and negative space. All of these are legitimate tools:
- Asymmetry: column grids that don't divide evenly, intentional visual weight on one side
- Overlap: elements that break their containing rows to create depth
- Diagonal flow: content that leads the eye along a non-horizontal axis
- Generous negative space OR controlled density, not an accidental middle ground

Never use a card where a row would do. Use cards only for items that must be independently scannable, draggable, or selected, not as a visual wrapper for sections, tabs, or form groups. One card inside another card means your information architecture is wrong. Fix the hierarchy, not the nesting.

- Stable UI elements need stable dimensions: boards, grids, icon buttons,
  counters, tiles, canvases, and toolbars should not resize when labels, hover
  states, loading text, or data changes.
- Build a semantic z-index scale: dropdown → sticky → modal-backdrop → modal →
  toast → tooltip. Never arbitrary values like 999 or 9999.
- On landing pages, the first viewport must show the brand, product, or offer
  clearly and leave a hint of the next section visible on mobile and desktop.
- Text must not overlap, clip, or fight its container at any viewport.

### Controls

- Use icon buttons for familiar commands when the icon exists in the local icon set. Add tooltips for icons that are not obvious.
- Use segmented controls for modes, toggles or checkboxes for binary settings, sliders or inputs for numeric values, tabs for views, menus for option sets, and text buttons for commands.
- Keep touch targets usable and focus states visible.
- A dropdown or popover rendered with `position: absolute` inside a parent with `overflow: hidden` or `overflow: auto` gets clipped. Use the native `<dialog>`/popover API, `position: fixed`, or a portal to escape the stacking context.

### Component Laws

**Forms:**
Every form field shows its label above the input, never as placeholder text. Placeholder is hint text only. It disappears on focus and must not carry required information. Error messages appear below the field they belong to, not as a toast. Required fields are marked; optional fields are not (the default expectation is required). A submit button is always the primary action; it is disabled only when the form is provably incomplete, never as the default initial state.

BEFORE: `<input placeholder="Email address" />` with no visible label
AFTER: `<label>Email address</label><input placeholder="e.g. you@studio.com" />`

**Modals:**
A modal is for a destructive action, a focused sub-task that needs temporary full attention, or a preview that shouldn't break navigation context. It is not the first answer to "the user needs more information." Use inline expansion, a side drawer, or a dedicated route instead when the content is browseable or the action is reversible. Every modal has one primary action and one escape (keyboard Escape + backdrop click). Never stack modals.

BEFORE: clicking "details" opens a modal with a scrollable list of 12 items
AFTER: clicking "details" expands an inline panel or navigates to a detail route

**Empty states:**
An empty state is a conversion opportunity, not a placeholder. It must contain: what would be here (one concrete example), why it's empty (the specific reason), and what to do next (a single, specific action). Never show just an illustration and "No results found." Name the specific thing that's missing.

BEFORE: `[Icon] No tracks yet.` with a disabled button
AFTER: `Register your first work to start building your rights ledger. [Register a Work →]`

**Data tables:**
Column headers are left-aligned except numeric columns, which are right-aligned. Rows are 40-48px tall for data-dense tables, 56-64px when each row needs a secondary line. Alternating row fills are a last resort for wide tables with more than 8 columns. Prefer generous column padding and strong header contrast instead. Sort indicators are visible on hover for all sortable columns, not just the active one. Pagination controls live below the table, right-aligned, with total count visible at all times.

**Navigation:**
Primary navigation shows the user's current location at all times with a visible active state that is not just color. Use weight, underline, or background shape so it survives grayscale. Depth beyond three levels means the information architecture needs restructuring, not another nav level. Mobile nav collapses to a bottom tab bar (max 5 items) or a full-screen drawer. Never a hamburger that reveals a sidebar on a phone.

### Assets

- Use real product, creator, media, logo, or generated bitmap imagery when the
  surface needs a visual asset. Do not replace visible brand assets, product
  imagery, or nonstandard icons with CSS shapes, emoji, placeholder divs, or
  improvised inline drawings.
- Use approved Suede logo files from the current project, public repo assets,
  or an operator-provided brand folder. Do not reference private local asset
  paths in public docs, screenshots, or generated output.
- For 3D work, use Three.js and verify the canvas is nonblank, framed,
  interactive or moving as intended, and responsive.

### Motion

Every animation must justify its CPU cost. If removing it makes the UI clearer, remove it. If keeping it makes an action legible (a row sliding out when deleted, a panel expanding from its trigger, a success state settling into place), keep it.

Never animate width, height, top, left, or margin. Animate `transform` and `opacity` only.

Exit curve: `ease-out-expo` (`cubic-bezier(0.16, 1, 0.3, 1)`), duration 220-280ms. The UI should feel like it arrives, not drifts.

Entrance sequencing for lists, cards, and panels: `translate3d(0, 12px, 0)` → `translate3d(0, 0, 0)` + opacity 0→1, 240ms ease-out-expo, stagger 40ms per item, max 6 items staggered then clamp. Cap total reveal sequence at 480ms. Panels enter at 300ms; hero content at 180ms.

Scroll-triggered reveals fire once, not on every scroll direction change. Use `IntersectionObserver` with `threshold: 0.15`.

In React, use Motion (Framer Motion). Always include a `prefers-reduced-motion` variant that removes translate and cuts duration to 0ms.

## Design System Quality Of Life

For any major Suede surface, reusable app shell, launch system, or important component family, produce these artifacts at the smallest useful fidelity:

- **Token map:** color roles, type scale, spacing, radii, shadows, motion, z-layers, and semantic state names, stored in `DESIGN.md` or `design-tokens.json`.
- **State matrix:** default, hover, focus, active, disabled, loading, empty, success, warning, error, and permission-denied states for every component that touches data.
- **Copy vocabulary:** action labels, toast language, error messages, and empty-state prompts that stay consistent across the product.
- **Screenshot contract:** named states with seeded demo data so marketing, App Store, QA, and docs can reproduce the same visuals.
- **Accessibility pass:** contrast ratios, focus order, touch targets, keyboard paths, and reduced-motion compliance.
- **Migration notes:** what old styles still exist, what not to touch, and how new work adopts the system without rewriting unrelated screens.

Extract a design-system issue when a token, component, spacing pattern, color,
type treatment, or state pattern repeats at least three times or controls a
high-visibility surface. Classify drift root cause as token missing, token
ignored, component gap, content pressure, platform convention, or legacy debt.

For broad design-system audits, score:

```text
Color consistency: /10
Typography hierarchy: /10
Spacing rhythm: /10
Component consistency: /10
Responsive behavior: /10
Dark/light behavior: /10
Motion restraint: /10
Accessibility: /10
Information density: /10
Polish: /10
Total: /100
```

Below 70/100 the system is failing: fix the two lowest dimensions before styling new features on that surface. Any dimension at 4/10 or lower is a P1 finding in the audit report.

## Scoped Bans And Exceptions

These are not blanket bans. Keep or recreate a pattern when source fidelity, platform convention, accessibility, a confirmed brand system, or a direct user request makes it the right choice. When making an exception, name why it is earned.

Rewrite the element if any of these appear as a lazy default:

### Scaffolding And Typography Devices

**Tiny uppercase tracked eyebrow above every section.**
BEFORE: a small all-caps kicker ("ABOUT" · "PROCESS" · "PRICING") sitting above every section heading, page after page.
AFTER: vary the cadence, or drop the kicker and let the heading carry weight. One deliberate kicker as a named brand device is voice; one on every section is AI grammar.

**Numbered section markers as default scaffolding (01 / 02 / 03).**
BEFORE: `01 · About` / `02 · Process` / `03 · Pricing` stamped above every section regardless of content.
AFTER: reserve numbering for a real ordered sequence (an actual 3-step flow, a timeline) where the order carries information. Elsewhere, drop it.

**Identical icon-card grids as main page structure.**
BEFORE: 3×2 grid of cards each with icon + title + one-line description
AFTER: A task-driven layout where each row or section maps to a specific user action, not a product category

**Em dashes in UI or marketing copy.**
BEFORE: "Distribute your music. Own every right."
AFTER: "Distribute your music. Own every right." Use a period, a colon, or a comma. If the clause needs an em dash, restructure the sentence.

### Surface And Color Treatments

**Gradient text.**
BEFORE: `-webkit-background-clip: text` rainbow or metallic effect on headlines
AFTER: A single high-contrast headline at full weight with an accent word in a solid color, or a single-hue gradient at low chroma (essentially a slight lightness shift)

**Decorative glass panels (blur + translucent background).**
BEFORE: `backdrop-filter: blur(20px)` card floating over a gradient background
AFTER: An opaque surface at the correct elevation token, with a 1px border for definition

**Colored side-stripe borders on cards, alerts, or list items.**
BEFORE: A card with a 4px left border in `--color-warning` indicating status
AFTER: An icon + label in the semantic color inside the card; or a top-of-card banner strip that spans the full width and carries text

**The ghost-card pattern (thin border plus soft wide shadow, stacked).**
BEFORE: `border: 1px solid` combined with `box-shadow: 0 16px+ blur` on the same card or button as decoration.
AFTER: pick one: a defined border at the brand color, or a shadow no wider than 8px blur at the correct elevation token. Never both as ornament.

**Over-rounded corners.**
BEFORE: `border-radius: 32px` or higher on cards, sections, or inputs.
AFTER: cap cards and inputs at 12-16px radius. Full-pill radius is fine for tags and buttons only.

**Repeating-linear-gradient stripe backgrounds.**
BEFORE: diagonal stripe patterns in a section or body background via `repeating-linear-gradient`.
AFTER: a real art-direction choice: solid surface, noise texture, or a concrete product artifact.

**Decorative orbs, bokeh blobs, generic gradient backgrounds.**
BEFORE: Three radial gradients at 30% opacity behind the hero
AFTER: A concrete art-direction choice: a noise texture, a geometric system, a real product screenshot, an illustrated scene, or a typographic lock-up that IS the background

**Cream, sand, or beige as the default body background.**
BEFORE: a near-white warm-tinted background (OKLCH lightness 0.84-0.97, chroma below 0.06, hue 40-100) used as the safe default for "warm" or "editorial" briefs, under a name like `--paper`, `--cream`, `--sand`, `--linen`, or `--ivory`.
AFTER: pick a saturated brand color as the body, a true off-white at chroma 0 (or tinted toward the brand's own hue, not toward warmth by default), or a darker tinted neutral that reads as this brand's own. Carry "warmth" through accent color, typography, and imagery instead. Same chroma-tinting discipline as the Color Strategy Axis above, applied to the one background choice teams default on without thinking.

### Content Integrity And Structure

**The hero-metric template (big number, tiny label, support stats, gradient accent).**
BEFORE: `$2.4M` in 80px weight-900 with "Revenue generated" in 12px below it
AFTER: A metric placed inside a real workflow context. E.g., the royalty total shown inside the rights ledger column it belongs to, not isolated as a hero number.

**Modal as the first answer to every interaction.**
BEFORE: Every "view details" → opens modal
AFTER: Inline expansion, side panel, or dedicated route; modal reserved for destructive confirmation or focused isolated actions

**Centered hero copy over a stock-feeling gradient with no real Suede artifact.**
BEFORE: "Own Your Music" centered on dark purple, no visual content below
AFTER: A hero that contains a real product artifact (a partial rights registry UI, an animated waveform ledger, a claim receipt) with copy anchored to it.

**Fake metrics, fake testimonials, fake partner claims.**
No exception. Remove and replace with either: (a) a real stat with a source note, (b) a placeholder with a `[NEEDS REAL DATA]` flag, or (c) a structural element that doesn't depend on a specific number.

**Hand-drawn or sketchy SVG illustrations.**
BEFORE: crude wavy-line doodles, `feTurbulence`/`feDisplacementMap` "paper grain" filters, or a 5-30 path sketch standing in for a real subject.
AFTER: ship a real asset (photo, product screenshot, a properly illustrated scene) or ship no illustration at all.

## Copy Rules

- Write like a product operator, not a brochure.
- Every label names an action, not a category. "Register Work" not "Registration." "Verify Rights" not "Rights Verification." The actor is always the user; the object is always specific.
- Cut filler, vague promises, and restated headings.
- Use the same action name across button, toast, empty state, and confirmation.
- Errors must say what happened and how to fix it.
- Empty states point to the next specific action, not a generic "get started."

## Aesthetic Direction

For any new surface or significant redesign, commit to a clear aesthetic direction before writing code. Name it explicitly.

Tonal spectrum. Choose one and execute it with precision:
- **Refined minimal**: restraint, negative space, weight as the only accent, no ornamentation
- **Editorial**: strong typography hierarchy, asymmetry, text as structure, headline-first layout
- **Brutalist**: raw grids, exposed structure, high contrast, deliberate anti-polish
- **Retro-technical**: monospace, terminal palette, scan-line texture, system-UI references
- **Organic**: rounded forms, warm neutrals, tactile texture, soft shadow
- **Maximalist**: density as delight, layered elements, multiple active typefaces, controlled chaos
- **Luxury refined**: generous space, serif hierarchy, muted palette, detail-obsessed craft
- **Product-utilitarian**: information density, data-first, compact controls, no decorative chrome

Bold maximalism and refined minimalism both work. The failure mode is neither: a design with no committed direction reads as generic. Pick one tone and execute it fully.

**Unforgettable factor**: every major surface should have one move that earns memory. For Suede that might be a rights ledger, a waveform proof panel, or a chain-of-title timeline. For other companies, it should be one subject-native device: something that only makes sense for THEIR product. Name it before implementation.

**AI slop check**: before committing to an aesthetic, run two reflex tests:
1. Could someone guess the theme and palette from the product category alone ("observability → dark blue", "healthcare → white + teal")? That's the first-order training-data reflex. Reject it.
2. Could someone guess the aesthetic family from category-plus-anti-references? That's the second-order trap: the first reflex was avoided but the second wasn't. Go further.

**Theme sentence**: name the physical scene concretely enough that it forces the design answer. "A studio engineer reviewing a rights dispute at 2am on a secondary monitor" forces different choices than "a user looking at data." If the sentence doesn't force the answer, it's not concrete enough. Add detail until it does. Dark vs. light is never a default. Not dark because tools look cool dark, not light to be safe.

**Background and atmosphere**: gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, grain overlays, and decorative borders are all legitimate tools when they serve the aesthetic. Do not substitute generic gradient blobs, bokeh orbs, or CSS-only approximations for real art direction.

## Implementation Workflow

1. **Scan:** inspect current files, styles, rendered UI, and route behavior.
2. **Shape:** when needed, write a compact plan with color, type, layout, motion,
   asset, copy, and verification decisions.
3. **Build:** edit narrowly inside the local architecture. Keep unrelated
   refactors out.
4. **Render:** run the local server or use the existing preview. Capture desktop
   and mobile screenshots when practical: `npx playwright screenshot <url>
   --viewport-size=1280,900 desktop.png` and `--viewport-size=390,844
   mobile.png`, or your environment's built-in preview/screenshot tool if one
   is available.
5. **Review:** check typography, spacing, colors, asset fidelity, copy,
   accessibility, responsive behavior, loading, empty, error, hover, focus, and
   active states.
6. **Verify:** run the relevant lint, typecheck, test, build, or focused command.
   Run `git diff --check` when files changed. Verify live URLs or APIs before
   claiming public behavior.
7. **Handoff:** for meaningful work, record target, files changed, commands,
   verification, caveats, and the next step.

## Red Flags — Stop

If any of these thoughts appear, stop and run the check you were about to skip:

- "The code reads right, so it will render right." Render it. Screenshots beat code inspection.
- "This change is too small for visual QA." One-line CSS changes break mobile nav. Check desktop and mobile.
- "Music tool, so dark purple." That is the first-order reflex the Color law exists to reject.
- "A placeholder metric is fine for now." Fake numbers ship unless they carry a `[NEEDS REAL DATA]` flag.
- "I remember what the reference looks like." Compare source and implementation in the same pass, never from memory.
- "I'll write the tokens down later." Unlogged tokens are how drift starts. Note the gap now.

## Ship Gate

For launch pages, app shells, public marketing surfaces, App Store assets, or
high-visibility dashboard work, end with a short ship gate:

```text
Surface:
Done signal:
Evidence:
Blockers:
Accepted caveats:
Next action:
Status: ship | ship-with-caveats | hold
```

Use `hold` when a core path is broken, claims are false, screenshots do not
match implementation, accessibility blocks a primary action, or the live route
cannot be verified. Use `ship-with-caveats` only when the caveat is explicit,
non-critical, and acceptable for the launch stage.

## Visual QA Report

When comparing a source visual target against an implementation, save
`visual-qa-report.md` with:

- source visual truth path or URL
- implementation path, URL, or screenshot
- viewport and state
- theme, auth state, content/data state, and interaction state
- full-view comparison evidence
- focused region comparison evidence, or why it was not needed
- findings ordered by P0/P1/P2/P3 severity
- patches made after the previous pass
- `final result: passed` or `final result: blocked`

Compare source and implementation in the same visual pass, not from memory.
Render the implementation with `npx playwright screenshot <url>
--viewport-size=1280,900 impl.png` (matching viewport to the source target), or
your environment's built-in preview/screenshot tool if one is available. Check
typography, spacing/layout, colors/tokens, image and asset fidelity,
logos/icons, copy/content, loading/empty/error/hover/focus/active states,
responsiveness, accessibility, and motion where relevant.

Use `final result: blocked` when the source or rendered artifact is missing for
a required comparison, or when actionable P0/P1/P2 layout, typography, color,
asset, copy, accessibility, responsive, interaction-state, or source-fidelity
issues remain. Use `passed` only when no actionable P0/P1/P2 findings remain.

## Output Style

Findings lead, rationale follows. Name the file and line. For builds, state what changed and show the render evidence. Never name internal process steps (preflight, task router, mutation) in user-visible output.

## Routing

- Full copy + design + QA build or launch → johnny-suede-design
- Broad UI/UX pattern lookup or framework examples → (private Suede Labs companion, not in this pack: ui-ux-pro-max)
- Deck-only or HTML presentation generation → (private Suede Labs companion, not in this pack: power-design)
- Words that carry the surface → suede-copy (johnny-suede-write for the full writing stack)
- Page conversion architecture beyond visual polish → suede-site-alchemy
- Design change touches shared components, routing, auth, payments, or analytics → suede-code-review before the ship gate
- Multi-lane build with parallel copy, layout, asset, and QA work → suede-agent-teams
