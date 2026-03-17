---
name: atomic-design
description: >-
  Brad Frost's Atomic Design for UI component hierarchy: atoms, molecules,
  organisms, templates. Activate when building user interfaces, creating
  design systems, organizing components, or structuring frontend code.
  Applies to any UI framework (React, Vue, SwiftUI, etc.).
license: CC0-1.0
compatibility: Designed for any coding agent (Claude Code, Codex, Cursor, OpenCode, etc.)
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: [source-files]
  phase: build
  standalone: true
---

# Atomic Design

**Value:** Simplicity and communication. Building UI from small, named,
composable pieces makes the interface understandable to everyone on the team
and prevents the complexity that comes from monolithic components.

## Purpose

Teaches how to organize UI components into a hierarchy of increasing complexity:
atoms, molecules, organisms, and templates. Each level has clear responsibilities
and composition rules. The outcome is a component system where every piece is
reusable, testable in isolation, and named in a shared vocabulary.

## Practices

### Build Bottom-Up Through Four Levels

Start with the smallest reusable elements and compose upward. Never skip a level.

**The four levels:**

1. **Atoms:** Indivisible UI elements. A button, an input, a label, an icon.
   One visual element, one responsibility. Atoms reference design tokens for
   all visual properties (color, spacing, typography).

2. **Molecules:** Small groups of atoms functioning as a unit. A form field
   (label + input + error message). A search bar (input + button + icon).
   One interaction pattern per molecule.

3. **Organisms:** Complex components composed of molecules and atoms that form
   a distinct section of the interface. A navigation header, a complete form,
   a data table. One feature area per organism.

4. **Templates:** Page-level layouts that arrange organisms into a complete
   view. A dashboard template, a list-detail template. Templates define
   structure and content slots, not specific data.

**Example:**
```
Atom: Button, Input, Label, ErrorMessage
Molecule: FormField (Label + Input + ErrorMessage)
Organism: LoginForm (FormField + FormField + Button)
Template: AuthPage (Header + LoginForm + Footer)
```

**Do:**
- Start with atoms when building new UI
- Name components by what they ARE, not what data they show
- Keep atoms under 50 lines, molecules under 100

**Do not:**
- Build organisms directly from raw markup -- extract atoms first
- Create a molecule that does not compose atoms from your system
- Skip to templates before organisms exist

### Keep Components Presentational

Components render UI. They receive data as props. They do not fetch data,
manage business logic, or hold application state.

1. Pass all data through props or equivalent
2. Emit events for user actions -- do not handle side effects
3. Separate data containers from presentational components

**Example:**
```
Presentational (good):
  UserCard({ name, email, avatar }) -> renders UI

Container (separate):
  UserCardContainer() -> fetches data, passes to UserCard
```

**Do not:**
- Put API calls inside atoms, molecules, or organisms
- Couple a component to a specific data source
- Mix rendering logic with business logic in the same component

### Use Design Tokens for All Visual Properties

Extract every design decision (colors, spacing, typography, shadows, radii)
into named tokens. Components reference tokens, never raw values.

1. Define tokens as the first step of any new design system
2. Every color, spacing value, and font size in a component must come from a token
3. Changing a token updates every component that references it

**Example:**
```css
/* Tokens */
--color-primary: #0066cc;
--spacing-sm: 8px;
--spacing-md: 16px;

/* Component uses tokens, not values */
.button { background: var(--color-primary); padding: var(--spacing-sm); }
```

**Do not:**
- Hard-code `#0066cc` or `8px` in any component
- Create one-off token names for single components
- Define tokens that are never used (tokens should earn their place)

### Compose, Do Not Inherit

Build complex components by nesting simpler ones. Do not extend base components
through class inheritance or deep prop-forwarding chains.

1. Pass children or slots to compose layout
2. Keep the component tree flat -- prefer siblings over deep nesting
3. When you need a variant, compose a new molecule from atoms rather than
   adding flags to an existing molecule

**Do:**
- `IconButton = Icon + Button` (composition)
- `Card > CardHeader + CardBody` (slots)

**Do not:**
- `FancyButton extends Button` (inheritance)
- A single Button component with 15 variant props

## Enforcement Note

This skill provides advisory guidance on component organization. It cannot
mechanically prevent an agent from skipping levels or hard-coding design
values. On harnesses with plugin support, enforcement plugins can lint for
token usage and validate component hierarchy. On harnesses without enforcement,
the agent follows these practices by convention. If you observe the agent
building organisms from raw markup, point it out. For available enforcement
plugins, see the
[Harness Plugin Availability](../../README.md#harness-plugin-availability) table.

## Verification

After completing work guided by this skill, verify:

- [ ] Every UI element traces to an atom (no raw markup in organisms/templates)
- [ ] Design tokens exist and components reference them (no hard-coded values)
- [ ] Each component has a single responsibility appropriate to its level
- [ ] Components are presentational (data passed in, events emitted out)
- [ ] The hierarchy is documented or self-evident from directory structure

If any criterion is not met, revisit the relevant practice before proceeding.

## Dependencies

This skill works standalone. For enhanced workflows, it integrates with:

- **domain-modeling:** Read models from the domain define what data components
  receive as props.
- **tdd-cycle:** Test components in isolation at each level -- atom tests,
  molecule tests, organism tests.
- **event-modeling:** Wireframes from event modeling sessions identify which
  components are needed.

Missing a dependency? Install with:
```
npx skills add jwilger/agent-skills --skill tdd-cycle
```
