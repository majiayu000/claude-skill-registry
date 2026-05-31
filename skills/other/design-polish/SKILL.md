---
name: design-polish
description: "Final quality pass fixing alignment, spacing, consistency, interaction states, and micro-details before shipping. Executes changes (unlike design-audit and design-critique which are report-only). Triggers on polish, finishing touches, final pass, something looks off, pre-launch, good to great."
argument-hint: "[target]"
---

Perform a meticulous final pass to catch all the small details that separate good work from great work. This skill makes changes — `/design-audit` and `/design-critique` are report-only. Polish is the last step, not the first — don't polish work that isn't functionally complete.

Detector and automated QA output are defect evidence only. A clean script result is never proof that the design is strong; gather browser evidence and inspect the real interaction path.

## Preparation

Read `~/.claude/skills/minoan-frontend-design/SKILL.md` for aesthetic principles. Check `.design-context.md` for project context.

Confirm the work is functionally complete before starting. If it's not, tell the user and suggest finishing the feature first.

**Pull in prior critique** (optional signal): If `/design-critique` has been run on the same target, read the latest snapshot from `.design-critique/` and fold its P0/P1 items into your polish list. The critique is one input among many — do your own pass either way.

**Triage cosmetic vs functional**: Classify each issue as **cosmetic** (looks off, doesn't impede the user) or **functional** (breaks, blocks, or confuses the experience). When polish time is tight, functional issues ship first; cosmetic ones can land in a follow-up. Quality should be consistent — never perfect one corner while leaving another rough.

## Design System Discovery

Aligning the feature to the design system is **not optional**. Polish without alignment is decoration on top of drift.

1. **Find the design system**: Search for design system documentation, component libraries, style guides, or token definitions. Study core patterns: color tokens, spacing scale, typography styles, component API, motion conventions.
2. **Note the conventions**: How are shared components imported? What spacing scale is used? Which colors come from tokens vs hard-coded values? What flow shapes are used for comparable actions (modal vs full-page, inline vs route)?
3. **Identify drift, then name the root cause**: For every deviation, classify as a **missing token** (value should exist but doesn't), a **one-off implementation** (shared component exists but wasn't used), or a **conceptual misalignment** (feature's flow/IA/hierarchy doesn't match neighboring features). The fix differs by category.

If a design system exists, polish **must** align the feature with it. If none exists, polish against conventions visible in the codebase.

## Systematic Polish

Work through these dimensions methodically:

### Visual Alignment & Spacing
- Everything lines up to grid. No random 13px gaps — all spacing uses the scale.
- Optical alignment: text at `margin-left: 0` looks indented — use `-0.05em` negative margin. Play icons shift right.
- Concentric border radius on nested elements (`outerRadius = innerRadius + padding`).
- Responsive consistency: spacing and alignment hold at all breakpoints.

### Information Architecture & Flow
Visual polish on a misshapen flow is wasted work. Match the *shape* of the experience to the system, not just the surface.
- **Progressive disclosure**: Match how much is revealed when, compared to neighboring features.
- **Established user flows**: Multi-step actions follow the same shape as comparable flows (modal vs full-page, inline edit vs separate route, save-on-blur vs explicit submit).
- **Hierarchy & complexity**: Same conceptual weight gets same visual weight. Primary actions don't become tertiary in one corner.
- **Naming and mental model**: Feature uses the same nouns and verbs as the rest of the system.

### Typography
- Same elements use same sizes/weights throughout.
- Line length capped at 45-75ch for body text.
- No widows or orphans — use `text-wrap: balance` (headings) and `text-wrap: pretty` (body).
- Font loading: no FOUT/FOIT flashes. `font-display: swap` with size-adjust fallback.
- Font smoothing: `antialiased` on root layout (macOS renders heavier without it).
- Dynamic numbers use `tabular-nums` to prevent layout shift.

### Color & Contrast
- All text meets WCAG contrast (4.5:1 normal, 3:1 large).
- No hard-coded colors — all use design tokens.
- Tinted neutrals: no pure gray or pure black. Add 0.01 chroma of brand hue.
- Never gray text on colored backgrounds — use a darker shade of that color.
- Focus indicators visible with sufficient contrast.

### Interaction States
Every interactive element needs all 8 states:
- **Default**, **Hover** (subtle scale/color/shadow), **Focus** (keyboard indicator — never remove), **Active** (click feedback), **Disabled** (clearly non-interactive), **Loading** (async feedback), **Error** (validation state), **Success** (completion)

Missing states create confusion. Check every button, link, input, toggle.

- **Scale on press**: Buttons get `scale(0.96)` on `:active` for tactile feedback. Always 0.96—never below 0.95 (feels exaggerated). Use CSS transitions for interruptibility. Tailwind: `active:scale-[0.96] transition-transform duration-150 ease-out`. Add a `static` prop to disable when motion would be distracting. Framer Motion: `whileTap={{ scale: 0.96 }}`.
- **Hit area expansion**: Interactive elements need 40-44px minimum hit area. If visible element is smaller (e.g., 20px icon), extend with pseudo-element: `&::after { content: ""; position: absolute; inset: 50%; transform: translate(-50%, -50%); width: 40px; height: 40px; }`. Never let two hit areas overlap.

### Transitions & Motion
- All state changes animated 150-300ms.
- Easing: `cubic-bezier(0.25, 1, 0.5, 1)` (ease-out-quart) or similar. Never bounce or elastic.
- Only animate `transform` and `opacity`. For height: `grid-template-rows: 0fr → 1fr`.
- Respects `prefers-reduced-motion`.
- CSS transitions (interruptible) for interactive state changes; keyframes only for one-shot sequences.
- Never `transition: all` — specify exact properties.
- Enter animations split and staggered (~100ms per group); exits shorter and subtler.
- No enter animations on page load for elements already in default state.

### Content & Copy
- Consistent terminology: same things called same names.
- Consistent capitalization: Title Case vs Sentence case applied uniformly.
- No typos. Punctuation consistent (periods on sentences, not on labels).

### Surfaces & Depth
- Shadows over borders on cards/buttons — layered transparent `box-shadow` adapts to any background.
- Image outlines: subtle `1px` inset outline (`outline-black/10` light, `outline-white/10` dark) — never tinted neutrals.
- Icon cross-fade: keep both icons in DOM (one absolute-positioned), cross-fade with CSS transitions.

### Edge Cases
- Loading states: all async actions have feedback.
- Empty states: helpful message + clear next action, not blank space.
- Error states: clear messages with recovery paths.
- Long content: handles very long names, descriptions gracefully (truncation, wrapping).

### Responsiveness
- Touch targets 44x44px minimum on touch devices. Extend small elements with pseudo-element hit areas.
- No text smaller than 14px on mobile.
- No horizontal scroll.
- Content adapts logically, not just shrinks.

### Performance
- No layout shift on load (CLS). Set dimensions on images/videos.
- Below-fold images lazy loaded.
- No console errors or warnings.
- `will-change` only on GPU-compositable properties (transform, opacity, filter) and only when first-frame stutter observed.

### Code Quality
- Remove console.logs, commented-out code, unused imports.
- Consistent naming. No TypeScript `any` or ignored errors.
- Proper ARIA labels and semantic HTML.

## Verification Checklist

Before marking as done:

- [ ] Visual alignment perfect at all breakpoints
- [ ] Spacing uses design tokens consistently
- [ ] Typography hierarchy consistent
- [ ] All interactive states implemented
- [ ] All transitions smooth (60fps)
- [ ] Copy is consistent and polished
- [ ] All forms properly labeled and validated
- [ ] Error states are helpful
- [ ] Loading states are clear
- [ ] Empty states are welcoming
- [ ] Touch targets 44px minimum
- [ ] Contrast ratios meet WCAG AA
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] No console errors or warnings
- [ ] No layout shift on load
- [ ] Respects reduced motion preference
- [ ] Code is clean (no TODOs, console.logs, commented code)
- [ ] Nested rounded elements use concentric border radius
- [ ] No `transition: all` — only specific properties
- [ ] Dynamic numbers use `tabular-nums`
- [ ] Images have subtle inset outlines for depth
- [ ] Buttons scale on press (0.96)

## Clean Up

After polishing, ensure code quality:
- **Replace custom implementations**: If the design system provides a component you reimplemented, switch to the shared version.
- **Remove orphaned code**: Delete unused styles, components, or files made obsolete by polish.
- **Consolidate tokens**: If you introduced new values, check whether they should be tokens.

## Reference

For implementation details (code examples, specific CSS values, Tailwind patterns): `references/interface-craft-techniques.md`.

Polish until it feels effortless, looks intentional, and works flawlessly.
