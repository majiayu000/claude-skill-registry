---
name: deer-sense
description: Sense accessibility barriers with gentle awareness. Listen to the forest, scan for obstacles, test the paths, guide toward inclusion, and protect all wanderers. Use when auditing accessibility, testing for a11y, or ensuring inclusive design.
---

# Deer Sense

The deer moves through the forest with heightened awareness. It hears what others miss—a twig snapping underfoot, a bird's warning call. It notices what blocks the path. The deer guides the herd around danger, ensuring everyone can travel safely. In the digital forest, the deer senses barriers that stop some wanderers from finding their way.

## When to Activate

- User asks to "check accessibility" or "a11y audit"
- User says "make this accessible" or "screen reader test"
- User calls `/deer-sense` or mentions deer/accessibility
- Building new UI components
- Reviewing existing interfaces
- After visual redesigns
- Before major releases
- When accessibility complaints arise

**Pair with:** `chameleon-adapt` for accessible UI implementation

---

## The Sense

```
LISTEN --> SCAN --> TEST --> GUIDE --> PROTECT
   |         |        |        |          |
 Hear     Look for  Validate  Fix      Prevent
 Needs    Barriers   Paths   Issues   Regression
```

### Phase 1: LISTEN

*The deer's ears twitch, hearing what others miss before the danger arrives...*

Understand who we're building for and what barriers they face. Map disability types to assistive technologies. Establish WCAG level targets for this project.

- Identify relevant disability types: visual, motor, cognitive, auditory — and which assistive technologies they use
- Confirm WCAG target: Grove standard is WCAG 2.1 AA minimum
- Map common barriers for this specific interface: color contrast, missing alt text, keyboard traps, small touch targets, missing form labels, confusing navigation
- Note Grove-specific considerations: GroveTerm components, glass surfaces, seasonal animations, reduced motion

**Reference:** Load `references/automated-scanning.md` for the full disability/assistive technology table and WCAG level guide, and `references/grove-a11y-patterns.md` for Grove-specific barrier patterns

---

### Phase 2: SCAN

*The deer's eyes scan the forest floor, spotting what blocks the path before setting a hoof forward...*

Run automated scanning to surface mechanical violations quickly. Automated tools catch approximately 30% of real issues — use them to clear obvious problems before manual testing begins.

- Install and run axe-core CLI: `npx axe https://localhost:5173 --tags wcag2aa`
- Review Svelte compiler's built-in a11y warnings (missing alt, unlabeled inputs, `div` with click)
- Check the common issues checklist: images, forms, navigation, color contrast, page structure, language attribute
- Note violations and group by severity: blockers (missing labels, keyboard traps) vs. warnings (suboptimal alt text)

**Reference:** Load `references/automated-scanning.md` for axe-core commands, Lighthouse CI setup, ESLint plugin config, CI integration YAML, and the full issues checklist

---

### Phase 3: TEST

*The deer tests each path personally, because knowing the map is not the same as walking the trail...*

Manual testing catches what automation misses. Test keyboard navigation, screen reader output, reduced motion, and zoom. Work through the test scenarios relevant to this interface.

- Keyboard testing: Tab order, Enter/Space activation, focus indicators, escape key, skip links, no traps
- Screen reader testing (VoiceOver or NVDA): page title, heading navigation, landmarks, images, buttons, forms, live regions
- Zoom testing at 200%: no horizontal scroll, all content visible, no overlapping elements
- Reduced motion: verify all animations are conditional on `prefers-reduced-motion`

**Reference:** Load `references/keyboard-testing.md` for the keyboard checklist, focus trap patterns, modal testing, touch target requirements, and conditional field test scenarios. Load `references/screen-reader-testing.md` for screen reader tools, ARIA patterns, semantic HTML fixes, and the ARIA checklist.

---

### Phase 4: GUIDE

*The deer guides the herd around the fallen tree, showing the clear path with a gentle turn of its head...*

Fix accessibility issues with proper implementations. Prefer semantic HTML over ARIA when possible. Every fix should leave the interface clearer for everyone.

- Fix color contrast issues: use Grove palette tokens which are pre-tested for contrast ratios
- Replace div soup with semantic HTML (`article`, `button`, `nav`, `main`)
- Add focus management: `openModal()` focuses first element, `closeModal()` returns focus to trigger
- Add ARIA labels to icon-only buttons; add live regions for dynamic status updates
- Fix form accessibility: `for`/`id` pairs, `aria-describedby` for errors, `role="alert"` on error messages
- Ensure 44px minimum touch targets on all interactive Grove elements

**Reference:** Load `references/screen-reader-testing.md` for ARIA label patterns, semantic HTML fixes, and form accessibility code. Load `references/grove-a11y-patterns.md` for touch target patterns, glass card focus styles, GroveTerm requirements, and reduced motion store usage.

