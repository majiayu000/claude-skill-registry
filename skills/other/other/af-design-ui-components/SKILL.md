---
name: af-design-ui-components
description: Design UI components with Storybook stories, RTL tests, and accessibility compliance. Use when creating component specifications, performing UX reviews, aligning BDD scenarios with UI design, or working with shadcn/ui.

# AgentFlow documentation fields
title: UX Design Expertise
created: 2025-10-29
updated: 2026-03-09
last_checked: 2026-03-09
tags: [skill, expertise, ux, design, storybook, atomic-design, accessibility, rtl, review, brand-system, view-components, design-grammar]
parent: ../README.md
related:
  - ../../docs/guides/ux-design-guide.md
  - ../af-sync-figma-designs/SKILL.md
---

# UX Design Expertise

## When to Use This Skill

Load this skill when you need to:
- Create or classify components using Atomic Design
- Transform BDD scenarios into Storybook stories
- Create RTL tests or Storybook play functions
- Define selector contracts for testing
- Perform UX review before PR approval
- Create or update the brand system specification
- Check the component catalog before creating new components

**Common triggers:**
- Refinement phase creates visual sub-tasks
- UI features need Storybook stories
- PR touches `src/components/` or `stories/`
- Discovery phase needs brand system specification
- New feature may duplicate existing components

## Quick Reference

**Core principles:**
1. Design happens in code (Storybook) — Figma is an optional visual layer (see `af-sync-figma-designs`)
2. Extended Atomic Design hierarchy: Tokens → Primitives → Atoms → Molecules → Organisms → Templates → Pages → Flows
3. Component Catalog Check before creating anything new
4. Storybook play functions are PRIMARY for UI testing
5. RTL tests are for non-visual logic only
6. View Components are the single source of truth — shared by Storybook stories AND app pages
7. Design Grammar (`.design-grammar/`) defines the shared cross-project vocabulary

**The 7-Stage Design Flow:**
1. UX Intent Extraction → Understand requirements
2. Visual Language + Base Tokens → Establish tokens from day one
3. Component Design in Storybook → Build in atomic folders
4. Behavior Locked with Tests → Play functions + RTL
5. Design Sign-off → Storybook + tests complete
6. Handoff to Engineering → Ownership transfer
7. Pattern Tokenisation → Extract emergent patterns

**Key deliverables:**
- View components (`src/components/views/`) — rendering logic shared by stories and pages
- Storybook stories (all states, themes, viewports)
- Selector contract (`/tests/selectors/[capability].ts`)
- Components in atomic folders (`src/components/{primitives,atoms,molecules,organisms,templates}/`)

## Rules

### Extended Atomic Design Hierarchy

The full hierarchy extends classic Atomic Design with Primitives below and Pages/Flows above:

```
Tokens → Primitives → Atoms → Molecules → Organisms → Templates → Pages → Flows
```

| Level | Purpose | Examples |
|-------|---------|---------|
| **Tokens** | Design values (colors, spacing, typography) | `--color-primary`, `--spacing-md` |
| **Primitives** | Unstyled behavioural + layout building blocks | Component: `<Pressable>`, `<Slot>`; Layout: `<Stack>`, `<Grid>` |
| **Atoms** | Styled single-purpose elements | `<Button>`, `<Badge>`, `<Input>` |
| **Molecules** | Small atom combinations | `<FormField>`, `<NavItem>`, `<PricingCard>` |
| **Organisms** | Large UI sections (page sections) | `<Hero>`, `<FeatureGrid>`, `<Pricing>` |
| **Templates** | Page structure without content | `<LandingTemplate>`, `<DashboardTemplate>` |
| **Pages** | Templates + real content (data-fetching boundary) | `<LandingPage>`, `<PricingPage>` |
| **Flows** | Multi-page user journeys | Signup flow, Onboarding flow, Checkout flow |

**Primitives** split into two categories:
- **Component primitives** — Behavioural wrappers (e.g., `<Pressable>`, `<Collapsible>`, `<Slot>`)
- **Layout primitives** — Spatial containers (e.g., `<Stack>`, `<Grid>`, `<Container>`, `<Spacer>`)

