---
name: frontend-design-review
description: Design, review, and visually QA web and app interfaces against explicit design laws so shipped screens look intentional instead of generic AI output.
---

# Frontend Design Review

Most AI-generated interfaces fail the same way: they compile, they look plausible
in code, and they render as the average of every landing page in the training
data. Dark blue for a developer tool. Purple gradient for a music app. Three
icon cards in a row. A tiny uppercase eyebrow above every section.

This skill replaces taste-by-vibes with thresholds. It gives Claude a design
contract to lock before writing CSS, numeric laws to satisfy while writing it, a
list of banned defaults with the specific replacement for each, and a
render-and-compare loop so nothing is called done from reading code. It works on
product UI, dashboards, marketing pages, component systems, and app store
assets.

**Core principle:** strip the logo and the surface must still be unmistakably
this product, and render the result before claiming it works.

## When to Use This Skill

- Building a new landing page, dashboard, app shell, or component family and you
  want it to look designed rather than defaulted.
- Reviewing an interface someone (or an agent) already built, and you need
  specific findings with file names, not "looks good."
- Auditing a design system for drift: inconsistent tokens, ad hoc spacing,
  five shades of the same gray, components that disagree with each other.
- Comparing a mock, Figma frame, screenshot, or reference URL against a built
  implementation and reporting the gaps by severity.
- Fixing a UI that feels generic and you cannot articulate why.
- Preparing high-visibility surfaces: launch pages, app store screenshots,
  investor demos, docs sites.

Skip it for backend-only work, or a one-line copy change with no visual
consequence.

## What This Skill Does

1. **Locks a design contract before implementation**: audience, surface job,
   primary action, register (brand vs. product), spacing scale, color roles,
   type roles, copy vocabulary, and acceptance checks. Ambiguity resolved up
   front instead of relitigated in review.
2. **Forces a committed aesthetic direction**: pick one of eight named tonal
   directions (refined minimal, editorial, brutalist, retro-technical, organic,
   maximalist, luxury refined, product-utilitarian) and execute it fully. The
   failure mode is not "too bold" or "too plain," it is uncommitted.
3. **Applies numeric design laws**: color strategy, dark-mode surface lightness
   and contrast floors, fluid type scale with `clamp()`, line measure, layout
   and z-index rules, component laws for forms, modals, tables, navigation, and
   empty states, plus motion curves and durations. See
   [references/design-laws.md](./references/design-laws.md).
4. **Rejects AI-slop defaults with named replacements**: gradient text,
   decorative glass panels, orb backgrounds, ghost cards, over-rounded corners,
   numbered section scaffolding, hero-metric templates, fake statistics. Each
   ban ships with a BEFORE and an AFTER and the narrow case where the exception
   is earned. See [references/scoped-bans.md](./references/scoped-bans.md).
5. **Renders and verifies**: captures desktop and mobile screenshots, compares
   source visual target to implementation in the same pass, and writes a
   `visual-qa-report.md` with findings ordered P0 to P3.
6. **Scores design systems out of 100** across ten dimensions and names the two
   weakest to fix first.
7. **Ends with a ship gate**: `ship`, `ship-with-caveats`, or `hold`, with the
   evidence that supports the verdict.

## How to Use

### Basic Usage

```
Review the design of the dashboard at http://localhost:3000/app and tell me
what is wrong with it. Render it at desktop and mobile before answering.
```

Claude inspects the source, renders the page, checks it against the design laws
and the banned-defaults list, and reports findings with file names and specific
fixes.

### Advanced Usage

```
Redesign our pricing page. Before writing code:
1. Write the design contract (audience, page job, primary action, register).
2. Name the aesthetic direction and the one memorable move, and explain why the
   obvious choice for this category is the wrong one.
3. Propose two approaches with tradeoffs and let me pick.
Then build it, render at 1280x900 and 390x844, and finish with a ship gate.
```

```
Compare ./designs/hero-mock.png against the implementation at
http://localhost:5173 and save visual-qa-report.md with P0-P3 findings.
```

```
Audit our design system in ./src/styles and score it out of 100 across color
consistency, typography hierarchy, spacing rhythm, component consistency,
responsive behavior, dark/light behavior, motion restraint, accessibility,
information density, and polish. Fix the two lowest dimensions.
```

## Example

**User**: "Our analytics dashboard looks like every other analytics dashboard.
Fix it."

**Output**:

```
DESIGN PREFLIGHT
target=./apps/web  surface=/dashboard  register=product
context=partial (no DESIGN.md)  render=pass (1280x900, 390x844)

DIAGNOSIS
The surface is the category average. Three findings explain most of it.

P0  Color is decorative, not semantic. src/styles/tokens.css:14
    Six blues, none of which encode meaning. Threshold breaches, healthy
    ranges, and stale data all render in the same accent.
    Fix: commit to Restrained strategy. Tinted neutrals plus one accent
    under 10% of surface area, reserved for threshold breaches only.

P1  Card-in-card nesting. src/components/MetricGrid.tsx:31
    Each metric is a card inside a section card. Cards are for items that
    are independently scannable or selectable, not section wrappers.
    Fix: rows with a shared rule, one card level maximum.

P1  Hero-metric template. src/components/Headline.tsx:8
    "$2.4M" at 80px/weight-900 with a 12px label under it. Isolated big
    numbers read as marketing, not instrumentation.
    Fix: put the number back in the row it belongs to, with its delta and
    its comparison window beside it.

DIRECTION
Aesthetic: product-utilitarian. Scene: an on-call engineer scanning for the
one number that moved, at 2am, on a second monitor. That scene forbids hero
type and rewards density plus one loud state color.

Memorable move: a sparkline gutter down the left edge of every row, so the
shape of the week is readable before any number is.

SHIP GATE
Surface: /dashboard
Done signal: desktop + mobile render, contrast pass
Evidence: dashboard-desktop.png, dashboard-mobile.png, contrast 7.1:1 body
Blockers: none
Accepted caveats: empty state still generic, tracked separately
Next action: apply P0 token change, re-render
Status: ship-with-caveats
```