---

### Phase 5: PROTECT

*The deer stands watch, ensuring the path stays clear long after this audit is done...*

Prevent future accessibility regressions. Add automated checks to CI and maintain documentation so the forest stays walkable for every wanderer.

- Add axe-core to vitest/puppeteer test suite: any violation fails the test
- Add eslint-plugin-svelte-a11y for development-time warnings
- Configure CI to run axe-core on every pull request
- Update accessibility documentation with standards, testing process, and tooling
- Generate the final audit report: pages tested, automated results, manual testing results, issues fixed, ongoing protections

**Reference:** Load `references/automated-scanning.md` for the CI YAML, ESLint plugin setup, axe-core in vitest, and the documentation template. Load `references/screen-reader-testing.md` for the final audit report template.

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| LISTEN | `references/automated-scanning.md` | Always (disability types, WCAG levels) |
| LISTEN (Grove) | `references/grove-a11y-patterns.md` | Any Grove component audit |
| SCAN | `references/automated-scanning.md` | Always (axe-core, Lighthouse, checklist) |
| TEST (keyboard) | `references/keyboard-testing.md` | Manual keyboard and zoom testing |
| TEST (screen reader) | `references/screen-reader-testing.md` | Screen reader testing scenarios |
| GUIDE | `references/screen-reader-testing.md` + `references/grove-a11y-patterns.md` | Fixing issues |
| PROTECT | `references/automated-scanning.md` + `references/screen-reader-testing.md` | CI setup, final report |

---

## Deer Rules

### Awareness
Notice what others miss. Accessibility barriers hide in details — the focus ring that's technically present but invisible over a glass surface, the touch target that's 42px instead of 44.

### Inclusion
Design for everyone. The forest is for all wanderers. Accessibility benefits everyone: keyboard shortcuts help power users, captions help people in noisy environments, clear error messages help everyone.

### Persistence
Accessibility is ongoing, not one-time. Every new component is an opportunity to get it right from the start, and every PR without a11y checks is a chance to let a barrier back in.

### Communication
Use sensory metaphors:
- "Listening for barriers..." (understanding needs)
- "Scanning the path..." (automated testing)
- "Testing the route..." (manual verification)
- "Guiding around obstacles..." (fixing issues)
- "The path is clear." (audit complete)

---

## Anti-Patterns

**The deer does NOT:**
- Skip testing with real assistive technology
- Rely only on automated tools (they catch ~30% of real issues)
- Use "accessibility overlays" or third-party widget patches (they don't work)
- Ignore cognitive accessibility — confusing navigation is a barrier too
- Treat a11y as an afterthought added after "the design is done"
- Suppress focus outlines without providing visible alternatives
- Use color alone to convey meaning

---

## Example Audit

**User:** "Audit the new dashboard for accessibility"

**Deer flow:**

1. **LISTEN** — "Dashboard has complex data, charts, tables. Users: screen reader, keyboard, motor. WCAG AA target. Grove glass cards with custom focus needed."

2. **SCAN** — "axe-core: 5 violations. Missing alt on charts, low contrast on metrics, no table headers. Svelte warns: 2 `div` with onclick."

3. **TEST** — "Keyboard: Can't reach filter dropdowns (trap in date picker). Screen reader: Tables not navigable (no `scope`). Zoom: Sidebar overlaps main content at 200%."

4. **GUIDE** — "Add aria-labels to charts, increase metric contrast to 4.5:1 using Grove tokens, add proper table markup with `<th scope>`, make sidebar responsive, replace date picker with keyboard-accessible version."

5. **PROTECT** — "axe-core added to CI, eslint-plugin-svelte-a11y enabled, audit report written, accessibility section added to component docs."

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| New component | Semantic HTML first, test keyboard/screen reader before shipping |
| Color choice | Check contrast ratio (4.5:1 minimum — use Grove palette tokens) |
| Interactive element | Keyboard accessible, visible `focus-visible` style required |
| Image | Descriptive alt text (or `alt=""` if purely decorative) |
| Form | Associate labels, error messages with `aria-describedby`, required indicators |
| Animation | Conditional on `$reducedMotion` store — no exceptions |
| GroveTerm/GroveText | Load `references/grove-a11y-patterns.md` for required ARIA attributes |
| Touch target | 44px minimum — use padding if visual size must stay smaller |

---

## Integration with Other Skills

**Before Sensing:**
- `chameleon-adapt` — If building new UI, design with accessibility in mind from the start

**After Sensing:**
- `chameleon-adapt` — For accessible UI implementation of fixes
- `beaver-build` — Add accessibility regression tests after fixing issues
- `owl-archive` — Document accessibility standards for the project

---

*The forest welcomes all who seek it. Remove the barriers.*