### Atomic Design Rules

1. **MUST classify components** using the extended hierarchy above
2. **MUST check component catalog BEFORE creating** — Browse Storybook sidebar, check shadcn/ui, compose before creating
3. **MUST use atomic folder structure** — `src/components/{primitives,atoms,molecules,organisms,templates}/`
4. **MUST mirror atomic levels in Storybook titles** — `title: 'Atoms/Button'`, `title: 'Organisms/Auth/SignupForm'`
5. **SHOULD prefer shadcn/ui for atoms** — Only create custom atoms when shadcn/ui doesn't cover the need

### Component Rules

6. **MUST read design system FIRST** — `/docs/design/design-system.md`
7. **MUST map every BDD scenario to a story** — 100% coverage
8. **MUST create selector contracts** — Bridge between stories and tests
9. **MUST separate components from stories** — Stories import from `src/components/`, never embed code
10. **MUST check tsconfig.json paths before imports** — Path aliases vary by project

### View Components Pattern

View components are the **single source of truth** for rendering logic. Both Storybook stories and app pages import the same view component — no duplication.

```
src/components/views/
  ├── PricingView.tsx      ← rendering logic (props in, JSX out)
  ├── DashboardView.tsx
  └── OnboardingView.tsx

src/app/pricing/page.tsx   ← data fetching + auth → passes props to PricingView
stories/PricingView.stories.tsx ← mock data → passes props to PricingView
```

**Rules:**
11. **MUST create view components** for any page-level UI — `src/components/views/[Name]View.tsx`
12. **View components accept props, return JSX** — No data fetching, no auth, no side effects
13. **Pages are thin wrappers** — `page.tsx` handles data/auth, passes props to the view component
14. **Stories import views directly** — Stories provide mock data to the same view component that pages use
15. **MUST NOT duplicate rendering logic** — If a story and a page render the same UI, extract to a view component

### Design Grammar

The **Design Grammar** at `.design-grammar/` defines the shared cross-project vocabulary. It provides JSON definitions for every level of the atomic hierarchy.

**Rules:**
16. **MUST consult Design Grammar** before creating new components — check if a grammar definition exists
17. **Components SHOULD conform to grammar JSON** — structure, prop names, and variants defined in grammar
18. **New patterns MUST be proposed to grammar** — if you create a novel organism or molecule, add its JSON definition
19. **Token values come from grammar** — never invent token names; use what the grammar defines
20. **Grammar is platform-agnostic** — same JSON drives React, Flutter, and other renderers

**Grammar structure:**
```
.design-grammar/
  ├── primitives/           ← component + layout primitive definitions
  │   ├── components.json
  │   └── layouts.json
  ├── atoms.json            ← atom definitions
  ├── molecules.json        ← molecule definitions
  ├── organisms.json        ← organism definitions (including marketing sections)
  ├── templates.json        ← template definitions
  ├── pipeline/             ← token build tooling (Style Dictionary)
  └── tokens-studio/        ← Figma ↔ repo token sync
```

### Testing Rules

21. **Storybook play functions are PRIMARY** for UI component testing (real browser)
22. **RTL tests are for non-visual logic ONLY** — Hooks, utils, state machines
23. **MUST NOT duplicate assertions** — If play function tests it, don't repeat in RTL
24. **MUST include accessibility assertions** — Roles, labels, focus management
25. **Tests MUST pass before handoff** — Engineering keeps them passing

### Design Token Rules

26. **MUST establish base tokens in Stage 2** — Brand colors, typography, spacing, radius, shadows
27. **Stage 7 is for emergent patterns ONLY** — Not base tokens
28. **MUST use design system tokens** — Never hard-code values that have tokens
29. **Token changes require pipeline validation** — Run `npm run validate` and `npm run build` in `.design-grammar/pipeline/`

### Accessibility Rules (WCAG 2.1 AA)

30. **Semantic HTML mandatory** — Headings, ARIA roles, landmarks, form labels
31. **Keyboard navigation complete** — Tab order, focus visible, Escape closes modals
32. **Screen reader support** — ARIA labels, live regions, described-by
33. **Color contrast minimum 4.5:1** — Text on background
34. **Touch targets minimum 44px** — Mobile-friendly