**Inspired by:** the design workflow from the
[Suede Creator Skills](https://github.com/JasonColapietro/suede-creator-skills)
collection by Jason Colapietro, generalized for any product.

## Tips

- Name the physical scene concretely enough that it forces the design answer.
  "A studio engineer reviewing a rights dispute at 2am on a secondary monitor"
  forces different choices than "a user looking at data." If the sentence does
  not force the answer, add detail until it does.
- Run the two-step slop check before committing to an aesthetic. First: could
  someone guess the palette from the product category alone (observability to
  dark blue, healthcare to white and teal)? Reject that. Second: could someone
  guess it from category plus your anti-references? That is the subtler trap.
  Go further.
- Render before you claim. One-line CSS changes break mobile navigation.
  Minimum coverage: 1280px wide desktop and 390px wide mobile.
- `npx playwright screenshot <url> --viewport-size=1280,900 desktop.png`
  captures the render. One-time setup: `npx playwright install chromium`.
- Extract a design-system issue when a token, spacing pattern, color, or state
  treatment repeats three or more times, or controls a high-visibility surface.
- Never redraw, trace, recolor, or approximate a logo or brand mark. Use the
  approved asset file. If it is unavailable, omit the mark and say so rather
  than improvise one.
- Fake metrics and fake testimonials ship if nobody stops them. Flag every
  placeholder number with `[NEEDS REAL DATA]`.
- Below 70/100 on the design-system score, the system is failing. Fix the two
  lowest dimensions before styling new features on that surface.

## Common Use Cases

- Rescuing a page that feels generic and stating precisely why.
- Pre-launch visual QA on marketing sites, docs sites, and product tours.
- Mock-versus-implementation fidelity checks with a written report.
- Design-system audits and drift cleanups before a redesign.
- Dark-mode passes that are not just inverted light mode.
- Component reviews for forms, tables, modals, navigation, and empty states.
- App store screenshot preparation (1290x2796 for 6.7-inch, 1488x2266 for
  iPad Pro 13-inch).
- Accessibility sweeps: contrast ratios, focus order, touch targets, keyboard
  paths, reduced-motion compliance.

---

## Reference: Working Method

The sections below are the operating detail. Read them when doing the work, not
when deciding whether the skill applies.

### Operating Stance

- Work from current source and a rendered screen. Do not design from memory when
  a repo, live URL, screenshot, or local preview can be checked.
- Prefer the existing framework, tokens, components, icon library, and routing
  patterns. Add a new abstraction only when it removes real complexity or
  matches an established local pattern.
- Keep the product's actual differentiators in the copy. Do not flatten a
  specific product into generic category language.
- Never redraw, trace, approximate, typeset, recolor, or generate a replacement
  for a brand mark. Use the approved file or omit it.

Before design work, read the surface context:

- `PRODUCT.md` if present: users, brand, tone, anti-references, principles.
- `DESIGN.md` if present: color tokens, type scale, component inventory, spacing.
- `AGENTS.md`, `CLAUDE.md`, `AI_HANDOFF.md`, or `README.md` for surface context.

If those files are missing on a major surface, note the gap, proceed with what is
available, and offer to create them afterward.

State the preflight before starting:

```text
DESIGN PREFLIGHT
target=<repo-or-folder>  surface=<route-or-url>  register=<brand|product>
context=<pass|partial|none>  design_system=<loaded|not_found>
render=<pass|pending|skipped:reason>
```

### Task Router

Choose the smallest path that fits the request.

- **Clear small fix**: inspect current UI, make the narrow edit, verify the
  render, report what changed.
- **Ambiguous or net-new design**: gather context, propose two or three
  approaches with tradeoffs, recommend one, get approval before implementing.
- **Large redesign**: write a compact shape brief first, covering audience, page
  job, register, scene, color strategy, typography, layout, signature moment,
  constraints, and QA plan.
- **Visual system work**: scan current CSS, tokens, components, spacing,
  shadows, breakpoints, icon usage, and repeated patterns before proposing
  changes.
- **Source-to-implementation QA**: compare the visual target and the rendered
  build in the same pass, then save `visual-qa-report.md`.
- **Long polish loop**: iterate through a visible checklist. If the same failure
  repeats, freeze the loop, reduce scope to the failing unit, and rerun with
  explicit acceptance criteria.

### Design Contract

Before a new surface, significant redesign, reusable component family, or
design-system pass, lock these:

- audience, surface job, primary action, and launch stage;
- spacing scale, grid behavior, breakpoints, and stable dimensions;
- color roles, semantic states, contrast requirements, and dark/light behavior;
- typography roles, hierarchy limits, body measure, and truncation strategy;
- copy vocabulary for buttons, empty states, loading, errors, and success;
- asset sources, logo use, crop rules, screenshot states, and motion rules;
- acceptance checks for desktop, mobile, accessibility, and rendered evidence.

For a narrow one-element fix, document only the relevant items instead of
forcing a full spec.

### Context Checklist

1. Identify the surface: repo or folder, route, live URL, deployment target,
   branch, dirty files, and relevant local docs.
2. Read repo-local agent and product docs when present.
3. Decide the register:
   - **Brand**: marketing, launch, campaign, public page, portfolio, editorial.
   - **Product**: app shell, dashboard, tool, form, settings, admin, workflow.
4. Name the physical scene: who uses this, where, under what light, with what
   pressure, and what they need to do next.
5. Inspect the current rendered UI at desktop and mobile breakpoints before
   making claims about quality.

### Design Laws

The numeric rules (spacing, type scale, color, contrast, dark mode, density,
motion, component behavior) are in
[references/design-laws.md](./references/design-laws.md). Read that file whenever
writing or reviewing actual styles. It is not needed to route a request or scope
the work.

### Scoped Bans And Exceptions

What is banned, the scope each ban applies to, and the narrow allowed exceptions
are in [references/scoped-bans.md](./references/scoped-bans.md). Read it when a
design choice looks like it needs an exception, or when reviewing whether one was
legitimately taken.

### Aesthetic Direction

Commit to a direction before writing code, and name it explicitly.

Tonal spectrum, pick one and execute it with precision:

- **Refined minimal**: restraint, negative space, weight as the only accent, no
  ornamentation.
- **Editorial**: strong typographic hierarchy, asymmetry, text as structure,
  headline-first layout.
- **Brutalist**: raw grids, exposed structure, high contrast, deliberate
  anti-polish.
- **Retro-technical**: monospace, terminal palette, scan-line texture, system-UI
  references.
- **Organic**: rounded forms, warm neutrals, tactile texture, soft shadow.
- **Maximalist**: density as delight, layered elements, multiple active
  typefaces, controlled chaos.
- **Luxury refined**: generous space, serif hierarchy, muted palette,
  detail-obsessed craft.
- **Product-utilitarian**: information density, data-first, compact controls, no
  decorative chrome.

Bold maximalism and refined minimalism both work. The failure mode is neither: a
design with no committed direction reads as generic.

**Unforgettable factor**: every major surface should have one move that earns
memory, and it should be subject-native, something that only makes sense for this
product. A chain-of-title timeline for a rights platform. A live request waterfall
for an API tool. A shift-coverage ribbon for a scheduling app. Name it before
implementation.

**AI slop check**: run both reflex tests before committing.

1. Could someone guess the theme and palette from the product category alone?
   That is the first-order training-data reflex. Reject it.
2. Could someone guess the aesthetic family from category plus anti-references?
   That is the second-order trap. Go further.

**Theme sentence**: name the physical scene concretely enough that it forces the
design answer. Dark versus light is never a default. Not dark because tools look
cool dark, not light to play it safe.

**Background and atmosphere**: gradient meshes, noise textures, geometric
patterns, layered transparencies, dramatic shadows, grain overlays, and
decorative borders are legitimate tools when they serve the aesthetic. Do not
substitute generic gradient blobs, bokeh orbs, or CSS-only approximations for
real art direction.

### Copy Rules

- Write like a product operator, not a brochure.
- Every label names an action, not a category. "Create Invoice" not "Invoice
  Creation." "Verify Domain" not "Domain Verification." The actor is the user;
  the object is specific.
- Cut filler, vague promises, and restated headings.
- Use the same action name across button, toast, empty state, and confirmation.
- Errors must say what happened and how to fix it.
- Empty states point to the next specific action, not a generic "get started."

### Design System Quality Of Life

For any major surface, reusable app shell, or important component family,
produce these at the smallest useful fidelity:

- **Token map**: color roles, type scale, spacing, radii, shadows, motion,
  z-layers, and semantic state names, stored in `DESIGN.md` or
  `design-tokens.json`.
- **State matrix**: default, hover, focus, active, disabled, loading, empty,
  success, warning, error, and permission-denied for every component that
  touches data.
- **Copy vocabulary**: action labels, toast language, error messages, and
  empty-state prompts that stay consistent across the product.
- **Screenshot contract**: named states with seeded demo data so marketing, app
  store, QA, and docs reproduce the same visuals.
- **Accessibility pass**: contrast ratios, focus order, touch targets, keyboard
  paths, and reduced-motion compliance.
- **Migration notes**: what old styles still exist, what not to touch, and how
  new work adopts the system without rewriting unrelated screens.

Extract a design-system issue when a token, component, spacing pattern, color,
type treatment, or state pattern repeats at least three times or controls a
high-visibility surface. Classify drift root cause as token missing, token
ignored, component gap, content pressure, platform convention, or legacy debt.

For broad audits, score:

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

Below 70/100 the system is failing: fix the two lowest dimensions before styling
new features on that surface. Any dimension at 4/10 or lower is a P1 finding.

### Implementation Workflow

1. **Scan**: inspect current files, styles, rendered UI, and route behavior.
2. **Shape**: when needed, write a compact plan with color, type, layout,
   motion, asset, copy, and verification decisions.
3. **Build**: edit narrowly inside the local architecture. Keep unrelated
   refactors out.
4. **Render**: run the local server or existing preview. Capture desktop and
   mobile screenshots:
   `npx playwright screenshot <url> --viewport-size=1280,900 desktop.png` and
   `--viewport-size=390,844 mobile.png`, or the environment's built-in preview
   or screenshot tool. For app store submissions: 1290x2796 (6.7-inch),
   1488x2266 (iPad Pro 13-inch).
5. **Review**: check typography, spacing, colors, asset fidelity, copy,
   accessibility, responsive behavior, and loading, empty, error, hover, focus,
   and active states.
6. **Verify**: run the relevant lint, typecheck, test, build, or focused
   command. Run `git diff --check` when files changed. Verify live URLs before
   claiming public behavior.
7. **Handoff**: record target, files changed, commands, verification, caveats,
   and the next step.

### Red Flags, Stop

If any of these thoughts appear, stop and run the check being skipped:

- "The code reads right, so it will render right." Render it. Screenshots beat
  code inspection.
- "This change is too small for visual QA." One-line CSS changes break mobile
  navigation. Check desktop and mobile.
- "Music tool, so dark purple." That is the first-order reflex the Color law
  exists to reject. Substitute your own category and its obvious palette.
- "A placeholder metric is fine for now." Fake numbers ship unless they carry a
  `[NEEDS REAL DATA]` flag.
- "I remember what the reference looks like." Compare source and implementation
  in the same pass, never from memory.
- "I will write the tokens down later." Unlogged tokens are how drift starts.
  Note the gap now.

### Visual QA Report

When comparing a source visual target against an implementation, save
`visual-qa-report.md` with:

- source visual truth path or URL;
- implementation path, URL, or screenshot;
- viewport and state;
- theme, auth state, content or data state, and interaction state;
- full-view comparison evidence;
- focused region comparison evidence, or why it was not needed;
- findings ordered by P0/P1/P2/P3 severity;
- patches made after the previous pass;
- `final result: passed` or `final result: blocked`.

Compare source and implementation in the same visual pass, not from memory.
Check typography, spacing and layout, colors and tokens, image and asset
fidelity, logos and icons, copy and content, loading/empty/error/hover/focus/
active states, responsiveness, accessibility, and motion where relevant.

Use `blocked` when a required artifact is missing for the comparison, or when
actionable P0/P1/P2 issues remain. Use `passed` only when no actionable P0/P1/P2
findings remain.

### Ship Gate

For launch pages, app shells, public marketing surfaces, app store assets, or
high-visibility dashboard work, end with:

```text
Surface:
Done signal:
Evidence:
Blockers:
Accepted caveats:
Next action:
Status: ship | ship-with-caveats | hold
```

Use `hold` when a core path is broken, claims are false, screenshots do not match
the implementation, accessibility blocks a primary action, or the live route
cannot be verified. Use `ship-with-caveats` only when the caveat is explicit,
non-critical, and acceptable for the launch stage.

Do not call work done because the code changed. Call it done only when the done
signal has been checked or the remaining gap is named.

### Output Style

Findings lead, rationale follows. Name the file and the line. For builds, state
what changed and show the render evidence. Do not narrate internal process step
names in user-visible output.
