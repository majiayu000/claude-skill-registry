---
name: af-ux-design-expertise
description: Use when creating Storybook stories, component specifications, RTL tests, performing UX reviews, or aligning BDD scenarios with UI design. Covers Atomic Design, the 7-stage design flow, component catalog management, selector contracts, shadcn/ui components, and accessibility (WCAG 2.1 AA).

# AgentFlow documentation fields
title: UX Design Expertise
created: 2025-10-29
updated: 2026-02-07
last_checked: 2026-02-07
tags: [skill, expertise, ux, design, storybook, atomic-design, accessibility, rtl, review, brand-guidelines]
parent: ../README.md
related:
  - ../../docs/guides/ux-design-guide.md
  - ../af-figma-design-expertise/SKILL.md
---

# UX Design Expertise

## When to Use This Skill

Load this skill when you need to:
- Create or classify components using Atomic Design
- Transform BDD scenarios into Storybook stories
- Create RTL tests or Storybook play functions
- Define selector contracts for testing
- Perform UX review before PR approval
- Create or update brand guidelines
- Check the component catalog before creating new components

**Common triggers:**
- Refinement phase creates visual sub-tasks
- UI features need Storybook stories
- PR touches `src/components/` or `stories/`
- Discovery phase needs brand guidelines
- New feature may duplicate existing components

## Quick Reference

**Core principles:**
1. Design happens in code (Storybook) — Figma is an optional visual layer (see `af-figma-design-expertise`)
2. Atomic Design classifies components: Atoms → Molecules → Organisms → Templates
3. Component Catalog Check before creating anything new
4. Storybook play functions are PRIMARY for UI testing
5. RTL tests are for non-visual logic only

**The 7-Stage Design Flow:**
1. UX Intent Extraction → Understand requirements
2. Visual Language + Base Tokens → Establish tokens from day one
3. Component Design in Storybook → Build in atomic folders
4. Behavior Locked with Tests → Play functions + RTL
5. Design Sign-off → Storybook + tests complete
6. Handoff to Engineering → Ownership transfer
7. Pattern Tokenisation → Extract emergent patterns

**Key deliverables:**
- Storybook stories (all states, themes, viewports)
- Selector contract (`/tests/selectors/[capability].ts`)
- Components in atomic folders (`src/components/{atoms,molecules,organisms,templates}/`)

## Rules

### Atomic Design Rules

1. **MUST classify components** — Atoms (primitives), Molecules (atom groups), Organisms (feature compositions), Templates (layouts)
2. **MUST check component catalog BEFORE creating** — Browse Storybook sidebar, check shadcn/ui, compose before creating
3. **MUST use atomic folder structure** — `src/components/{atoms,molecules,organisms,templates}/`
4. **MUST mirror atomic levels in Storybook titles** — `title: 'Atoms/Button'`, `title: 'Organisms/Auth/SignupForm'`
5. **SHOULD prefer shadcn/ui for atoms** — Only create custom atoms when shadcn/ui doesn't cover the need

### Component Rules

6. **MUST read design system FIRST** — `/docs/design/design-system.md`
7. **MUST map every BDD scenario to a story** — 100% coverage
8. **MUST create selector contracts** — Bridge between stories and tests
9. **MUST separate components from stories** — Stories import from `src/components/`, never embed code
10. **MUST check tsconfig.json paths before imports** — Path aliases vary by project

### Testing Rules

11. **Storybook play functions are PRIMARY** for UI component testing (real browser)
12. **RTL tests are for non-visual logic ONLY** — Hooks, utils, state machines
13. **MUST NOT duplicate assertions** — If play function tests it, don't repeat in RTL
14. **MUST include accessibility assertions** — Roles, labels, focus management
15. **Tests MUST pass before handoff** — Engineering keeps them passing

### Design Token Rules

16. **MUST establish base tokens in Stage 2** — Brand colors, typography, spacing, radius, shadows
17. **Stage 7 is for emergent patterns ONLY** — Not base tokens
18. **MUST use design system tokens** — Never hard-code values that have tokens

### Accessibility Rules (WCAG 2.1 AA)

19. **Semantic HTML mandatory** — Headings, ARIA roles, landmarks, form labels
20. **Keyboard navigation complete** — Tab order, focus visible, Escape closes modals
21. **Screen reader support** — ARIA labels, live regions, described-by
22. **Color contrast minimum 4.5:1** — Text on background
23. **Touch targets minimum 44px** — Mobile-friendly