### Story Variant Rules

35. **MUST create responsive variants** — Mobile (320-768px), Tablet (768-1024px), Desktop (1024px+)
36. **MUST create theme variants** — Light and Dark mode using decorators
37. **MUST use `tags: ['autodocs']`** — Enable auto-generated component documentation
38. **SHOULD add JSDoc to props interfaces** — Appears in autodocs as prop descriptions
39. **SHOULD use CSF 3 with `satisfies Meta`** — Modern Storybook pattern

## Workflows

### Workflow: Creating Stories from Scenarios

**When:** Refinement phase, after BDD scenarios.

1. Read BDD scenarios from mini-PRD Section 4
2. **Check Design Grammar** — Does `.design-grammar/` define this component type?
3. **Component Catalog Check** — Browse Storybook, check shadcn/ui
4. Read design system at `/docs/design/design-system.md`
5. Create selector contract at `/tests/selectors/[capability].ts`
6. Classify components using extended hierarchy (Tokens → Primitives → ... → Flows)
7. **Create view components** at `src/components/views/` for page-level UI
8. Create atomic components in `src/components/{primitives,atoms,molecules,organisms,templates}/`
9. Create stories that import view components or atomic components
10. Write stories per scenario (happy, error, boundary, validation)
11. Add responsive variants (Mobile, Tablet, Desktop)
12. Add theme variants (Light, Dark)
13. Add play functions for interaction testing
14. Add `tags: ['autodocs']` and JSDoc on props
15. Test locally: `npm run storybook`

See [UX Design Guide](../../docs/guides/ux-design-guide.md) for detailed steps and examples.

### Workflow: UX Review

**When:** Delivery phase, before PR approval for UI changes.

1. Gather inputs: UI under review, brand system specification, design decision log, reference class
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
| Flat component structure | Use atomic folders with `primitives/` level |
| Deferring all tokens | Base tokens go in Stage 2 |
| Duplicating render logic | Extract to view components (`src/components/views/`) |
| Page components doing rendering | Pages fetch data only — delegate rendering to views |
| Ignoring Design Grammar | Check `.design-grammar/` before creating new component types |
| Inventing token names | Use grammar-defined tokens only |

## Integration with AgentFlow Phases

| Phase | Activities |
|-------|-----------|
| **Discovery** | Brand system specification, reference class, base design tokens, Brand Page in Storybook |
| **Refinement** | Catalog Check → Components → Stories → Tests → Sign-off |
| **Delivery** | Engineering wires components, UX Review before PR |
| **Post-Delivery** | Extract emergent pattern tokens |

## Essential Reading

**Comprehensive guide (workflows, examples, review checklists):**
- [UX Design Guide](../../docs/guides/ux-design-guide.md)

**Design system:**
- Project design system: `/docs/design/design-system.md`

**Variant reference:**
- Tailwind Plus catalogue: `.design-grammar/sources/tailwind-plus/catalogue.json` — 657 component variants mapped to grammar types. Use as a reference when choosing variants for new components.

**Related skills:**
- `af-write-bdd-scenarios` — Scenario understanding
- `af-configure-test-frameworks` — Test patterns
- `af-develop-flutter-apps` — Mobile-specific patterns
- `af-sync-figma-designs` — Figma round-trip workflows (optional visual layer)

**MCP Tools:**
- `mcp__shadcn-ui-server__list_shadcn_components` — List available components
- `mcp__shadcn-ui-server__get_component_details` — Get component specs
- `mcp__shadcn-ui-server__get_component_examples` — Get usage examples

---

**Remember:**
1. Extended hierarchy: Tokens → Primitives → Atoms → Molecules → Organisms → Templates → Pages → Flows
2. View components (`src/components/views/`) are the single source of truth for rendering
3. Check Design Grammar (`.design-grammar/`) AND component catalog BEFORE creating
4. Play functions are PRIMARY for UI testing
5. Base tokens established in Stage 2, emergent patterns in Stage 7
6. Storybook is the source of truth, not Figma
7. Pages fetch data only — delegate all rendering to view components