### Story Variant Rules

24. **MUST create responsive variants** — Mobile (320-768px), Tablet (768-1024px), Desktop (1024px+)
25. **MUST create theme variants** — Light and Dark mode using decorators
26. **MUST use `tags: ['autodocs']`** — Enable auto-generated component documentation
27. **SHOULD add JSDoc to props interfaces** — Appears in autodocs as prop descriptions
28. **SHOULD use CSF 3 with `satisfies Meta`** — Modern Storybook pattern

## Workflows

### Workflow: Creating Stories from Scenarios

**When:** Refinement phase, after BDD scenarios.

1. Read BDD scenarios from mini-PRD Section 4
2. **Component Catalog Check** — Browse Storybook, check shadcn/ui
3. Read design system at `/docs/design/design-system.md`
4. Create selector contract at `/tests/selectors/[capability].ts`
5. Classify and create components in atomic folders
6. Create stories that import components (title uses atomic prefix)
7. Write stories per scenario (happy, error, boundary, validation)
8. Add responsive variants (Mobile, Tablet, Desktop)
9. Add theme variants (Light, Dark)
10. Add play functions for interaction testing
11. Add `tags: ['autodocs']` and JSDoc on props
12. Test locally: `npm run storybook`

See [UX Design Guide](../../docs/guides/ux-design-guide.md) for detailed steps and examples.

### Workflow: UX Review

**When:** Delivery phase, before PR approval for UI changes.

1. Gather inputs: UI under review, brand guidelines, design decision log, reference class
2. Run 7-point checklist: Structure, Component Discipline, Density, State/Feedback, Accessibility, Brand Alignment, Decision Log Compliance
3. Classify findings as: Aligned | Tension | Violation
4. Emit outputs: Implementation fixes, token evolution, guideline amendments, design decisions

**Hard rule:** If a reference class can't be stated, the review is invalid.

See [UX Design Guide](../../docs/guides/ux-design-guide.md#ux-review-workflow) for full checklist.

### Workflow: Component Catalog Check

**When:** Before creating ANY new component.

1. Browse Storybook sidebar — does this component already exist?
2. Check shadcn/ui — `mcp__shadcn-ui-server__list_shadcn_components`
3. Can you compose from existing atoms/molecules?
4. Only create new if nothing exists at the right level
5. Classify the new component: atom, molecule, organism, or template

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Creating duplicates | Check Storybook catalog first |
| Embedding code in stories | Stories import from `src/components/` |
| RTL duplicating play functions | Play functions are primary for UI |
| No theme variants | Add Light/Dark mode stories |
| Missing autodocs | Add JSDoc + `tags: ['autodocs']` |
| Wrong import paths | Read tsconfig.json first |
| Flat component structure | Use atomic folders |
| Deferring all tokens | Base tokens go in Stage 2 |

## Integration with AgentFlow Phases

| Phase | Activities |
|-------|-----------|
| **Discovery** | Brand guidelines, reference class, base design tokens |
| **Refinement** | Catalog Check → Components → Stories → Tests → Sign-off |
| **Delivery** | Engineering wires components, UX Review before PR |
| **Post-Delivery** | Extract emergent pattern tokens |

## Essential Reading

**Comprehensive guide (workflows, examples, review checklists):**
- [UX Design Guide](../../docs/guides/ux-design-guide.md)

**Design system:**
- Project design system: `/docs/design/design-system.md`

**Related skills:**
- `af-bdd-expertise` — Scenario understanding
- `af-testing-expertise` — Test patterns
- `af-flutter-expertise` — Mobile-specific patterns
- `af-figma-design-expertise` — Figma round-trip workflows (optional visual layer)

**MCP Tools:**
- `mcp__shadcn-ui-server__list_shadcn_components` — List available components
- `mcp__shadcn-ui-server__get_component_details` — Get component specs
- `mcp__shadcn-ui-server__get_component_examples` — Get usage examples

---

**Remember:**
1. Atomic Design: Atoms → Molecules → Organisms → Templates
2. Check the component catalog BEFORE creating new components
3. Play functions are PRIMARY for UI testing
4. Base tokens established in Stage 2, emergent patterns in Stage 7
5. Storybook is the source of truth, not Figma
